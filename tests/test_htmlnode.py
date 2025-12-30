import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_html(self):
        node = HTMLNode(
            "a", "Google", [], {"href": "https://www.google.com", "target": "_blank"}
        )
        actual = node.props_to_html()
        expected = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
