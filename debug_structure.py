from scrapy import Selector
import json


def debug_structure():
    with open("page.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    sel = Selector(text=html_content)

    # Check what element has id="experience"
    exp = sel.xpath('//*[@id="experience"]')
    if exp:
        print(f"Experience Info: Tag={exp[0].root.tag}, Attribs={exp[0].root.attrib}")
        # Print parent
        parent = exp.xpath("..")
        if parent:
            print(f"Parent: Tag={parent[0].root.tag}, Attribs={parent[0].root.attrib}")
    else:
        print("id='experience' NOT FOUND")

    # Check for artdeco-list__item
    items = sel.xpath('//li[contains(@class, "artdeco-list__item")]')
    print(f"Found {len(items)} artdeco-list__items")
    if items:
        # Print the HTML of the first item to see structure
        print("First Item HTML snippet:")
        print(items[0].get()[:500])  # Print first 500 chars

    # Check About
    about = sel.xpath('//*[@id="about"]')
    if about:
        print(f"About Info: Tag={about[0].root.tag}, Attribs={about[0].root.attrib}")
        # Check for inline-show-more-text in vicinity
        # Try to find it in the same section
        # Go up to section
        section = about.xpath("./ancestor::section")
        if section:
            print("Found ancestor section for About")
            texts = section.xpath('.//div[contains(@class, "inline-show-more-text")]')
            print(f"Found {len(texts)} inline-show-more-text divs in about section")
            if texts:
                print(texts[0].get()[:200])


if __name__ == "__main__":
    debug_structure()
