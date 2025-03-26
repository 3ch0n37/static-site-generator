import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a text with a link [to google](https://www.google.com) and [DuckDuckGo](https://ddg.co)."
        )
        self.assertListEqual(matches, [
            ("to google", "https://www.google.com"),
            ("DuckDuckGo", "https://ddg.co")
        ])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_and_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode(
                    "link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_no_image(self):
        node = TextNode("This is a text node", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_link_consecutive(self):
        node = TextNode("This test has two [consecutive](https://example.com/1)[links](https://example.com/2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This test has two ", TextType.TEXT),
                TextNode("consecutive", TextType.LINK, "https://example.com/1"),
                TextNode("links", TextType.LINK, "https://example.com/2")
            ],
            new_nodes
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )
