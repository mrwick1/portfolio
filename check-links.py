import os
import json
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import urllib.parse

def check():
    base_dir = "/home/mrwick/coding/personal/projects/portfolio-p8"
    os.chdir(base_dir)

    assert not os.path.exists("writing/tradersconnect-rework"), "Old directory still exists"
    assert os.path.exists("demos/tradersconnect/index.html"), "New index.html missing"
    assert os.path.exists("demos/tradersconnect/images"), "New images dir missing"

    images = os.listdir("demos/tradersconnect/images")
    webp_count = sum(1 for f in images if f.endswith(".webp"))
    assert webp_count == 8, f"Expected 8 .webp files, found {webp_count}"

    with open("writing/tradersconnect-rework.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert "tradersconnect-rework/images" not in content, "Old image path found in article"

    with open("vercel.json", "r", encoding="utf-8") as f:
        vj = json.load(f)
        redirects = vj.get("redirects", [])
        assert any(r.get("source") == "/writing/tradersconnect-rework/" and r.get("statusCode") == 301 for r in redirects), "Missing 301 redirect with trailing slash"
        assert any(r.get("source") == "/writing/tradersconnect-rework" and r.get("statusCode") == 301 for r in redirects), "Missing 301 redirect without trailing slash"
        assert any(r.get("source") == "/writing/article-template.html" and r.get("statusCode") == 404 for r in redirects), "Missing 404 redirect 1"
        assert any(r.get("source") == "/writing/company-rework-template.html" and r.get("statusCode") == 404 for r in redirects), "Missing 404 redirect 2"

    tree = ET.parse("sitemap.xml")
    root = tree.getroot()
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [url.find("sm:loc", ns).text for url in root.findall("sm:url", ns) if url.find("sm:loc", ns) is not None]
    assert "https://www.arjunp.pro/demos/tradersconnect/" in urls, "New URL not in sitemap.xml"

    class LinkParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.links = []
        def handle_starttag(self, tag, attrs):
            for attr, value in attrs:
                if attr in ("href", "src"):
                    self.links.append(value)

    files_to_check = [
        "writing/tradersconnect-rework.html",
        "demos/tradersconnect/index.html",
        "index.html",
        "writing/index.html"
    ]

    for filepath in files_to_check:
        if not os.path.exists(filepath):
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            parser = LinkParser()
            parser.feed(f.read())
            file_dir = os.path.dirname(filepath)
            for link in parser.links:
                if link.startswith(("http://", "https://", "mailto:", "//")) or link.startswith("#"):
                    continue
                
                # strip fragment if present
                link_path = urllib.parse.urlparse(link).path
                if not link_path:
                    continue

                if link_path.startswith("/"):
                    # root-relative
                    target = os.path.join(base_dir, link_path.lstrip("/"))
                else:
                    # relative
                    target = os.path.normpath(os.path.join(base_dir, file_dir, link_path))

                if os.path.isdir(target) and not os.path.isfile(target):
                    # Check for index.html if it points to a directory
                    if os.path.exists(os.path.join(target, "index.html")):
                        target = os.path.join(target, "index.html")
                    elif os.path.exists(os.path.join(target, "index.xml")):
                        target = os.path.join(target, "index.xml")

                assert os.path.exists(target), f"Broken link in {filepath}: {link} (resolved to {target})"
                print(f"Checked in {filepath}: {link} -> {target}")

    print("PASS: All checks succeeded.")

if __name__ == "__main__":
    check()
