# Claude Skills - Python Scripts

This directory contains Claude skills for the Brygd brewery management system, with companion Python scripts for automation.

## Overview

Each skill has both a markdown prompt file (`SKILL.md`) and a Python script for automation:

1. **metadata-validator** - Validates YAML frontmatter in documentation files
2. **branded-document-generator** - Generates branded PDFs and presentations
3. **brewery-doc-template** - Creates new documentation files with proper structure

## Installation

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `PyYAML>=6.0` - YAML parsing for metadata validation
- `markdown>=3.4` - Markdown to HTML conversion
- `weasyprint>=60.0` - HTML to PDF conversion for branded documents

**Note:** `weasyprint` may require system dependencies. See [weasyprint installation docs](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation) for platform-specific instructions.

## Skills and Scripts

### 1. Metadata Validator

**Purpose:** Validate YAML frontmatter in all brewery documentation files

**Script:** `metadata-validator/validate_metadata.py`

**Usage:**
```bash
# Basic validation with text report
python .claude/skills/metadata-validator/validate_metadata.py

# JSON output for programmatic use
python .claude/skills/metadata-validator/validate_metadata.py --json

# Verbose output to see progress
python .claude/skills/metadata-validator/validate_metadata.py --verbose
```

**What it validates:**
- All required fields present (title, description, owner, status, tags)
- Owner roles are valid
- Status values are valid (draft, published, archived)
- Tags are present and properly formatted
- YAML syntax is correct

**Exit codes:**
- `0` - All files valid
- `1` - Critical issues or errors found

### 2. Branded Document Generator

**Purpose:** Generate professionally formatted, brand-compliant documents

**Script:** `branded-document-generator/generate_branded_doc.py`

**Usage:**
```bash
# Generate a manual (default)
python .claude/skills/branded-document-generator/generate_branded_doc.py \
  docs/3_Livsmedelssäkerhet/HACCP_plan.md

# Generate a print checklist
python .claude/skills/branded-document-generator/generate_branded_doc.py \
  docs/3_Livsmedelssäkerhet/Rengöringsschema.md --type checklist

# Generate a poster
python .claude/skills/branded-document-generator/generate_branded_doc.py \
  safety.md --type poster --output safety_poster.pdf

# Generate HTML preview (for debugging, doesn't require weasyprint)
python .claude/skills/branded-document-generator/generate_branded_doc.py \
  doc.md --html-preview
```

**Document Types:**
- `checklist` - Print-ready checklists with checkboxes (A4 portrait)
- `manual` - Professional manuals with cover and TOC (A4 portrait)
- `poster` - High-contrast posters for walls (A3 portrait)
- `presentation` - Presentation slides (A4 landscape)

**Output locations:**
- Checklists: `docs/exports/checklists/`
- Manuals: `docs/exports/manuals/`
- Posters: `docs/exports/posters/`
- Presentations: `docs/exports/presentations/`

**Brand colors applied:**
- Copper (`#B87333`) - Headers and accents
- Cast Iron (`#2F3542`) - Dark text
- Steam (`#F1F2F6`) - Light backgrounds
- Hops (`#7BED9F`) - Success/approval indicators
- Malt (`#ECCC68`) - Warnings

### 3. Brewery Document Template

**Purpose:** Create new documentation files with proper YAML frontmatter

**Script:** `brewery-doc-template/create_doc.py`

**Usage:**
```bash
# Interactive mode (recommended for first-time users)
python .claude/skills/brewery-doc-template/create_doc.py --interactive

# Command-line mode with auto-suggestions
python .claude/skills/brewery-doc-template/create_doc.py \
  --title "Dry Hopping Procedure" \
  --description "Step-by-step procedure for dry hopping" \
  --category 4

# Full command-line mode
python .claude/skills/brewery-doc-template/create_doc.py \
  --title "CO2 Safety Procedures" \
  --description "Safety procedures for CO2 handling and monitoring" \
  --category 6 \
  --owner Skyddsombud \
  --status draft \
  --tags "säkerhet,co2,arbetsmiljö"
```

**Categories:**
1. Tillstånd och registrering (Permits and Registration)
2. Skatt och rapportering (Tax and Reporting)
3. Livsmedelssäkerhet (Food Safety)
4. Produktion (Production)
5. Kvalitetskontroll (Quality Control)
6. Arbetsmiljö (Work Environment)
7. Miljö och avfall (Environment and Waste)
8. Inköp och lager (Purchasing and Inventory)
9. Försäljning och distribution (Sales and Distribution)
10. Underhåll och fastighet (Maintenance and Property)
11. Varumärke och kommunikation (Brand and Communication)

**Features:**
- Interactive prompts with smart suggestions
- Auto-suggests category based on title keywords
- Auto-suggests owner role based on category
- Auto-suggests relevant tags
- Validates all inputs before creating file
- Generates proper Swedish filenames

## Integration with Claude Skills

These scripts are designed to work seamlessly with Claude skills:

1. **Claude invokes script** - When a skill is activated, Claude can run the appropriate Python script
2. **Script does heavy lifting** - Fast, consistent processing of files
3. **Claude interprets results** - Claude explains output to user in context
4. **User gets best of both** - Speed of automation + intelligence of Claude

## Examples

### Example 1: Validate all documentation

```bash
python .claude/skills/metadata-validator/validate_metadata.py
```

Output:
```
======================================================================
METADATA VALIDATION REPORT
======================================================================
Date: 2025-12-09
Files Checked: 53
Total Issues: 0

SUMMARY
----------------------------------------------------------------------
✅ Valid:    53 files
❌ Critical: 0 issues
⚠️  Errors:   0 issues
⚠️  Warnings: 0 issues

🎉 All documentation files are valid!
```

### Example 2: Create a new production document

```bash
python .claude/skills/brewery-doc-template/create_doc.py --interactive
```

Interactive prompts:
```
Document title: Dry Hopping Procedure
Description: Step-by-step procedure for adding dry hops during fermentation
Suggested categories: 4. Produktion
Select category [4]: 4
Owner [Bryggmästaren]:
Status [draft]:
Tags [produktion, bryggning]: produktion,humle,rutin

✅ SUCCESS!
Document created: docs/4_Produktion/Dry_Hopping_Procedure.md
```

### Example 3: Generate a branded checklist

```bash
python .claude/skills/branded-document-generator/generate_branded_doc.py \
  docs/3_Livsmedelssäkerhet/Rengöringsschema.md \
  --type checklist
```

Output:
```
Generating checklist document...
Input: docs/3_Livsmedelssäkerhet/Rengöringsschema.md
Output: docs/exports/checklists/Rengöringsschema.pdf

✅ Successfully generated: docs/exports/checklists/Rengöringsschema.pdf
🎉 Success! Document ready at: docs/exports/checklists/Rengöringsschema.pdf
```

## Development

### Making Scripts Executable

```bash
chmod +x .claude/skills/*/*.py
```

### Testing

Each script has built-in help:

```bash
python .claude/skills/metadata-validator/validate_metadata.py --help
python .claude/skills/branded-document-generator/generate_branded_doc.py --help
python .claude/skills/brewery-doc-template/create_doc.py --help
```

### CI/CD Integration

These scripts are designed to be used in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Validate documentation metadata
  run: |
    python .claude/skills/metadata-validator/validate_metadata.py --json > validation-report.json

- name: Check for validation errors
  run: |
    python .claude/skills/metadata-validator/validate_metadata.py
```

## Troubleshooting

### weasyprint installation issues

If `weasyprint` fails to install, you may need system dependencies:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-pip python3-cffi python3-brotli \
  libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0
```

**macOS:**
```bash
brew install python3 cairo pango gdk-pixbuf libffi
```

**Windows:**
Follow the [GTK installation guide](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows)

### Font issues in generated PDFs

The branded document generator uses Google Fonts (loaded via CDN). If you're generating documents offline, fonts will fall back to system fonts (Arial, serif, monospace).

To use custom fonts offline, install them locally:
- Roboto Slab (headers)
- Inter (body text)
- JetBrains Mono (technical data)

## License

These scripts are part of the Brygd brewery management system and follow the repository's license.

## Support

For issues or questions about these scripts:
1. Check script help: `python script.py --help`
2. Review the corresponding SKILL.md file
3. Test with `--verbose` flag for detailed output
4. Check Claude Code documentation

---

**Last updated:** 2025-12-09
**Version:** 1.0
