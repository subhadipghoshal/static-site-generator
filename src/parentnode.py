from src.htmlnode import HTMLNode


class ParentNode(HTMLNode):

    def __init__(
        self,
        tag: str | None = None,
        children: list[HTMLNode] = [],
        props: dict[str, str] = {},
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Tag is required to convert to HTML")
        if not self.children:
            raise ValueError("At least one child node is required to convert to HTML")
        props_html = self.props_to_html()
        props_section = f" {props_html}" if props_html else ""
        children_html = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{props_section}>{children_html}</{self.tag}>"
