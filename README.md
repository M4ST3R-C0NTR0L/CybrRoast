# 🔥 CybrRoast

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/CybrRoast.svg)](https://badge.fury.io/py/CybrRoast)
[![GitHub stars](https://img.shields.io/github/stars/M4ST3R-C0NTR0L/CybrRoast.svg?style=social&label=Star)](https://github.com/M4ST3R-C0NTR0L/CybrRoast)

> **Roast any website's SEO, performance, and design with brutal honesty and actual technical scores.**
> 
> Think Gordon Ramsay meets web development. 🍳

## ✨ What is CybrRoast?

`CybrRoast` is a CLI tool that audits websites across 10 critical categories and delivers the results with **genuinely funny** commentary. No corporate cringe — just hard truths served with humor.

Perfect for:
- Developers who want honest feedback
- SEO specialists validating their work
- Agencies roasting competitor sites (or their own)
- Anyone who enjoys watching bad websites get dragged

## 🚀 Quick Start

```bash
pip install CybrRoast
CybrRoast https://example.com
```

That's it. No API keys. No config files. Just pure roast energy.

## 📊 Demo Output

```
╔══════════════════════════════════════════════════════════════╗
║  🔥  ███████╗██╗████████╗███████╗      ██████╗  ██████╗  █████╗ ███████╗████████╗  ║
║  🔥  ██╔════╝██║╚══██╔══╝██╔════╝      ██╔══██╗██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝  ║
║  🔥  ███████╗██║   ██║   ███████╗█████╗██████╔╝██║   ██║███████║███████╗   ██║     ║
║  🔥  ╚════██║██║   ██║   ╚════██║╚════╝██╔══██╗██║   ██║██╔══██║╚════██║   ██║     ║
║  🔥  ███████║██║   ██║   ███████║      ██║  ██║╚██████╔╝██║  ██║███████║   ██║     ║
║  🔥  ╚══════╝╚═╝   ╚═╝   ╚══════╝      ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝     ║
╠══════════════════════════════════════════════════════════════╣
║     Gordon Ramsay meets Web Development                       ║
╚══════════════════════════════════════════════════════════════╝

Target: https://example.com
Audit completed in 847ms

▶ Title Tag
  Score: 45/100 ████████░░░░░░░░░░░░
  💬 Yikes. Did an intern build this during their lunch break?
  Findings:
    • Title found: 'Example Domain'
    • Title length: 14 characters
    • Title is too short
    • Title appears to be generic

▶ Meta Description
  Score: 0/100 ░░░░░░░░░░░░░░░░░░░░
  💬 This isn't a website. This is a cry for help. 💀
  Findings:
    • No meta description found

▶ Headings
  Score: 70/100 ██████████████░░░░░░
  💬 It's giving 'we did the bare minimum' vibes.
  Findings:
    • Found 1 H1, 0 H2, 0 H3 tags
    • No H1 tag found - every page needs one main heading

▶ Images
  Score: 100/100 ████████████████████
  💬 Okay, this is actually fire. Respect. 🔥
  Findings:
    • Found 0 image(s)

▶ Mobile
  Score: 100/100 ████████████████████
  💬 Finally! A website that doesn't make me want to cry.
  Findings:
    • Viewport found: width=device-width, initial-scale=1

▶ SSL/Security
  Score: 70/100 ██████████████░░░░░░
  💬 Functional, but about as exciting as a tax form.
  Findings:
    • HTTPS is enabled ✓
    • Security headers found: 0/5

▶ Performance
  Score: 95/100 ███████████████████░
  💬 Not bad, not bad. Your SEO person deserves a raise.
  Findings:
    • Page size: 1.2 KB
    • External resources: 0 CSS, 0 JS, 0 images

▶ Links
  Score: 30/100 ██████░░░░░░░░░░░░░░
  💬 I've seen better websites on GeoCities in 1998.
  Findings:
    • Found 1 link(s)
    • Internal links: 1
    • External links: 0
    • Very few links on page

▶ Open Graph
  Score: 0/100 ░░░░░░░░░░░░░░░░░░░░
  💬 Your website just asked me if it could copy my homework.
  Findings:
    • Open Graph tags found: 0/5

▶ Schema/Structured Data
  Score: 0/100 ░░░░░░░░░░░░░░░░░░░░
  💬 Burn it down and start over. Trust me on this one.
  Findings:
    • Found 0 JSON-LD script(s)
    • No structured data found

════════════════════════════════════════════════════════════════

                    FINAL GRADE

                         D
                       (35/100)

           F stands for 'Find a new web developer'. Immediately.

════════════════════════════════════════════════════════════════

Built by Cybrflux — We build what AI can't... yet.
https://github.com/M4ST3R-C0NTR0L
```

## 🎯 Features

- ✅ **10 Comprehensive Audits**: Title, meta description, headings, images, mobile, SSL, performance, links, Open Graph, Schema
- ✅ **Colorful Terminal Output**: Beautiful ANSI-colored reports with progress bars
- ✅ **Multiple Output Formats**: Terminal (default), JSON (`--json`), Markdown (`--markdown`)
- ✅ **Serious Mode**: `--no-roast` flag for professional reports without jokes
- ✅ **Verbose Recommendations**: `--verbose` flag for detailed improvement tips
- ✅ **File Export**: Save reports with `--output report.json` or `--output report.md`
- ✅ **Genuinely Funny Roasts**: No corporate cringe. Just honest comedy.
- ✅ **Zero Config**: Works out of the box
- ✅ **Fast**: Audits complete in under a second

## 📋 Audit Categories

| Category | What We Check |
|----------|---------------|
| **Title Tag** | Existence, length (50-60 chars optimal), keyword quality |
| **Meta Description** | Existence, length (150-160 chars), compelling copy |
| **Headings** | H1 presence, proper hierarchy (H1→H2→H3), count |
| **Images** | Alt tags, lazy loading hints, modern formats |
| **Mobile** | Viewport meta, responsive indicators, fixed widths |
| **SSL/Security** | HTTPS enforcement, security headers (HSTS, CSP, etc.) |
| **Performance** | Page size, resource count, render-blocking hints |
| **Links** | Internal/external ratio, rel attributes, structure |
| **Open Graph** | Social sharing tags (title, description, image, URL) |
| **Schema** | JSON-LD structured data, schema types, microdata |

## 🔧 Installation

### From PyPI (Recommended)

```bash
pip install CybrRoast
```

### From Source

```bash
git clone https://github.com/M4ST3R-C0NTR0L/CybrRoast.git
cd CybrRoast
pip install -e .
```

## 📖 Usage

### Basic Usage

```bash
# Roast a website
CybrRoast https://example.com

# Output as JSON
CybrRoast https://example.com --json

# Generate Markdown report
CybrRoast https://example.com --markdown --output report.md

# Serious mode (no jokes)
CybrRoast https://example.com --no-roast

# Verbose with recommendations
CybrRoast https://example.com --verbose
```

### All Options

```
usage: CybrRoast [-h] [--version] [--json] [--markdown] [--no-roast] 
                  [--verbose] [--timeout TIMEOUT] [--user-agent USER_AGENT] 
                  [--output OUTPUT]
                  url

🔥 Roast any website's SEO, performance, and design.

positional arguments:
  url                   The website URL to roast

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --json                Output results as JSON
  --markdown, --md      Output results as Markdown
  --no-roast            Serious mode: output scores without jokes
  --verbose, -v         Show detailed recommendations
  --timeout TIMEOUT     Request timeout in seconds (default: 30)
  --user-agent USER_AGENT
                        Custom User-Agent string
  --output OUTPUT, -o OUTPUT
                        Save output to file
```

## 📝 Scoring Methodology

Each category is scored 0-100 based on:

- **100**: Meets or exceeds all best practices
- **80-99**: Minor issues, mostly compliant
- **60-79**: Acceptable but needs improvement
- **40-59**: Significant problems
- **20-39**: Poor, major issues
- **0-19**: Critical failures

### Grade Scale

| Score | Grade | Description |
|-------|-------|-------------|
| 97-100 | A+ | Exceptional |
| 93-96 | A | Excellent |
| 90-92 | A- | Very Good |
| 87-89 | B+ | Good |
| 83-86 | B | Above Average |
| 80-82 | B- | Average Plus |
| 77-79 | C+ | Slightly Above Average |
| 73-76 | C | Average |
| 70-72 | C- | Below Average |
| 67-69 | D+ | Poor |
| 63-66 | D | Very Poor |
| 60-62 | D- | Critical |
| 0-59 | F | Failing |

## 🧪 Examples

### CI/CD Integration

```bash
# Fail build if score is below 70
CybrRoast https://example.com --json | jq '.overall_score' | xargs -I {} sh -c '[ {} -ge 70 ] || exit 1'
```

### Batch Auditing

```bash
# Audit multiple sites
for url in site1.com site2.com site3.com; do
    CybrRoast "https://$url" --markdown --output "reports/$url.md"
done
```

### API Integration

```bash
# Get JSON for programmatic use
CybrRoast https://example.com --json | jq '.categories.title.score'
# Output: 45
```

## 🤝 Contributing

We love contributions! Here's how to get started:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/your-username/CybrRoast.git`
3. **Install dev dependencies**: `pip install -e ".[dev]"`
4. **Create a branch**: `git checkout -b feature/amazing-feature`
5. **Make your changes** and add tests
6. **Run tests**: `pytest`
7. **Commit**: `git commit -m "Add amazing feature"`
8. **Push**: `git push origin feature/amazing-feature`
9. **Open a Pull Request**

### Development Setup

```bash
# Clone and setup
git clone https://github.com/M4ST3R-C0NTR0L/CybrRoast.git
cd CybrRoast
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=site_roast

# Format code
black site_roast/

# Type checking
mypy site_roast/
```

### Adding New Roast Comments

Want to make the roasts even funnier? Edit `site_roast/roaster.py` and add your best burns to the appropriate score range lists. Keep it:
- Actually funny (no dad jokes)
- Constructive (roast + inform)
- Original

## 🗺️ Roadmap

- [ ] Lighthouse-style performance metrics
- [ ] Broken link checker
- [ ] Accessibility audit (WCAG)
- [ ] Content quality analysis (readability)
- [ ] Sitemap.xml validation
- [ ] robots.txt analysis
- [ ] Core Web Vitals integration
- [ ] HTML email report generation

## 📄 License

MIT License — see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the brutally honest feedback we all need sometimes
- Built with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) and [Requests](https://requests.readthedocs.io/)
- ASCII art generated with love (and a bit of rage)

---

<div align="center">

**Built by [Cybrflux](https://github.com/M4ST3R-C0NTR0L)** — *We build what AI can't... yet.*

[Website](https://github.com/M4ST3R-C0NTR0L) • [GitHub](https://github.com/M4ST3R-C0NTR0L) • [Twitter](https://github.com/M4ST3R-C0NTR0L)

</div>
