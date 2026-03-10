"""
Core audit engine for site-roast.

Fetches websites and analyzes them across 10 SEO/performance categories.
"""

import re
import ssl
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


@dataclass
class AuditResult:
    """Container for a single audit category result."""
    score: int  # 0-100
    max_score: int = 100
    findings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WebsiteAudit:
    """Complete audit results for a website."""
    url: str
    timestamp: float
    duration_ms: int
    title: AuditResult
    meta_description: AuditResult
    headings: AuditResult
    images: AuditResult
    mobile: AuditResult
    ssl_security: AuditResult
    performance: AuditResult
    links: AuditResult
    open_graph: AuditResult
    schema: AuditResult
    
    def get_overall_score(self) -> int:
        """Calculate the overall score across all categories."""
        scores = [
            self.title.score,
            self.meta_description.score,
            self.headings.score,
            self.images.score,
            self.mobile.score,
            self.ssl_security.score,
            self.performance.score,
            self.links.score,
            self.open_graph.score,
            self.schema.score,
        ]
        return round(sum(scores) / len(scores))
    
    def get_grade(self) -> str:
        """Convert overall score to letter grade."""
        score = self.get_overall_score()
        if score >= 97:
            return "A+"
        elif score >= 93:
            return "A"
        elif score >= 90:
            return "A-"
        elif score >= 87:
            return "B+"
        elif score >= 83:
            return "B"
        elif score >= 80:
            return "B-"
        elif score >= 77:
            return "C+"
        elif score >= 73:
            return "C"
        elif score >= 70:
            return "C-"
        elif score >= 67:
            return "D+"
        elif score >= 63:
            return "D"
        elif score >= 60:
            return "D-"
        else:
            return "F"


class WebsiteAuditor:
    """
    Website auditor that fetches and analyzes web pages.
    
    Performs comprehensive audits across 10 categories:
    - Title Tag
    - Meta Description
    - Headings (H1-H6)
    - Images (alt tags)
    - Mobile Responsiveness
    - SSL/Security
    - Performance
    - Links
    - Open Graph
    - Schema/Structured Data
    """

    def __init__(self, timeout: int = 30, user_agent: str = "site-roast/1.0"):
        """
        Initialize the auditor.
        
        Args:
            timeout: Request timeout in seconds.
            user_agent: User-Agent string for HTTP requests.
        """
        self.timeout = timeout
        self.user_agent = user_agent
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
        })

    def audit(self, url: str) -> WebsiteAudit:
        """
        Perform a complete audit of the given URL.
        
        Args:
            url: The URL to audit.
            
        Returns:
            WebsiteAudit containing all results.
        """
        start_time = time.time()
        
        # Fetch the page
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        html_content = response.text
        
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Get response size
        content_length = len(response.content)
        
        # Perform all audits
        return WebsiteAudit(
            url=url,
            timestamp=start_time,
            duration_ms=duration_ms,
            title=self._audit_title(soup),
            meta_description=self._audit_meta_description(soup),
            headings=self._audit_headings(soup),
            images=self._audit_images(soup),
            mobile=self._audit_mobile(soup, response),
            ssl_security=self._audit_ssl_security(url, response),
            performance=self._audit_performance(response, content_length, html_content),
            links=self._audit_links(soup, url),
            open_graph=self._audit_open_graph(soup),
            schema=self._audit_schema(soup),
        )

    def _audit_title(self, soup: BeautifulSoup) -> AuditResult:
        """Audit the page title."""
        findings = []
        recommendations = []
        
        title_tag = soup.find("title")
        
        if not title_tag or not title_tag.get_text(strip=True):
            findings.append("No title tag found")
            recommendations.append("Add a <title> tag to your <head> section")
            return AuditResult(score=0, findings=findings, recommendations=recommendations)
        
        title = title_tag.get_text(strip=True)
        title_length = len(title)
        
        findings.append(f"Title found: '{title}'")
        findings.append(f"Title length: {title_length} characters")
        
        # Score based on length
        if 50 <= title_length <= 60:
            score = 100
            findings.append("Title length is optimal for search engines")
        elif 30 <= title_length < 50 or 60 < title_length <= 70:
            score = 80
            findings.append("Title length is acceptable but could be improved")
            recommendations.append("Aim for 50-60 characters for optimal display")
        elif title_length < 30:
            score = 50
            findings.append("Title is too short")
            recommendations.append("Expand your title to 50-60 characters")
        else:
            score = 60
            findings.append("Title is too long and may be truncated in search results")
            recommendations.append("Shorten your title to 50-60 characters")
        
        # Check for generic titles
        generic_words = ["home", "untitled", "index", "page", "website"]
        if any(word in title.lower() for word in generic_words):
            score = max(0, score - 30)
            findings.append("Title appears to be generic")
            recommendations.append("Use a descriptive, unique title that describes your page content")
        
        return AuditResult(
            score=score,
            findings=findings,
            recommendations=recommendations,
            raw_data={"title": title, "length": title_length}
        )

    def _audit_meta_description(self, soup: BeautifulSoup) -> AuditResult:
        """Audit the meta description."""
        findings = []
        recommendations = []
        
        meta_desc = soup.find("meta", attrs={"name": "description"})
        
        if not meta_desc:
            findings.append("No meta description found")
            recommendations.append("Add a meta description: <meta name='description' content='...'>")
            return AuditResult(score=0, findings=findings, recommendations=recommendations)
        
        content = meta_desc.get("content", "").strip()
        desc_length = len(content)
        
        findings.append(f"Meta description found")
        findings.append(f"Description length: {desc_length} characters")
        
        if not content:
            findings.append("Meta description is empty")
            recommendations.append("Add meaningful content to your meta description")
            return AuditResult(score=10, findings=findings, recommendations=recommendations)
        
        # Score based on length
        if 150 <= desc_length <= 160:
            score = 100
            findings.append("Description length is optimal")
        elif 120 <= desc_length < 150 or 160 < desc_length <= 170:
            score = 85
            findings.append("Description length is good")
            recommendations.append("Aim for 150-160 characters for optimal display")
        elif desc_length < 120:
            score = 60
            findings.append("Description is too short")
            recommendations.append("Expand your description to 150-160 characters")
        else:
            score = 70
            findings.append("Description is too long and may be truncated")
            recommendations.append("Shorten your description to 150-160 characters")
        
        # Check for generic descriptions
        generic_phrases = ["this is a website", "welcome to", "click here", "learn more"]
        if any(phrase in content.lower() for phrase in generic_phrases):
            score = max(0, score - 20)
            findings.append("Description appears to be generic")
            recommendations.append("Write a compelling, unique description that entices clicks")
        
        return AuditResult(
            score=score,
            findings=findings,
            recommendations=recommendations,
            raw_data={"description": content, "length": desc_length}
        )

    def _audit_headings(self, soup: BeautifulSoup) -> AuditResult:
        """Audit heading structure (H1-H6)."""
        findings = []
        recommendations = []
        
        h1_tags = soup.find_all("h1")
        h2_tags = soup.find_all("h2")
        h3_tags = soup.find_all("h3")
        all_headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        
        findings.append(f"Found {len(h1_tags)} H1, {len(h2_tags)} H2, {len(h3_tags)} H3 tags")
        
        score = 100
        
        # Check for H1
        if len(h1_tags) == 0:
            score = max(0, score - 40)
            findings.append("No H1 tag found - every page needs one main heading")
            recommendations.append("Add an H1 tag that describes your main content")
        elif len(h1_tags) > 1:
            score = max(0, score - 20)
            findings.append(f"Multiple H1 tags found ({len(h1_tags)}). Use only one H1 per page.")
            recommendations.append("Consolidate to a single H1 tag")
        else:
            h1_text = h1_tags[0].get_text(strip=True)
            if h1_text:
                findings.append(f"H1 content: '{h1_text[:50]}...'")
            else:
                score = max(0, score - 15)
                findings.append("H1 tag is empty")
                recommendations.append("Add text content to your H1 tag")
        
        # Check heading hierarchy
        heading_levels = []
        for tag in all_headings:
            level = int(tag.name[1])
            heading_levels.append(level)
        
        if heading_levels:
            # Check for skipped levels
            prev_level = 0
            skipped_levels = []
            for level in heading_levels:
                if level > prev_level + 1:
                    skipped_levels.append(f"H{prev_level} -> H{level}")
                prev_level = level
            
            if skipped_levels:
                score = max(0, score - 10)
                findings.append(f"Skipped heading levels detected: {', '.join(skipped_levels[:3])}")
                recommendations.append("Maintain proper heading hierarchy (don't skip from H1 to H3)")
        
        if len(all_headings) == 0:
            score = 0
            findings.append("No heading tags found at all")
            recommendations.append("Structure your content with proper heading tags (H1-H6)")
        
        return AuditResult(
            score=score,
            findings=findings,
            recommendations=recommendations,
            raw_data={
                "h1_count": len(h1_tags),
                "h2_count": len(h2_tags),
                "h3_count": len(h3_tags),
                "total_headings": len(all_headings),
            }
        )

    def _audit_images(self, soup: BeautifulSoup) -> AuditResult:
        """Audit images for alt tags and optimization."""
        findings = []
        recommendations = []
        
        images = soup.find_all("img")
        total_images = len(images)
        
        findings.append(f"Found {total_images} image(s)")
        
        if total_images == 0:
            findings.append("No images on page - consider adding visual content")
            return AuditResult(score=70, findings=findings, recommendations=recommendations)
        
        # Check for alt tags
        missing_alt = 0
        empty_alt = 0
        
        for img in images:
            alt = img.get("alt")
            if alt is None:
                missing_alt += 1
            elif not alt.strip():
                empty_alt += 1
        
        with_alt = total_images - missing_alt - empty_alt
        
        findings.append(f"Images with alt text: {with_alt}/{total_images}")
        
        if missing_alt > 0:
            findings.append(f"Missing alt attributes: {missing_alt}")
        if empty_alt > 0:
            findings.append(f"Empty alt attributes: {empty_alt}")
        
        # Calculate score
        if total_images > 0:
            alt_coverage = with_alt / total_images
            score = int(alt_coverage * 100)
        else:
            score = 100
        
        # Penalties for specific issues
        if missing_alt > 0:
            score = max(0, score - 10)
            recommendations.append(f"Add alt attributes to {missing_alt} image(s)")
        
        if empty_alt > 0:
            score = max(0, score - 5)
            recommendations.append(f"Add descriptive alt text to {empty_alt} image(s)")
        
        # Check for lazy loading hints
        lazy_loaded = sum(1 for img in images if img.get("loading") == "lazy")
        if lazy_loaded < total_images * 0.5 and total_images > 5:
            recommendations.append("Consider adding loading='lazy' to images below the fold")
        
        return AuditResult(
            score=score,
            findings=findings,
            recommendations=recommendations,
            raw_data={
                "total": total_images,
                "with_alt": with_alt,
                "missing_alt": missing_alt,
                "empty_alt": empty_alt,
                "lazy_loaded": lazy_loaded,
            }
        )

    def _audit_mobile(self, soup: BeautifulSoup, response: requests.Response) -> AuditResult:
        """Audit mobile responsiveness."""
        findings = []
        recommendations = []
        
        score = 100
        
        # Check for viewport meta tag
        viewport = soup.find("meta", attrs={"name": "viewport"})
        
        if not viewport:
            score = max(0, score - 40)
            findings.append("No viewport meta tag found")
            recommendations.append("Add: <meta name='viewport' content='width=device-width, initial-scale=1'>")
        else:
            content = viewport.get("content", "")
            findings.append(f"Viewport found: {content}")
            
            if "width=device-width" not in content:
                score = max(0, score - 20)
                findings.append("Viewport missing 'width=device-width'")
                recommendations.append("Add width=device-width to viewport content")
        
        # Check for mobile-friendly CSS hints
        styles = soup.find_all("link", rel="stylesheet")
        media_queries = len(soup.find_all(string=re.compile(r"@media")))
        
        if media_queries > 0:
            findings.append(f"Found {media_queries} media query references")
        
        # Check for large fixed widths that break mobile
        fixed_width_pattern = re.compile(r'width\s*:\s*\d{4,}px', re.IGNORECASE)
        if fixed_width_pattern.search(response.text):
            score = max(0, score - 15)
            findings.append("Fixed widths >1000px detected - may cause horizontal scrolling on mobile")
            recommendations.append("Use relative units (%, vw, rem) instead of large fixed pixel widths")
        
        return AuditResult(
            score=score,
            findings=findings,
            recommendations=recommendations,
            raw_data={"viewport": viewport.get("content") if viewport else None}
        )

    def _audit_ssl_security(self, url: str, response: requests.Response) -> AuditResult:
        """Audit SSL/HTTPS and security headers."""
        findings = []
        recommendations = []
        
        score = 100
        parsed = urlparse(url)
        
        # Check HTTPS
        if parsed.scheme != "https":
            score = max(0, score - 50)
            findings.append("Site is not using HTTPS")
            recommendations.append("Enable HTTPS - it's free with Let's Encrypt and essential for security")
        else:
            findings.append("HTTPS is enabled ✓")
        
        # Check security headers
        headers = response.headers
        
        security_headers = {
            "Strict-Transport-Security": "HSTS - forces HTTPS connections",
            "Content-Security-Policy": "CSP - prevents XSS attacks",
            "X-Frame-Options": "Prevents clickjacking",
            "X-Content-Type-Options": "Prevents MIME sniffing",
            "Referrer-Policy": "Controls referrer information leakage",
        }
        
        found_headers = []
        missing_headers = []
        
        for header, description in security_headers.items():
            if header in headers:
                found_headers.append(header)
            else:
                missing_headers.append((header, description))
        
        findings.append(f"Security headers found: {len(found_headers)}/{len(security_headers)}")
        
        # Score penalties for missing headers
        if missing_headers:
            penalty = min(30, len(missing_headers) * 6)
            score = max(0, score - penalty)
            
            for header, desc in missing_headers[:3]:
                recommendations.append(f"Add {header} header: {desc}")
        
        return AuditResult(
            score=score,
            findings=findings,
            recommendations=recommendations,
            raw_data={
                "https": parsed.scheme == "https",
                "found_headers": found_headers,
                "missing_headers": [h[0] for h in missing_headers],
            }
        )

    def _audit_performance(
        self, 
        response: requests.Response, 
        content_length: int,
        html_content: str
    ) -> AuditResult:
        """Audit page performance indicators."""
        findings = []
        recommendations = []
        
        score = 100
        
        # Page size
        size_kb = content_length / 1024
        findings.append(f"Page size: {size_kb:.1f} KB")
        
        if size_kb > 2000:
            score = max(0, score - 30)
            findings.append("Page is very large (>2MB)")
            recommendations.append("Optimize images and minify CSS/JS to reduce page size")
        elif size_kb > 1000:
            score = max(0, score - 15)
            findings.append("Page is quite large (>1MB)")
            recommendations.append("Consider compressing images and lazy loading")
        elif size_kb > 500:
            score = max(0, score - 5)
            findings.append("Page is moderately large")
        
        # Count resources
        soup = BeautifulSoup(html_content, "html.parser")
        
        css_files = len(soup.find_all("link", rel="stylesheet"))
        js_files = len(soup.find_all("script", src=True))
        images = len(soup.find_all("img"))
        
        findings.append(f"External resources: {css_files} CSS, {js_files} JS, {images} images")
        
        # Penalties for excessive resources
        total_external = css_files + js_files
        if total_external > 20:
            score = max(0, score - 15)
            findings.append(f"Excessive external resources ({total_external})")
            recommendations.append("Combine and minify CSS/JS files to reduce HTTP requests")
        elif total_external > 10:
            score = max(0, score - 5)
            findings.append("Many external resources")
            recommendations.append("Consider combining some CSS/JS files")
        
        # Check for render-blocking resources
        blocking_css = sum(1 for link in soup.find_all("link", rel="stylesheet")
                          if link.get("media") != "print")
        
        if blocking_css > 3:
            recommendations.append("Consider loading non-critical CSS asynchronously")
        
        # Check for modern image formats
        img_srcs = [img.get("src", "") for img in soup.find_all("img")]
        modern_formats = sum(1 for src in img_srcs if any(ext in src.lower() 
                           for ext in [".webp", ".avif"]))
        
        if images > 0 and modern_formats == 0:
            recommendations.append("Consider using WebP format for better compression")
        
        return AuditResult(
            score=score,
            findings=findings,
            recommendations=recommendations,
            raw_data={
                "size_kb": size_kb,
                "css_files": css_files,
                "js_files": js_files,
                "image_count": images,
            }
        )

    def _audit_links(self, soup: BeautifulSoup, base_url: str) -> AuditResult:
        """Audit internal and external links."""
        findings = []
        recommendations = []
        
        links = soup.find_all("a", href=True)
        total_links = len(links)
        
        findings.append(f"Found {total_links} link(s)")
        
        if total_links == 0:
            findings.append("No links found on page")
            recommendations.append("Add navigation links to help users explore your site")
            return AuditResult(score=30, findings=findings, recommendations=recommendations)
        
        parsed_base = urlparse(base_url)
        base_domain = parsed_base.netloc
        
        internal = 0
        external = 0
        nofollow = 0
        
        for link in links:
            href = link.get("href", "")
            
            # Parse the link
            if href.startswith(("http://", "https://")):
                parsed_link = urlparse(href)
                if parsed_link.netloc == base_domain:
                    internal += 1
                else:
                    external += 1
            elif not href.startswith(("#", "javascript:", "mailto:", "tel:")):
                # Relative URL = internal
                internal += 1
            
            if link.get("rel") and "nofollow" in link.get("rel", []):
                nofollow += 1
        
        findings.append(f"Internal links: {internal}")
        findings.append(f"External links: {external}")
        
        # Calculate score
        score = 100
        
        if total_links < 3:
            score = max(0, score - 30)
            findings.append("Very few links on page")
            recommendations.append("Add more navigation links to improve site structure")
        
        # Check external link attributes
        if external > 0:
            external_no_rel = sum(1 for link in links 
                                 if link.get("href", "").startswith(("http://", "https://"))
                                 and urlparse(link.get("href")).netloc != base_domain
                                 and (not link.get("rel") or "noopener" not in link.get("rel", [])))
            
            if external_no_rel > 0:
                score = max(0, score - 10)
                findings.append(f"{external_no_rel} external links missing rel='noopener noreferrer'")
                recommendations.append("Add rel='noopener noreferrer' to external links for security")
        
        return AuditResult(
            score=score,
            findings=findings,
            recommendations=recommendations,
            raw_data={
                "total": total_links,
                "internal": internal,
                "external": external,
                "nofollow": nofollow,
            }
        )

    def _audit_open_graph(self, soup: BeautifulSoup) -> AuditResult:
        """Audit Open Graph tags for social sharing."""
        findings = []
        recommendations = []
        
        # Essential OG tags
        og_tags = {
            "og:title": "Title for social sharing",
            "og:description": "Description for social sharing",
            "og:image": "Image displayed when shared",
            "og:url": "Canonical URL",
            "og:type": "Content type (website, article, etc.)",
        }
        
        found_tags = {}
        missing_tags = []
        
        for tag_name, description in og_tags.items():
            tag = soup.find("meta", property=tag_name)
            if tag and tag.get("content"):
                found_tags[tag_name] = tag.get("content")
            else:
                missing_tags.append((tag_name, description))
        
        findings.append(f"Open Graph tags found: {len(found_tags)}/{len(og_tags)}")
        
        # Calculate score
        coverage = len(found_tags) / len(og_tags)
        score = int(coverage * 100)
        
        if missing_tags:
            for tag_name, desc in missing_tags[:3]:
                recommendations.append(f"Add {tag_name}: {desc}")
        
        # Check for Twitter Cards as bonus
        twitter_card = soup.find("meta", attrs={"name": "twitter:card"})
        if twitter_card:
            findings.append("Twitter Card tags also present ✓")
        else:
            recommendations.append("Consider adding Twitter Card meta tags for better X/Twitter sharing")
        
        return AuditResult(
            score=score,
            findings=findings,
            recommendations=recommendations,
            raw_data={"found_tags": found_tags, "missing_tags": [t[0] for t in missing_tags]}
        )

    def _audit_schema(self, soup: BeautifulSoup) -> AuditResult:
        """Audit Schema.org structured data (JSON-LD)."""
        findings = []
        recommendations = []
        
        # Look for JSON-LD script tags
        jsonld_scripts = soup.find_all("script", type="application/ld+json")
        
        findings.append(f"Found {len(jsonld_scripts)} JSON-LD script(s)")
        
        if len(jsonld_scripts) == 0:
            findings.append("No structured data found")
            recommendations.append("Add JSON-LD structured data for better search visibility")
            recommendations.append("Consider Organization, WebSite, or Article schema types")
            return AuditResult(score=0, findings=findings, recommendations=recommendations)
        
        score = min(100, 40 + (len(jsonld_scripts) * 20))
        
        # Check for common schema types
        schema_types_found = []
        for script in jsonld_scripts:
            try:
                import json
                data = json.loads(script.string) if script.string else {}
                
                if isinstance(data, dict):
                    schema_type = data.get("@type", "Unknown")
                    schema_types_found.append(schema_type)
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            schema_types_found.append(item.get("@type", "Unknown"))
            except (json.JSONDecodeError, AttributeError):
                pass
        
        if schema_types_found:
            findings.append(f"Schema types found: {', '.join(schema_types_found[:5])}")
        
        # Check for microdata as bonus
        microdata = soup.find_all(attrs={"itemscope": True})
        if microdata:
            findings.append(f"Also found {len(microdata)} microdata element(s)")
        
        if len(jsonld_scripts) < 2:
            recommendations.append("Consider adding more structured data types (BreadcrumbList, Article, etc.)")
        
        return AuditResult(
            score=score,
            findings=findings,
            recommendations=recommendations,
            raw_data={
                "jsonld_count": len(jsonld_scripts),
                "schema_types": schema_types_found,
                "microdata_count": len(microdata),
            }
        )
