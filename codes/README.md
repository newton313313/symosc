# symosc：對稱群與耦合振盪子（ManimGL 動畫）

用耦合振盪子把三個群論例子畫出來：**D3**（三個擺的約化、模式、拍）、**破缺到 C3／C2**（兩種標示、能階分裂、進動）、
**四元群 Q8**（8 個擺、同一個二維表示出現兩次、左右標籤、四元數型的四重簡併）。

**路徑的寫法：** 本檔裡沒有寫磁碟機的相對路徑，一律相對於本資料夾 `C:\mypython\manim\projects\symosc\codes`。
權威說明是上一層的 `交接說明_HANDOFF.md`。

## 1. 環境

- ManimGL **1.7.2**（3Blue1Brown 版，`manimgl` 指令），**不是** Manim Community；不要升級或重裝。
- combkit **1.32.0 以上**（`C:\mypython\manim\projects\combkit`；場景用 `sys.path.insert` 載入）：`ChuScene`、`tex_table`、`assert_in_frame`。
- numpy（數學模組 `utils/symosc.py`）。
- 只要數學、不要 manim：在上一層（專案根目錄）執行 `pip install -e .`（`pyproject.toml` 只裝 `symosc` 這個模組，相依只有 numpy），
  之後任何地方都能 `import symosc`，`symosc-check` 或 `python -m symosc` 跑自我測試。

## 2. 指令（都在本資料夾執行）

| 做什麼 | 指令 |
|---|---|
| 預覽一幕 | `manimgl scenes/s01_d3_modes.py S01D3Modes` |
| 輸出全部 1080p | `python render_all.py`（加 `--demo` 另外輸出連續播放；`-l` 480p；已存在的影片預設**跳過**，重做加 `--force`） |
| 連續播放 | `manimgl main.py SymOscDemo -w --hd` |
| 數學自我測試 | `python utils/symosc.py` |
| 試渲染＋總覽圖 | 在 `C:\mypython\manim\projects\combkit` 執行 `python tools/render_check.py C:/mypython/manim/projects/symosc/codes/scenes/<檔名> <類別> --config C:/mypython/manim/projects/symosc/codes/custom_config.yml --tile 480` |

## 3. 場景（`scenes/`）

| 代號 | 檔名 | 類別 | 內容 | 長度 |
|---|---|---|---|---|
| S01 | `s01_d3_modes.py` | `S01D3Modes` | 三個擺的 $K$、D3 的 6 個操作、置換表示約化成 $A_1\oplus E$、類和當標籤、$A_1$ 與 $E$ 模式（$\omega^2=1$、$2.5$）、只推擺 1 的拍（週期 10.8，擺 1 最低 1/3） | 1:28 |
| S02 | `s02_breaking.py` | `S02Breaking` | $D_3\supset C_3$（相量 $(1,\omega,\omega^2)$）與 $D_3\supset C_2$（駐波）兩種標示；實對稱＋$C_3$ ⇒ $D_3$；帶相位耦合的分裂 $\sqrt3\sin\varphi$；陀螺項 $\Delta\omega=\sqrt3g$ 與駐波進動；三欄能階圖（$C_3$ ← $D_3$ → $C_2$） | 1:12 |
| S03 | `s03_q8.py` | `S03Q8` | Q8 的乘法與 $\rho(i),\rho(j)$；8 個擺的 Cayley 圖（彈簧＝右乘、對稱＝左乘）；$8=A_1+A_2+A_3+A_4+2E$；能階；中心 $-1$ 分偶奇；$E$ 的基底 $v_1..v_4$ 與標籤 $(m,n)=(L(i),R(i))$；四元數型 ⇒ 四重簡併 | 1:04 |

連續播放：`main.py` 的 `SymOscDemo`（S01–S03），長度 3:46。

## 4. 程式結構

```text
codes/
├── custom_config.yml     ManimGL 設定（只能寫英文）
├── main.py               S01–S03 的同名子類別＋SymOscDemo
├── render_all.py         批次輸出（已存在的影片預設跳過）
├── scenes/               s01_d3_modes.py、s02_breaking.py、s03_q8.py（輔助函式都是模組層級；每幕 check_math() assert 畫面上的數字）
├── utils/
│   ├── symosc.py         數學（numpy）：D3、破缺、Q8；check() 用兩種以上的算法核對（積分＝公式、解析＝一階化本徵值、左右乘法互換）
│   └── osc_draw.py       畫圖元件：三角形與彈簧、會動的質點、徑向長條、相量、能階圖、Q8 的 Cayley 圖
└── renders/              影片（不進 git）
```

`symosc.py`、`osc_draw.py` 的複本在 combkit（`combkit.symosc`、`combkit.draw.osc_draw`，範例 `examples/ex34_symmetric_oscillators.py`），
用 combkit 的 `tools/sync_from_symosc.py` 同步；改這裡的正本，再到 combkit 執行同步、升版、打包。
