"""
main.py —— symosc 全部場景的入口與連續播放（在 codes/ 裡執行）

    manimgl main.py                列出所有場景，選一個預覽
    manimgl main.py SymOscDemo -w  三幕連續播放（S01–S03），輸出到 renders/SymOscDemo.mp4

ManimGL 只列出「定義在這個檔案裡」的場景，所以每個場景在這裡都有一個同名子類別。
連續播放是拿 SymOscDemo 這個物件依序去跑各場景的 construct，所以場景的輔助函式都寫在模組層級。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))          # codes/，讓 scenes.*、utils.* 可以 import
sys.path.insert(0, r"C:\mypython\manim\projects\combkit")

from manimlib import *

from scenes import s01_d3_modes as s01
from scenes import s02_breaking as s02
from scenes import s03_q8 as s03


def play_sequence(scene, classes):
    """依序借用各場景的 construct 連續播放；場景之間清空畫面、鏡頭歸位。"""
    for k, cls in enumerate(classes):
        cls.construct(scene)
        if k < len(classes) - 1:
            scene.fade_all(run_time=0.8)
            scene.frame.to_default_state()
            scene.wait(0.4)


class S01D3Modes(s01.S01D3Modes):
    pass


class S02Breaking(s02.S02Breaking):
    pass


class S03Q8(s03.S03Q8):
    pass


ALL_SCENES = [s01.S01D3Modes, s02.S02Breaking, s03.S03Q8]


class SymOscDemo(s01.S01D3Modes):
    """三幕連續播放（S01–S03）。"""

    def construct(self):
        play_sequence(self, ALL_SCENES)
