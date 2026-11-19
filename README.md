# 日本語 스피킹 훈련소 (jp-speaking)

아이폰 Safari '홈 화면에 추가'로 쓰는 **일본어 회화 스피킹 훈련 PWA**입니다.

- **앱: https://neveziel.github.io/Jp-speaking-/**
- 전체 표현집: [phrases_guide.md](phrases_guide.md) · 앱 안의 **💡 팁·출처** 탭에서도 열람 가능
- 저장소: https://github.com/neveziel/Jp-speaking-

> 아이폰: Safari에서 위 주소를 연 뒤 **공유(□↑) → 홈 화면에 추가**. 음성은 사전 녹음된 MP3라 **무음 모드에서도** 재생됩니다.

## 무엇이 들어 있나

| 항목 | 수량 |
|---|---|
| 수록 표현 | **141문장** (Lv.1 26 / Lv.2 31 / Lv.3 28 / Lv.4 28 / Lv.5 28) |
| 멀티턴 롤플레이 | **14개 상황 · 84턴** |
| 성우 MP3 | **366개** = 표현 141 + 예문 141 + 대화 턴 84 (남 `ja-JP-KeitaNeural`, 여 `ja-JP-NanamiNeural`) |
| 학습 팁 | 25개 (출처 19건) |

### 5단계 구성
1. **Lv.1 최신 유행·MZ·SNS 리액션** — それな / ガチで / 草 / エモい / きまZ / あーね / ワンチャン …
2. **Lv.2 일상 표준 회화** — 인사, 카페·식당, 쇼핑, 약속, 가벼운 부탁·거절, タメ口↔敬語
3. **Lv.3 직장·사회생활** — 쿠션어, 완곡한 거절, 사과·감사, 보류·조율, 결론부터 보고
4. **Lv.4 감정·관계·고민 상담** — 공감·위로, 서운함 전달, 조언 구하기·건네기
5. **Lv.5 고급 심화** — 불안·후회·가치관, 경청과 깊은 질문

## 기능

- **스피킹 카드(인출 훈련)**: 한국어 뜻만 먼저 보이고 → 직접 소리 내어 말한 뒤 → 정답(일본어·후리가나·가나·로마자·뉘앙스·예문) 확인
- **쉐도잉 루프**: 원어민 음성 → 3초 카운트다운 따라 말하기 → 다시 듣기, 최대 5회 / 재생속도 0.75x · 1.0x · 1.15x
- **내 목소리 녹음·비교**: MediaRecorder (iOS Safari 마이크 권한 필요, 미지원 시 안내 후 비활성)
- **실전 롤플레이**: A(상대) 음성 → B(내 턴)는 한국어 힌트만 보고 말하기 → 정답·음성 공개 / 전체 연속 재생 / B만 연속 재생
- **오늘의 드릴**: 무작위 10문장 집중 훈련, 진행 점 표시
- **저장함·완료 체크**: localStorage(기기별) — 상단 진행률 `n/141`
- **후리가나 ON/OFF**, **반말·정중체 배지**, **레벨 필터**, **한국어·일본어·태그 검색**, 카드 스와이프
- **팁·출처 탭**: 훈련법 5단계 + 유튜브·네이버·X·구글·인스타(공개 웹) 학습 팁 25개 + 수집 한계 고지

## 아이폰 무음 모드 대응

iOS Safari는 무음 모드에서 `speechSynthesis`가 막히므로, **모든 표현·예문·대화 턴을 edge-tts로 사전 생성한 MP3**(`audio/`)로 재생합니다. `speechSynthesis`는 MP3 로드 실패 시 폴백으로만 남겨 두었습니다.

## 구조

```
index.html          # 단일 페이지 앱 (데이터 임베드, 224KB)
audio/              # p_*.mp3 표현 / e_*.mp3 예문 / d*_*.mp3 대화 턴 (366개, 9.4MB)
content/            # 원본 데이터 — lv12.json, lv345.json, dialogues.json, meta.json
build/              # contentlib.py, make_audio.py, build_html.py, build_guide.py, verify.py
phrases_guide.md    # 전체 표현집 (레벨별 표 + 예문 + 롤플레이 대본 + 출처/한계)
icon-192.png, apple-touch-icon.png, .nojekyll
```

## 다시 빌드하기

```bash
cd build
python3 make_audio.py     # MP3 생성 (edge-tts, 6 병렬, 실패 시 재시도)
python3 build_html.py     # content/*.json → index.html
python3 build_guide.py    # phrases_guide.md
python3 verify.py         # 표현 수·레벨 분포·MP3 누락/0바이트·JSON 무결성 검사 → PASS
```

내용을 고칠 때는 `content/*.json`을 수정하고 위 스크립트를 다시 돌립니다. 문장을 바꾸면 `make_audio.py`가 해당 MP3만 다시 만듭니다(기존 파일은 건너뜀, `--force`로 전체 재생성).

## 배포 방법 (중요)

GitHub Pages가 **`gh-pages` 브랜치 루트**를 소스로 빌드하고 있습니다. 따라서 수정 사항은 **main과 gh-pages 두 브랜치에 모두 푸시**해야 사이트에 반영됩니다.

```bash
git add -A && git commit -m "..."
git push origin main
git push origin main:gh-pages
```

> 계정의 저장소 생성·이름 변경·Pages 설정 API는 현재 연동 권한에 없어서, Pages는 `gh-pages` 브랜치를 푸시해 활성화했습니다. 저장소 이름은 `Jp-speaking-`(대문자 J + 끝 하이픈)로 확정되었고, 그래서 앱 주소도 `github.io/Jp-speaking-/`입니다.

## 출처와 한계

표현은 공개 자료(유튜브 채널·네이버 블로그·X 공개 포스트·웹 문서)를 참고해 학습용으로 다시 쓴 것이며 원문 인용이 아닙니다. 인스타그램은 로그인 장벽 때문에 공개 웹에 색인된 범위만 반영했습니다. 유행어는 2025~2026년 공개 자료 기준이므로 실제 사용 전 상대와 장면(TPO)을 확인하세요.
