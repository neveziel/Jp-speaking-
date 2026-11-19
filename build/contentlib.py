"""Parse the authored content (with [kanji|kana] ruby marks) into plain/ruby/kana forms."""
import json, os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "..", "content")
RUBY = re.compile(r"\[([^\[\]\|]+)\|([^\[\]\|]+)\]")


def plain(s):
    """Kanji kept, reading dropped — used for TTS and for furigana-off display."""
    return RUBY.sub(lambda m: m.group(1), s)


def kana(s):
    """Full kana reading."""
    return RUBY.sub(lambda m: m.group(2), s)


def ruby(s):
    """HTML with <ruby> tags."""
    return RUBY.sub(lambda m: "<ruby>%s<rt>%s</rt></ruby>" % (m.group(1), m.group(2)), s)


def _load(name):
    with open(os.path.join(CONTENT, name), encoding="utf-8") as f:
        return json.load(f)


def phrases():
    out = []
    for name in ("lv12.json", "lv345.json"):
        out.extend(_load(name))
    return out


def dialogues():
    return _load("dialogues.json")


def meta():
    return _load("meta.json")


def processed():
    ps = []
    for p in phrases():
        ps.append({
            "id": p["id"], "lv": p["lv"], "tag": p["tag"], "pol": p["pol"], "v": p["v"],
            "jp": plain(p["jp"]), "ruby": ruby(p["jp"]), "kana": kana(p["jp"]),
            "ko": p["ko"], "note": p["note"],
            "ex": plain(p["ex"]), "exRuby": ruby(p["ex"]), "exKana": kana(p["ex"]),
            "exKo": p["exKo"],
        })
    ds = []
    for d in dialogues():
        ds.append({
            "id": d["id"], "lv": d["lv"],
            "title": plain(d["title"]), "titleRuby": ruby(d["title"]), "titleKana": kana(d["title"]),
            "situation": d["situation"], "a": d["a"], "b": d["b"],
            "lines": [{"r": l["r"], "jp": plain(l["jp"]), "ruby": ruby(l["jp"]), "kana": kana(l["jp"]),
                       "ko": l["ko"], "note": l.get("note", "")} for l in d["lines"]],
        })
    return {"phrases": ps, "dialogues": ds, "meta": meta()}


if __name__ == "__main__":
    data = processed()
    print("phrases:", len(data["phrases"]), "dialogues:", len(data["dialogues"]),
          "turns:", sum(len(d["lines"]) for d in data["dialogues"]))
    lv = {}
    for p in data["phrases"]:
        lv[p["lv"]] = lv.get(p["lv"], 0) + 1
    print("by level:", dict(sorted(lv.items())))
    for p in data["phrases"][:2]:
        print(p["jp"], "|", p["kana"], "|", p["ruby"])
