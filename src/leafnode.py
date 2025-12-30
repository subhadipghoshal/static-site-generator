from src.htmlnode import HTMLNode


class LeafNode(HTMLNode):

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict[str, str] = {},
    ) -> None:
        super().__init__(tag, value, [], props)

    def to_html(self):
        props_html = self.props_to_html()
        props_section = f" {props_html}" if props_html else ""
        value = self.value if self.value is not None else ""
        return f"<{self.tag}{props_section}>{value}</{self.tag}>"
