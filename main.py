from src.textnode import TextNode, TextType


def main():
    print("Hello from static-site-generator!")
    print(__text_types())


def __text_types():
    text_nodes = []
    for text_type in TextType:
        text = f"Text of type {text_type.value}"
        match text_type.value:
            case "ANCHOR_TEXT":
                url = "http://www.boot.dev"
            case "ALT_TEXT":
                url = "https://www.boot.dev/img/bootdev-logo-full-small.webp"
            case _:
                url = None
        text_node = TextNode(text, text_type, url)
        text_nodes.append(text_node)
    return text_nodes


if __name__ == "__main__":
    main()
