import re, sys

README = "README.md"
START = "<!-- PROGRESS-START -->"
END = "<!-- PROGRESS-END -->"

with open(README, "r", encoding="utf-8") as f:
    content = f.read()

# 체크박스 집계: [ ] / [x] / [X] 만 카운트
total = len(re.findall(r"\[(?: |x|X)\]", content))
done = len(re.findall(r"\[(?:x|X)\]", content))
percent = int(round((done / total) * 100)) if total else 0

# 게이지 바(20칸)
bar_len = 20
filled = int(round(bar_len * percent / 100))
bar = "█" * filled + "░" * (bar_len - filled)

block = f"""{START}
- ✅ 완료: {done} / {total}
- 진행률: {percent}%

#### Progress Bar
`{bar}` {percent}%
{END}"""

pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
if not pattern.search(content):
    print("⚠️  PROGRESS 마커가 README에 없습니다. README에 마커 블록을 추가하세요.")
    sys.exit(0)

new_content = pattern.sub(block, content)

if new_content != content:
    with open(README, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"✅ Updated progress: {done}/{total} ({percent}%)")
else:
    print("ℹ️ 변경 사항 없음 (진행률 동일).")
