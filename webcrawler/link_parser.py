from bs4 import BeautifulSoup


def parse_links_from_html(html_body):
    soup = BeautifulSoup(html_body, "html.parser")
    links = [link.get("href") for link in soup.findAll("a")]
    http_links = [link for link in links if link and link.startswith("http")]
    return http_links
