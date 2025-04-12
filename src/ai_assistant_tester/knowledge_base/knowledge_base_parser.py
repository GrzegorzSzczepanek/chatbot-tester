from typing import Optional
from urllib.parse import urlparse

from ai_assistant_tester.scraping.WebCrawler import WebCrawler
from ai_assistant_tester.utils import get_openai_api_key


def get_content(
    start_url: str = "https://eg-zine.pages.dev",
    cli: bool = False,
    output_file: Optional[str] = None,
    max_depth: int = 2,
) -> str:
    """
    Crawl a website starting from the given URL and return the aggregated
    scraped content as a knowledge base string.

    This function creates an instance of the WebCrawler, crawls the specified
    start URL (and its internal links up to a specified depth), and aggregates
    the collected markdown-formatted content. The output is returned as a single
    string that represents the combined knowledge base.

    Parameters:
        start_url (str): The starting URL for the crawl. Defaults to
                         "https://eg-zine.pages.dev".
        cli (bool): If True, enables verbose output during crawling. Defaults to False.
        output_file (str): If specified, the crawler writes scraped results into this file;
                           if None, results are stored in memory. Defaults to None.
        unlimited (bool): If true, crawler will recursively crawl through subpages until it reaches the bottom.
        max_depth (int): The maximum depth for recursive crawling. Defaults to 2.

    Returns:
        str: A single string containing the aggregated markdown content from all
             crawled pages.
    """
    start_domain = urlparse(start_url).netloc

    crawler = WebCrawler(
        domain=start_domain,
        cli=cli,
        output_file=output_file,
        max_depth=max_depth,
    )

    crawler.crawl(start_url)

    for url, content in crawler.results.items():
        print(f"URL: {url}")
        print("Content Preview:")
        print(content[:300])
        print("-" * 80)

    knowledge_base = "\n\n".join(crawler.results.values())
    return knowledge_base


def format_knowledge_base(knowledge_base: str):
    OPENAI_API_KEY = get_openai_api_key()
