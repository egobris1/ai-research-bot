"""Research Bot - Multi-Agent Research System."""

import argparse
import logging
import os
import sys
from pathlib import Path

# Ensure output is not buffered
os.environ["PYTHONUNBUFFERED"] = "1"

from research_bot.config.settings import Settings
from research_bot.services.research_service import ResearchService

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🔬 RESEARCH BOT                                            ║
║   ─────────────────────────────────────────────────────────  ║
║   Multi-Agent AI Research System                             ║
║                                                              ║
║   Agents:                                                    ║
║   • Research Planner    - Strategic research planning        ║
║   • Lead Researcher     - Deep technical research            ║
║   • Market Analyst      - Industry trends & applications     ║
║   • Research Director   - Quality assurance & synthesis      ║
║   • Report Writer       - Professional documentation         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""


def setup_logging(level: str) -> None:
    """Configure logging."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Research Bot - Multi-Agent AI Research System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  research-bot "Impact of AI on healthcare in 2025"
  research-bot "Quantum computing market analysis" -o quantum_report.md
  research-bot "Electric vehicle trends" --verbose
        """,
    )
    parser.add_argument(
        "topic",
        help="The research topic or question",
    )
    parser.add_argument(
        "--output", "-o",
        default="research_report.md",
        help="Output file path (default: research_report.md)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose agent output",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Minimal output (no banner)",
    )

    args = parser.parse_args()

    # Load settings
    try:
        settings = Settings()
    except Exception as e:
        print(f"❌ Error loading settings: {e}")
        print("\n📋 Make sure you have a .env file with:")
        print("   TAVILY_API_KEY=your-key")
        print("   SCRAPE_DO_API_KEY=your-key")
        print("   GOOGLE_API_KEY=your-key")
        sys.exit(1)

    # Set API keys in environment for CrewAI/Gemini
    os.environ["GOOGLE_API_KEY"] = settings.google_api_key

    # Setup logging
    log_level = "DEBUG" if args.verbose else settings.log_level
    setup_logging(log_level)

    # Show banner
    if not args.quiet:
        print(BANNER)

    # Execute research
    try:
        service = ResearchService(settings)
        report = service.execute_research(args.topic, output_file=args.output)

        # Show success
        output_path = Path(args.output)
        print(f"\n📊 Report Preview:")
        print("-" * 40)
        # Show first 500 chars of report
        preview = report[:500] + "..." if len(report) > 500 else report
        print(preview)
        print("-" * 40)
        print(f"\n✅ Full report saved to: {output_path.absolute()}")

    except KeyboardInterrupt:
        print("\n\n⚠️ Research interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logging.getLogger(__name__).exception("Research failed")
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
