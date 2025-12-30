from typing import List


class HTMLNode:

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: List[HTMLNode] = [],
        props: dict[str, str] = {},
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented yet!")

    def props_to_html(self):
        if not self.props:
            return ""

        prop_exps = []

        for prop, value in self.props.items():
            prop_exps.append(f'{prop}="{value}"')

        return " ".join(prop_exps)

    def __repr__(self) -> str:
        node_dict = {
            "tag": self.tag,
            "value": self.value,
            "children": self.children,
            "props": self.props,
        }

        return f"HTMLNode {node_dict}"
