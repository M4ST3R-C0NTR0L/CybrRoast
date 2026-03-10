"""
CLI interface for CybrRoast.

Handles argument parsing, validation, and orchestrates the audit flow.
"""

import argparse
import sys
from typing import Optional

from . import __version__
from .auditor import WebsiteAuditor
from .reporter import TerminalReporter, MarkdownReporter, JsonReporter


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="CybrRoast",
        description="🔥 Roast any website's SEO, performance, and design.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  CybrRoast https://example.com
  CybrRoast https://example.com --json
  CybrRoast https://example.com --markdown --verbose
  CybrRoast https://example.com --no-roast --json > report.json
        """,
    )

    parser.add_argument(
        "url",
        help="The website URL to roast (e.g., https://example.com)",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON (machine-readable)",
    )

    parser.add_argument(
        "--markdown",
        "--md",
        action="store_true",
        help="Output results as Markdown report",
    )

    parser.add_argument(
        "--no-roast",
        action="store_true",
        help="Serious mode: output scores without jokes",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed recommendations for each category",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Request timeout in seconds (default: 30)",
    )

    parser.add_argument(
        "--user-agent",
        type=str,
        default="site-roast/1.0 (Website Auditor)",
        help="Custom User-Agent string for requests",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Save output to file (auto-detects format from extension: .json, .md)",
    )

    return parser


def validate_url(url: str) -> str:
    """
    Validate and normalize the URL.
    
    Args:
        url: The URL string to validate.
        
    Returns:
        The normalized URL.
        
    Raises:
        SystemExit: If the URL is invalid.
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    if not url.startswith("http") or "." not in url:
        print(f"Error: Invalid URL '{url}'", file=sys.stderr)
        print("Please provide a valid URL (e.g., https://example.com)", file=sys.stderr)
        sys.exit(1)

    return url


def detect_output_format(output_path: Optional[str]) -> Optional[str]:
    """
    Detect output format from file extension.
    
    Args:
        output_path: Path to the output file.
        
    Returns:
        The detected format ('json', 'md', or None).
    """
    if not output_path:
        return None

    output_path = output_path.lower()
    if output_path.endswith(".json"):
        return "json"
    elif output_path.endswith((".md", ".markdown")):
        return "markdown"
    return None


def main() -> int:
    """
    Main entry point for the CLI.
    
    Returns:
        Exit code (0 for success, 1 for error).
    """
    parser = create_parser()
    args = parser.parse_args()

    # Validate URL
    url = validate_url(args.url)

    # Detect output format from file extension if not specified
    output_format = detect_output_format(args.output)
    if output_format == "json":
        args.json = True
    elif output_format == "markdown":
        args.markdown = True

    # Run the audit
    try:
        auditor = WebsiteAuditor(
            timeout=args.timeout,
            user_agent=args.user_agent,
        )
        results = auditor.audit(url)

    except KeyboardInterrupt:
        print("\n\n🛑 Audit interrupted by user.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n💥 Audit failed: {e}", file=sys.stderr)
        return 1

    # Generate output
    if args.json:
        reporter = JsonReporter(no_roast=args.no_roast, verbose=args.verbose)
        output = reporter.generate(results)
    elif args.markdown:
        reporter = MarkdownReporter(no_roast=args.no_roast, verbose=args.verbose)
        output = reporter.generate(results)
    else:
        reporter = TerminalReporter(no_roast=args.no_roast, verbose=args.verbose)
        output = reporter.generate(results)

    # Write to file or stdout
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ Report saved to: {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
