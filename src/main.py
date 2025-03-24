#! /bin/env python3
from textnode import TextNode, TextType

def main():
    test_node = TextNode("This is a test", TextType.LINK, "https://google.com")
    print(test_node)

if __name__ == '__main__':
    main()
