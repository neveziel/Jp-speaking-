"""Pre-deploy verification: audio completeness, data integrity, HTML sanity."""
import json, os, re, sys, glob
import contentlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
AUD = os.path.join(ROOT, "audio")
ok = True
def chk(cond, msg):
    global ok
    print(("  OK   " if cond else "  FAIL ") + msg)
    if not cond: ok = False

data = contentlib.processed()
ps, ds = data["phrases"], data["dialogues"]

print("[1] content")
chk(len(ps) >= 120, "표현 %d개 (기준 120+)" % len(ps))
chk(12 <= len(ds) <= 15, "롤플레이 %d개 (기준 12~15)" % len(ds))
lv = {}
for p in ps: lv[p["lv"]] = lv.get(p["lv"], 0) + 1
chk(len(lv) == 5 and all(v >= 20 for v in lv.values()), "5단계 분포 %s" % dict(sorted(lv.items())))
chk(all(p["jp"] and p["ko"] and p["note"] and p["ex"] and p["exKo"] for p in ps), "모든 표현에 jp/ko/note/ex/exKo 존재")
chk(all(p["kana"] != p["jp"] or not re.search(r"[\u4e00-\u9fff]", p["jp"]) for p in ps), "한자 포함 표현에 후리가나 지정")
chk(len(set(p["id"] for p in ps)) == len(ps), "표현 ID 중복 없음")
chk(all(len(d["lines"]) >= 5 for d in ds), "모든 대화 5턴 이상")

print("[2] audio")
files = [f for f in os.listdir(AUD) if f.endswith(".mp3")]
need = ["p_" + p["id"] + ".mp3" for p in ps] + ["e_" + p["id"] + ".mp3" for p in ps]
for d in ds:
    need += ["d%s_%d.mp3" % (d["id"], i) for i in range(len(d["lines"]))]
missing = [n for n in need if not os.path.exists(os.path.join(AUD, n))]
zero = [n for n in need if os.path.exists(os.path.join(AUD, n)) and os.path.getsize(os.path.join(AUD, n)) <= 800]
chk(len(files) == len(need), "MP3 %d개 생성 / 필요 %d개" % (len(files), len(need)))
chk(not missing, "누락 파일 %d개" % len(missing))
chk(not zero, "0바이트(손상) 파일 %d개" % len(zero))
total = sum(os.path.getsize(os.path.join(AUD, f)) for f in files)
print("       총 용량 %.1f MB, 평균 %.1f KB" % (total/1e6, total/len(files)/1e3))
chk(1.0e6 < total < 60e6, "용량 정상 범위")

print("[3] html")
html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
chk(html.startswith("<!DOCTYPE html>"), "doctype")
chk("apple-mobile-web-app-capable" in html, "iOS 홈화면 메타")
m = re.search(r"var DATA = (\{.*?\});\n", html, re.S)
chk(bool(m), "DATA 블록 존재")
if m:
    try:
        d2 = json.loads(m.group(1))
        chk(len(d2["phrases"]) == len(ps) and len(d2["dialogues"]) == len(ds), "임베디드 JSON이 원본과 일치")
    except Exception as e:
        chk(False, "임베디드 JSON 파싱 실패: %s" % e)
for tag in ["</html>", "id=\"deck\"", "id=\"tab-card\"", "id=\"tab-role\"", "id=\"tab-drill\"", "id=\"tab-saved\"", "id=\"tab-tips\""]:
    chk(tag in html, "필수 요소 %s" % tag)
chk(html.count("<script") == 1 and html.count("</script>") == 1, "script 블록 1개")
# every audio name used by JS must follow the generated naming
refs = set(re.findall(r"playFile\('([a-z]_)", html))
chk(refs == {"p_", "e_"}, "카드 오디오 참조 접두사 %s" % sorted(refs))
chk("/*__DATA__*/" not in html, "플레이스홀더 치환 완료")
for f in ["icon-192.png", "apple-touch-icon.png"]:
    chk(os.path.exists(os.path.join(ROOT, f)), f)

print("[4] ruby / romaji sample")
RUBY = re.compile(r"\[([^\[\]\|]+)\|([^\[\]\|]+)\]")
bad = [p["id"] for p in ps if RUBY.search(p["jp"]) and "<ruby>" not in p["ruby"]]
chk(not bad, "ruby 변환 누락 %s" % bad[:5])
chk(all("<rt>" in p["ruby"] or not re.search(r"[\u4e00-\u9fff]", p["jp"]) for p in ps), "후리가나 rt 태그")
for p in ps[:3] + [ps[50], ps[100]]:
    print("       %-6s %-28s %s" % (p["id"], p["jp"], p["kana"]))

print("\nRESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
