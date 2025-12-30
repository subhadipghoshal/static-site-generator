import unittest
from markdown import (
    text_to_textnodes,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextType, TextNode
from typing import List


class TestMarkDown(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.symbol_map = {
            "**": TextType.BOLD,
            "_": TextType.ITALIC,
            "`": TextType.CODE,
        }

    def test_parse_markdown_to_text_nodes(self):

        sample_text = "This is **bold** text and _italic_ text with `code`."
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]
        print("---- Expected nodes -----")
        print(expected_nodes)
        parsed_nodes = text_to_textnodes(sample_text)
        # old_nodes: List[TextNode] = [TextNode(sample_text, text_type=TextType.TEXT)]
        # for delimiter, text_type in self.symbol_map.items():
        #     parsed_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        print("---- Parsed nodes -----")
        print(parsed_nodes)
        self.assertEqual(set(parsed_nodes), set(expected_nodes))

    def test_extract_markdown_links(self):
        sample_text = "This is a [link](https://example.com) in the text."
        expected_links = [("link", "https://example.com")]
        extracted_links = extract_markdown_links(sample_text)
        self.assertEqual(extracted_links, expected_links)

    def test_extract_markdown_images(self):
        sample_text = "Here is an image: ![alt text](https://example.com/image.png)"
        expected_images = [("alt text", "https://example.com/image.png")]
        extracted_images = extract_markdown_images(sample_text)
        self.assertEqual(extracted_images, expected_images)

    def test_markdown_to_image_nodes(self):
        sample_text = "Here is an image: ![alt text](https://example.com/image.png)"
        expected_nodes = [
            TextNode("Here is an image: ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
        ]
        old_nodes = [TextNode(sample_text, TextType.TEXT)]
        parsed_nodes = split_nodes_image(old_nodes)
        self.assertEqual(set(parsed_nodes), set(expected_nodes))

    def test_markdown_to_link_nodes(self):
        sample_text = "This is a [link](https://example.com) in the text."
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" in the text.", TextType.TEXT),
        ]
        old_nodes = [TextNode(sample_text, TextType.TEXT)]
        parsed_nodes = split_nodes_link(old_nodes)
        self.assertEqual(set(parsed_nodes), set(expected_nodes))

    def test_text_to_textnodes_empty(self):
        sample_text = ""
        expected_nodes: List[TextNode] = []
        parsed_nodes = text_to_textnodes(sample_text)
        self.assertEqual(parsed_nodes, expected_nodes)

    def test_text_to_textnodes_no_formatting(self):
        sample_text = "This is plain text without any markdown."
        expected_nodes = [TextNode(sample_text, TextType.TEXT)]
        parsed_nodes = text_to_textnodes(sample_text)
        self.assertEqual(parsed_nodes, expected_nodes)

    def test_text_to_textnodes_only_formatting(self):
        sample_text = "**bold** _italic_ `code`"
        expected_nodes = [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        parsed_nodes = text_to_textnodes(sample_text)
        self.assertEqual(set(parsed_nodes), set(expected_nodes))

    def test_text_to_textnodes_nested_formatting(self):
        sample_text = "This is **bold and _italic_** text."
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold and _italic_", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        parsed_nodes = text_to_textnodes(sample_text)
        self.assertEqual(set(parsed_nodes), set(expected_nodes))

    def test_text_to_textnodes_multiple_images_links(self):
        sample_text = (
            "Image1: ![alt1](url1) and Image2: ![alt2](url2) with a [link](linkurl)."
        )
        expected_nodes = [
            TextNode("Image1: ", TextType.TEXT),
            TextNode("alt1", TextType.IMAGE, "url1"),
            TextNode(" and Image2: ", TextType.TEXT),
            TextNode("alt2", TextType.IMAGE, "url2"),
            TextNode(" with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "linkurl"),
            TextNode(".", TextType.TEXT),
        ]
        parsed_nodes = text_to_textnodes(sample_text)
        self.assertEqual(set(parsed_nodes), set(expected_nodes))


if __name__ == "__main__":
    unittest.main()
