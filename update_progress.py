import re

# README 파일 읽기
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# 체크박스 카운트
total = len(re.findall(r"\[.\]", content))
done = len(re.findall(r"\[x\]", content, re.IGNORECASE))
percent = int(done / total * 100) if total > 0 else 0

# 진행률 바 생성 (10칸)
filled = int(percent / 10)
progress_bar = "█" * filled + "░" * (10 - filled)

# 새로운 요약
new_summary = f"""- ✅ 완료: {done} / {total}  
- 진행률: {percent}%  

#### Progress Bar
`{progress_bar}` {percent}%"""

# 기존 요약 부분 교체
content = re.sub(r"- ✅ 완료:.*?Progress Bar\n`.*?%`.*", new_summary, content, flags=re.S)

# 저장
with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)
