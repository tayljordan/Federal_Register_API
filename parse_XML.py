import os
import json
from lxml import etree

BASE_DIR = "/Users/jordantaylor/PycharmProjects/US_Federal_Register_API/eCFR"
DOWNLOADS = os.path.join(BASE_DIR, "downloads")
OUT_JSON = os.path.join(BASE_DIR, "output/json")
OUT_HTML = os.path.join(BASE_DIR, "output/html")

os.makedirs(OUT_JSON, exist_ok=True)
os.makedirs(OUT_HTML, exist_ok=True)


def parse_ecfr(xml_path: str):
    tree = etree.parse(xml_path)
    root = tree.getroot()

    sections = root.findall(".//DIV8")

    for idx, div8 in enumerate(sections, start=1):
        section_id = f"section_{idx:04d}"

        head = div8.findtext("HEAD", "").strip()
        paragraphs = [
            p.text.strip()
            for p in div8.findall("P")
            if p.text and p.text.strip()
        ]

        parents = []
        current = div8.getparent()
        level = 1
        while current is not None and current.tag.startswith("DIV"):
            parents.append({
                "level": level,
                "name": current.findtext("HEAD", "").strip(),
                "type": current.get("TYPE")
            })
            current = current.getparent()
            level += 1

        parents = list(reversed(parents))

        json_payload = {
            "id": section_id,
            "title": head,
            "paragraphs": paragraphs,
            "parents": parents
        }

        # ---- SAVE JSON ----
        with open(os.path.join(OUT_JSON, f"{section_id}.json"), "w") as f:
            json.dump(json_payload, f, indent=2)

        # ---- SAVE HTML ----
        html = [
            "<html><body>",
            f"<h1>{head}</h1>",
        ]

        for p in paragraphs:
            html.append(f"<p>{p}</p>")

        html.append("<hr><h3>Hierarchy</h3><ul>")
        for p in parents:
            html.append(f"<li>{p['type']}: {p['name']}</li>")
        html.append("</ul></body></html>")

        with open(os.path.join(OUT_HTML, f"{section_id}.html"), "w") as f:
            f.write("\n".join(html))


if __name__ == "__main__":
    for file in os.listdir(DOWNLOADS):
        if file.endswith(".xml"):
            parse_ecfr(os.path.join(DOWNLOADS, file))
