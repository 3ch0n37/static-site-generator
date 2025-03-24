import unittest
from htmlnode import HTMLNode, LeafNode

class TestHtmlNode(unittest.TestCase):
    def test_props(self):
        html_node = HTMLNode(None,None,None, {"href": "https://ddg.co"})
        props_html = html_node.props_to_html()
        self.assertEqual(props_html, ' href="https://ddg.co"')

    def test_no_props(self):
        html_node = HTMLNode()
        props_html = html_node.props_to_html()
        self.assertEqual(props_html, '')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "DuckDuckGo", {"href": "https://ddg.co"})
        self.assertEqual(node.to_html(), '<a href="https://ddg.co">DuckDuckGo</a>')
