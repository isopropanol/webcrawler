from unittest.mock import patch

from asynctest import TestCase as AsyncTestCase


class BaseTestCase(AsyncTestCase):
    def setUp(self):
        self.seen_links = set()
        patcher = patch("webcrawler.worker.seen_links", self.seen_links)
        patcher.start()

        self.addCleanup(patcher.stop)
