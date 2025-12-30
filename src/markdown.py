import re
from typing import List, Tuple
from textnode import TextType, TextNode

SYMBOL_MAP = {
    "**": TextType.BOLD,
    "_": TextType.ITALIC,
    "`": TextType.CODE,
}


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[TextNode]:
    if text_type not in SYMBOL_MAP.values():
        raise ValueError(f"Unsupported text type for delimiter splitting: {text_type}")
    if text_type != SYMBOL_MAP[delimiter]:
        raise ValueError(
            f"Delimiter '{delimiter}' does not match text type '{text_type}'"
        )
    # if text_type == TextType.TEXT:
    #     return old_nodes or []
    if not old_nodes:
        return []
    # print(f"Existing nodes before splitting by '{delimiter}': {old_nodes}")
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            # Even number of parts means the delimiter did not have a closing pair
            raise ValueError(f"Unmatched delimiter: {delimiter} for text: {node.text}")

        for i in range(1, len(parts) - 1, 2):
            new_nodes.append(TextNode(parts[i], text_type=SYMBOL_MAP[delimiter]))
        for i in range(0, len(parts), 2):
            if parts[i]:
                new_nodes.append(TextNode(parts[i], text_type=TextType.TEXT))
    # print(f"Split nodes by '{delimiter}': {new_nodes}")
    return new_nodes


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    if not old_nodes:
        return []
    new_nodes = []
    new_nodes = [node for node in old_nodes if node.text_type != TextType.TEXT]
    text_nodes = [node for node in old_nodes if node.text_type == TextType.TEXT]
    if not text_nodes:
        return new_nodes
    for node in text_nodes:
        matches = extract_markdown_images(node.text)
        print(f"matches for images: {matches}")
        if not matches:
            new_nodes.append(node)
            continue
        for alt_text, url in matches:
            print(f"Found image - Alt text: '{alt_text}', URL: '{url}'")
            image_node = TextNode(alt_text, TextType.IMAGE, url)
            new_nodes.append(image_node)

        text_parts = extract_markdown_images_nc(node.text)
        print(f"Text parts after extracting images: {text_parts}")
        for part in text_parts:
            new_nodes.append(TextNode(part, TextType.TEXT))
    print(f"Nodes after image splitting: {new_nodes}")
    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    if not old_nodes:
        return []
    new_nodes = [node for node in old_nodes if node.text_type != TextType.TEXT]
    old_nodes = [node for node in old_nodes if node.text_type == TextType.TEXT]
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        for link_text, url in matches:
            print(f"Found link - Link text: '{link_text}', URL: '{url}'")
            link_node = TextNode(link_text, TextType.LINK, url)
            new_nodes.append(link_node)

        text_parts = extract_markdown_links_nc(node.text)
        for part in text_parts:
            if not part:
                continue
            new_nodes.append(TextNode(part, TextType.TEXT))
    print(f"Nodes after link splitting: {new_nodes}")
    return new_nodes


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    markdown_image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(markdown_image_pattern, text)
    return [(alt_text, url) for alt_text, url in matches]


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    markdown_link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(markdown_link_pattern, text)
    return [(link_text, url) for link_text, url in matches]


def extract_text_markdown(text: str) -> List[str]:
    markdown_link_nc_pattern = r"(?<!!)\[(?:[^\[\]]*)\]\((?:[^\(\)]*)\)"
    markdown_image_nc_pattern = r"!\[(?:[^\[\]]*)\]\((?:[^\(\)]*)\)"
    combined_pattern = rf"(?:{markdown_image_nc_pattern}|{markdown_link_nc_pattern})"
    parts = re.split(combined_pattern, text)
    return [part for part in parts if part]


def extract_markdown_images_nc(text: str) -> List[str]:
    markdown_image_nc_pattern = r"!\[(?:[^\[\]]*)\]\((?:[^\(\)]*)\)"
    results = [result for result in re.split(markdown_image_nc_pattern, text) if result]
    return results


def extract_markdown_links_nc(text: str) -> List[str]:
    markdown_link_nc_pattern = r"(?<!!)\[(?:[^\[\]]*)\]\((?:[^\(\)]*)\)"
    results = [result for result in re.split(markdown_link_nc_pattern, text) if result]
    return results


def text_to_textnodes(markdown_text: str) -> List[TextNode]:
    if not markdown_text:
        return []
    nodes: List[TextNode] = [TextNode(markdown_text, text_type=TextType.TEXT)]
    for delimiter in SYMBOL_MAP.keys():
        nodes = split_nodes_delimiter(nodes, delimiter, SYMBOL_MAP[delimiter])
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


if __name__ == "__main__":
    sample_text = "This is **bold** text and _italic_ text with `code`. This is an image: ![alt text](https://example.com/image.png) and a link: [link](https://example.com)."
    nodes = text_to_textnodes(sample_text)
    for node in nodes:
        print(f"Type: {node.text_type}, Text: '{node.text}'")
    print(nodes)
    print("Done")
