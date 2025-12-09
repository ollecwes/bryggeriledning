---
name: metadata-validator
description: Validates YAML frontmatter and metadata structure in brewery documentation files. Use when the user asks to check documentation quality, validate metadata, find missing fields, verify document structure, or audit the documentation system.
---

# Metadata Validator

## Overview
This skill validates that all markdown documentation files in the Brygd brewery management system follow the correct metadata structure and contain valid values.

## When to Use This Skill

- User asks to "validate documentation" or "check metadata"
- User wants to "find documents with missing fields"
- User requests to "audit the documentation structure"
- Before deploying documentation changes
- As part of quality assurance processes
- When investigating documentation inconsistencies

## Validation Rules

### Required YAML Frontmatter Structure

Every `.md` file in the `docs/` directory (except `index.md` and `tags.md`) must have:

```yaml
---
title: [Document Title]
description: [Brief description]
owner: [Valid Owner Role]
status: [Valid Status]
tags:
  - [tag1]
  - [tag2]
---
```

### Field Validation Rules

#### 1. **title** (Required)
- **Type**: String
- **Rules**:
  - Must be present and non-empty
  - Should be concise and descriptive
  - Typically matches the main heading in the document
- **Example**: `title: HACCP-plan`

#### 2. **description** (Required)
- **Type**: String
- **Rules**:
  - Must be present and non-empty
  - Should be 1-2 sentences
  - Should clearly explain the document's purpose
  - Should not exceed ~200 characters
- **Example**: `description: Analys av faror och kritiska styrpunkter (CCP) i bryggprocessen.`

#### 3. **owner** (Required)
- **Type**: String
- **Rules**: Must be one of these valid roles (based on existing documentation):
  - `VD` (CEO)
  - `Bryggmästaren` or `Bryggmästare` (Brewmaster)
  - `Bryggerichef` (Brewery Manager)
  - `Kvalitetsansvarig` (Quality Manager)
  - `Lageransvarig` (Warehouse Responsible)
  - `Marknadsansvarig` (Marketing Manager)
  - `Ekonomiansvarig` (Finance Manager)
  - `Inköpsansvarig` (Purchasing Manager)
  - `Miljöansvarig` (Environmental Manager)
  - `Logistikansvarig` (Logistics Manager)
  - `Fastighetsansvarig` (Property Manager)
  - `Skyddsombud` (Safety Representative)
  - `Säljare` (Salesperson)
  - `Besöksansvarig` (Visitor Manager)
- **Invalid Examples**:
  - ❌ `owner: John Smith` (use role, not name)
  - ❌ `owner: Bryggare` (not a valid role)
  - ❌ `owner: Manager` (use Swedish role name)

#### 4. **status** (Required)
- **Type**: String
- **Rules**: Must be exactly one of:
  - `published` - Document is finalized and in use
  - `draft` - Document is in development
  - `archived` - Document is no longer active
- **Invalid Examples**:
  - ❌ `status: Published` (must be lowercase)
  - ❌ `status: in-progress` (not a valid status)
  - ❌ `status: active` (use "published")

#### 5. **tags** (Required)
- **Type**: List of strings
- **Rules**:
  - Must have at least 1 tag
  - Recommended: 2-4 tags per document
  - Tags should be lowercase
  - Tags should be relevant to content
  - Each tag on a new line with `  - ` prefix
- **Common tag categories**:
  - Process type: `produktion`, `kvalitet`, `säkerhet`, `miljö`
  - Domain: `haccp`, `livsmedel`, `bryggning`, `dokumentation`, `spårbarhet`
  - Type: `rutin`, `policy`, `plan`, `analys`, `recept`
  - Compliance: `tillstånd`, `skatt`, `rapportering`

### Files to Skip

Do NOT validate these files (they have different structures):
- `docs/index.md` (homepage)
- `docs/tags.md` (tag index)
- `docs/Strategi_metadata.md` (may have different structure)
- Any file not in a numbered category folder

## Validation Process

When validating documentation:

### Step 1: Find All Documentation Files

```bash
# Find all markdown files in category folders
find docs/ -path "docs/[0-9]*/*.md" -type f
```

Expected pattern: `docs/[1-11]_Category_Name/*.md`

### Step 2: Check Each File

For each file, verify:

1. **Frontmatter exists**: File starts with `---`
2. **Frontmatter is closed**: Second `---` exists
3. **All required fields present**: title, description, owner, status, tags
4. **Field values are valid**: Check against validation rules
5. **YAML syntax is correct**: Proper indentation, no syntax errors

### Step 3: Report Issues

Create a clear report with:
- **Summary**: Total files checked, issues found
- **By severity**:
  - **Critical**: Missing frontmatter, missing required fields
  - **Errors**: Invalid values (wrong status, invalid owner)
  - **Warnings**: Suspicious values (very long descriptions, too many tags)
- **Per-file details**: Specific issues with line numbers if possible

## Validation Report Format

```markdown
# Metadata Validation Report

**Date**: [ISO date]
**Files Checked**: [number]
**Issues Found**: [number]

## Summary
- ✅ Valid: [number] files
- ❌ Critical: [number] files
- ⚠️  Warnings: [number] files

## Critical Issues

### Missing Frontmatter
- `docs/4_Produktion/example.md` - No YAML frontmatter found

### Missing Required Fields
- `docs/3_Livsmedelssäkerhet/example.md`:
  - Missing: `description`
  - Missing: `tags`

## Errors

### Invalid Field Values
- `docs/5_Kvalitetskontroll/example.md`:
  - `owner: "Manager"` - Invalid owner role (must be one of: VD, Bryggmästaren, ...)
  - `status: "active"` - Invalid status (must be: draft, published, archived)

## Warnings

### Suspicious Values
- `docs/6_Arbetsmiljö/example.md`:
  - Description is very long (250 characters, recommend < 200)
  - Has 7 tags (recommend 2-4)

## Recommendations

1. Fix critical issues immediately
2. Review and correct invalid field values
3. Consider updating warnings for consistency
```

## Common Issues and Fixes

### Issue: Missing Frontmatter
**Problem**: File doesn't start with `---`
**Fix**: Add frontmatter at the top:
```yaml
---
title: [Title]
description: [Description]
owner: [Owner]
status: draft
tags:
  - [tag]
---
```

### Issue: Invalid Owner Role
**Problem**: `owner: "Brewer"` or `owner: "John Doe"`
**Fix**: Use valid Swedish role name: `owner: Bryggmästaren`

### Issue: Invalid Status
**Problem**: `status: "Active"` or `status: "Published"` (capitalized)
**Fix**: Use lowercase: `status: published`

### Issue: No Tags
**Problem**: `tags:` field is empty or missing
**Fix**: Add relevant tags:
```yaml
tags:
  - produktion
  - bryggning
```

### Issue: Malformed YAML
**Problem**: Inconsistent indentation or missing dashes
**Fix**: Ensure proper YAML syntax:
- Tags must have 2 spaces before the dash
- Each tag on a new line
- Closing `---` must be present

## Python Script Available

This skill has a companion Python script that automates validation:

**Location:** `.claude/skills/metadata-validator/validate_metadata.py`

**Usage:**
```bash
# Basic validation with text report
python validate_metadata.py

# JSON output for programmatic use
python validate_metadata.py --json

# Verbose output to see progress
python validate_metadata.py --verbose

# Custom docs directory
python validate_metadata.py --docs-dir /path/to/docs
```

**Benefits of using the script:**
- Fast: Validates all 53+ files in seconds
- Consistent: Same validation logic every time
- Repeatable: Can be run in CI/CD pipelines
- Machine-readable: JSON output for automation

## Implementation Instructions

When the user requests validation:

1. **Option A: Use the Python script** (recommended for full validation):
   ```bash
   python .claude/skills/metadata-validator/validate_metadata.py
   ```
   - Then parse and explain the results to the user
   - Offer to fix specific issues

2. **Option B: Manual validation** (for specific files or when script unavailable):
   - Use Glob to find files: `docs/[0-9]*/*.md`
   - Read each file and check:
     - Extract frontmatter (between first two `---`)
     - Parse YAML structure
     - Validate each required field
     - Check values against valid options

3. **Categorize issues**:
   - Critical: Missing frontmatter or required fields
   - Error: Invalid values
   - Warning: Suspicious but not invalid

4. **Generate report** using the format above

5. **Offer to fix issues**: Ask if the user wants Claude to fix the problems automatically

## Automated Fixing

If the user requests automatic fixes:

1. **For missing fields**: Ask what values to use
2. **For invalid status**: Suggest closest valid value
3. **For invalid owner**: Ask user to specify correct owner
4. **For missing tags**: Suggest tags based on content and category
5. **Create fixes one file at a time** and confirm before proceeding to the next

## Best Practices

- **Run validation regularly**: Before merging changes
- **Fix critical issues first**: They break the documentation system
- **Be conservative with warnings**: They're suggestions, not requirements
- **Preserve user intent**: When fixing, ask before changing meaningful values
- **Batch similar fixes**: Fix all "status: Published" → "status: published" at once

## Example Validation Session

```
User: "Validate the documentation metadata"

Claude:
1. Uses Glob to find all docs/[0-9]*/*.md files
2. Reads each file and checks frontmatter
3. Identifies issues:
   - 2 files missing description
   - 1 file has invalid status "Active"
   - 3 files have no tags
4. Generates comprehensive report
5. Offers to fix issues automatically

User: "Yes, fix them"

Claude:
1. For missing descriptions: Reads content and suggests descriptions
2. For invalid status: Changes "Active" → "published"
3. For missing tags: Suggests tags based on content and category
4. Applies fixes using Edit tool
5. Re-validates to confirm all issues resolved
```

## Validation Checklist

When validating, verify:

- [ ] All `.md` files in category folders have frontmatter
- [ ] All required fields present: title, description, owner, status, tags
- [ ] `owner` is a valid role name
- [ ] `status` is one of: draft, published, archived (lowercase)
- [ ] `tags` list has at least 1 tag
- [ ] YAML syntax is correct (indentation, dashes)
- [ ] No duplicate or conflicting metadata

## Integration with Repository

This skill works with:
- **All 11 documentation categories** in the docs/ folder
- **MkDocs configuration** (ensures compatibility)
- **Brewery document template generator** (validates generated docs)
- **Git workflows** (can be used as pre-commit check)

## Success Criteria

A successful validation run should:
- Check all documentation files systematically
- Identify all metadata issues
- Categorize issues by severity
- Provide clear, actionable reports
- Offer automated fixes when appropriate
- Ensure documentation system integrity