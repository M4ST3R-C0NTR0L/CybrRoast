"""
CybrRoast: A brutal, funny website auditor.

Roast any website's SEO, performance, and design with actual technical scores.
Think Gordon Ramsay meets web development.
"""

__version__ = "1.0.0"
__author__ = "Cybrflux"
__email__ = ""
__license__ = "MIT"

from .auditor import WebsiteAuditor
from .roaster import Roaster
from .reporter import TerminalReporter, MarkdownReporter, JsonReporter

__all__ = [
    "WebsiteAuditor",
    "Roaster",
    "TerminalReporter",
    "MarkdownReporter",
    "JsonReporter",
]
