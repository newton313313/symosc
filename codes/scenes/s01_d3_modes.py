"""
S01 —— D3：三個耦合振盪子的對稱、約化、模式與拍
執行（在 codes/ 內）：manimgl scenes/s01_d3_modes.py S01D3Modes
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, r"C:\mypython\manim\projects\combkit")

from manimlib import *

from combkit.draw.fulton_draw import assert_in_frame
from combkit.draw.scene_base import ChuScene
from combkit.draw.styles import mixed, zh
from combkit.draw.walk_draw import tex_table
from utils import osc_draw as O
from utils import symosc as S

K0, KK = 1.0, 0.5
CEN = np.array([-3.6, 0.2, 0])
RAD = 1.55


def check_math():
    K = S.K_d3(K0, KK)
    assert np.allclose(K, [[2, -0.5, -0.5], [-0.5, 2, -0.5], [-0.5, -0.5, 2]])
    for g in S.D3_NAMES:
        assert np.allclose(S.d3_matrix(g) @ K, K @ S.d3_matrix(g))
    assert S.d3_chars_of(S.d3_matrix) == (3, 0, 1)
    assert S.decompose((3, 0, 1), S.D3_CHARS, S.D3_SIZES) == {"A1": 1, "A2": 0, "E": 1}
    assert np.allclose(S.projector_d3("E") @ [1, 0, 0], np.array([2, -1, -1]) / 3)
    wa, we = S.d3_freqs(K0, KK)
    assert (round(wa ** 2, 3), round(we ** 2, 3)) == (1.0, 2.5) and round(we, 3) == 1.581
    assert round(2 * math.pi / (we - wa), 1) == 10.8
    assert S.class_sum_values(S.D3_CHARS, S.D3_SIZES) == {"A1": (1, 2, 3), "A2": (1, 2, -3), "E": (1, -1, 0)}
    c2 = S.d3_matrix("r") + S.d3_matrix("r2")
    c3 = S.d3_matrix("s1") + S.d3_matrix("s2") + S.d3_matrix("s3")
    assert np.allclose(c2 @ [1, 1, 1], 2 * np.ones(3)) and np.allclose(c3 @ [1, 1, 1], 3 * np.ones(3))
    assert np.allclose(c2 @ [0, 1, -1], -np.array([0, 1, -1])) and np.allclose(c3 @ [0, 1, -1], 0)
    x = S.beat(math.pi / (we - wa) * 0 + 0.0, K0, KK)
    assert np.allclose(x, [1, 0, 0])


def rows_k():
    return r"K=\begin{pmatrix}k_0+2k&-k&-k\\-k&k_0+2k&-k\\-k&-k&k_0+2k\end{pmatrix}"


def part_setup(s):
    s.say("問：三個相同的擺兩兩用彈簧相連，會怎麼擺？")
    tri = O.osc_triangle(RAD, CEN)
    eq = Tex(r"m\ddot x=-Kx", font_size=40).move_to([2.6, 2.3, 0])
    km = Tex(rows_k(), font_size=36).move_to([2.6, 0.9, 0])
    par = Tex(r"k_0=1,\ k=0.5,\ m=1", font_size=30).set_color(GREY_A).next_to(km, DOWN, buff=0.35)
    assert_in_frame(tri, eq, km, par)
    s.play(ShowCreation(tri[0]), FadeIn(tri[1]), FadeIn(tri[2]), run_time=1.2)
    s.play(Write(eq), FadeIn(km), run_time=1.2)
    s.play(FadeIn(par), run_time=0.5)
    s.wait(2.5)
    return tri, VGroup(eq, km, par)


def part_symmetry(s, tri, info):
    labs = tri[2]
    s.say("轉 120°：擺 1→2→3→1，", "$K$", " 不變")
    old = [l.get_center().copy() for l in labs]
    s.play(*[labs[j].animate.move_to(old[(j + 1) % 3]) for j in range(3)], run_time=1.2)
    s.play(*[labs[j].animate.move_to(old[j]) for j in range(3)], run_time=0.6)
    s.say("鏡射：交換擺 2、3（擺 1 不動），", "$K$", " 也不變")
    s.play(labs[1].animate.move_to(old[2]), labs[2].animate.move_to(old[1]), run_time=1.0)
    s.play(labs[1].animate.move_to(old[1]), labs[2].animate.move_to(old[2]), run_time=0.6)
    comm = Tex(r"D(g)\,K=K\,D(g)\quad(g\in D_3,\ |D_3|=6)", font_size=32).set_color(YELLOW)
    comm.next_to(info, DOWN, buff=0.45)
    assert_in_frame(comm)
    s.say("6 個操作都和 ", "$K$", " 交換：可以共用本徵空間")
    s.play(Write(comm), run_time=1.0)
    s.wait(2.5)
    s.play(FadeOut(info), FadeOut(comm), run_time=0.6)


def part_characters(s):
    s.say("置換表示的特徵標：每個操作固定幾個擺")
    rows = [["", "e", "2C_3", "3\\sigma"],
            ["A_1", "1", "1", "1"],
            ["A_2", "1", "1", "-1"],
            ["E", "2", "-1", "0"],
            ["\\chi_{\\rm perm}", "3", "0", "1"]]
    tab = tex_table(rows, [1.3, 0.9, 1.1, 1.1], row_h=0.55, font_size=30).move_to([2.4, 1.3, 0])
    dec = Tex(r"\chi_{\rm perm}=A_1\oplus E", font_size=40).set_color(YELLOW).move_to([2.4, -0.55, 0])
    note = Tex(r"n_\alpha=\tfrac16\sum_g\chi_\alpha(g)\chi_{\rm perm}(g):\ n_{A_1}=1,\ n_{A_2}=0,\ n_E=1",
               font_size=28).move_to([2.4, -1.35, 0])
    assert_in_frame(tab, dec, note)
    s.play(FadeIn(tab), run_time=1.0)
    s.wait(2.5)
    s.say("約化：", "$3=1+2$", "，不用解三次方程")
    s.play(Write(dec), FadeIn(note), run_time=1.2)
    s.wait(2.0)
    s.play(FadeOut(tab), FadeOut(dec), FadeOut(note), run_time=0.6)


def part_labels(s):
    s.say("怎麼標本徵空間？", "$D(r)$", " 與 ", "$D(\\sigma)$", " 不交換，不能同時對角化")
    rows = [["", "c_2=r+r^2", "c_3=\\sigma_1+\\sigma_2+\\sigma_3"],
            ["A_1", "2", "3"], ["A_2", "2", "-3"], ["E", "-1", "0"]]
    tab = tex_table(rows, [1.0, 2.2, 3.0], row_h=0.6, font_size=30).move_to([2.4, 1.2, 0])
    vec = VGroup(Tex(r"(1,1,1):\ (c_2,c_3)=(2,3)\Rightarrow A_1", font_size=30),
                 Tex(r"(1,1,1)^\perp:\ (c_2,c_3)=(-1,0)\Rightarrow E", font_size=30)).arrange(DOWN, buff=0.25)
    vec.move_to([2.4, -0.9, 0])
    assert_in_frame(tab, vec)
    s.play(FadeIn(tab), run_time=1.0)
    s.say("類和和所有 ", "$D(g)$", "、", "$K$", " 都交換：它的值就是不可約表示的標籤", wait=2.5)
    s.play(FadeIn(vec), run_time=1.0)
    s.wait(2.0)
    s.say("$E$", " 是二維：還要一個子群標籤（", "$C_3$", " 的 ", "$\\omega^m$", " 或 ", "$C_2$", " 的 ", "$\\pm$", "）——見 S02", wait=2.5)
    s.play(FadeOut(tab), FadeOut(vec), run_time=0.6)


def animate_mode(s, springs, vec, omega, label, run_time):
    t = ValueTracker(0.0)
    m = O.masses_updater(lambda: [v * math.cos(omega * t.get_value()) for v in vec], RAD, CEN)
    s.play(FadeOut(springs), FadeIn(m), FadeIn(label), run_time=0.6)
    s.play(t.animate.set_value(run_time * 1.4), run_time=run_time, rate_func=linear)
    s.play(FadeOut(label), FadeOut(m), FadeIn(springs), run_time=0.5)


def part_modes(s, springs):
    wa, we = S.d3_freqs(K0, KK)
    s.say("投影算子給出模式：", "$A_1=(1,1,1)$", "，三個一起擺，彈簧不伸縮")
    la = VGroup(Tex(r"A_1:\ (1,1,1)", font_size=40).set_color(YELLOW),
                Tex(r"\omega_A^2=k_0=1", font_size=36)).arrange(DOWN, buff=0.3).move_to([2.6, 1.0, 0])
    animate_mode(s, springs, [1, 1, 1], wa, la, 6.0)
    s.say("$E$", " 是二維：", "$(2,-1,-1)$", "、", "$(0,1,-1)$", " 同頻率")
    le1 = VGroup(Tex(r"E:\ (2,-1,-1)", font_size=40).set_color(YELLOW),
                 Tex(r"\omega_E^2=k_0+3k=2.5", font_size=36)).arrange(DOWN, buff=0.3).move_to([2.6, 1.0, 0])
    animate_mode(s, springs, [1, -0.5, -0.5], we, le1, 5.5)
    le2 = VGroup(Tex(r"E:\ (0,1,-1)", font_size=40).set_color(YELLOW),
                 Tex(r"\omega_E^2=2.5", font_size=36)).arrange(DOWN, buff=0.3).move_to([2.6, 1.0, 0])
    animate_mode(s, springs, [0, 0.87, -0.87], we, le2, 5.5)
    s.say("模式形狀由群決定（與 ", "$k_0$", "、", "$k$", " 無關），參數只決定頻率", wait=2.5)
    s.say("簡併是對稱保證的：只要保持 ", "$D_3$", "，", "$E$", " 的兩個模式永遠同頻率", wait=2.5)


def part_beats(s, springs):
    wa, we = S.d3_freqs(K0, KK)
    s.say("只推擺 1：", "$(1,0,0)=\\tfrac13(1,1,1)+\\tfrac13(2,-1,-1)$")
    t = ValueTracker(0.0)
    m = O.masses_updater(lambda: S.beat(t.get_value(), K0, KK), RAD, CEN)
    f1 = Tex(r"x_1=\tfrac13\cos\omega_At+\tfrac23\cos\omega_Et", font_size=32).move_to([2.6, 2.0, 0])
    f2 = Tex(r"x_2=x_3=\tfrac13\cos\omega_At-\tfrac13\cos\omega_Et", font_size=32).move_to([2.6, 1.25, 0])
    ax = Axes(x_range=[0, 22, 5], y_range=[-1, 1, 1], width=5.2, height=1.8).move_to([2.6, -1.0, 0])
    g1 = ax.get_graph(lambda u: S.beat(u, K0, KK)[0], x_range=[0, 22]).set_stroke(YELLOW, 2)
    g2 = ax.get_graph(lambda u: S.beat(u, K0, KK)[1], x_range=[0, 22]).set_stroke(BLUE_C, 2)
    l1 = Tex(r"x_1", font_size=26).set_color(YELLOW).next_to(ax, LEFT, buff=0.1).shift(0.4 * UP)
    l2 = Tex(r"x_2", font_size=26).set_color(BLUE_C).next_to(ax, LEFT, buff=0.1).shift(0.4 * DOWN)
    assert_in_frame(f1, f2, ax, l1, l2)
    s.play(FadeOut(springs), FadeIn(m), FadeIn(f1), FadeIn(f2), ShowCreation(ax), FadeIn(l1), FadeIn(l2), run_time=1.0)
    s.play(t.animate.set_value(21.6), ShowCreation(g1), ShowCreation(g2), run_time=14.0, rate_func=linear)
    s.say("能量在擺 1 與擺 2、3 之間來回：拍的週期 ", "$2\\pi/(\\omega_E-\\omega_A)\\approx10.8$", wait=2.5)
    s.say("擺 1 最低只剩 ", "$\\tfrac13$", " 的振幅（能量 ", "$\\tfrac19$", "）：三個擺無法完全換手", wait=2.5)
    s.play(FadeOut(m), FadeIn(springs), run_time=0.5)
    return VGroup(f1, f2, ax, g1, g2, l1, l2)


class S01D3Modes(ChuScene):
    def construct(self):
        self.show_header("S01　D3：三個耦合振盪子")
        check_math()
        tri, info = part_setup(self)
        part_symmetry(self, tri, info)
        part_characters(self)
        part_labels(self)
        part_modes(self, tri[0])
        beats = part_beats(self, tri[0])
        self.play(FadeOut(beats), run_time=0.6)
        self.say("對稱先把問題拆成 ", "$A_1\\oplus E$", "：模式形狀由群決定，參數只決定頻率")
        self.wait(1.0)
