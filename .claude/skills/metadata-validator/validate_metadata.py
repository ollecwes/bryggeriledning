#!/usr/bin/env python3
"""
Metadata Validator for Brygd Brewery Documentation

Validates YAML frontmatter in all brewery documentation files.
Usage: python validate_metadata.py [--json] [--fix] [--verbose]
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import yaml


class Severity(Enum):
    """Issue severity levels"""
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"


@dataclass
class Issue:
    """Represents a validation issue"""
    file_path: str
    severity: Severity
    field: str
    message: str
    line_number: int = None


@dataclass
class ValidationResult:
    """Results from validating all documentation files"""
    total_files: int = 0
    valid_files: int = 0
    files_with_issues: int = 0
    issues: List[Issue] = field(default_factory=list)

    def add_issue(self, issue: Issue):
        """Add an issue to the results"""
        self.issues.append(issue)

    def get_critical_count(self) -> int:
        """Count critical issues"""
        return sum(1 for i in self.issues if i.severity == Severity.CRITICAL)

    def get_error_count(self) -> int:
        """Count errors"""
        return sum(1 for i in self.issues if i.severity == Severity.ERROR)

    def get_warning_count(self) -> int:
        """Count warnings"""
        return sum(1 for i in self.issues if i.severity == Severity.WARNING)


class MetadataValidator:
    """Validates YAML frontmatter in markdown documentation files"""

    # Valid owner roles
    VALID_OWNERS = {
        "VD",
        "Bryggmästaren",
        "Bryggmästare",
        "Bryggerichef",
        "Kvalitetsansvarig",
        "Lageransvarig",
        "Marknadsansvarig",
        "Ekonomiansvarig",
        "Inköpsansvarig",
        "Miljöansvarig",
        "Logistikansvarig",
        "Fastighetsansvarig",
        "Skyddsombud",
        "Säljare",
        "Besöksansvarig",
    }

    # Valid status values
    VALID_STATUSES = {"published", "draft", "archived"}

    # Required fields in frontmatter
    REQUIRED_FIELDS = {"title", "description", "owner", "status", "tags"}

    # Files to skip during validation
    SKIP_FILES = {"index.md", "tags.md", "Strategi_metadata.md", "README.md"}

    def __init__(self, docs_dir: Path, verbose: bool = False):
        """
        Initialize validator

        Args:
            docs_dir: Path to docs directory
            verbose: Enable verbose output
        """
        self.docs_dir = docs_dir
        self.verbose = verbose
        self.result = ValidationResult()

    def find_documentation_files(self) -> List[Path]:
        """
        Find all markdown files in category directories

        Returns:
            List of Path objects for documentation files
        """
        files = []

        # Find all markdown files in numbered category directories
        for category_dir in self.docs_dir.glob("[0-9]*"):
            if category_dir.is_dir():
                for md_file in category_dir.glob("*.md"):
                    if md_file.name not in self.SKIP_FILES:
                        files.append(md_file)

        return sorted(files)

    def extract_frontmatter(self, file_path: Path) -> Tuple[Dict[str, Any], bool, str]:
        """
        Extract YAML frontmatter from a markdown file

        Args:
            file_path: Path to markdown file

        Returns:
            Tuple of (frontmatter_dict, success, error_message)
        """
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return None, False, f"Could not read file: {e}"

        # Check if file starts with frontmatter delimiter
        if not content.startswith('---'):
            return None, False, "No YAML frontmatter found (file doesn't start with '---')"

        # Find the closing delimiter
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None, False, "No closing frontmatter delimiter found (missing second '---')"

        # Parse YAML
        frontmatter_text = parts[1].strip()
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if not isinstance(frontmatter, dict):
                return None, False, "Frontmatter is not a valid YAML dictionary"
            return frontmatter, True, None
        except yaml.YAMLError as e:
            return None, False, f"Invalid YAML syntax: {e}"

    def validate_file(self, file_path: Path):
        """
        Validate a single documentation file

        Args:
            file_path: Path to markdown file
        """
        rel_path = file_path.relative_to(self.docs_dir.parent)

        if self.verbose:
            print(f"  Validating: {rel_path}")

        # Extract frontmatter
        frontmatter, success, error = self.extract_frontmatter(file_path)

        if not success:
            self.result.add_issue(Issue(
                file_path=str(rel_path),
                severity=Severity.CRITICAL,
                field="frontmatter",
                message=error
            ))
            return

        # Check for required fields
        missing_fields = self.REQUIRED_FIELDS - set(frontmatter.keys())
        for field in missing_fields:
            self.result.add_issue(Issue(
                file_path=str(rel_path),
                severity=Severity.CRITICAL,
                field=field,
                message=f"Missing required field: {field}"
            ))

        # Validate individual fields
        self._validate_title(rel_path, frontmatter)
        self._validate_description(rel_path, frontmatter)
        self._validate_owner(rel_path, frontmatter)
        self._validate_status(rel_path, frontmatter)
        self._validate_tags(rel_path, frontmatter)

    def _validate_title(self, rel_path: Path, frontmatter: Dict[str, Any]):
        """Validate title field"""
        if 'title' not in frontmatter:
            return  # Already reported as missing

        title = frontmatter['title']
        if not title or not str(title).strip():
            self.result.add_issue(Issue(
                file_path=str(rel_path),
                severity=Severity.ERROR,
                field="title",
                message="Title is empty"
            ))

    def _validate_description(self, rel_path: Path, frontmatter: Dict[str, Any]):
        """Validate description field"""
        if 'description' not in frontmatter:
            return  # Already reported as missing

        description = frontmatter['description']
        if not description or not str(description).strip():
            self.result.add_issue(Issue(
                file_path=str(rel_path),
                severity=Severity.ERROR,
                field="description",
                message="Description is empty"
            ))
        elif len(str(description)) > 200:
            self.result.add_issue(Issue(
                file_path=str(rel_path),
                severity=Severity.WARNING,
                field="description",
                message=f"Description is long ({len(str(description))} characters, recommend < 200)"
            ))

    def _validate_owner(self, rel_path: Path, frontmatter: Dict[str, Any]):
        """Validate owner field"""
        if 'owner' not in frontmatter:
            return  # Already reported as missing

        owner = frontmatter['owner']
        if not owner or not str(owner).strip():
            self.result.add_issue(Issue(
                file_path=str(rel_path),
                severity=Severity.ERROR,
                field="owner",
                message="Owner is empty"
            ))
        elif str(owner) not in self.VALID_OWNERS:
            self.result.add_issue(Issue(
                file_path=str(rel_path),
                severity=Severity.ERROR,
                field="owner",
                message=f"Invalid owner role: '{owner}' (must be one of: {', '.join(sorted(self.VALID_OWNERS))})"
            ))

    def _validate_status(self, rel_path: Path, frontmatter: Dict[str, Any]):
        """Validate status field"""
        if 'status' not in frontmatter:
            return  # Already reported as missing

        status = frontmatter['status']
        if not status or not str(status).strip():
            self.result.add_issue(Issue(
                file_path=str(rel_path),
                severity=Severity.ERROR,
                field="status",
                message="Status is empty"
            ))
        elif str(status) not in self.VALID_STATUSES:
            # Check for capitalization issues
            if str(status).lower() in self.VALID_STATUSES:
                self.result.add_issue(Issue(
                    file_path=str(rel_path),
                    severity=Severity.ERROR,
                    field="status",
                    message=f"Invalid status: '{status}' (must be lowercase: '{str(status).lower()}')"
                ))
            else:
                self.result.add_issue(Issue(
                    file_path=str(rel_path),
                    severity=Severity.ERROR,
                    field="status",
                    message=f"Invalid status: '{status}' (must be one of: {', '.join(sorted(self.VALID_STATUSES))})"
                ))

    def _validate_tags(self, rel_path: Path, frontmatter: Dict[str, Any]):
        """Validate tags field"""
        if 'tags' not in frontmatter:
            return  # Already reported as missing

        tags = frontmatter['tags']
        if not tags:
            self.result.add_issue(Issue(
                file_path=str(rel_path),
                severity=Severity.ERROR,
                field="tags",
                message="Tags list is empty (must have at least 1 tag)"
            ))
        elif not isinstance(tags, list):
            self.result.add_issue(Issue(
                file_path=str(rel_path),
                severity=Severity.ERROR,
                field="tags",
                message="Tags must be a list"
            ))
        else:
            # Check tag count
            if len(tags) > 6:
                self.result.add_issue(Issue(
                    file_path=str(rel_path),
                    severity=Severity.WARNING,
                    field="tags",
                    message=f"Many tags ({len(tags)}, recommend 2-4)"
                ))

            # Check for empty tags
            for i, tag in enumerate(tags):
                if not tag or not str(tag).strip():
                    self.result.add_issue(Issue(
                        file_path=str(rel_path),
                        severity=Severity.ERROR,
                        field="tags",
                        message=f"Tag at position {i+1} is empty"
                    ))

    def validate_all(self) -> ValidationResult:
        """
        Validate all documentation files

        Returns:
            ValidationResult object with all issues found
        """
        files = self.find_documentation_files()
        self.result.total_files = len(files)

        if self.verbose:
            print(f"Found {len(files)} documentation files to validate\n")

        for file_path in files:
            self.validate_file(file_path)

        # Count valid files (files with no issues)
        files_with_issues = {issue.file_path for issue in self.result.issues}
        self.result.files_with_issues = len(files_with_issues)
        self.result.valid_files = self.result.total_files - self.result.files_with_issues

        return self.result


def print_report(result: ValidationResult):
    """
    Print validation report in human-readable format

    Args:
        result: ValidationResult object
    """
    from datetime import datetime

    print("=" * 70)
    print("METADATA VALIDATION REPORT")
    print("=" * 70)
    print(f"Date: {datetime.now().isoformat()}")
    print(f"Files Checked: {result.total_files}")
    print(f"Total Issues: {len(result.issues)}")
    print()

    print("SUMMARY")
    print("-" * 70)
    print(f"✅ Valid:    {result.valid_files} files")
    print(f"❌ Critical: {result.get_critical_count()} issues")
    print(f"⚠️  Errors:   {result.get_error_count()} issues")
    print(f"⚠️  Warnings: {result.get_warning_count()} issues")
    print()

    if not result.issues:
        print("🎉 All documentation files are valid!")
        return

    # Group issues by severity
    critical_issues = [i for i in result.issues if i.severity == Severity.CRITICAL]
    error_issues = [i for i in result.issues if i.severity == Severity.ERROR]
    warning_issues = [i for i in result.issues if i.severity == Severity.WARNING]

    # Print critical issues
    if critical_issues:
        print("CRITICAL ISSUES")
        print("-" * 70)
        for issue in critical_issues:
            print(f"❌ {issue.file_path}")
            print(f"   Field: {issue.field}")
            print(f"   Issue: {issue.message}")
            print()

    # Print errors
    if error_issues:
        print("ERRORS")
        print("-" * 70)
        for issue in error_issues:
            print(f"⚠️  {issue.file_path}")
            print(f"   Field: {issue.field}")
            print(f"   Issue: {issue.message}")
            print()

    # Print warnings
    if warning_issues:
        print("WARNINGS")
        print("-" * 70)
        for issue in warning_issues:
            print(f"⚠️  {issue.file_path}")
            print(f"   Field: {issue.field}")
            print(f"   Issue: {issue.message}")
            print()

    # Print recommendations
    print("RECOMMENDATIONS")
    print("-" * 70)
    if critical_issues:
        print("1. Fix critical issues immediately - they prevent proper documentation")
    if error_issues:
        print("2. Review and correct invalid field values")
    if warning_issues:
        print("3. Consider updating warnings for consistency")
    print()


def print_json_report(result: ValidationResult):
    """
    Print validation report in JSON format

    Args:
        result: ValidationResult object
    """
    import json
    from datetime import datetime

    report = {
        "date": datetime.now().isoformat(),
        "summary": {
            "total_files": result.total_files,
            "valid_files": result.valid_files,
            "files_with_issues": result.files_with_issues,
            "total_issues": len(result.issues),
            "critical_count": result.get_critical_count(),
            "error_count": result.get_error_count(),
            "warning_count": result.get_warning_count()
        },
        "issues": [
            {
                "file": issue.file_path,
                "severity": issue.severity.value,
                "field": issue.field,
                "message": issue.message,
                "line_number": issue.line_number
            }
            for issue in result.issues
        ]
    }

    print(json.dumps(report, indent=2, ensure_ascii=False))


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Validate YAML frontmatter in brewery documentation files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_metadata.py                    # Validate with text report
  python validate_metadata.py --json             # Output JSON format
  python validate_metadata.py --verbose          # Show progress
  python validate_metadata.py --docs-dir ./docs  # Custom docs directory
        """
    )

    parser.add_argument(
        '--docs-dir',
        type=Path,
        default=Path('docs'),
        help='Path to docs directory (default: docs)'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    # Check if docs directory exists
    if not args.docs_dir.exists():
        print(f"Error: Documentation directory not found: {args.docs_dir}", file=sys.stderr)
        sys.exit(1)

    if not args.docs_dir.is_dir():
        print(f"Error: Not a directory: {args.docs_dir}", file=sys.stderr)
        sys.exit(1)

    # Run validation
    validator = MetadataValidator(args.docs_dir, verbose=args.verbose)
    result = validator.validate_all()

    # Print report
    if args.json:
        print_json_report(result)
    else:
        print_report(result)

    # Exit with appropriate code
    if result.get_critical_count() > 0 or result.get_error_count() > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
