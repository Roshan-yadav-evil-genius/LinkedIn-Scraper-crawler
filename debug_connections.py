from scrapy import Selector


def find_connections_context():
    with open("page.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    sel = Selector(text=html_content)

    # Find any element containing "500+"
    elements = sel.xpath('//*[contains(text(), "500+")]')
    print(f"Found {len(elements)} elements with '500+'")

    for i, el in enumerate(elements):
        print(f"\nElement {i+1}:")
        print(f"Tag: {el.root.tag}")
        print(f"Attributes: {el.root.attrib}")
        print(f"Text: {el.xpath('./text()').get()}")
        print(f"Parent: {el.xpath('..')[0].root.tag} ({el.xpath('..')[0].root.attrib})")

        # Also check for "connections"
        if "connections" in str(el.get()):
            print("Contains 'connections' in HTML/Text")


if __name__ == "__main__":
    find_connections_context()
