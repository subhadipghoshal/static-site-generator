import unittest
from src.textnode import TextNode, TextType
from src.utils import text_node_to_html_node


class TestUtils(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code(self):
        node = TextNode("print('Hello, World!')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello, World!')")

    def test_image(self):
        node = TextNode("An image", TextType.IMAGE, url="http://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "http://example.com/image.png")
        self.assertEqual(html_node.props["alt"], "An image")

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, url="http://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props["href"], "http://example.com")

    def test_link_no_url(self):
        node = TextNode("Click here", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertNotIn("href", html_node.props)

    def test_image_no_url(self):
        node = TextNode("An image", TextType.IMAGE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "")
        self.assertEqual(html_node.props["alt"], "An image")

    def test_unknown_text_type(self):
        node = TextNode("Unknown", "UNKNOWN_TYPE")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
