import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

class TestInlineMarkdown(unittest.TestCase):
    def test_code_normal(self):
        node = TextNode("This node has `inline` code.", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("This node has ", TextType.TEXT),
            TextNode("inline", TextType.CODE),
            TextNode(" code.", TextType.TEXT)
        ]
        self.assertEqual(result, expected_result)

    def test_bold_multiple(self):
        node = TextNode("This is **bold** and this is **also bold**.", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and this is ", TextType.TEXT),
            TextNode("also bold", TextType.BOLD),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected_result)

    def test_link_text_list(self):
        old_nodes = [
            TextNode("Google", TextType.LINK, "https://www.google.com"),
            TextNode("_That_ is a link to _Google_.", TextType.TEXT)
        ]
        result = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        expected_result = [
            TextNode("Google", TextType.LINK, "https://www.google.com"),
            TextNode("That", TextType.ITALIC),
            TextNode(" is a link to ", TextType.TEXT),
            TextNode("Google", TextType.ITALIC),
            TextNode(".", TextType.TEXT)
        ]
        self.assertEqual(result, expected_result)

    def test_invalid_markdown(self):
        node = TextNode("This contains a `mistake.", TextType.TEXT)
        self.assertRaises(ValueError, split_nodes_delimiter, [node], "`", TextType.CODE)
