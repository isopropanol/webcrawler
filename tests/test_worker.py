from asyncio import create_task
from asyncio import Queue

import aiohttp
from aioresponses import aioresponses

from tests.base import BaseTestCase
from webcrawler.worker import worker


class TestWorker(BaseTestCase):
    @aioresponses()
    async def test_worker(self, mocked_client):
        initial_url = "hello"
        queue = Queue()
        queue.put_nowait(initial_url)
        iteration_limit = 5
        mocked_client.get(initial_url, status=200, body="world")

        async with aiohttp.ClientSession() as session:
            worker_instance = create_task(
                worker(queue=queue, session=session, iteration_limit=iteration_limit)
            )
            await queue.join()
            worker_instance.cancel()

        self.assertEqual(len(mocked_client.requests), 1)
        self.assertTrue(initial_url in self.seen_links)

    @aioresponses()
    async def test_worker_requeues_returned_links(self, mocked_client):
        initial_url = "hello"
        queue = Queue()
        queue.put_nowait(initial_url)
        iteration_limit = None

        follow_urls = ["http://follow_url1", "https://follow_url2"]
        extraneous_url = "doesnotstartwith_http"

        body = (
            f'<body><a href="{follow_urls[0]}">follow me</a> asdfaesf <a href="{follow_urls[1]}">follow me</a></body>'
            + f'<a href="{extraneous_url}">follow me</a></body>'
        )

        mocked_client.get(initial_url, status=200, body=body)

        async with aiohttp.ClientSession() as session:
            worker_instance = create_task(
                worker(queue=queue, session=session, iteration_limit=iteration_limit)
            )
            await queue.join()
            worker_instance.cancel()

        self.assertEqual(len(mocked_client.requests), 3)
        self.assertCountEqual(set([initial_url] + follow_urls), self.seen_links)

    @aioresponses()
    async def test_worker_ignores_non_http(self, mocked_client):
        initial_url = "hello"
        queue = Queue()
        queue.put_nowait(initial_url)
        iteration_limit = 2

        follow_urls = ["http://follow_url1", "https://follow_url2"]
        extraneous_url = "doesnotstartwith_http"

        body = (
            f'<body><a href="{follow_urls[0]}">follow me</a> asdfaesf <a href="{follow_urls[1]}">follow me</a></body>'
            + f'<a href="{extraneous_url}">follow me</a></body>'
        )

        mocked_client.get(initial_url, status=200, body=body)

        async with aiohttp.ClientSession() as session:
            worker_instance = create_task(
                worker(queue=queue, session=session, iteration_limit=iteration_limit)
            )
            await queue.join()
            worker_instance.cancel()

        self.assertEqual(len(mocked_client.requests), 2)
        self.assertEqual(len(self.seen_links), 2)
