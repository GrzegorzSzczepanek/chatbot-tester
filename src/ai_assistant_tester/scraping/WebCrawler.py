import argparse
from typing import Optional
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup


class WebCrawler:
    def __init__(
        self,
        domain: Optional[str] = None,
        cli: bool = False,
        output_file: Optional[str] = None,
        unlimited_depth: bool = False,
        max_depth: int = 3,
    ):
        """
        Initialize the crawler.

        :param domain: Domain to limit the crawling to (e.g. 'example.com').
        :param cli: If True, print verbose output during crawling.
        :param output_file: Path to the file to save scraped markdown.
        :param unlimited_depth: If True, crawl all subpages without depth limit.
        :param max_depth: Maximum depth of recursion if unlimited_depth is False.
        """
        self.domain = domain
        self.cli = cli
        self.output_file = output_file
        self.unlimited_depth = unlimited_depth
        self.max_depth = max_depth
        self.crawled = set()
        # url and it's content
        self.results = {}
        # Optionally clear the output file at the start
        if self.output_file:
            with open(self.output_file, "w", encoding="utf-8") as f:
                f.write("# Scraped Knowledge Base\n\n")

    def _normalize_url(self, url: str) -> str:
        parsed = urlparse(url)
        normalized_path = parsed.path.rstrip("/")
        if not normalized_path:
            normalized_path = "/"
        normalized = urlunparse(
            (
                parsed.scheme,
                parsed.netloc,
                normalized_path,
                parsed.params,
                parsed.query,
                "",
            )
        )
        return normalized

    def crawl(self, url: str, depth: int = 0):
        """
        Recursively crawl the given URL.

        :param url: URL to crawl.
        :param depth: Current recursion depth.
        """
        url = self._normalize_url(url)

        if url in self.crawled:
            return
        self.crawled.add(url)

        parsed_url = urlparse(url)
        if self.domain and self.domain not in parsed_url.netloc:
            return

        if self.cli:
            print(f"Crawling: {url} at depth {depth}")

        try:
            # Use headers for a better User-Agent
            headers = {"User-Agent": "Mozilla/5.0 (compatible; WebCrawler/1.0)"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            if self.cli:
                print(f"Error fetching {url}: {e}")
            return

        # Check if the content seems to be HTML
        content_type = response.headers.get("Content-Type", "")
        if (
            "text/html" not in content_type.lower()
            and "application/xhtml+xml" not in content_type.lower()
        ):
            if self.cli:
                print(f"Skipping non-HTML content at: {url} [{content_type}]")
            return

        markdown_content = self.scrape_content_from_html(response.text, url)
        self.save_content(url, markdown_content)

        # Do not recurse further if reached max depth (unless unlimited)
        if not self.unlimited_depth and depth >= self.max_depth:
            return

        new_urls = self.extract_urls(response.text, url)
        for new_url in new_urls:
            self.crawl(new_url, depth + 1)

    def extract_urls(self, html, base_url):
        """
        Extract absolute URLs from the HTML.

        :param html: HTML content as string.
        :param base_url: The base URL to resolve relative links.
        :return: List of absolute URLs.
        """
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            href = a.get("href")
            # Skip links that are just anchors or javascript or mailto links.
            if (
                href.startswith("#")
                or href.startswith("mailto:")
                or href.startswith("javascript:")
            ):
                continue
            abs_url = urljoin(base_url, href)
            links.append(abs_url)
        return links

    def scrape_content_from_html(self, html, base_url):
        """
        Convert HTML to cleaned text (Markdown format) while removing unwanted tags.

        :param html: Raw HTML text.
        :param base_url: Fallback for title if no <title> is found.
        :return: A string with markdown formatted content.
        """
        soup = BeautifulSoup(html, "html.parser")

        tags_to_remove = [
            "script",
            "style",
            "img",
            "svg",
            "canvas",
            "noscript",
            "iframe",
            "header",
            "footer",
            "nav",
            "form",
            "link",
            "meta",
        ]
        for tag in soup.find_all(tags_to_remove):
            tag.decompose()

        # Optionally remove specific classes or ids that match known banners or ads.
        # For instance:
        # for div in soup.find_all("div", class_="ad-banner"):
        #     div.decompose()

        # Use the <title> tag if available, otherwise use the URL.
        if soup.title:
            title = soup.title.get_text().strip()
        else:
            title = base_url

        text = soup.get_text(separator="\n")
        # Clean up text: remove extra whitespace and empty lines.
        lines = [line.strip() for line in text.splitlines()]
        cleaned_text = "\n".join(line for line in lines if line)

        content = f"# {title}\n\n" + cleaned_text
        return content

    def save_content(self, url: str, content: str):
        formatted_content = f"\n\n<!-- URL: {url} -->\n\n{content}\n\n"
        if self.output_file:
            try:
                with open(self.output_file, "a", encoding="utf-8") as f:
                    f.write(formatted_content)
            except requests.exceptions.RequestException as e:
                if self.cli:
                    print(f"Error saving content from {url}: {e}")
        else:
            self.results[url] = content


def main():
    parser = argparse.ArgumentParser(
        description="A domain-limited web crawler that scrapes HTML pages to markdown for an LLM knowledge base."
    )
    parser.add_argument("url", help="Starting URL, e.g. https://example.com")
    parser.add_argument("--cli", action="store_true", help="Show verbose output")
    parser.add_argument(
        "--output", default="output.txt", help="Output text file (default: output.txt)"
    )
    parser.add_argument(
        "--unlimited",
        action="store_true",
        help="Crawl until every subpage on the domain is visited (ignores max-depth)",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=3,
        help="Maximum crawl depth if not unlimited (default: 3)",
    )

    args = parser.parse_args()

    start_domain = urlparse(args.url).netloc

    crawler = WebCrawler(
        domain=start_domain,
        cli=args.cli,
        output_file=args.output,
        unlimited_depth=args.unlimited,
        max_depth=args.max_depth,
    )
    crawler.crawl(args.url)

    if not args.output:
        for url, content in crawler.results.items():
            print(f"URL: {url}")
            print("Content Preview:")
            print(content[:300])
            print("-" * 80)


if __name__ == "__main__":
    main()
