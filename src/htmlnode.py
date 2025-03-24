class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None or not len(self.props.keys()):
            return ""
        return " " + " ".join(map(lambda key: f'{key}="{self.props[key]}"', self.props.keys()))

    def __repr__(self):
        print(f"""HTMLNode(
            tag: {self.tag}
            value: {self.value}
            children: {self.children}
            props: {self.props_to_html()}
        )
        """)

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("value is a mandatory property of LeafNode")
        if self.tag is None or self.tag == "":
            return self.value
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"