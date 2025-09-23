import re

README = "README.md"
START = "<!-- PROGRESS-START -->"
END = "<!-- PROGRESS-END -->"

with open(README, "r", encoding="utf-8") as f:
    content = f.read()

# 체크박스 카운트
total = len(re.findall(r"\[(?: |x|X)\]", content))
done = len(re.findall(r"\[(?:x|X)\]", content))
percent = int(round((done / total) * 100)) if total else 0

# 진행률 바 (20칸)
bar_len = 20
filled = int(round(bar_len * percent / 100))
bar = "█" * filled + "░" * (bar_len - filled)

block = f"""{START}
- ✅ 완료: {done} / {total}  
- 진행률: {percent}%  

#### Progress Bar
`{bar}` {percent}%
{END}"""

pattern = re.compile(rf"{re.escape(START)}.*?{re.escape(END)}", re.S)

# 마커 구간이 있으면 교체, 없으면 그냥 추가
if pattern.search(content):
    new_content = pattern.sub(block, content)
else:
    new_content = content + "\n\n" + block

if new_content != content:
    with open(README, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"✅ Updated progress: {done}/{total} ({percent}%)")
else:
    print("ℹ️ 변경 사항 없음 (진행률 동일).")
