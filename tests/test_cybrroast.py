"""
Tests for CybrRoast.

Run with: pytest
"""

import pytest
from cybrroast.auditor import AuditResult, WebsiteAuditor
from cybrroast.roaster import Roaster
from cybrroast.reporter import TerminalReporter, MarkdownReporter, JsonReporter
from cybrroast.scores import ScoreCalculator, ScoreThresholds


class TestAuditResult:
    """Tests for AuditResult dataclass."""

    def test_audit_result_creation(self):
        result = AuditResult(score=85, findings=["test"], recommendations=["fix"])
        assert result.score == 85
        assert result.findings == ["test"]
        assert result.recommendations == ["fix"]

    def test_audit_result_defaults(self):
        result = AuditResult(score=50)
        assert result.max_score == 100
        assert result.findings == []
        assert result.recommendations == []


class TestRoaster:
    """Tests for Roaster class."""

    def test_roaster_creation(self):
        roaster = Roaster()
        assert roaster.no_roast is False

    def test_roaster_no_roast_mode(self):
        roaster = Roaster(no_roast=True)
        assert roaster.no_roast is True
        comment = roaster.get_roast(50)
        assert "This isn't a website" not in comment  # Should be serious

    def test_get_roast_returns_string(self):
        roaster = Roaster()
        for score in [0, 25, 50, 75, 95, 100]:
            roast = roaster.get_roast(score)
            assert isinstance(roast, str)
            assert len(roast) > 0

    def test_get_overall_roast(self):
        roaster = Roaster()
        roast = roaster.get_overall_roast("A", 95)
        assert isinstance(roast, str)
        assert len(roast) > 0


class TestScoreCalculator:
    """Tests for ScoreCalculator class."""

    def test_normalize_score(self):
        calc = ScoreCalculator()
        assert calc.normalize_score(50, 0, 100) == 50
        assert calc.normalize_score(75, 0, 100) == 75
        assert calc.normalize_score(0, 0, 100) == 0
        assert calc.normalize_score(100, 0, 100) == 100

    def test_calculate_average(self):
        calc = ScoreCalculator()
        assert calc.calculate_average([80, 90, 100]) == 90
        assert calc.calculate_average([50]) == 50
        assert calc.calculate_average([]) == 0

    def test_score_to_grade(self):
        calc = ScoreCalculator()
        assert calc.score_to_grade(98) == "A+"
        assert calc.score_to_grade(95) == "A"
        assert calc.score_to_grade(85) == "B"
        assert calc.score_to_grade(75) == "C"
        assert calc.score_to_grade(65) == "D"
        assert calc.score_to_grade(50) == "F"

    def test_grade_description(self):
        calc = ScoreCalculator()
        desc = calc.grade_description("A+")
        assert isinstance(desc, str)
        assert len(desc) > 0

    def test_penalty(self):
        calc = ScoreCalculator()
        assert calc.penalty(100, 20) == 80
        assert calc.penalty(50, 20, min_score=40) == 40

    def test_bonus(self):
        calc = ScoreCalculator()
        assert calc.bonus(50, 20) == 70
        assert calc.bonus(90, 20, max_score=100) == 100


class TestScoreThresholds:
    """Tests for ScoreThresholds class."""

    def test_categorize(self):
        assert ScoreThresholds.categorize(95) == "excellent"
        assert ScoreThresholds.categorize(80) == "good"
        assert ScoreThresholds.categorize(65) == "average"
        assert ScoreThresholds.categorize(50) == "poor"
        assert ScoreThresholds.categorize(30) == "critical"
        assert ScoreThresholds.categorize(10) == "disaster"

    def test_get_threshold(self):
        assert ScoreThresholds.get_threshold("excellent") == 90
        assert ScoreThresholds.get_threshold("good") == 75


class TestReporters:
    """Tests for reporter classes."""

    def test_terminal_reporter_creation(self):
        reporter = TerminalReporter(no_roast=False, verbose=True)
        assert reporter.no_roast is False
        assert reporter.verbose is True

    def test_markdown_reporter_creation(self):
        reporter = MarkdownReporter(no_roast=False, verbose=True)
        assert reporter.no_roast is False

    def test_json_reporter_creation(self):
        reporter = JsonReporter(no_roast=False, verbose=True)
        assert reporter.no_roast is False


class TestCLI:
    """Tests for CLI functionality."""

    def test_validate_url_adds_https(self):
        from site_roast.cli import validate_url
        # Mock test - just check function exists
        assert callable(validate_url)

    def test_detect_output_format(self):
        from site_roast.cli import detect_output_format
        assert detect_output_format("report.json") == "json"
        assert detect_output_format("report.md") == "markdown"
        assert detect_output_format("report.markdown") == "markdown"
        assert detect_output_format("report.txt") is None
        assert detect_output_format(None) is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
