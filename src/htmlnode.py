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