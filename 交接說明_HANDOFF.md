# symosc 交接說明（權威說明）

整理日期：2026-10-23。**路徑的寫法：** 本文件裡沒有寫磁碟機的相對路徑，一律相對於 `C:\mypython\manim\projects\symosc`。

## 1. 一句話

使用者問「D3 群對耦合振盪子的解有什麼用、破缺到 C3 會怎樣、非阿貝爾群怎麼標基底、給個 Q8 例子」，
這個小專案把那三段解答做成 ManimGL 動畫（繁中字幕）：S01 D3、S02 破缺到 C3／C2、S03 四元群 Q8，加連續播放 `SymOscDemo`。

## 2. 現況

| 項目 | 狀態 |
|---|---|
| 數學 | `codes/utils/symosc.py`（numpy；`python utils/symosc.py` 自我測試通過）；根目錄 `pyproject.toml` 把它做成套件 `symosc`（`pip install -e .`、`symosc-check`） |
| 畫圖 | `codes/utils/osc_draw.py` |
| 動畫 | S01 1:28、S02 1:12、S03 1:04、`SymOscDemo` 3:46，1080p 在 `codes/renders/`（不進 git） |
| combkit | 1.32.0：`combkit.symosc`、`combkit.draw.osc_draw`、`examples/ex34_symmetric_oscillators.py`、`tools/sync_from_symosc.py`；`projects/combkit_v1.32.0.zip`（相對於 `C:\mypython\manim`） |
| git | 本資料夾是獨立的 repo（master，無遠端）；`.gitattributes` 是 `* -text` |

## 3. 參數與畫面上的數字（全部在 `check_math()` 與 `symosc.check()` 裡 assert）

- S01：$k_0=1$、$k=0.5$、$m=1$；$K$ 對角 2、非對角 −0.5；$\chi_{\rm perm}=(3,0,1)$ ⇒ $A_1\oplus E$；類和 $(c_2,c_3)$：$A_1$ (2,3)、$A_2$ (2,−3)、$E$ (−1,0)；
  $\omega_A^2=1$、$\omega_E^2=2.5$；拍的週期 $2\pi/(\omega_E-\omega_A)\approx10.8$；擺 1 最低振幅 1/3（能量 1/9）。
- S02：$a=2$、$b=-0.5$、$\varphi=0.2$：$E_0=1.0199$、$E_{-1}=2.3180$、$E_{+1}=2.6621$、裂距 $\sqrt3\sin\varphi=0.3441$；
  陀螺 $g=0.2$：$\omega_{+1}=1.4174$、$\omega_{-1}=1.7638$、$\Delta\omega=\sqrt3g=0.3464$、圖樣 $\cos(2\pi j/3-\Delta\omega t/2)$ 往 1→2→3 轉，每 $4\pi/(3\Delta\omega)\approx12.1$ 移一格；$C_2$：$\delta=0.25$ ⇒ 1、2.5（偶）、3.0（奇）。
- S03：$k_0=1$、$k_i=0.05$、$k_j=0.25$、$k_k=0.5$：$\omega^2$ = $A_1$ 1、$A_4$ 2.2、$E$ 2.6（×4）、$A_3$ 3.2、$A_2$ 4.0；
  $E$ 的基底標籤 $(L(i),R(i))$：$v_1$ $(i,-i)$、$v_2$ $(-i,i)$、$v_3=L(j)v_1$ $(-i,-i)$、$v_4=L(j)v_2$ $(i,i)$；Frobenius–Schur 指標 −1。

## 4. 注意事項

1. Q8 的元素順序固定為 `['1','i','j','k','-1','-i','-j','-k']`；左乘 $(L(g)x)_h=x_{g^{-1}h}$、右乘 $(R(g)x)_h=x_{hg}$，彈簧用右乘，所以 $K$ 和所有 $L(g)$ 交換。
2. Axes 的 x 軸畫在 $y=0$：y 範圍不含 0 時軸會跑到圖外（S02 曾發生），y_range 從 0 起。
3. Tex 裡 `\cos\!\big(` 這種寫法在這台的 LaTeX 會失敗（Argument of \bBigg@ has an extra }），用一般括號。
4. 含反斜線的 Python 一律用 Write 工具或 Python 檔改，不要用 Git Bash heredoc。

## 5. 進度紀錄

- 2026-10-23：建立專案；`symosc`／`osc_draw`；S01–S03（每幕最後一次嚴格模式 render_check 都是最終版）、`SymOscDemo`；combkit 1.32.0。
- 2026-10-26：`precession()` 的方向原本反了（$+\delta t/2$ → $-\delta t/2$，S02 螢幕公式同步改）；`check()` 加 RK4 積分陀螺方程核對進動方向。
  加 `pyproject.toml`（只裝數學模組 `symosc`）。
  重新輸出 S02 與 `SymOscDemo`（1080p）到 `codes/renders/2026-10-26_precession_fix/`；`renders/` 裡的舊影片（舊方向）沒動。
  這次是在另一台電腦上輸出：Python 3.12 venv `%USERPROFILE%\.venvs\mgl312`、combkit 1.35.1、ManimGL fafa083、ffmpeg 9.0.2、MiKTeX。踩到的坑：
  1. 解壓來的 `codes/latex_cache/working.dvi` 是舊機器的；第一次編譯失敗時 ManimGL 會沿用它（`tex_file_writing.py`：returncode≠0 但 dvi 存在就不報錯），
     連 Tex 的尺寸校正（參考字 "0"）都錯，結果存進磁碟快取。輸出前先刪 `working.dvi`，出錯後清快取（`manimlib.utils.cache.clear_cache()`）。
  2. MiKTeX 的使用者字型對照表沒包含 cm-super（`dvisvgm` 報 `failed to create ecrm1000.gf`，`\text{}` 變空白）：執行 `initexmf --mkmaps` 修好。
  3. 這台的 `Text` 校正比原機器小 1.3625 倍；為了和舊影片一致，輸出時加 `--config_file`，內容是 `text: font_size_for_unit_height: 105.7`（不放進 `custom_config.yml`，免得原機器變大）。
  4. 設 `PYTHONUTF8=1`，不然 latex 輸出用 cp950 解碼會丟 `UnicodeDecodeError`。
  已同步到 combkit 並升到 1.35.2（`python tools/sync_from_symosc.py <symosc 的 codes/utils>`；位置是這台的 `combkit_v1.35.1_with_manimgl\combkit_with_manim\combkit`）。
  **尚未做：** `make_zip.py` 沒跑：它要求自我測試全過，而這台的 scipy 1.11 讓 `walk_eps` 失敗（`special.factorial2(-1, exact=True)` 回傳 0，舊版回傳 1；要在 walk017 的正本修）。
