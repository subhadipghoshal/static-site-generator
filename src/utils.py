from src.textnode import TextType
from src.htmlnode import HTMLNode
from src.leafnode import LeafNode


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return HTMLNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return HTMLNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.IMAGE:
            props = {
                "src": text_node.url if text_node.url else "",
                "alt": text_node.text,
            }
            return LeafNode(tag="img", value="", props=props)
        case TextType.LINK:
            props = {"href": text_node.url} if text_node.url else {}
            return LeafNode(tag="a", value=text_node.text, props=props)
        case _:
            raise ValueError(f"Unknown TextType: {text_node.text_type}")
