import argparse
import asyncio

import aiohttp

from webcrawler.worker import worker

WORKER_SIZE = 40


async def run_workers(initial_url, iteration_limit):
    queue = asyncio.Queue()
    queue.put_nowait(initial_url)
    async with aiohttp.ClientSession() as session:
        workers = [
            asyncio.create_task(
                worker(queue=queue, session=session, iteration_limit=iteration_limit)
            )
            for n in range(WORKER_SIZE)
        ]
        await queue.join()
        for w in workers:
            w.cancel()


if __name__ == "__main__":
    """
    Prints <a href={url}> tags found in a webpage,
    and then follows those urls and recurses

    """
    parser = argparse.ArgumentParser(description="Recursive link webcrawler")
    parser.add_argument(help="Url of page to start the crawler at", dest="inital_url")
    parser.add_argument(
        "-l",
        "--limit",
        help="max pages to visit, default runs continuously",
        dest="limit",
        type=int,
        default=None,
    )
    args = parser.parse_args()
    asyncio.run(
        run_workers(initial_url=args.inital_url, iteration_limit=args.limit), debug=True
    )
