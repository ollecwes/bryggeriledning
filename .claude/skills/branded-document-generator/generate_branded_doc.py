#!/usr/bin/env python3
"""
Branded Document Generator for Brygd Brewery

Generates professionally formatted, brand-compliant documents following
the "Radikal Transparens" design philosophy.

Usage: python generate_branded_doc.py <input.md> [--type TYPE] [--output OUTPUT]
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import re

try:
    import markdown
    from weasyprint import HTML, CSS
    import yaml
except ImportError as e:
    print(f"Error: Missing required package: {e}")
    print("Install with: pip install markdown weasyprint PyYAML")
    sys.exit(1)


class BrygdBranding:
    """Brygd brand colors and constants"""

    # Brand colors
    COPPER = "#B87333"
    CAST_IRON = "#2F3542"
    STEAM = "#F1F2F6"
    HOPS = "#7BED9F"
    MALT = "#ECCC68"

    # Typography
    FONT_HEADER = "'Roboto Slab', serif"
    FONT_BODY = "'Inter', 'Helvetica', 'Arial', sans-serif"
    FONT_TECHNICAL = "'JetBrains Mono', 'Courier New', monospace"

    # Logo path (relative to repo root)
    LOGO_PATH = "docs/assets/brygd_logo_header.webp"


class DocumentType:
    """Document type configurations"""

    CHECKLIST = {
        "name": "checklist",
        "page_size": "A4 portrait",
        "font_size": "12pt",
        "show_checkboxes": True,
        "output_dir": "docs/exports/checklists"
    }

    MANUAL = {
        "name": "manual",
        "page_size": "A4 portrait",
        "font_size": "11pt",
        "show_toc": True,
        "show_cover": True,
        "output_dir": "docs/exports/manuals"
    }

    POSTER = {
        "name": "poster",
        "page_size": "A3 portrait",
        "font_size": "14pt",
        "high_contrast": True,
        "output_dir": "docs/exports/posters"
    }

    PRESENTATION = {
        "name": "presentation",
        "page_size": "A4 landscape",
        "font_size": "16pt",
        "slides": True,
        "output_dir": "docs/exports/presentations"
    }

    @classmethod
    def get(cls, doc_type: str) -> Dict[str, Any]:
        """Get document type config"""
        types = {
            "checklist": cls.CHECKLIST,
            "manual": cls.MANUAL,
            "poster": cls.POSTER,
            "presentation": cls.PRESENTATION
        }
        return types.get(doc_type.lower(), cls.MANUAL)


class BrandedDocumentGenerator:
    """Generate branded documents from markdown"""

    def __init__(self, input_file: Path, doc_type: str = "manual",
                 output_file: Optional[Path] = None, repo_root: Optional[Path] = None):
        """
        Initialize generator

        Args:
            input_file: Path to input markdown file
            doc_type: Type of document to generate
            output_file: Optional output path
            repo_root: Repository root path (for resolving assets)
        """
        self.input_file = input_file
        self.doc_type_config = DocumentType.get(doc_type)
        self.repo_root = repo_root or Path.cwd()

        # Set output file
        if output_file:
            self.output_file = output_file
        else:
            output_dir = self.repo_root / self.doc_type_config["output_dir"]
            output_dir.mkdir(parents=True, exist_ok=True)
            output_name = self.input_file.stem + ".pdf"
            self.output_file = output_dir / output_name

        # Parse input file
        self.metadata = {}
        self.content = ""
        self._parse_input()

    def _parse_input(self):
        """Parse markdown file and extract frontmatter"""
        content = self.input_file.read_text(encoding='utf-8')

        # Extract YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    self.metadata = yaml.safe_load(parts[1])
                    self.content = parts[2].strip()
                except yaml.YAMLError:
                    self.content = content
            else:
                self.content = content
        else:
            self.content = content

    def _get_css(self) -> str:
        """Generate CSS for the document"""
        config = self.doc_type_config

        css = f"""
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;700&family=Inter:wght@400;600&family=JetBrains+Mono&display=swap');

        :root {{
            --copper: {BrygdBranding.COPPER};
            --cast-iron: {BrygdBranding.CAST_IRON};
            --steam: {BrygdBranding.STEAM};
            --hops: {BrygdBranding.HOPS};
            --malt: {BrygdBranding.MALT};
        }}

        @page {{
            size: {config['page_size']};
            margin: 2cm;

            @top-right {{
                content: "{self.metadata.get('title', 'Brygd Bryggeri')}";
                font-family: {BrygdBranding.FONT_TECHNICAL};
                font-size: 9pt;
                color: var(--copper);
            }}

            @bottom-center {{
                content: "Sida " counter(page) " av " counter(pages);
                font-family: {BrygdBranding.FONT_BODY};
                font-size: 9pt;
                color: var(--cast-iron);
            }}

            @bottom-left {{
                content: "{datetime.now().strftime('%Y-%m-%d')}";
                font-family: {BrygdBranding.FONT_TECHNICAL};
                font-size: 9pt;
                color: var(--cast-iron);
            }}
        }}

        body {{
            font-family: {BrygdBranding.FONT_BODY};
            color: var(--cast-iron);
            background: white;
            font-size: {config['font_size']};
            line-height: 1.6;
        }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: {BrygdBranding.FONT_HEADER};
            color: var(--copper);
            font-weight: 700;
            page-break-after: avoid;
        }}

        h1 {{
            font-size: 2em;
            border-bottom: 3px solid var(--copper);
            padding-bottom: 0.3em;
            margin-top: 0;
        }}

        h2 {{
            font-size: 1.5em;
            border-bottom: 2px solid var(--steam);
            padding-bottom: 0.2em;
        }}

        h3 {{
            font-size: 1.2em;
            color: var(--cast-iron);
        }}

        code, pre, .technical {{
            font-family: {BrygdBranding.FONT_TECHNICAL};
            background: var(--steam);
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.9em;
        }}

        pre {{
            padding: 1em;
            overflow-x: auto;
            border-left: 4px solid var(--copper);
        }}

        pre code {{
            background: none;
            padding: 0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1em 0;
            page-break-inside: avoid;
        }}

        th {{
            background: var(--copper);
            color: white;
            padding: 0.5em;
            text-align: left;
            font-weight: 600;
        }}

        td {{
            border: 1px solid var(--steam);
            padding: 0.5em;
        }}

        tr:nth-child(even) {{
            background: var(--steam);
        }}

        blockquote {{
            border-left: 4px solid var(--hops);
            padding-left: 1em;
            margin-left: 0;
            font-style: italic;
            color: var(--cast-iron);
        }}

        ul, ol {{
            margin: 0.5em 0;
            padding-left: 2em;
        }}

        li {{
            margin: 0.3em 0;
            page-break-inside: avoid;
        }}

        a {{
            color: var(--copper);
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        strong {{
            font-weight: 600;
            color: var(--cast-iron);
        }}

        em {{
            font-style: italic;
        }}

        img {{
            max-width: 100%;
            height: auto;
        }}

        .document-header {{
            border-bottom: 3px solid var(--copper);
            padding-bottom: 1em;
            margin-bottom: 2em;
            page-break-after: avoid;
        }}

        .document-header img {{
            max-height: 60px;
            margin-bottom: 0.5em;
        }}

        .document-header .title {{
            font-family: {BrygdBranding.FONT_HEADER};
            font-size: 2.5em;
            color: var(--copper);
            margin: 0.2em 0;
        }}

        .metadata {{
            font-family: {BrygdBranding.FONT_TECHNICAL};
            font-size: 0.9em;
            color: var(--cast-iron);
        }}

        .metadata span {{
            margin-right: 1em;
        }}

        .document-footer {{
            border-top: 2px solid var(--steam);
            padding-top: 1em;
            margin-top: 2em;
            text-align: center;
            font-family: {BrygdBranding.FONT_TECHNICAL};
            font-size: 0.8em;
            color: var(--cast-iron);
        }}

        .page-break {{
            page-break-after: always;
        }}
        """

        # Add checklist-specific styles
        if config.get("show_checkboxes"):
            css += """
            .checklist-item {
                margin: 1em 0;
                padding: 0.8em;
                border-left: 4px solid var(--hops);
                background: var(--steam);
                page-break-inside: avoid;
            }

            .checklist-item::before {
                content: "☐ ";
                font-size: 1.2em;
                margin-right: 0.5em;
                color: var(--copper);
            }

            ul li {
                position: relative;
                list-style: none;
                margin-left: 0;
            }

            ul li::before {
                content: "☐";
                position: absolute;
                left: -1.5em;
                color: var(--copper);
                font-size: 1.1em;
            }
            """

        # Add poster-specific styles
        if config.get("high_contrast"):
            css += """
            body {
                font-size: 14pt;
            }

            h1 {
                font-size: 3em;
                text-align: center;
            }

            h2 {
                font-size: 2em;
            }

            p {
                font-size: 1.2em;
            }
            """

        return css

    def _get_html_header(self) -> str:
        """Generate HTML document header"""
        title = self.metadata.get('title', self.input_file.stem)
        owner = self.metadata.get('owner', '')
        status = self.metadata.get('status', '')

        # Check if logo exists
        logo_path = self.repo_root / BrygdBranding.LOGO_PATH
        logo_html = ""
        if logo_path.exists():
            logo_html = f'<img src="{logo_path}" alt="Brygd Bryggeri">'

        header = f"""
        <div class="document-header">
            {logo_html}
            <div class="title">{title}</div>
            <div class="metadata">
        """

        if owner:
            header += f'<span>Ansvarig: {owner}</span>'
        if status:
            header += f'<span>Status: {status}</span>'

        header += f'<span>Datum: {datetime.now().strftime("%Y-%m-%d")}</span>'
        header += """
            </div>
        </div>
        """

        return header

    def _get_html_footer(self) -> str:
        """Generate HTML document footer"""
        return """
        <div class="document-footer">
            <p>Brygd Bryggeri | Radikal Transparens | The Open Source Brewery</p>
        </div>
        """

    def _markdown_to_html(self) -> str:
        """Convert markdown content to HTML"""
        # Configure markdown extensions
        extensions = [
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.nl2br',
            'markdown.extensions.sane_lists'
        ]

        md = markdown.Markdown(extensions=extensions)
        html_content = md.convert(self.content)

        # Post-process for checklists
        if self.doc_type_config.get("show_checkboxes"):
            # Wrap list items in checklist-item divs (simplified approach)
            # A more sophisticated approach would parse and restructure the HTML
            pass

        return html_content

    def generate(self) -> Path:
        """
        Generate the branded PDF document

        Returns:
            Path to generated PDF file
        """
        print(f"Generating {self.doc_type_config['name']} document...")
        print(f"Input: {self.input_file}")
        print(f"Output: {self.output_file}")

        # Generate HTML
        html_content = self._markdown_to_html()

        # Build complete HTML document
        html_document = f"""
        <!DOCTYPE html>
        <html lang="sv">
        <head>
            <meta charset="UTF-8">
            <title>{self.metadata.get('title', self.input_file.stem)}</title>
        </head>
        <body>
            {self._get_html_header()}
            <div class="content">
                {html_content}
            </div>
            {self._get_html_footer()}
        </body>
        </html>
        """

        # Generate CSS
        css_content = self._get_css()

        # Convert to PDF using weasyprint
        try:
            html = HTML(string=html_document, base_url=str(self.repo_root))
            css = CSS(string=css_content)
            html.write_pdf(self.output_file, stylesheets=[css])

            print(f"✅ Successfully generated: {self.output_file}")
            return self.output_file

        except Exception as e:
            print(f"❌ Error generating PDF: {e}", file=sys.stderr)
            raise

    def generate_html_preview(self) -> Path:
        """
        Generate HTML preview (useful for debugging)

        Returns:
            Path to generated HTML file
        """
        html_content = self._markdown_to_html()

        html_document = f"""
        <!DOCTYPE html>
        <html lang="sv">
        <head>
            <meta charset="UTF-8">
            <title>{self.metadata.get('title', self.input_file.stem)}</title>
            <style>
                {self._get_css()}
            </style>
        </head>
        <body>
            {self._get_html_header()}
            <div class="content">
                {html_content}
            </div>
            {self._get_html_footer()}
        </body>
        </html>
        """

        html_output = self.output_file.with_suffix('.html')
        html_output.write_text(html_document, encoding='utf-8')

        print(f"✅ Generated HTML preview: {html_output}")
        return html_output


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate branded documents for Brygd Brewery",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Document Types:
  checklist     - Print-ready checklists with checkboxes (A4 portrait)
  manual        - Professional manuals with cover and TOC (A4 portrait)
  poster        - High-contrast posters for walls (A3 portrait)
  presentation  - Presentation slides (A4 landscape)

Examples:
  python generate_branded_doc.py docs/3_Livsmedelssäkerhet/HACCP_plan.md
  python generate_branded_doc.py cleaning.md --type checklist
  python generate_branded_doc.py safety.md --type poster --output safety_poster.pdf
  python generate_branded_doc.py presentation.md --type presentation --html-preview
        """
    )

    parser.add_argument(
        'input',
        type=Path,
        help='Input markdown file'
    )

    parser.add_argument(
        '--type', '-t',
        choices=['checklist', 'manual', 'poster', 'presentation'],
        default='manual',
        help='Document type (default: manual)'
    )

    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output PDF file (default: auto-generated in exports/)'
    )

    parser.add_argument(
        '--html-preview',
        action='store_true',
        help='Generate HTML preview instead of PDF'
    )

    parser.add_argument(
        '--repo-root',
        type=Path,
        help='Repository root path (default: current directory)'
    )

    args = parser.parse_args()

    # Validate input file
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Initialize generator
    generator = BrandedDocumentGenerator(
        input_file=args.input,
        doc_type=args.type,
        output_file=args.output,
        repo_root=args.repo_root or Path.cwd()
    )

    # Generate document
    try:
        if args.html_preview:
            output_path = generator.generate_html_preview()
        else:
            output_path = generator.generate()

        print(f"\n🎉 Success! Document ready at: {output_path}")

    except Exception as e:
        print(f"\n❌ Failed to generate document: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
