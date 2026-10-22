# symosc 交接說明（權威說明）

整理日期：2026-10-23。**路徑的寫法：** 本文件裡沒有寫磁碟機的相對路徑，一律相對於 `C:\mypython\manim\projects\symosc`。

## 1. 一句話

使用者問「D3 群對耦合振盪子的解有什麼用、破缺到 C3 會怎樣、非阿貝爾群怎麼標基底、給個 Q8 例子」，
這個小專案把那三段解答做成 ManimGL 動畫（繁中字幕）：S01 D3、S02 破缺到 C3／C2、S03 四元群 Q8，加連續播放 `SymOscDemo`。

## 2. 現況

| 項目 | 狀態 |
|---|---|
| 數學 | `codes/utils/symosc.py`（numpy；`python utils/symosc.py` 自我測試通過） |
| 畫圖 | `codes/utils/osc_draw.py` |
| 動畫 | S01 1:28、S02 1:12、S03 1:04、`SymOscDemo` 3:46，1080p 在 `codes/renders/`（不進 git） |
| combkit | 1.32.0：`combkit.symosc`、`combkit.draw.osc_draw`、`examples/ex34_symmetric_oscillators.py`、`tools/sync_from_symosc.py`；`projects/combkit_v1.32.0.zip`（相對於 `C:\mypython\manim`） |
| git | 本資料夾是獨立的 repo（master，無遠端）；`.gitattributes` 是 `* -text` |

## 3. 參數與畫面上的數字（全部在 `check_math()` 與 `symosc.check()` 裡 assert）

- S01：$k_0=1$、$k=0.5$、$m=1$；$K$ 對角 2、非對角 −0.5；$\chi_{\rm perm}=(3,0,1)$ ⇒ $A_1\oplus E$；類和 $(c_2,c_3)$：$A_1$ (2,3)、$A_2$ (2,−3)、$E$ (−1,0)；
  $\omega_A^2=1$、$\omega_E^2=2.5$；拍的週期 $2\pi/(\omega_E-\omega_A)\approx10.8$；擺 1 最低振幅 1/3（能量 1/9）。
- S02：$a=2$、$b=-0.5$、$\varphi=0.2$：$E_0=1.0199$、$E_{-1}=2.3180$、$E_{+1}=2.6621$、裂距 $\sqrt3\sin\varphi=0.3441$；
  陀螺 $g=0.2$：$\omega_{+1}=1.4174$、$\omega_{-1}=1.7638$、$\Delta\omega=\sqrt3g=0.3464$、每 $4\pi/(3\Delta\omega)\approx12.1$ 移一格；$C_2$：$\delta=0.25$ ⇒ 1、2.5（偶）、3.0（奇）。
- S03：$k_0=1$、$k_i=0.05$、$k_j=0.25$、$k_k=0.5$：$\omega^2$ = $A_1$ 1、$A_4$ 2.2、$E$ 2.6（×4）、$A_3$ 3.2、$A_2$ 4.0；
  $E$ 的基底標籤 $(L(i),R(i))$：$v_1$ $(i,-i)$、$v_2$ $(-i,i)$、$v_3=L(j)v_1$ $(-i,-i)$、$v_4=L(j)v_2$ $(i,i)$；Frobenius–Schur 指標 −1。

## 4. 注意事項

1. Q8 的元素順序固定為 `['1','i','j','k','-1','-i','-j','-k']`；左乘 $(L(g)x)_h=x_{g^{-1}h}$、右乘 $(R(g)x)_h=x_{hg}$，彈簧用右乘，所以 $K$ 和所有 $L(g)$ 交換。
2. Axes 的 x 軸畫在 $y=0$：y 範圍不含 0 時軸會跑到圖外（S02 曾發生），y_range 從 0 起。
3. Tex 裡 `\cos\!\big(` 這種寫法在這台的 LaTeX 會失敗（Argument of \bBigg@ has an extra }），用一般括號。
4. 含反斜線的 Python 一律用 Write 工具或 Python 檔改，不要用 Git Bash heredoc。

## 5. 進度紀錄

- 2026-10-23：建立專案；`symosc`／`osc_draw`；S01–S03（每幕最後一次嚴格模式 render_check 都是最終版）、`SymOscDemo`；combkit 1.32.0。
