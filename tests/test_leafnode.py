import unittest
from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_to_html_p(self):
        actual = LeafNode(tag="p", value="Hello, World!").to_html()
        expected = "<p>Hello, World!</p>"
        self.assertEqual(actual, expected)

    def test_to_html_with_props(self):
        actual = LeafNode(
            tag="a",
            value="Click here",
            props={"href": "https://www.example.com", "target": "_blank"},
        ).to_html()
        expected = '<a href="https://www.example.com" target="_blank">Click here</a>'
        self.assertEqual(actual, expected)

    def test_with_null_value(self):
        actual = LeafNode(tag="span", value=None).to_html()
        expected = "<span></span>"
        self.assertEqual(actual, expected)
