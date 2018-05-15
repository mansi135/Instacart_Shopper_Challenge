import unittest

from server import app
from flask import session


class ServerTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_base_layout(self):
        result = self.client.get("/")
        self.assertIn("Instacart Shopper", result.data)

    def test_home_page(self):
        # FIXME: Add a test to show we see the RSVP form, but NOT the
        # party details
        result = self.client.get("/")
        self.assertIn("I am legally authorized to work in USA", result.data)
        self.assertNotIn("Application Status", result.data)


if __name__ == "__main__":
    unittest.main()