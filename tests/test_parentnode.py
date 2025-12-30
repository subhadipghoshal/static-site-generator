import unittest
from src.parentnode import ParentNode
from src.leafnode import LeafNode


class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child1 = ParentNode(tag="li", children=[], props={})
        child1_child = LeafNode(tag="p", value=None, props={})
        child1.children.append(child1_child)
        child2 = ParentNode(tag="li", children=[], props={})
        child2_child = LeafNode(tag="p", value=None, props={})
        child2.children.append(child2_child)
        parent = ParentNode(tag="ul", children=[child1, child2], props={})
        actual = parent.to_html()
        expected = "<ul><li><p></p></li><li><p></p></li></ul>"
        self.assertEqual(actual, expected)

    def test_to_html_with_one_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
