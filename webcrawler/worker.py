from webcrawler.html_client import get_page_async
from webcrawler.link_manager import seen_links
from webcrawler.link_parser import parse_links_from_html


def at_iteration_limit(link_set, iteration_limit):
    return iteration_limit is not None and len(link_set) >= iteration_limit


async def worker(queue, session, iteration_limit):
    while True:
        url = await queue.get()
        seen_links.add(url)
        html_response = await get_page_async(session=session, url=url)
        links = parse_links_from_html(html_body=html_response)
        print(url)
        for link in links:
            if link not in seen_links and not at_iteration_limit(
                link_set=seen_links, iteration_limit=iteration_limit
            ):
                seen_links.add(link)
                queue.put_nowait(link)
            print("  " + link)

        queue.task_done()
