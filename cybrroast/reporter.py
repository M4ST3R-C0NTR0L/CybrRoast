"""
Output formatters for site-roast.

Handles terminal, markdown, and JSON output formats.
"""

import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List

from .auditor import WebsiteAudit, AuditResult
from .roaster import Roaster


class BaseReporter(ABC):
    """Base class for all reporters."""

    def __init__(self, no_roast: bool = False, verbose: bool = False):
        """
        Initialize the reporter.
        
        Args:
            no_roast: If True, disable humorous roasts.
            verbose: If True, include detailed recommendations.
        """
        self.no_roast = no_roast
        self.verbose = verbose
        self.roaster = Roaster(no_roast=no_roast)

    @abstractmethod
    def generate(self, audit: WebsiteAudit) -> str:
        """Generate the report output."""
        pass


class TerminalReporter(BaseReporter):
    """
    Generate colorful terminal output with ASCII art.
    
    Uses ANSI color codes for a vibrant display.
    """

    # ANSI color codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"

    def _color(self, text: str, color: str) -> str:
        """Apply color to text."""
        return f"{color}{text}{self.RESET}"

    def _score_color(self, score: int) -> str:
        """Get color based on score."""
        if score >= 80:
            return self.GREEN
        elif score >= 60:
            return self.YELLOW
        elif score >= 40:
            return "\033[38;5;208m"  # Orange
        else:
            return self.RED

    def _get_progress_bar(self, score: int, width: int = 20) -> str:
        """Generate a progress bar for the score."""
        filled = int(width * score / 100)
        empty = width - filled
        
        color = self._score_color(score)
        bar_char = "█"
        empty_char = "░"
        
        bar = bar_char * filled + empty_char * empty
        return f"{color}{bar}{self.RESET}"

    def _get_ascii_header(self) -> str:
        """Generate the ASCII art header."""
        header = f"""
{self._color('╔══════════════════════════════════════════════════════════════╗', self.RED)}
{self._color('║', self.RED)}  {self._color('🔥', self.YELLOW)}  {self._color('███████╗██╗████████╗███████╗      ██████╗  ██████╗  █████╗ ███████╗████████╗', self.RED)}  {self._color('║', self.RED)}
{self._color('║', self.RED)}  {self._color('🔥', self.YELLOW)}  {self._color('██╔════╝██║╚══██╔══╝██╔════╝      ██╔══██╗██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝', self.RED)}  {self._color('║', self.RED)}
{self._color('║', self.RED)}  {self._color('🔥', self.YELLOW)}  {self._color('███████╗██║   ██║   ███████╗█████╗██████╔╝██║   ██║███████║███████╗   ██║   ', self.RED)}  {self._color('║', self.RED)}
{self._color('║', self.RED)}  {self._color('🔥', self.YELLOW)}  {self._color('╚════██║██║   ██║   ╚════██║╚════╝██╔══██╗██║   ██║██╔══██║╚════██║   ██║   ', self.RED)}  {self._color('║', self.RED)}
{self._color('║', self.RED)}  {self._color('🔥', self.YELLOW)}  {self._color('███████║██║   ██║   ███████║      ██║  ██║╚██████╔╝██║  ██║███████║   ██║   ', self.RED)}  {self._color('║', self.RED)}
{self._color('║', self.RED)}  {self._color('🔥', self.YELLOW)}  {self._color('╚══════╝╚═╝   ╚═╝   ╚══════╝      ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝   ', self.RED)}  {self._color('║', self.RED)}
{self._color('╠══════════════════════════════════════════════════════════════╣', self.RED)}
{self._color('║', self.RED)}     {self._color('Gordon Ramsay meets Web Development', self.YELLOW)}                       {self._color('║', self.RED)}
{self._color('╚══════════════════════════════════════════════════════════════╝', self.RED)}
"""
        return header

    def _format_category(self, name: str, result: AuditResult) -> str:
        """Format a single category for terminal output."""
        lines = []
        
        score_color = self._score_color(result.score)
        progress_bar = self._get_progress_bar(result.score)
        
        # Category header with score
        lines.append(f"\n{self.BOLD}{self._color('▶', self.CYAN)} {name}{self.RESET}")
        lines.append(f"  Score: {self._color(f'{result.score}/100', score_color)} {progress_bar}")
        
        # Roast comment
        roast = self.roaster.get_roast(result.score, name)
        if roast:
            lines.append(f"  {self._color('💬', self.MAGENTA)} {roast}")
        
        # Findings
        if result.findings:
            lines.append(f"  {self.DIM}Findings:{self.RESET}")
            for finding in result.findings[:4]:  # Limit to 4 findings
                lines.append(f"    {self._color('•', self.BLUE)} {finding}")
        
        # Recommendations (if verbose)
        if self.verbose and result.recommendations:
            lines.append(f"  {self._color('💡', self.YELLOW)} Recommendations:")
            for rec in result.recommendations[:3]:  # Limit to 3 recommendations
                lines.append(f"    {self._color('→', self.GREEN)} {rec}")
        
        return "\n".join(lines)

    def _format_grade(self, grade: str, score: int) -> str:
        """Format the overall grade display."""
        grade_colors = {
            "A+": self.GREEN, "A": self.GREEN, "A-": self.GREEN,
            "B+": self.CYAN, "B": self.CYAN, "B-": self.CYAN,
            "C+": self.YELLOW, "C": self.YELLOW, "C-": self.YELLOW,
            "D+": "\033[38;5;208m", "D": "\033[38;5;208m", "D-": "\033[38;5;208m",
            "F": self.RED,
        }
        
        color = grade_colors.get(grade, self.WHITE)
        
        # Big grade display
        lines = [
            "",
            self._color("═" * 64, self.RED),
            "",
            f"                    {self.BOLD}{self._color('FINAL GRADE', self.WHITE)}{self.RESET}",
            "",
            f"                         {self.BOLD}{self._color(grade, color)}{self.RESET}",
            f"                       {self._color(f'({score}/100)', self.DIM)}",
            "",
        ]
        
        # Overall roast
        overall_roast = self.roaster.get_overall_roast(grade, score)
        lines.append(f"           {self._color(overall_roast, self.CYAN)}")
        lines.append("")
        lines.append(self._color("═" * 64, self.RED))
        
        return "\n".join(lines)

    def generate(self, audit: WebsiteAudit) -> str:
        """Generate the complete terminal report."""
        lines = []
        
        # Header
        lines.append(self._get_ascii_header())
        
        # URL info
        lines.append(f"\n{self.BOLD}Target:{self.RESET} {self._color(audit.url, self.CYAN)}")
        lines.append(f"{self.DIM}Audit completed in {audit.duration_ms}ms{self.RESET}")
        
        # Categories
        categories = [
            ("Title Tag", audit.title),
            ("Meta Description", audit.meta_description),
            ("Headings", audit.headings),
            ("Images", audit.images),
            ("Mobile", audit.mobile),
            ("SSL/Security", audit.ssl_security),
            ("Performance", audit.performance),
            ("Links", audit.links),
            ("Open Graph", audit.open_graph),
            ("Schema/Structured Data", audit.schema),
        ]
        
        for name, result in categories:
            lines.append(self._format_category(name, result))
        
        # Overall grade
        lines.append(self._format_grade(audit.get_grade(), audit.get_overall_score()))
        
        # Footer
        lines.append(f"\n{self.DIM}Built by Cybrflux — We build what AI can't... yet.{self.RESET}")
        lines.append(f"{self.DIM}https://github.com/M4ST3R-C0NTR0L{self.RESET}\n")
        
        return "\n".join(lines)


class MarkdownReporter(BaseReporter):
    """Generate Markdown report output."""

    def generate(self, audit: WebsiteAudit) -> str:
        """Generate the complete Markdown report."""
        lines = []
        
        # Header
        lines.append("# 🔥 Site Roast Report")
        lines.append("")
        lines.append(f"**Target:** `{audit.url}`  ")
        lines.append(f"**Audited:** {self._format_timestamp(audit.timestamp)}  ")
        lines.append(f"**Duration:** {audit.duration_ms}ms")
        lines.append("")
        
        # Overall grade
        grade = audit.get_grade()
        score = audit.get_overall_score()
        
        grade_emoji = self._grade_emoji(grade)
        lines.append(f"## {grade_emoji} Overall Grade: **{grade}** ({score}/100)")
        lines.append("")
        
        overall_roast = self.roaster.get_overall_roast(grade, score)
        lines.append(f"> {overall_roast}")
        lines.append("")
        
        # Summary table
        lines.append("## 📊 Category Summary")
        lines.append("")
        lines.append("| Category | Score | Grade | Status |")
        lines.append("|----------|-------|-------|--------|")
        
        categories = [
            ("Title Tag", audit.title),
            ("Meta Description", audit.meta_description),
            ("Headings", audit.headings),
            ("Images", audit.images),
            ("Mobile", audit.mobile),
            ("SSL/Security", audit.ssl_security),
            ("Performance", audit.performance),
            ("Links", audit.links),
            ("Open Graph", audit.open_graph),
            ("Schema/Structured Data", audit.schema),
        ]
        
        for name, result in categories:
            status = self._score_status(result.score)
            mini_grade = self._score_to_mini_grade(result.score)
            lines.append(f"| {name} | {result.score}/100 | {mini_grade} | {status} |")
        
        lines.append("")
        
        # Detailed breakdown
        lines.append("## 🔍 Detailed Analysis")
        lines.append("")
        
        for name, result in categories:
            lines.append(self._format_category_markdown(name, result))
        
        # Footer
        lines.append("---")
        lines.append("")
        lines.append("*Generated by [site-roast](https://github.com/M4ST3R-C0NTR0L/site-roast) — Built by [Cybrflux](https://github.com/M4ST3R-C0NTR0L)*")
        
        return "\n".join(lines)

    def _format_timestamp(self, timestamp: float) -> str:
        """Format timestamp for display."""
        from datetime import datetime
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    def _grade_emoji(self, grade: str) -> str:
        """Get emoji for grade."""
        if grade.startswith("A"):
            return "🌟"
        elif grade.startswith("B"):
            return "✅"
        elif grade.startswith("C"):
            return "⚠️"
        elif grade.startswith("D"):
            return "🔧"
        else:
            return "💀"

    def _score_status(self, score: int) -> str:
        """Get status emoji for score."""
        if score >= 80:
            return "✅ Good"
        elif score >= 60:
            return "⚠️ Needs Work"
        else:
            return "🔴 Poor"

    def _score_to_mini_grade(self, score: int) -> str:
        """Convert score to mini grade."""
        if score >= 93:
            return "A"
        elif score >= 85:
            return "B"
        elif score >= 75:
            return "C"
        elif score >= 65:
            return "D"
        else:
            return "F"

    def _format_category_markdown(self, name: str, result: AuditResult) -> str:
        """Format a single category for Markdown."""
        lines = []
        
        roast = self.roaster.get_roast(result.score, name)
        
        lines.append(f"### {name}: {result.score}/100")
        lines.append("")
        lines.append(f"*{roast}*")
        lines.append("")
        
        if result.findings:
            lines.append("**Findings:**")
            for finding in result.findings:
                lines.append(f"- {finding}")
            lines.append("")
        
        if self.verbose and result.recommendations:
            lines.append("**Recommendations:**")
            for rec in result.recommendations:
                lines.append(f"- {rec}")
            lines.append("")
        
        return "\n".join(lines)


class JsonReporter(BaseReporter):
    """Generate JSON report output."""

    def generate(self, audit: WebsiteAudit) -> str:
        """Generate the complete JSON report."""
        data = {
            "url": audit.url,
            "timestamp": audit.timestamp,
            "duration_ms": audit.duration_ms,
            "overall_score": audit.get_overall_score(),
            "grade": audit.get_grade(),
            "categories": {
                "title": self._category_to_dict("Title Tag", audit.title),
                "meta_description": self._category_to_dict("Meta Description", audit.meta_description),
                "headings": self._category_to_dict("Headings", audit.headings),
                "images": self._category_to_dict("Images", audit.images),
                "mobile": self._category_to_dict("Mobile", audit.mobile),
                "ssl_security": self._category_to_dict("SSL/Security", audit.ssl_security),
                "performance": self._category_to_dict("Performance", audit.performance),
                "links": self._category_to_dict("Links", audit.links),
                "open_graph": self._category_to_dict("Open Graph", audit.open_graph),
                "schema": self._category_to_dict("Schema/Structured Data", audit.schema),
            }
        }
        
        return json.dumps(data, indent=2)

    def _category_to_dict(self, name: str, result: AuditResult) -> Dict[str, Any]:
        """Convert AuditResult to dictionary."""
        roast = self.roaster.get_roast(result.score, name) if not self.no_roast else ""
        
        data = {
            "name": name,
            "score": result.score,
            "max_score": result.max_score,
            "findings": result.findings,
            "recommendations": result.recommendations if self.verbose else [],
            "raw_data": result.raw_data,
        }
        
        if roast:
            data["roast"] = roast
        
        return data
