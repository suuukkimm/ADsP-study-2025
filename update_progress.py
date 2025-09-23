#!/usr/bin/env python3
import re, io, sys

README = "README.md"
START = "<!-- PROGRESS-START -->"
END   = "<!-- PROGRESS-END -->"

def main():
    try:
        with io.open(README, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("README.md not found; skipping.")
        return 0

    # 체크박스 집계: [ ] / [x] / [X]
    total = len(re.findall(r"\[(?: |x|X)\]", content))
    done  = len(re.findall(r"\[(?:x|X)\]", content))
    percent = int(round((done / total) * 100)) if total else 0

    # 진행률 바 (20칸)
    bar_len = 20
    filled = int(round(bar_len * percent / 100))
    bar = "█" * filled + "░" * (bar_len - filled)

    new_block = f"""{START}
- ✅ 완료: {done} / {total}  
- 진행률: {percent}%  

#### Progress Bar
`{bar}` {percent}%
{END}"""

    pat = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)

    if pat.search(content):
        updated = pat.sub(new_block, content)
    else:
        print("Markers not found; appending block to end of README.")
        updated = content.rstrip() + "\n\n" + new_block + "\n"

    if updated != content:
        with io.open(README, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"✅ Updated progress: {done}/{total} ({percent}%)")
    else:
        print("ℹ️ No changes (progress unchanged).")

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        # 어떤 이유로든 실패해도 잡을 수 있게
        print(f"⚠️ Script error (non-fatal): {e}")
        sys.exit(0)
