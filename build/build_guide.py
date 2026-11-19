"""Generate the full expression compendium as Markdown (repo + workspace copy)."""
import os
import contentlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

LVNAME = {
    1: "Lv.1 최신 유행 · MZ · SNS 리액션",
    2: "Lv.2 일상 표준 회화",
    3: "Lv.3 직장 · 사회생활 표준 회화",
    4: "Lv.4 감정 · 관계 · 고민 상담",
    5: "Lv.5 고급 심화 — 마음속 깊은 이야기",
}
LVNOTE = {
    1: "유튜브·X·인스타에서 지금 실제로 쓰이는 추임새·줄임말·감정 표현. **친한 사이 전용**이며 윗사람·비즈니스에서는 Lv.2~3의 표준 표현을 쓰세요.",
    2: "인사, 카페·식당·쇼핑, 약속, 가벼운 부탁·거절, 일상 잡담. タメ口(반말)와 です・ます(정중체)의 전환을 함께 익힙니다.",
    3: "쿠션어(クッション言葉), 완곡한 거절, 상사·동료와의 조율, 사과·감사, 일본어 특유의 돌려 말하기.",
    4: "고민 털어놓기, 위로·공감, 서운함을 부드럽게 전달, 조언 구하기·건네기. '해결'보다 '받아주기'가 중심입니다.",
    5: "내면의 불안·후회·가치관, 삶의 방향, 관계의 진심, 상대의 깊은 이야기를 끌어내는 경청·질문.",
}


def main():
    data = contentlib.processed()
    ps, ds, M = data["phrases"], data["dialogues"], data["meta"]
    L = []
    A = L.append
    A("# 日本語 스피킹 표현집 총정리")
    A("")
    A("> 일본어 스피킹 훈련 웹앱 **https://neveziel.github.io/jp-speaking/** 의 전체 수록 내용입니다.")
    A("> 모든 표현은 뜻(한국어) → 일본어 → 가나 → 뉘앙스 → 예문 순으로, 앱에서는 같은 문장의 성우 MP3로 듣고 따라 말할 수 있습니다.")
    A("")
    lvc = {}
    for p in ps:
        lvc[p["lv"]] = lvc.get(p["lv"], 0) + 1
    A("| 항목 | 수량 |")
    A("|---|---|")
    A("| 수록 표현 | **%d문장** |" % len(ps))
    for k in sorted(lvc):
        A("| └ Lv.%d | %d문장 |" % (k, lvc[k]))
    A("| 멀티턴 롤플레이 | **%d개 상황 / %d턴** |" % (len(ds), sum(len(d["lines"]) for d in ds)))
    A("| 성우 MP3 | **%d개** (남 ja-JP-KeitaNeural · 여 ja-JP-NanamiNeural) |" % (len(ps) * 2 + sum(len(d["lines"]) for d in ds)))
    A("| 학습 팁 | %d개 |" % len(M["tips"]))
    A("")
    A("## 쓰는 법 (5단계)")
    A("")
    for m in M["method"]:
        A("%d. **%s** — %s" % (m["n"], m["t"], m["d"]))
    A("")
    A("---")
    A("")
    for lv in sorted(lvc):
        A("## %s" % LVNAME[lv])
        A("")
        A("%s" % LVNOTE[lv])
        A("")
        A("| # | 일본어 | 가나 | 한국어 | 반말/정중 | 뉘앙스 |")
        A("|---|---|---|---|---|---|")
        for p in [x for x in ps if x["lv"] == lv]:
            pol = "반말" if p["pol"] == "casual" else "정중체"
            A("| %s | %s | %s | %s | %s | %s |" % (
                p["id"], p["jp"], p["kana"], p["ko"], pol, p["note"].replace("|", "／")))
        A("")
        A("<details><summary>예문 보기</summary>")
        A("")
        for p in [x for x in ps if x["lv"] == lv]:
            A("- **%s** %s / %s  " % (p["id"], p["ex"], p["exKo"]))
        A("")
        A("</details>")
        A("")
        A("---")
        A("")
    A("## 실전 롤플레이 %d개" % len(ds))
    A("")
    A("A(상대) 음성을 먼저 듣고, B(내 턴)는 한국어 힌트만 보고 직접 말한 뒤 정답을 확인합니다.")
    A("")
    for d in ds:
        A("### %s. %s  <sub>Lv.%d</sub>" % (d["id"], d["title"], d["lv"]))
        A("")
        A("*상황: %s*" % d["situation"])
        A("")
        for l in d["lines"]:
            who = "**A**" if l["r"] == "A" else "**B(나)**"
            A("- %s  %s  " % (who, l["jp"]))
            A("  %s  " % l["ko"])
            if l["note"]:
                A("  <sub>%s</sub>" % l["note"])
        A("")
    A("---")
    A("")
    A("## 학습 팁 (유튜브 · 네이버 · X · 구글 · 인스타 공개 웹)")
    A("")
    cat = {}
    order = []
    for t in M["tips"]:
        if t["cat"] not in cat:
            cat[t["cat"]] = []
            order.append(t["cat"])
        cat[t["cat"]].append(t)
    for c in order:
        A("### %s" % c)
        A("")
        for t in cat[c]:
            A("- **%s** — %s  " % (t["t"], t["d"]))
            A("  <sub>[%s](%s)</sub>" % (t["srcName"], t["src"]))
        A("")
    A("---")
    A("")
    A("## 수집 출처")
    A("")
    A("| 구분 | 자료 |")
    A("|---|---|")
    for s in M["sources"]:
        A("| %s | [%s](%s) |" % (s["k"], s["n"], s["u"]))
    A("")
    A("## 수집 한계 (정직 고지)")
    A("")
    for l in M["limits"]:
        A("- %s" % l)
    A("")
    A("---")
    A("")
    A("## 부록 — 레벨별 사용 장면 요약")
    A("")
    A("| 레벨 | 누구에게 | 어디서 | 조심할 점 |")
    A("|---|---|---|---|")
    A("| Lv.1 | 친구·동갑·SNS | 메신저, 사적 대화 | 윗사람·거래처에서는 쓰지 않음. 유행어는 반감기가 짧음 |")
    A("| Lv.2 | 누구에게나 | 여행, 가게, 이웃 | です・ます 유지, タメ口는 상대가 먼저 쓸 때 |")
    A("| Lv.3 | 상사·동료·거래처 | 회의, 전화, 메일 | 쿠션어는 한 문장에 하나, 결론 먼저 |")
    A("| Lv.4 | 가까운 사람 | 사적 대화, 상담 | 조언보다 감정 인정이 먼저 |")
    A("| Lv.5 | 신뢰하는 사이 | 긴 대화, 새벽 통화 | 단정하지 않기, 답을 서두르지 않기 |")
    A("")
    A("*생성: %s · 앱 버전 %s*" % (M["app"]["builtAt"], M["app"]["version"]))

    text = "\n".join(L) + "\n"
    targets = [os.path.join(ROOT, "phrases_guide.md"),
               os.path.join(ROOT, "..", "..", "일본어_스피킹_표현집_총정리.md")]
    for t in targets:
        with open(t, "w", encoding="utf-8") as f:
            f.write(text)
        print("wrote", os.path.abspath(t), len(text), "chars")


if __name__ == "__main__":
    main()
