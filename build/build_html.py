"""Inject the processed content into the app template → ../index.html"""
import json, os
import contentlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")


def main():
    data = contentlib.processed()
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(HERE, "app_template.html"), encoding="utf-8") as f:
        tpl = f.read()
    if "/*__DATA__*/" not in tpl:
        raise SystemExit("placeholder missing")
    html = tpl.replace("/*__DATA__*/", payload)
    out = os.path.join(ROOT, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html:", os.path.getsize(out), "bytes, data:", len(payload), "chars")
    m = data["meta"]
    print("phrases", len(data["phrases"]), "dialogues", len(data["dialogues"]),
          "tips", len(m["tips"]), "sources", len(m["sources"]))


if __name__ == "__main__":
    main()
