---
name: branded-document-generator
description: Generate professionally formatted, brand-compliant documents and presentations for Brygd brewery. Use when creating print-ready documents (checklists, procedures, posters), presentations, PDFs for export, or any material that needs to follow the Brygd brand guidelines. Handles both internal documentation and external communication materials.
---

# Branded Document Generator

## Overview
This skill generates professionally formatted documents and presentations that follow Brygd's brand guidelines ("Radikal Transparens" / "The Open Source Brewery"). Outputs include print-ready PDFs, presentation slides, posters, and branded exports of documentation.

## When to Use This Skill

- Creating **print-ready documents** for brewery walls (checklists, procedures, safety instructions)
- Generating **presentations** from documentation content
- Exporting documentation to **branded PDF** format
- Creating **posters or signs** for the brewery
- Producing **training materials** for staff
- Preparing **external communication** materials (for partners, events)
- Converting markdown docs to **professional layouts**

## Brand Guidelines Reference

### Brygd Brand Philosophy
**"Radikal Transparens"** - The Open Source Brewery
- Functional, technical, and honest aesthetic
- Show the process, not just polished results
- Documentary industrial style
- Data-driven and transparent

### Color Palette

Use these official Brygd colors:

| Color Name | Hex Code | Usage |
|------------|----------|-------|
| **Koppar (Copper)** | `#B87333` | Primary accent - headers, important elements, links |
| **Gjutjärn (Cast Iron)** | `#2F3542` | Dark backgrounds and text |
| **Ånga (Steam)** | `#F1F2F6` | Light backgrounds (off-white) |
| **Humle (Hops)** | `#7BED9F` | Secondary accent - "new", "fresh", "approved" |
| **Malt** | `#ECCC68` | Warning color, warm accent |

### Typography

**Headers:** Roboto Slab (or similar slab serif)
- Strong, industrial feel
- Use for H1, H2, H3

**Body Text:** Inter (or Helvetica/Arial)
- Clean, readable, modern
- All paragraph text

**Technical Data:** JetBrains Mono (or Courier New)
- Recipes, batch numbers, technical specs
- Examples: `OG: 1.054`, `IBU: 45`, `Batch #042`

### Logo and Branding

**Logo Location:** `docs/assets/brygd_logo_header.webp`
- Simple, stamp-like design
- Can be combined with technical data
- Works in monochrome or full color

**Note:** If logo doesn't exist locally, it should be copied from `\iceman\public\images\brygd_logo_header.webp`

## Document Types and Use Cases

### 1. Print-Ready Checklists & Procedures

**Use Case:** Documents to print and hang in the brewery for daily operations

**Format:** A4 PDF with clear typography
**Requirements:**
- Large, readable text
- Checkbox items for checklists
- Header with Brygd logo and document title
- Footer with revision date and owner
- Color-coded sections using brand colors
- Technical data in monospace font

**Example Documents:**
- Daily cleaning checklists
- Quality control procedures
- Safety instructions
- Batch documentation templates

### 2. Presentations

**Use Case:** Training, external presentations, brewery tours

**Format:** HTML slides (reveal.js) or PowerPoint
**Requirements:**
- Title slide with Brygd branding
- Consistent header/footer on slides
- Content pulled from existing documentation
- Technical aesthetic (not corporate polished)
- Data visualizations in brand colors
- Process photos if available

**Example Presentations:**
- "Brewing Process Overview" (for tours)
- "HACCP Training" (for staff)
- "Our Quality System" (for partners/auditors)
- "New Product Launch" (for sales team)

### 3. Branded PDF Exports

**Use Case:** Converting existing markdown documentation to professional PDFs

**Format:** PDF with consistent styling
**Requirements:**
- Cover page with logo and title
- Table of contents
- Consistent typography throughout
- Code blocks and technical data styled appropriately
- Page numbers and document metadata
- Links preserved where possible

**Example Exports:**
- Full HACCP plan as PDF
- Quality control manual
- Training handbook
- Regulatory compliance package

### 4. Posters and Signs

**Use Case:** Visual communication in the brewery

**Format:** Large format PDF (A3, A2, or custom sizes)
**Requirements:**
- High contrast for readability
- Large typography
- Minimal text, maximum impact
- Safety information color-coded
- Can include QR codes to full documentation

**Example Posters:**
- "5 Steps to Perfect Cleaning"
- "Emergency Contact Information"
- "Today's Batch: #042 West Coast IPA"
- "Batch Timeline" (visual process chart)

## Technical Implementation

### Tools and Technologies

**Recommended Approach:** Markdown → HTML → PDF pipeline

1. **Pandoc** - Universal document converter
   - Converts markdown to PDF via LaTeX or HTML
   - Supports custom templates
   - Preserves code blocks and tables

2. **weasyprint** - HTML/CSS to PDF
   - Better CSS support than wkhtmltopdf
   - Pythonic and integrates well
   - Install: `pip install weasyprint`

3. **reveal.js** - HTML presentations
   - Markdown-based slides
   - Beautiful transitions
   - Can export to PDF

4. **LaTeX** - Professional typesetting
   - Ultimate control over layout
   - Steep learning curve
   - Best for complex documents

### Basic Workflow

#### For Print-Ready Checklists

```markdown
1. Take source markdown document
2. Add HTML wrapper with:
   - Brygd CSS styles (colors, fonts, logo)
   - Print-optimized layout
   - Page breaks where appropriate
3. Convert HTML → PDF using weasyprint
4. Output: print-ready A4 PDF
```

#### For Presentations

```markdown
1. Extract key sections from documentation
2. Create reveal.js markdown structure
3. Apply Brygd theme (custom CSS)
4. Generate HTML presentation
5. Optional: Export to PDF for sharing
```

#### For Branded PDFs

```markdown
1. Combine multiple markdown files if needed
2. Apply pandoc template with:
   - Custom LaTeX or HTML template
   - Brygd styling
   - Cover page, TOC, headers/footers
3. Convert to PDF
4. Output: Professional documentation PDF
```

## HTML/CSS Template Structure

### Base CSS for Brygd Documents

```css
/* Brygd Brand Colors */
:root {
  --copper: #B87333;
  --cast-iron: #2F3542;
  --steam: #F1F2F6;
  --hops: #7BED9F;
  --malt: #ECCC68;
}

/* Typography */
body {
  font-family: 'Inter', 'Helvetica', 'Arial', sans-serif;
  color: var(--cast-iron);
  background: var(--steam);
  font-size: 11pt;
  line-height: 1.6;
}

h1, h2, h3 {
  font-family: 'Roboto Slab', serif;
  color: var(--copper);
  font-weight: 700;
}

code, pre, .technical {
  font-family: 'JetBrains Mono', 'Courier New', monospace;
  background: #f8f9fa;
  padding: 2px 6px;
  border-radius: 3px;
}

/* Header with Logo */
.document-header {
  border-bottom: 3px solid var(--copper);
  padding: 20px 0;
  margin-bottom: 30px;
}

.document-header img {
  max-height: 60px;
}

/* Print-specific */
@media print {
  body {
    background: white;
  }

  .page-break {
    page-break-after: always;
  }

  .no-print {
    display: none;
  }
}

/* Checklists */
.checklist-item {
  margin: 12px 0;
  padding: 10px;
  border-left: 4px solid var(--hops);
}

.checklist-item input[type="checkbox"] {
  margin-right: 10px;
  transform: scale(1.3);
}
```

### Document Header Template

```html
<!DOCTYPE html>
<html lang="sv">
<head>
  <meta charset="UTF-8">
  <title>{DOCUMENT_TITLE}</title>
  <style>
    /* Include Brygd CSS here */
  </style>
</head>
<body>
  <div class="document-header">
    <img src="docs/assets/brygd_logo_header.webp" alt="Brygd">
    <h1>{DOCUMENT_TITLE}</h1>
    <div class="metadata">
      <span class="technical">Owner: {OWNER}</span> |
      <span class="technical">Status: {STATUS}</span> |
      <span class="technical">Date: {DATE}</span>
    </div>
  </div>

  <div class="content">
    {CONTENT}
  </div>

  <div class="document-footer">
    <p class="technical">Brygd Bryggeri | Radikal Transparens</p>
  </div>
</body>
</html>
```

## Python Script Available

This skill has a companion Python script that automates document generation:

**Location:** `.claude/skills/branded-document-generator/generate_branded_doc.py`

**Usage:**
```bash
# Generate a manual (default)
python generate_branded_doc.py docs/3_Livsmedelssäkerhet/HACCP_plan.md

# Generate a print checklist
python generate_branded_doc.py cleaning.md --type checklist

# Generate a poster
python generate_branded_doc.py safety.md --type poster

# Generate HTML preview (for debugging)
python generate_branded_doc.py doc.md --html-preview

# Custom output location
python generate_branded_doc.py doc.md --output custom_name.pdf
```

**Document Types:**
- `checklist` - Print-ready checklists with checkboxes (A4 portrait)
- `manual` - Professional manuals with cover and TOC (A4 portrait)
- `poster` - High-contrast posters for walls (A3 portrait)
- `presentation` - Presentation slides (A4 landscape)

**Benefits:**
- Automated: One command generates branded PDFs
- Consistent: Always follows Brygd brand guidelines
- Fast: Converts markdown to PDF in seconds
- Customizable: Different templates for different use cases

## Step-by-Step Instructions

### When User Requests a Branded Document

1. **Identify the document type**:
   - Print checklist?
   - Presentation?
   - PDF export?
   - Poster?

2. **Gather source content**:
   - Single document or multiple?
   - Need to extract specific sections?
   - Include images?

3. **Use the Python script** (recommended):
   ```bash
   python .claude/skills/branded-document-generator/generate_branded_doc.py \
     <input.md> --type <checklist|manual|poster|presentation>
   ```

   **OR manually apply template**:
   - Choose CSS/HTML template based on type
   - Customize for specific use case
   - Use weasyprint, pandoc, or HTML generation

4. **Verify output**:
   - Check colors match brand
   - Typography correct
   - Layout is clean and readable
   - Technical data uses monospace font
   - Logo is present

5. **Provide to user**:
   - Files saved to `docs/exports/` by default
   - Provide path to generated document

### Example: Creating a Print Checklist

```
User: "Create a print-ready version of the daily cleaning checklist"

Steps:
1. Read docs/3_Livsmedelssäkerhet/Rengöringsscheman.md
2. Extract checklist items
3. Create HTML with:
   - Brygd header with logo
   - Large checkbox items
   - Color-coded sections
   - Footer with date and owner
4. Use weasyprint to convert to PDF
5. Save as docs/exports/Daily_Cleaning_Checklist.pdf
6. Provide to user
```

### Example: Creating a Presentation

```
User: "Create a 5-slide presentation about our HACCP process"

Steps:
1. Read docs/3_Livsmedelssäkerhet/HACCP_plan.md
2. Extract key sections:
   - What is HACCP?
   - Our critical control points
   - Monitoring procedures
   - Verification
3. Create reveal.js markdown:
   - Title slide with Brygd branding
   - One slide per section
   - Technical data highlighted
   - Use brand colors for emphasis
4. Generate HTML presentation
5. Provide link to open in browser
```

## File Organization

Generated documents should be saved to:
```
docs/exports/
├── checklists/
│   ├── Daily_Cleaning.pdf
│   └── Quality_Control.pdf
├── presentations/
│   ├── HACCP_Training.html
│   └── Brewing_Process.html
├── manuals/
│   ├── Complete_HACCP_Manual.pdf
│   └── Quality_System.pdf
└── posters/
    ├── Emergency_Contacts.pdf
    └── Batch_Timeline.pdf
```

## Dependencies and Setup

### Required Python Packages

```bash
pip install weasyprint pandoc-include markdown beautifulsoup4
```

### Font Installation

For best results, install brand fonts:
- Roboto Slab: https://fonts.google.com/specimen/Roboto+Slab
- Inter: https://fonts.google.com/specimen/Inter
- JetBrains Mono: https://fonts.google.com/specimen/JetBrains+Mono

Or use web fonts in HTML templates.

### Logo Setup

**Important:** Ensure logo is available locally:

```bash
# If logo doesn't exist, copy from iceman repo:
cp /path/to/iceman/public/images/brygd_logo_header.webp docs/assets/
```

## Best Practices

1. **Consistency**: Always use brand colors and typography
2. **Readability**: Prioritize clarity over decoration
3. **Authenticity**: Keep the "documentary industrial" feel
4. **Technical Transparency**: Show data, specs, batch numbers
5. **Accessibility**: Ensure sufficient contrast and readable font sizes
6. **Print Testing**: Test print output before mass printing

## Common Use Cases Summary

| Use Case | Input | Output | Key Features |
|----------|-------|--------|--------------|
| Wall Checklist | Markdown procedure | A4 PDF | Large text, checkboxes, Brygd header |
| Training Presentation | Multiple docs | HTML slides | 5-10 slides, brand colors, technical data |
| HACCP Manual | HACCP docs | Professional PDF | Cover page, TOC, headers/footers |
| Batch Poster | Batch data | A3 PDF | High contrast, minimal text, data focus |
| Safety Sign | Safety procedure | A2 PDF | Color-coded, icons, emergency info |

## Integration with Other Skills

- **Brewery Doc Template**: Generate documents that can be exported
- **Metadata Validator**: Ensure source docs are valid before export
- **Batch Documentation**: Create branded batch reports

## Success Criteria

A successful branded document should:
- Follow all brand guidelines (colors, typography, logo)
- Be fit for purpose (print-ready, presentation-ready, etc.)
- Maintain the "Radikal Transparens" aesthetic
- Be technically accurate and detailed
- Look professional but not corporate/polished
- Include appropriate metadata (owner, date, batch#)