from enum import Enum


class TextType(Enum):
    TEXT = "TEXT"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"


class TextNode:

    def __init__(self, text="", text_type=TextType.TEXT, url=None) -> None:
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str | None = url

    def __eq__(self, other) -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def __hash__(self) -> int:
        return hash((self.text, self.text_type, self.url))
