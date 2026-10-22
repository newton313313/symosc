"""
render_all.py —— 一次把場景輸出成影片（存到 renders/）。在 codes/ 裡執行；一次只跑一個 manimgl。

    python render_all.py            S01–S03，1080p
    python render_all.py --demo     另外輸出連續播放 SymOscDemo
    python render_all.py -l         改用 480p（預覽）
    python render_all.py --force    影片已經存在也重新輸出（預設跳過：已完成的影片不覆寫）
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCENES = [("scenes/s01_d3_modes.py", "S01D3Modes"), ("scenes/s02_breaking.py", "S02Breaking"), ("scenes/s03_q8.py", "S03Q8")]
DEMOS = [("main.py", "SymOscDemo")]


def main(argv):
    quality = "-l" if "-l" in argv else "--hd"
    jobs = SCENES + (DEMOS if "--demo" in argv else [])
    failed = []
    for f, cls in jobs:
        out = HERE / "renders" / f"{cls}.mp4"
        if out.exists() and "--force" not in argv:
            print(f"略過（影片已存在，要重做請加 --force）：{cls}")
            continue
        print(f"=== {cls} ({quality}) ===", flush=True)
        r = subprocess.run(["manimgl", f, cls, "-w", quality], cwd=HERE)
        if r.returncode != 0 or not out.exists():
            failed.append(cls)
    print("全部完成。" if not failed else f"失敗：{failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
