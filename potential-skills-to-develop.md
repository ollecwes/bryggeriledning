# Potential Claude Skills to Develop for Bryggeriledning

This document outlines Claude skills that would be valuable for managing and maintaining the Brygd brewery management documentation system.

## Repository Overview

**Project**: Bryggeriledning (Brewery Management System)
**Domain**: Comprehensive operational documentation for a Swedish craft brewery
**Philosophy**: "Radikal Transparens" (Radical Transparency) - Open Source Brewery
**Tech Stack**: MkDocs with Material theme, Python, GitHub Actions

## Highly Recommended Skills

### 1. Document Template Generator
**Purpose**: Creates new documentation files with proper YAML frontmatter structure

**Features**:
- Auto-fills metadata (title, description, owner, status, tags)
- Ensures consistency across all docs
- Places files in the correct category folder
- Follows established patterns from existing documentation

**Use Cases**:
- Adding new regulatory procedures
- Creating production documentation
- Documenting new quality control processes

---

### 2. Metadata Validator
**Purpose**: Validates that all markdown files have correct structure and metadata

**Features**:
- Checks YAML frontmatter structure
- Validates required fields (title, description, owner, status, tags)
- Ensures valid values (status: draft/published/archived)
- Verifies proper owner roles (VD, Bryggmästare, Kvalitetsansvarig, etc.)

**Use Cases**:
- Pre-commit validation
- Periodic documentation audits
- Quality assurance for new contributions

---

### 3. Batch Documentation Creator
**Purpose**: Generates standardized batch documentation for brewing sessions

**Features**:
- Pre-filled templates with production checkpoints
- Links to relevant recipes, HACCP plans, and QC procedures
- Auto-generates batch numbers and dates
- Creates corresponding laboratory analysis placeholders

**Use Cases**:
- Starting a new brewing batch
- Documenting production runs
- Maintaining traceability requirements

---

### 4. Cross-Reference Checker
**Purpose**: Validates internal documentation links and relationships

**Features**:
- Checks that all markdown links resolve correctly
- Identifies broken references
- Suggests related documents that should be linked
- Ensures navigation consistency with mkdocs.yml

**Use Cases**:
- After restructuring documentation
- Regular maintenance checks
- Before deploying to production

---

### 5. Compliance Report Generator
**Purpose**: Automates regulatory documentation and reporting

**Features**:
- Monthly tax declaration summaries
- Quarterly inventory reports
- Annual HACCP review checklists
- Pulls data from relevant documentation sections

**Use Cases**:
- Preparing for regulatory submissions
- Internal compliance audits
- Management reporting

---

## Moderately Useful Skills

### 6. Tag Manager
**Purpose**: Helps organize content tagging system

**Features**:
- Suggests relevant tags based on document content
- Shows tag usage statistics across the repository
- Identifies under-tagged or mis-tagged documents
- Helps maintain the tags.md index

**Use Cases**:
- Improving content discoverability
- Periodic tag cleanup
- Organizing new content areas

---

### 7. Swedish-English Translator
**Purpose**: Facilitates international sharing (aligns with "Radical Transparency")

**Features**:
- Translates brewery terminology accurately
- Maintains technical precision for regulatory terms
- Creates parallel English documentation structure
- Preserves markdown formatting and links

**Use Cases**:
- Sharing knowledge with international brewing community
- Collaborating with international partners
- Educational outreach

---

### 8. Recipe Formatter
**Purpose**: Standardizes brewing recipe documentation

**Features**:
- Formats ingredient lists, timings, and procedures
- Calculates ABV, IBU, and other brewing metrics
- Links recipes to batch documentation
- Ensures consistency in the Produktion section

**Use Cases**:
- Adding new beer recipes
- Updating existing formulations
- Creating brewing instructions

---

## Implementation Priority

### Phase 1 (High Impact, Quick Wins)
1. Document Template Generator
2. Metadata Validator

### Phase 2 (Operational Efficiency)
3. Batch Documentation Creator
4. Cross-Reference Checker

### Phase 3 (Advanced Features)
5. Compliance Report Generator
6. Tag Manager
7. Recipe Formatter
8. Swedish-English Translator

---

## Technical Considerations

**Common Patterns Across Skills**:
- All skills should understand YAML frontmatter structure
- Must respect the existing folder hierarchy (11 main categories)
- Should integrate with the mkdocs.yml navigation structure
- Need to handle Swedish language content appropriately

**Metadata Structure Reference**:
```yaml
---
title: [Document Title]
description: [Brief summary]
owner: [Role responsible]
status: published/draft/archived
tags:
  - [relevant tags]
---
```

**Valid Owner Roles**:
- VD (CEO)
- Bryggmästare (Brewmaster)
- Kvalitetsansvarig (Quality Manager)
- Lagerchef (Warehouse Manager)
- Försäljningsansvarig (Sales Manager)

**Documentation Categories**:
1. Tillstånd och Registrering (Permits and Registration)
2. Skatt och Rapportering (Tax and Reporting)
3. Livsmedelssäkerhet (Food Safety)
4. Produktion (Production)
5. Kvalitetskontroll (Quality Control)
6. Arbetsmiljö (Work Environment)
7. Miljö och Avfall (Environment and Waste)
8. Inköp och Lager (Purchasing and Inventory)
9. Försäljning och Distribution (Sales and Distribution)
10. Underhåll och Fastighet (Maintenance and Property)
11. Varumärke och Kommunikation (Brand and Communication)

---

## Next Steps

1. Choose which skill to develop first
2. Define detailed specifications
3. Implement and test with existing documentation
4. Document the skill usage in this repository
5. Iterate based on real-world usage

---

*Generated: 2025-12-09*
