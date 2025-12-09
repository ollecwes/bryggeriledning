#!/usr/bin/env python3
"""
Brewery Document Template Generator

Creates properly formatted documentation files for the Brygd brewery
management system with YAML frontmatter.

Usage: python create_doc.py [--interactive] [--title TITLE] [--category CATEGORY]
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import re


class BreweryDocTemplate:
    """Manages brewery documentation templates"""

    # Documentation categories
    CATEGORIES = {
        "1": {
            "name": "1_Tillstånd_och_registrering",
            "title": "Tillstånd och registrering",
            "keywords": ["tillstånd", "permit", "registrering", "godkännande", "licens"]
        },
        "2": {
            "name": "2_Skatt_och_rapportering",
            "title": "Skatt och rapportering",
            "keywords": ["skatt", "tax", "rapportering", "deklaration", "statistik", "emcs"]
        },
        "3": {
            "name": "3_Livsmedelssäkerhet",
            "title": "Livsmedelssäkerhet",
            "keywords": ["haccp", "livsmedel", "säkerhet", "rengöring", "spårbarhet", "återkallande"]
        },
        "4": {
            "name": "4_Produktion",
            "title": "Produktion",
            "keywords": ["produktion", "bryggning", "recept", "mäskning", "kokning", "jäsning", "tappning"]
        },
        "5": {
            "name": "5_Kvalitetskontroll",
            "title": "Kvalitetskontroll",
            "keywords": ["kvalitet", "analys", "test", "batch", "avvikelse", "sensorisk"]
        },
        "6": {
            "name": "6_Arbetsmiljö",
            "title": "Arbetsmiljö",
            "keywords": ["arbetsmiljö", "säkerhet", "skydd", "kemikalier", "co2", "ergonomi"]
        },
        "7": {
            "name": "7_Miljö_och_avfall",
            "title": "Miljö och avfall",
            "keywords": ["miljö", "avfall", "återvinning", "avlopp", "drav"]
        },
        "8": {
            "name": "8_Inköp_och_lager",
            "title": "Inköp och lager",
            "keywords": ["inköp", "lager", "råvara", "leverantör", "mottagning"]
        },
        "9": {
            "name": "9_Försäljning_och_distribution",
            "title": "Försäljning och distribution",
            "keywords": ["försäljning", "distribution", "systembolaget", "restaurang", "logistik"]
        },
        "10": {
            "name": "10_Underhåll_och_fastighet",
            "title": "Underhåll och fastighet",
            "keywords": ["underhåll", "kalibrering", "utrustning", "fastighet"]
        },
        "11": {
            "name": "11_Varumärke_och_Kommunikation",
            "title": "Varumärke och kommunikation",
            "keywords": ["varumärke", "kommunikation", "design", "media", "webb"]
        }
    }

    # Valid owner roles
    VALID_OWNERS = [
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
        "Besöksansvarig"
    ]

    # Valid status values
    VALID_STATUSES = ["draft", "published", "archived"]

    # Common tags by category
    TAG_SUGGESTIONS = {
        "1": ["tillstånd", "registrering", "myndighet"],
        "2": ["skatt", "rapportering", "compliance"],
        "3": ["haccp", "livsmedel", "säkerhet", "rutin"],
        "4": ["produktion", "bryggning", "recept"],
        "5": ["kvalitet", "analys", "kontroll"],
        "6": ["arbetsmiljö", "säkerhet", "skydd"],
        "7": ["miljö", "avfall", "återvinning"],
        "8": ["inköp", "lager", "råvara"],
        "9": ["försäljning", "distribution", "kund"],
        "10": ["underhåll", "utrustning", "kalibrering"],
        "11": ["varumärke", "kommunikation", "design"]
    }

    def __init__(self, docs_dir: Path = None):
        """
        Initialize template generator

        Args:
            docs_dir: Path to docs directory
        """
        self.docs_dir = docs_dir or Path("docs")

    def suggest_category(self, title: str, description: str = "") -> List[str]:
        """
        Suggest categories based on title and description

        Args:
            title: Document title
            description: Document description

        Returns:
            List of suggested category numbers
        """
        text = (title + " " + description).lower()
        suggestions = []

        for cat_num, cat_info in self.CATEGORIES.items():
            for keyword in cat_info["keywords"]:
                if keyword in text:
                    suggestions.append(cat_num)
                    break

        return suggestions if suggestions else ["4"]  # Default to Production

    def suggest_owner(self, category: str) -> str:
        """
        Suggest owner based on category

        Args:
            category: Category number

        Returns:
            Suggested owner role
        """
        owner_map = {
            "1": "VD",
            "2": "Ekonomiansvarig",
            "3": "Kvalitetsansvarig",
            "4": "Bryggmästaren",
            "5": "Kvalitetsansvarig",
            "6": "Skyddsombud",
            "7": "Miljöansvarig",
            "8": "Inköpsansvarig",
            "9": "Säljare",
            "10": "Fastighetsansvarig",
            "11": "Marknadsansvarig"
        }
        return owner_map.get(category, "Bryggerichef")

    def suggest_tags(self, category: str, title: str) -> List[str]:
        """
        Suggest tags based on category and title

        Args:
            category: Category number
            title: Document title

        Returns:
            List of suggested tags
        """
        base_tags = self.TAG_SUGGESTIONS.get(category, [])[:2]

        # Add specific tags based on title
        title_lower = title.lower()
        extra_tags = []

        if any(word in title_lower for word in ["plan", "planering"]):
            extra_tags.append("plan")
        elif any(word in title_lower for word in ["rutin", "procedur"]):
            extra_tags.append("rutin")
        elif any(word in title_lower for word in ["policy", "policy"]):
            extra_tags.append("policy")
        elif any(word in title_lower for word in ["analys", "test"]):
            extra_tags.append("analys")

        return base_tags + extra_tags

    def create_filename(self, title: str) -> str:
        """
        Create a filename from title

        Args:
            title: Document title

        Returns:
            Filename (with .md extension)
        """
        # Replace spaces with underscores
        filename = title.replace(" ", "_")

        # Remove special characters except Swedish characters
        filename = re.sub(r'[^\w\såäöÅÄÖ_-]', '', filename)

        # Ensure it ends with .md
        if not filename.endswith('.md'):
            filename += '.md'

        return filename

    def generate_document_content(self, title: str, description: str,
                                   owner: str, status: str, tags: List[str]) -> str:
        """
        Generate document content with YAML frontmatter

        Args:
            title: Document title
            description: Document description
            owner: Owner role
            status: Document status
            tags: List of tags

        Returns:
            Complete document content
        """
        tags_yaml = "\n".join(f"  - {tag}" for tag in tags)

        content = f"""---
title: {title}
description: {description}
owner: {owner}
status: {status}
tags:
{tags_yaml}
---

# {title}

**Syfte:** {description}

**Ansvarig:** {owner}

## 1. Bakgrund

[Beskriv bakgrund och kontext för detta dokument]

## 2. Omfattning

[Beskriv vad som omfattas av detta dokument]

## 3. Ansvar

[Beskriv roller och ansvar]

## 4. Procedur/Process

[Beskriv stegvis hur arbetet ska utföras]

### 4.1 Förberedelse

[Beskrivning]

### 4.2 Genomförande

[Beskrivning]

### 4.3 Uppföljning

[Beskrivning]

## 5. Dokumentation

[Beskriv hur arbetet ska dokumenteras]

## 6. Referenser

[Lista relaterade dokument och resurser]

---

**Senast uppdaterad:** {datetime.now().strftime('%Y-%m-%d')}
**Version:** 1.0
"""
        return content

    def create_document(self, title: str, description: str, category: str,
                        owner: str, status: str, tags: List[str],
                        output_path: Optional[Path] = None) -> Path:
        """
        Create a new documentation file

        Args:
            title: Document title
            description: Document description
            category: Category number
            owner: Owner role
            status: Document status
            tags: List of tags
            output_path: Optional custom output path

        Returns:
            Path to created file
        """
        # Validate inputs
        if category not in self.CATEGORIES:
            raise ValueError(f"Invalid category: {category}")

        if owner not in self.VALID_OWNERS:
            raise ValueError(f"Invalid owner: {owner}")

        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")

        if not tags:
            raise ValueError("At least one tag is required")

        # Determine output path
        if output_path:
            file_path = output_path
        else:
            category_dir = self.docs_dir / self.CATEGORIES[category]["name"]
            category_dir.mkdir(parents=True, exist_ok=True)
            filename = self.create_filename(title)
            file_path = category_dir / filename

        # Check if file exists
        if file_path.exists():
            raise FileExistsError(f"File already exists: {file_path}")

        # Generate content
        content = self.generate_document_content(title, description, owner, status, tags)

        # Write file
        file_path.write_text(content, encoding='utf-8')

        return file_path


def interactive_mode(generator: BreweryDocTemplate) -> Dict[str, any]:
    """
    Interactive mode to gather document details

    Args:
        generator: BreweryDocTemplate instance

    Returns:
        Dictionary with document details
    """
    print("=" * 70)
    print("BRYGD BREWERY - NEW DOCUMENT GENERATOR")
    print("=" * 70)
    print()

    # Get title
    title = input("Document title: ").strip()
    if not title:
        print("Error: Title is required")
        sys.exit(1)

    # Get description
    description = input("Description (1-2 sentences): ").strip()
    if not description:
        print("Error: Description is required")
        sys.exit(1)

    # Suggest and select category
    suggestions = generator.suggest_category(title, description)
    print("\nSuggested categories:")
    for cat_num in suggestions[:3]:
        cat_info = generator.CATEGORIES[cat_num]
        print(f"  {cat_num}. {cat_info['title']}")

    print("\nAll categories:")
    for cat_num, cat_info in sorted(generator.CATEGORIES.items()):
        print(f"  {cat_num}. {cat_info['title']}")

    category = input(f"\nSelect category number [{suggestions[0]}]: ").strip()
    category = category if category else suggestions[0]

    if category not in generator.CATEGORIES:
        print(f"Error: Invalid category: {category}")
        sys.exit(1)

    # Suggest and select owner
    suggested_owner = generator.suggest_owner(category)
    print(f"\nValid owners:")
    for i, owner in enumerate(generator.VALID_OWNERS, 1):
        marker = " (suggested)" if owner == suggested_owner else ""
        print(f"  {i}. {owner}{marker}")

    owner_input = input(f"\nOwner [{suggested_owner}]: ").strip()
    if owner_input:
        # Check if it's a number (index) or a name
        if owner_input.isdigit():
            idx = int(owner_input) - 1
            if 0 <= idx < len(generator.VALID_OWNERS):
                owner = generator.VALID_OWNERS[idx]
            else:
                print(f"Error: Invalid owner index: {owner_input}")
                sys.exit(1)
        else:
            owner = owner_input
            if owner not in generator.VALID_OWNERS:
                print(f"Error: Invalid owner: {owner}")
                sys.exit(1)
    else:
        owner = suggested_owner

    # Select status
    print(f"\nValid statuses: {', '.join(generator.VALID_STATUSES)}")
    status = input("Status [draft]: ").strip().lower()
    status = status if status else "draft"

    if status not in generator.VALID_STATUSES:
        print(f"Error: Invalid status: {status}")
        sys.exit(1)

    # Suggest and input tags
    suggested_tags = generator.suggest_tags(category, title)
    print(f"\nSuggested tags: {', '.join(suggested_tags)}")
    tags_input = input("Tags (comma-separated) [use suggestions]: ").strip()

    if tags_input:
        tags = [tag.strip() for tag in tags_input.split(",")]
    else:
        tags = suggested_tags

    return {
        "title": title,
        "description": description,
        "category": category,
        "owner": owner,
        "status": status,
        "tags": tags
    }


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Create new brewery documentation files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_doc.py --interactive
  python create_doc.py --title "Dry Hopping" --category 4 --owner Bryggmästaren
  python create_doc.py --title "CO2 Safety" --description "Safety procedures" --category 6
        """
    )

    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Interactive mode (prompts for all fields)'
    )

    parser.add_argument(
        '--title', '-t',
        help='Document title'
    )

    parser.add_argument(
        '--description', '-d',
        help='Document description'
    )

    parser.add_argument(
        '--category', '-c',
        choices=[str(i) for i in range(1, 12)],
        help='Category number (1-11)'
    )

    parser.add_argument(
        '--owner', '-o',
        help='Owner role'
    )

    parser.add_argument(
        '--status', '-s',
        choices=BreweryDocTemplate.VALID_STATUSES,
        default='draft',
        help='Document status (default: draft)'
    )

    parser.add_argument(
        '--tags',
        help='Tags (comma-separated)'
    )

    parser.add_argument(
        '--output',
        type=Path,
        help='Custom output path'
    )

    parser.add_argument(
        '--docs-dir',
        type=Path,
        default=Path('docs'),
        help='Path to docs directory (default: docs)'
    )

    args = parser.parse_args()

    # Initialize generator
    generator = BreweryDocTemplate(docs_dir=args.docs_dir)

    # Get document details
    if args.interactive or not args.title:
        doc_details = interactive_mode(generator)
    else:
        # Validate required arguments
        if not args.description:
            print("Error: --description is required in non-interactive mode")
            sys.exit(1)

        if not args.category:
            # Try to suggest
            suggestions = generator.suggest_category(args.title, args.description)
            args.category = suggestions[0]
            print(f"Auto-selected category: {generator.CATEGORIES[args.category]['title']}")

        if not args.owner:
            args.owner = generator.suggest_owner(args.category)
            print(f"Auto-selected owner: {args.owner}")

        if not args.tags:
            tags = generator.suggest_tags(args.category, args.title)
        else:
            tags = [tag.strip() for tag in args.tags.split(",")]

        doc_details = {
            "title": args.title,
            "description": args.description,
            "category": args.category,
            "owner": args.owner,
            "status": args.status,
            "tags": tags
        }

    # Create document
    try:
        output_path = generator.create_document(
            title=doc_details["title"],
            description=doc_details["description"],
            category=doc_details["category"],
            owner=doc_details["owner"],
            status=doc_details["status"],
            tags=doc_details["tags"],
            output_path=args.output
        )

        print("\n" + "=" * 70)
        print("✅ SUCCESS!")
        print("=" * 70)
        print(f"Document created: {output_path}")
        print()
        print("Summary:")
        print(f"  Title:       {doc_details['title']}")
        print(f"  Category:    {generator.CATEGORIES[doc_details['category']]['title']}")
        print(f"  Owner:       {doc_details['owner']}")
        print(f"  Status:      {doc_details['status']}")
        print(f"  Tags:        {', '.join(doc_details['tags'])}")
        print()
        print("Next steps:")
        print("  1. Edit the document to add content")
        print("  2. Review and update metadata if needed")
        print("  3. Change status to 'published' when ready")

    except Exception as e:
        print(f"\n❌ Error creating document: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
