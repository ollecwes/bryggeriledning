---
name: brewery-doc-template
description: Generate new documentation files for the Brygd brewery management system with proper YAML frontmatter, following established patterns. Use when the user asks to create new documentation, add a new document, or needs a template for brewery procedures, regulations, or operational documentation.
---

# Brewery Document Template Generator

## Overview
This skill helps create properly formatted documentation files for the Brygd brewery management system. All documentation follows a consistent structure with YAML frontmatter and is organized into 11 main categories.

## Documentation Categories

When creating a new document, place it in the appropriate category folder:

1. **1_Tillstånd_och_registrering** (Permits and Registration)
   - Regulatory permits, approvals, food registration, serving licenses

2. **2_Skatt_och_rapportering** (Tax and Reporting)
   - Tax declarations, EMCS documentation, statistical reports

3. **3_Livsmedelssäkerhet** (Food Safety)
   - HACCP plans, self-monitoring, traceability, cleaning schedules, recall procedures

4. **4_Produktion** (Production)
   - Recipe development, mashing, boiling, fermentation, storage, bottling, product portfolio

5. **5_Kvalitetskontroll** (Quality Control)
   - Laboratory analyses, sensory evaluation, batch documentation, deviation handling

6. **6_Arbetsmiljö** (Work Environment)
   - SAM documentation, protective equipment, chemical inventory, CO2 safety

7. **7_Miljö_och_avfall** (Environment and Waste)
   - Waste sorting, wastewater management, spent grain handling

8. **8_Inköp_och_lager** (Purchasing and Inventory)
   - Supplier assessment, raw materials, finished goods, receipt control

9. **9_Försäljning_och_distribution** (Sales and Distribution)
   - Systembolaget procedures, restaurant agreements, distribution logistics

10. **10_Underhåll_och_fastighet** (Maintenance and Property)
    - Equipment maintenance plans, calibration

11. **11_Varumärke_och_Kommunikation** (Brand and Communication)
    - Graphic profile, tone of voice, visual style, web strategy, social media

## Valid Owner Roles

The `owner` field must be one of these valid roles:

- **VD** (CEO)
- **Bryggmästaren** / **Bryggmästare** (Brewmaster)
- **Bryggerichef** (Brewery Manager)
- **Kvalitetsansvarig** (Quality Manager)
- **Lageransvarig** (Warehouse Responsible)
- **Marknadsansvarig** (Marketing Manager)
- **Ekonomiansvarig** (Finance Manager)
- **Inköpsansvarig** (Purchasing Manager)
- **Miljöansvarig** (Environmental Manager)
- **Logistikansvarig** (Logistics Manager)
- **Fastighetsansvarig** (Property Manager)
- **Skyddsombud** (Safety Representative)
- **Säljare** (Salesperson)
- **Besöksansvarig** (Visitor Manager)

## Document Status Values

The `status` field must be one of:
- **published** - Document is finalized and in use
- **draft** - Document is in development
- **archived** - Document is no longer active but kept for reference

## Instructions for Creating Documents

When the user requests a new document:

1. **Ask for key information** if not provided:
   - Document title
   - Which category it belongs to (from the 11 categories above)
   - Who owns/maintains it (from valid owner roles)
   - Initial status (default to "draft" if creating a new document)
   - Relevant tags

2. **Determine the file path**:
   - Base path: `/home/user/bryggeriledning/docs/`
   - Add category folder (e.g., `4_Produktion/`)
   - Add filename (use Swedish characters, underscores for spaces)
   - Example: `/home/user/bryggeriledning/docs/4_Produktion/Ny_process.md`

3. **Create the document** using this exact template:

```markdown
---
title: [Document Title]
description: [Brief 1-2 sentence description of the document's purpose]
owner: [Valid Owner Role]
status: [draft|published|archived]
tags:
  - [tag1]
  - [tag2]
  - [tag3]
---

# [Document Title]

**Syfte:** [Purpose/objective of this document]

**Ansvarig:** [Responsible role/person]

## 1. [First Section]

[Content here]

## 2. [Second Section]

[Content here]

## 3. [Additional Sections as Needed]

[Content here]
```

4. **Follow these formatting guidelines**:
   - Use Swedish language for all content
   - Use YAML frontmatter exactly as shown (with dashes, proper indentation)
   - Tags should be lowercase and relevant to content
   - Document headings use `#` for title, `##` for main sections
   - Use bullet points with `*` or `-` for lists
   - Tables use markdown table syntax with alignment
   - Bold important terms with `**text**`
   - Italic for emphasis with `*text*`

5. **Common tag categories**:
   - Process type: produktion, kvalitet, säkerhet, miljö
   - Domain: haccp, livsmedel, bryggning, dokumentation, spårbarhet
   - Type: rutin, policy, plan, analys, recept
   - Compliance: tillstånd, skatt, rapportering

## Example Usage Scenarios

### Example 1: Creating a new production procedure
```
User: "Create a new document for our dry hopping procedure"

Assistant should:
- Identify category: 4_Produktion
- Suggest owner: Bryggmästaren
- Suggest status: draft
- Suggest tags: produktion, humle, bryggning
- Create file: docs/4_Produktion/Torr_humling.md
```

### Example 2: Creating a safety document
```
User: "I need a document for chemical storage procedures"

Assistant should:
- Identify category: 6_Arbetsmiljö
- Suggest owner: Kvalitetsansvarig
- Suggest status: draft
- Suggest tags: säkerhet, kemikalier, förvaring
- Create file: docs/6_Arbetsmiljö/Kemikalieförvaring.md
```

### Example 3: Creating a quality control document
```
User: "Add documentation for pH testing procedures"

Assistant should:
- Identify category: 5_Kvalitetskontroll
- Suggest owner: Kvalitetsansvarig
- Suggest status: draft
- Suggest tags: kvalitet, analys, pH
- Create file: docs/5_Kvalitetskontroll/pH_testning.md
```

## Document Content Guidelines

When filling in the content structure:

1. **Syfte (Purpose)**: Clearly state why this document exists and what it aims to achieve
2. **Ansvarig (Responsible)**: Specify the role responsible for maintaining this document
3. **Sections**: Organize content logically:
   - For procedures: step-by-step instructions
   - For plans: objectives, responsibilities, timelines, verification
   - For policies: principles, requirements, compliance references
   - For analyses: methodology, parameters, acceptance criteria

4. **Use tables** for structured data (critical control points, parameters, schedules)
5. **Use checklists** (`- [ ]`) for actionable items
6. **Cross-reference** other documents using relative markdown links

## Integration with MkDocs

After creating a new document:
1. The file will automatically appear in the MkDocs site structure
2. It can be cross-referenced from other documents
3. Tags will make it discoverable via the tag index
4. No need to manually update mkdocs.yml unless adding to nav structure

## Best Practices

- **Be consistent**: Follow the exact YAML structure shown
- **Use Swedish**: All content should be in Swedish (brewery is Swedish)
- **Be specific**: Descriptions should clearly state the document's purpose
- **Tag appropriately**: 2-4 tags per document is typical
- **Start as draft**: New documents should typically have status "draft" until reviewed
- **Ask for clarification**: If unsure about category or owner, ask the user

## Validation Checklist

Before finalizing a document, verify:
- [ ] YAML frontmatter is present and properly formatted
- [ ] All required fields are filled (title, description, owner, status, tags)
- [ ] Owner is a valid role from the list
- [ ] Status is one of: draft, published, archived
- [ ] File is in the correct category folder
- [ ] Filename uses Swedish characters and underscores
- [ ] Content is in Swedish
- [ ] Document structure is clear and logical
