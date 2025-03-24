import unittest
from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_props(self):
        html_node = HTMLNode(None,None,None, {"href": "https://ddg.co"})
        props_html = html_node.props_to_html()
        self.assertEqual(props_html, ' href="https://ddg.co"')

    def test_no_props(self):
        html_node = HTMLNode()
        props_html = html_node.props_to_html()
        self.assertEqual(props_html, '')