"""
S02 —— 破缺：D3 ⊃ C3（繞圈波）與 D3 ⊃ C2（駐波）兩種標示；帶相位的耦合、陀螺項、換一根彈簧
執行（在 codes/ 內）：manimgl scenes/s02_breaking.py S02Breaking
"""
import cmath
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, r"C:\mypython\manim\projects\combkit")

from manimlib import *

from combkit.draw.fulton_draw import assert_in_frame
from combkit.draw.scene_base import ChuScene
from combkit.draw.styles import zh
from utils import osc_draw as O
from utils import symosc as S

A, B = 2.0, -0.5            # K_d3(1, 0.5) = a I + b(P + Pᵀ)
PHI = 0.2
G = 0.2
DELTA = 0.25


def check_math():
    assert np.allclose(S.K_d3(1.0, 0.5), A * np.eye(3) + B * (S.P_CYC + S.P_CYC.T))
    w = S.OMEGA
    assert np.allclose(S.v_m(1) * math.sqrt(3), [1, w, w * w]) and np.allclose(S.v_m(-1) * math.sqrt(3), [1, w * w, w])
    lev = S.flux_levels(A, B, PHI)
    assert [round(lev[m], 4) for m in (0, -1, 1)] == [1.0199, 2.318, 2.6621]
    assert round(lev[1] - lev[-1], 4) == round(math.sqrt(3) * math.sin(PHI), 4) == 0.3441
    lev0 = S.flux_levels(A, B, 0.0)
    assert [round(lev0[m], 6) for m in (0, 1, -1)] == [1.0, 2.5, 2.5]
    gf = S.gyro_freqs(1.0, 0.5, G)
    assert [round(gf[m], 4) for m in (1, -1)] == [1.4174, 1.7638] and round(gf[-1] - gf[1], 4) == round(math.sqrt(3) * G, 4) == 0.3464
    d = gf[-1] - gf[1]
    assert round(4 * math.pi / (3 * d), 1) == 12.1
    assert S.c2_levels(1.0, 0.5, DELTA) == {"A1": 1.0, "sym": 2.5, "anti": 3.0}
    M = 2 * np.eye(3) + 0.3 * S.P_CYC + 0.7 * S.P_CYC @ S.P_CYC
    assert not np.allclose(M, M.T)


def tri_small(center, radius=0.95):
    return O.osc_triangle(radius, center, labels=False)


def part_bases(s):
    s.say("問：", "$E$", " 裡的兩個向量，該選哪一組？")
    cs = [np.array([-4.8, 0.9, 0]), np.array([-1.8, 0.9, 0]), np.array([1.8, 0.9, 0]), np.array([4.8, 0.9, 0])]
    tris = VGroup(*[tri_small(c) for c in cs])
    w = S.OMEGA
    ph1 = O.phasors([1, w, w * w], O.tri_points(0.95, cs[0]), 0.42, YELLOW)
    ph2 = O.phasors([1, w * w, w], O.tri_points(0.95, cs[1]), 0.42, YELLOW)
    b1 = O.radial_bars([1, -0.5, -0.5], 0.95, cs[2], 0.5)
    b2 = O.radial_bars([0, 0.87, -0.87], 0.95, cs[3], 0.5)
    t1 = Tex(r"m=+1:\ (1,\omega,\omega^2)", font_size=28).next_to(tris[0], DOWN, buff=0.45)
    t2 = Tex(r"m=-1:\ (1,\omega^2,\omega)", font_size=28).next_to(tris[1], DOWN, buff=0.45)
    t3 = Tex(r"\sigma_1=+1:\ (2,-1,-1)", font_size=28).next_to(tris[2], DOWN, buff=0.45)
    t4 = Tex(r"\sigma_1=-1:\ (0,1,-1)", font_size=28).next_to(tris[3], DOWN, buff=0.45)
    h1 = VGroup(zh("D3 ⊃ C3：", font_size=28), Tex(r"D(r)=\omega^m", font_size=30)).arrange(RIGHT, buff=0.1)
    h1.move_to([-3.3, 2.75, 0]).set_color(BLUE_B)
    h2 = VGroup(zh("D3 ⊃ C2：", font_size=28), Tex(r"D(\sigma_1)=\pm1", font_size=30)).arrange(RIGHT, buff=0.1)
    h2.move_to([3.3, 2.75, 0]).set_color(GREEN_B)
    assert_in_frame(tris, ph1, ph2, b1, b2, t1, t2, t3, t4, h1, h2)
    s.play(FadeIn(tris), FadeIn(h1), FadeIn(h2), run_time=1.0)
    s.say("左：用 ", "$C_3$", " 的 ", "$\\omega^m$", " 標（複數的相量，箭頭是每個擺的相位）")
    s.play(LaggedStartMap(GrowArrow, ph1, lag_ratio=0.3), FadeIn(t1), run_time=1.2)
    s.play(LaggedStartMap(GrowArrow, ph2, lag_ratio=0.3), FadeIn(t2), run_time=1.2)
    s.wait(1.5)
    s.say("右：用鏡射 ", "$\\sigma_1$", "（交換 2、3）的 ", "$\\pm1$", " 標（實數的駐波）")
    s.play(FadeIn(b1), FadeIn(t3), run_time=0.8)
    s.play(FadeIn(b2), FadeIn(t4), run_time=0.8)
    s.wait(1.5)
    s.say("$\\sigma r\\sigma=r^2$", "：鏡射把 ", "$m=+1$", " 送到 ", "$m=-1$", "——這就是 ", "$E$", " 簡併的來源", wait=2.5)
    s.say("$D_3$", " 完整時兩組都是本徵向量；破缺後剩下哪個子群，就決定哪一組活下來", wait=2.5)
    s.play(FadeOut(VGroup(tris, ph1, ph2, b1, b2, t1, t2, t3, t4, h1, h2)), run_time=0.6)


def part_real_c3(s):
    s.say("只用一般的彈簧（", "$K$", " 是實對稱）能做出只有 ", "$C_3$", " 的系統嗎？")
    l1 = Tex(r"[K,P]=0\ \Rightarrow\ K=aI+bP+cP^2", font_size=38)
    l2 = Tex(r"K^T=aI+cP+bP^2=K\ \Rightarrow\ b=c", font_size=38)
    l3 = Tex(r"\Rightarrow\ K=aI+b(P+P^{-1})\ \text{also commutes with }\sigma", font_size=34).set_color(YELLOW)
    grp = VGroup(l1, l2, l3).arrange(DOWN, buff=0.45).move_to([0, 0.6, 0])
    assert_in_frame(grp)
    s.play(Write(l1), run_time=1.0)
    s.play(Write(l2), run_time=1.0)
    s.play(FadeIn(l3), run_time=0.8)
    s.say("不能：實對稱又 ", "$C_3$", " 不變，自動也 ", "$D_3$", " 不變（時間反演把 ", "$m$", " 和 ", "$-m$", " 綁在一起）", wait=3.0)
    s.say("要真的破缺，得有分得出順、逆時針的東西：磁通、旋轉（科氏力）、陀螺耦合", wait=3.0)
    s.play(FadeOut(grp), run_time=0.6)


def part_flux(s):
    s.say("帶相位的耦合 ", "$b\\,e^{i\\varphi}$", "（三角形中間穿過磁通）")
    H = Tex(r"H=\begin{pmatrix}a&be^{i\varphi}&be^{-i\varphi}\\be^{-i\varphi}&a&be^{i\varphi}\\"
            r"be^{i\varphi}&be^{-i\varphi}&a\end{pmatrix}", font_size=32).move_to([-3.7, 1.4, 0])
    ev = Tex(r"E_m=a+2b\cos(\varphi+2\pi m/3)", font_size=32).move_to([-3.7, -0.3, 0])
    par = Tex(r"a=2,\ b=-0.5", font_size=28).set_color(GREY_A).next_to(ev, DOWN, buff=0.3)
    ax = Axes(x_range=[0, 0.8, 0.2], y_range=[0, 3.0, 0.5], width=4.8, height=3.8).move_to([2.6, 0.5, 0])
    xl = Tex(r"\varphi", font_size=30).next_to(ax.x_axis, RIGHT, buff=0.1)
    cols = {0: GREY_A, 1: YELLOW, -1: BLUE_C}
    curves = VGroup(*[ax.get_graph(lambda p, m=m: S.flux_levels(A, B, p)[m], x_range=[0, 0.8]).set_stroke(cols[m], 3)
                      for m in (0, 1, -1)])
    labs = VGroup(*[Tex(f"m={'+' if m > 0 else ''}{m}", font_size=26).set_color(cols[m])
                    .next_to(ax.c2p(0.8, S.flux_levels(A, B, 0.8)[m]), RIGHT, buff=0.1) for m in (0, 1, -1)])
    yt = VGroup(*[Tex(f"{v:g}", font_size=22).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (1, 1.5, 2, 2.5, 3)])
    assert_in_frame(H, ev, par, ax, xl, curves, labs, yt)
    s.play(FadeIn(H), run_time=1.0)
    s.play(Write(ev), FadeIn(par), run_time=1.0)
    s.say("本徵向量仍是 ", "$(1,\\omega^m,\\omega^{2m})$", "：", "$m$", " 是好量子數")
    s.play(ShowCreation(ax), FadeIn(xl), FadeIn(yt), run_time=0.8)
    s.play(*[ShowCreation(c) for c in curves], FadeIn(labs), run_time=2.0)
    lev = S.flux_levels(A, B, PHI)
    mark = DashedLine(ax.c2p(PHI, 0), ax.c2p(PHI, 3.0)).set_stroke(GREY_B, 1.5)
    num = Tex(rf"\varphi={PHI}:\ E_{{+1}}-E_{{-1}}={lev[1] - lev[-1]:.4f}=\sqrt3\sin\varphi", font_size=28)
    num.move_to([2.9, -1.95, 0])
    assert_in_frame(num)
    s.play(ShowCreation(mark), FadeIn(num), run_time=0.8)
    s.say("$\\varphi=0$", " 時 ", "$m=\\pm1$", " 簡併；", "$\\varphi\\ne0$", " 就分開，裂距 ", "$2\\sqrt3|b|\\sin\\varphi$", wait=3.0)
    s.play(FadeOut(VGroup(H, ev, par, ax, xl, curves, labs, yt, mark, num)), run_time=0.6)


def part_precession(s):
    gf = S.gyro_freqs(1.0, 0.5, G)
    d = gf[-1] - gf[1]
    s.say("力學版：陀螺項 ", "$G=g(P-P^T)$", "，", "$m\\ddot x+G\\dot x+Kx=0$")
    info = VGroup(Tex(rf"g={G}:\ \omega_{{+1}}={gf[1]:.4f},\ \omega_{{-1}}={gf[-1]:.4f}", font_size=30),
                  Tex(rf"\Delta\omega=\sqrt3\,g={d:.4f}", font_size=32).set_color(YELLOW)).arrange(DOWN, buff=0.3)
    info.move_to([3.0, 1.6, 0])
    cen = np.array([-3.2, 0.2, 0])
    tri = O.osc_triangle(1.5, cen)
    t = ValueTracker(0.0)
    bars = always_redraw(lambda: O.radial_bars(S.precession(t.get_value(), d), 1.5, cen, 0.33, width=10))
    note = Tex(r"\text{pattern}\ \propto\cos(2\pi j/3+\Delta\omega\,t/2)", font_size=28).move_to([3.0, 0.1, 0])
    hop = Tex(rf"4\pi/(3\Delta\omega)\approx{4 * math.pi / (3 * d):.1f}", font_size=30).move_to([3.0, -0.8, 0])
    assert_in_frame(info, tri, note, hop)
    s.play(FadeIn(info), FadeIn(tri), run_time=1.0)
    s.say("只推一個擺＝兩個繞圈波相加；兩者頻率不同，駐波的圖樣就會轉")
    s.add(bars)
    s.play(FadeIn(note), run_time=0.6)
    s.play(t.animate.set_value(4 * math.pi / d), run_time=12.0, rate_func=linear)
    s.play(FadeIn(hop), run_time=0.6)
    s.say("像傅科擺的擺動面：每 ", "$4\\pi/(3\\Delta\\omega)\\approx12.1$", " 移到下一個擺", wait=3.0)
    s.remove(bars)
    s.play(FadeOut(VGroup(info, tri, note, hop)), run_time=0.6)


def part_levels(s):
    s.say("對照：換掉一根彈簧（", "$k_{23}=k+\\delta$", "），只剩鏡射 ", "$\\sigma_1$", "：", "$D_3\\supset C_2$")
    lev = S.flux_levels(A, B, PHI)
    c2 = S.c2_levels(1.0, 0.5, DELTA)
    y0, ys = -3.4, 1.45
    left = O.level_diagram([(lev[0], rf"m=0:\ {lev[0]:.4f}", 1), (lev[-1], rf"m=-1:\ {lev[-1]:.4f}", 1),
                            (lev[1], rf"m=+1:\ {lev[1]:.4f}", 1)], x=-4.0, y0=y0, yscale=ys, color=BLUE_B,
                           label_side=LEFT)
    mid = O.level_diagram([(1.0, "A_1", 1), (2.5, "E", 2)], x=0.0, y0=y0, yscale=ys, label_side=UP)
    right = O.level_diagram([(c2["A1"], "A_1", 1), (c2["sym"], "(2,-1,-1)", 1), (c2["anti"], "(0,1,-1)", 1)], x=3.6,
                            y0=y0, yscale=ys, color=GREEN_B)
    hl = Tex(rf"C_3:\ \varphi={PHI}", font_size=30).set_color(BLUE_B).move_to([-3.6, 2.55, 0])
    hm = Tex(r"D_3", font_size=30).move_to([0.2, 2.55, 0])
    hr = Tex(rf"C_2:\ \delta={DELTA}", font_size=30).set_color(GREEN_B).move_to([4.0, 2.55, 0])
    links = VGroup()
    for (v1, v2) in ((1.0, lev[0]), (2.5, lev[-1]), (2.5, lev[1])):
        links.add(DashedLine([-0.6, y0 + ys * v1, 0], [-3.4, y0 + ys * v2, 0]).set_stroke(GREY_B, 1.2))
    for (v1, v2) in ((1.0, c2["A1"]), (2.5, c2["sym"]), (2.5, c2["anti"])):
        links.add(DashedLine([0.6, y0 + ys * v1, 0], [3.0, y0 + ys * v2, 0]).set_stroke(GREY_B, 1.2))
    vals = VGroup()
    assert_in_frame(left, mid, right, hl, hm, hr, links, vals)
    s.play(FadeIn(mid), FadeIn(hm), run_time=0.8)
    s.play(ShowCreation(links[:3]), FadeIn(left), FadeIn(hl), FadeIn(vals), run_time=1.2)
    s.say("剩 ", "$C_3$", "：", "$E$", " 分成兩個繞圈波 ", "$m=\\pm1$", wait=2.0)
    s.play(ShowCreation(links[3:]), FadeIn(right), FadeIn(hr), run_time=1.2)
    s.say("剩 ", "$C_2$", "：", "$E$", " 分成兩個駐波（", "$\\sigma_1$", " 的偶 2.5、奇 3.0）", wait=2.5)
    s.wait(1.0)
    return VGroup(left, mid, right, hl, hm, hr, links, vals)


class S02Breaking(ChuScene):
    def construct(self):
        self.show_header("S02　破缺：D3 ⊃ C3 與 D3 ⊃ C2")
        check_math()
        part_bases(self)
        part_real_c3(self)
        part_flux(self)
        part_precession(self)
        lv = part_levels(self)
        self.play(FadeOut(lv), run_time=0.6)
        self.say("子群鏈就是標籤：剩下的子群決定 ", "$E$", " 要拆成繞圈波還是駐波")
        self.wait(1.0)
