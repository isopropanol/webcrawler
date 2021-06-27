from asynctest import patch

from run_webcrawler import run_workers
from tests.base import BaseTestCase


class TestWebCrawler(BaseTestCase):
    @patch("run_webcrawler.aiohttp.ClientSession")
    async def test_run_workers(self, patched_session):
        initial_url = "hello"
        iteration_limit = 5
        await run_workers(initial_url, iteration_limit)
        self.assertEqual(patched_session.call_count, 1)
