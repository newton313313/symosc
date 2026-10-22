"""
S03 —— 四元群 Q8：8 個擺、E 出現兩次、左標籤 m 與右標籤 n、四元數型的四重簡併
執行（在 codes/ 內）：manimgl scenes/s03_q8.py S03Q8
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, r"C:\mypython\manim\projects\combkit")

from manimlib import *

from combkit.draw.fulton_draw import assert_in_frame
from combkit.draw.scene_base import ChuScene
from combkit.draw.styles import zh
from combkit.draw.walk_draw import tex_table
from utils import osc_draw as O
from utils import symosc as S

K0, KI, KJ, KK = 1.0, 0.05, 0.25, 0.5
GC = np.array([-3.7, -0.1, 0])


def check_math():
    assert S.q8_mul("i", "j") == "k" and S.q8_mul("j", "i") == "-k" and S.q8_mul("k", "k") == "-1"
    K = S.K_q8(K0, KI, KJ, KK)
    for g in S.Q8_NAMES:
        assert np.allclose(S.L(g) @ K, K @ S.L(g))
    lev = S.q8_levels(K0, KI, KJ, KK)
    assert {a: round(v, 6) for a, v in lev.items()} == {"A1": 1.0, "A2": 4.0, "A3": 3.2, "A4": 2.2, "E": 2.6}
    assert np.allclose(sorted(np.linalg.eigvalsh(K)), sorted([1.0, 4.0, 3.2, 2.2] + [2.6] * 4))
    chi = tuple(int(round(np.trace(S.L(c[0])))) for c in S.Q8_CLASSES.values())
    assert chi == (8, 0, 0, 0, 0)
    assert S.decompose(chi, S.Q8_CHARS, S.Q8_SIZES) == {"A1": 1, "A2": 1, "A3": 1, "A4": 1, "E": 2}
    assert np.allclose(S.q8_irrep_vector("A2"), [1, 1, -1, -1, 1, 1, -1, -1])
    basis = S.q8_E_basis()
    assert [(n, m, nn) for n, _, m, nn in basis] == [("v1", 1j, -1j), ("v2", -1j, 1j), ("v3", -1j, -1j), ("v4", 1j, 1j)]
    for _, v, _, _ in basis:
        assert np.allclose(K @ v, 2.6 * v) and np.allclose(S.L("-1") @ v, -v)
    assert np.allclose(S.Q8_REP2["j"] @ S.Q8_REP2["j"], -np.eye(2))
    assert S.frobenius_schur(S.Q8_CHARS["E"], S.Q8_CLASSES, S.Q8_SIZES, lambda g: S.q8_mul(g, g)) == -1
    assert S.q8_mul(S.q8_mul("j", "i"), S.q8_inv("j")) == "-i"


def part_group(s):
    s.say("問：非阿貝爾、而且同一個不可約表示出現兩次，基底怎麼標？")
    rule = Tex(r"Q_8=\{\pm1,\pm i,\pm j,\pm k\},\quad i^2=j^2=k^2=ijk=-1", font_size=36).move_to([0, 2.2, 0])
    rho = Tex(r"\rho(i)=\begin{pmatrix}i&0\\0&-i\end{pmatrix},\ \rho(j)=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\ "
              r"\rho(k)=\rho(i)\rho(j)", font_size=34).move_to([0, 0.8, 0])
    nonab = Tex(r"ij=k,\quad ji=-k", font_size=36).set_color(YELLOW).move_to([0, -0.5, 0])
    assert_in_frame(rule, rho, nonab)
    s.play(Write(rule), run_time=1.2)
    s.play(FadeIn(rho), run_time=1.0)
    s.play(FadeIn(nonab), run_time=0.6)
    s.wait(2.0)
    s.play(FadeOut(VGroup(rule, rho, nonab)), run_time=0.6)


def part_graph(s):
    pos = O.q8_positions(1.05, 2.25, GC)
    g = O.q8_graph(pos, S.q8_mul)
    kf = Tex(r"K=\Big(k_0+2\sum_s k_s\Big)I-\sum_{s=\pm i,\pm j,\pm k}k_sR(s)", font_size=30).move_to([3.0, 2.2, 0])
    rl = VGroup(Tex(r"(L(g)x)_h=x_{g^{-1}h}", font_size=30), Tex(r"(R(s)x)_h=x_{hs}", font_size=30)).arrange(DOWN, buff=0.25)
    rl.move_to([3.0, 1.0, 0])
    lr = Tex(r"L(g)R(s)=R(s)L(g)\ \Rightarrow\ [L(g),K]=0", font_size=30).set_color(YELLOW).move_to([3.0, -0.1, 0])
    par = Tex(rf"k_0={K0:g},\ k_i={KI:g},\ k_j={KJ:g},\ k_k={KK:g}", font_size=28).set_color(GREY_A).move_to([3.0, -0.9, 0])
    assert_in_frame(g, kf, rl, lr, par)
    s.say("8 個擺放在 8 個元素上：", "$h$", " 和 ", "$hs$", " 用彈簧連（藍 ", "$\\pm i$", "、綠 ", "$\\pm j$", "、橘 ", "$\\pm k$", "）")
    s.play(FadeIn(g[3]), FadeIn(g[4]), run_time=0.8)
    s.play(ShowCreation(g[0]), run_time=0.8)
    s.play(ShowCreation(g[1]), ShowCreation(g[2]), run_time=1.0)
    s.play(FadeIn(kf), run_time=0.8)
    s.say("彈簧是右乘 ", "$R(s)$", "；對稱是左乘 ", "$L(g)$", "：左右乘法互相交換")
    s.play(FadeIn(rl), run_time=0.8)
    s.play(FadeIn(lr), FadeIn(par), run_time=0.8)
    s.wait(2.5)
    s.play(FadeOut(VGroup(kf, rl, lr, par)), run_time=0.5)
    return pos, g


def part_spectrum(s):
    rows = [["", "1", "-1", "\\pm i", "\\pm j", "\\pm k"],
            ["A_1", "1", "1", "1", "1", "1"], ["A_2", "1", "1", "1", "-1", "-1"],
            ["A_3", "1", "1", "-1", "1", "-1"], ["A_4", "1", "1", "-1", "-1", "1"],
            ["E", "2", "-2", "0", "0", "0"], ["\\chi_L", "8", "0", "0", "0", "0"]]
    tab = tex_table(rows, [0.8, 0.6, 0.7, 0.8, 0.8, 0.8], row_h=0.48, font_size=26).move_to([2.6, 1.3, 0])
    dec = Tex(r"8=A_1+A_2+A_3+A_4+2E", font_size=32).set_color(YELLOW).move_to([2.6, -0.8, 0])
    assert_in_frame(tab, dec)
    s.say("正則表示：每個不可約表示出現「維度」那麼多次，", "$E$", " 出現兩次")
    s.play(FadeIn(tab), run_time=1.0)
    s.play(Write(dec), run_time=1.0)
    s.wait(2.0)
    s.play(FadeOut(VGroup(tab, dec)), run_time=0.5)
    lev = S.q8_levels(K0, KI, KJ, KK)
    ld = O.level_diagram([(lev["A1"], r"A_1", 1), (lev["A4"], r"A_4", 1), (lev["E"], r"E", 4), (lev["A3"], r"A_3", 1),
                          (lev["A2"], r"A_2", 1)], x=2.0, y0=-2.7, yscale=1.35, width=1.4)
    vals = VGroup(*[Tex(rf"\omega^2={v:g}", font_size=24).set_color(GREY_A).next_to([1.3, -2.7 + 1.35 * v, 0], LEFT, buff=0.1)
                    for v in (lev["A1"], lev["A4"], lev["E"], lev["A3"], lev["A2"])])
    assert_in_frame(ld, vals)
    s.say("頻率：四個一維表示各一個，", "$E$", " 是四重簡併（", "$2\\times2$", "）")
    s.play(LaggedStartMap(FadeIn, ld, lag_ratio=0.2), FadeIn(vals), run_time=1.5)
    s.wait(2.5)
    return VGroup(ld, vals)


def part_parity(s, pos):
    v = S.q8_irrep_vector("A2")
    marks = VGroup(*[Dot(pos[h], radius=0.24).set_fill(YELLOW if x > 0 else BLUE_C, 0.55).set_stroke(width=0)
                     for h, x in zip(S.Q8_NAMES, v)])
    s.say("第一層標籤：中心元素 ", "$-1$", "（類和）。一維表示是偶的：", "$x_{-h}=x_h$", "（圖：", "$A_2$", "）")
    s.play(FadeIn(marks), run_time=1.0)
    s.wait(2.5)
    s.say("$E$", " 是奇的：", "$x_{-h}=-x_h$", "。奇向量正好 4 維＝兩份 ", "$E$", wait=2.5)
    s.play(FadeOut(marks), run_time=0.5)


def part_labels(s, pos, levels):
    s.play(FadeOut(levels), run_time=0.5)
    basis = S.q8_E_basis()
    pts = [pos[h] for h in S.Q8_NAMES]
    ph = {n: O.phasors(list(v), pts, 0.55, YELLOW, zero_dot=False) for n, v, _, _ in basis}

    def lab(c):
        return {1j: "i", -1j: "-i"}[c]

    rows = [["", "m=L(i)", "n=R(i)"]] + [[rf"v_{n[1]}", lab(m), lab(nn)] for n, _, m, nn in basis]
    tab = tex_table(rows, [0.8, 1.6, 1.6], row_h=0.55, font_size=30).move_to([2.8, 1.5, 0])
    assert_in_frame(tab, *ph.values())
    s.say("$E$", " 裡：用子群 ", "$\\{\\pm1,\\pm i\\}$", " 的 ", "$L(i)=\\pm i$", " 標 ", "$m$", "（箭頭是相位）")
    s.play(LaggedStartMap(GrowArrow, ph["v1"], lag_ratio=0.1), run_time=1.2)
    s.play(FadeIn(tab), run_time=0.8)
    s.wait(1.5)
    s.say("$m=i$", " 仍有兩個向量（兩份 ", "$E$", "）：再用右乘 ", "$R(i)$", " 標「哪一份」", "$n$", wait=2.5)
    s.play(ReplacementTransform(ph["v1"], ph["v2"]), run_time=1.2)
    s.wait(1.0)
    s.say("$L(j)$", " 把 ", "$m$", " 翻號（", "$jij^{-1}=-i$", "）：", "$v_3=L(j)v_1$", " 搬到外圈")
    s.play(ReplacementTransform(ph["v2"], ph["v3"]), run_time=1.5)
    s.wait(1.5)
    s.play(ReplacementTransform(ph["v3"], ph["v4"]), run_time=1.2)
    s.say("四種 ", "$(m,n)$", " 都出現：", "$|E;m,n\\rangle$", " 是完整的標籤（左管 ", "$m$", "、右管 ", "$n$", "）", wait=3.0)
    s.play(FadeOut(ph["v4"]), FadeOut(tab), run_time=0.6)


def part_quaternionic(s):
    l1 = Tex(r"\rho(j)^2=-I\quad\Rightarrow\quad \tfrac18\sum_g\chi_E(g^2)=-1", font_size=34)
    l2 = Tex(r"K=\sum_g c_gR(g),\ c_g=c_{g^{-1}},\ \ g^{-1}=-g\ (g=\pm i,\pm j,\pm k)", font_size=30)
    l3 = Tex(r"K\big|_E=(c_1-c_{-1})\,I_{4\times4}", font_size=36).set_color(YELLOW)
    grp = VGroup(l1, l2, l3).arrange(DOWN, buff=0.45).move_to([2.6, 0.7, 0])
    assert_in_frame(grp)
    s.say("和 ", "$D_3$", " 不同：", "$\\rho(j)^2=-I$", "，", "$E$", " 不能寫成實矩陣（四元數型）")
    s.play(Write(l1), run_time=1.2)
    s.wait(1.5)
    s.say("實對稱的 ", "$K$", " 在 ", "$E$", " 上只能是常數：連「哪一份」", "$n$", " 也分不開")
    s.play(FadeIn(l2), run_time=1.0)
    s.play(Write(l3), run_time=1.0)
    s.say("所以 ", "$E$", " 一定四重簡併——時間反演造成的倍增（Kramers 型）", wait=3.0)
    s.play(FadeOut(grp), run_time=0.5)


class S03Q8(ChuScene):
    def construct(self):
        self.show_header("S03　四元群 Q8：E 出現兩次")
        check_math()
        part_group(self)
        pos, graph = part_graph(self)
        levels = part_spectrum(self)
        part_parity(self, pos)
        part_labels(self, pos, levels)
        part_quaternionic(self)
        self.say("非阿貝爾的標籤＝類和（哪個表示）＋子群（", "$m$", "）＋右作用（哪一份 ", "$n$", "）")
        self.wait(1.0)
