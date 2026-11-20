# D 题 · 宽带接入的最后一公里

Hallowell County 宽带资金分配问题的英文 ICM 论文、可复现分析、图表和交付工具都在本仓库。论文按 2024/2025 ICM-D 获奖论文的排版规范重做：正文 24 页（上限 25），AI 使用报告 2 页附在正文之后、不计入页数。

## 从哪里开始

| 想做什么 | 打开这里 |
|---|---|
| 阅读论文 | [英文审阅 PDF](output/pdf/Problem-D-review.pdf)（匿名版：24 页正文 + 2 页 AI 报告；队号显示占位符）。校赛提交版含封面与真实队号，只保存在被 Git 忽略的 `private/`。 |
| 修改论文 | [paper/main.typ](paper/main.typ) 是 Typst 主文件。[摘要页](paper/summary.typ)、[分节源文件](paper/sec_*.typ)、[参考文献](paper/references.typ)、[AI 报告](paper/ai.typ)（由 [ai_main.typ](paper/ai_main.typ) 单独编译，无页眉页码）。 |
| 修改模型或参数 | [Task 1](analysis/task1.py)、[Task 2](analysis/task2.py)、[Task 3](analysis/task3.py)。[参数与来源表](sources/) 可追溯各项设定。 |
| 查图表和验收证据 | [结果目录](results/) 包含图表、部署方案和逐镇结果。[逐项验收表](evidence/acceptance.csv) 与 [题面复核](evidence/final_prompt_check.md) 记录检查。 |

## 论文结构（与获奖论文对齐）

1. Introduction（含 1.1 Executive Summary 与总体流程图）
2. Assumptions and Justifications（14 条假设，含来源与区间）
3. Notations and Data
4. Task 1: The northern coverage discrepancy
5. Task 2(a): Deployment optimization
6. Task 2(b): Sensitivity analysis
7. Task 3: Choosing a procurement mechanism
8. Share Your Insights
9. Model Evaluation
10. Conclusions and Recommendations
11. Memorandum
12. References

AI 使用报告另编在正文之后，不计入 25 页。全文共 9 图 9 表，公式编号 (1)–(9)，页眉为 `Team # <队号> ... Page X of Y`，A4 纸、Times New Roman 12 pt。

## 重新生成与提交

前置：Python 3.12 及以上（本仓库用 3.13 验证）。

```powershell
py -3.13 -m venv .venv
$py = '.\.venv\Scripts\python.exe'
& $py -m pip install -r requirements.txt
$data = (Resolve-Path '..\Problem\2026_CQU_ICM_Problem_D_DATA').Path
& $py analysis/reproduce.py --data $data
```

`reproduce.py` 重算三组任务和独立复核、重建全部图表，并生成匿名审阅 PDF。

### 校赛提交版（含封面与真实队号）

1. 用 Word 打开 `..\校赛封面.docx`，补填论文题目（例如 "The Last Mile of Broadband"），导出为 `private/cover.pdf`（A4，一页）。
2. 把本队队号和需要匿名的个人信息写入 Git 忽略的 `private/identifiers.txt`（每行一个姓名、学号或电话），供构建脚本做匿名检查。
3. 构建并自动校验：

```powershell
& $py analysis/build_submission.py --team <队号> --out "private/ICM_D<队号><成员姓名>.pdf"
```

构建脚本会校验：封面 1 页、正文 ≤25 页、每页页眉与页码、Summary Sheet 首屏、AI 报告位于正文后且不计页数、无姓名/校名/学号/本地路径、全部 A4、图表与公式连续编号、PDF 小于 25 MB。

### 匿名版（COMAP 版式检查用）

```powershell
& $py analysis/build_submission.py --team <队号> --cover "" --out private/ICM_anonymous.pdf
```

## 从原始附件复现

附件目录需含 `blocks.csv`、`blocksV2.csv`、`road_segments.csv`、`road_segmentsV2.csv`。四个 CSV 的 SHA-256、键唯一性与字段范围见 [原始输入审计](results/task1_data_audit.json)；逐街块导出见 [results/task1_blocks.csv](results/task1_blocks.csv)（覆盖图中的网格图由它生成）。参数来源见 `sources/task1_parameters.csv`、`sources/task2_parameters.csv`、`sources/task3_parameters.csv`。

## 文件入口

| 任务 | 计算 | 结果及证据 |
|---|---|---|
| Task 1 口径、北部覆盖、质疑 | [task1.py](analysis/task1.py) | `results/task1_*`，[参数和来源](sources/task1_parameters.csv)，[独立复核](evidence/task1_review.md) |
| Task 2 资格、混合部署、敏感性 | [task2.py](analysis/task2.py) | `results/task2_*`，[参数和来源](sources/task2_parameters.csv)，[独立复核](evidence/task2_independent_review.txt) |
| Task 3 机制、财务、证据覆盖、公平反事实 | [task3.py](analysis/task3.py) | `results/task3_*`，[参数和来源](sources/task3_parameters.csv)，[独立重建](evidence/task3_independent_review.md) |
| 论文、图表、构建 | [paper_data.py](analysis/paper_data.py)、[build_paper.py](analysis/build_paper.py)、[build_submission.py](analysis/build_submission.py) | `results/fig_*.svg`、`results/paper_data.json`、[验收记录](evidence/acceptance.csv) |

## Git 与提交

- 提交版 PDF 与封面放在 `private/`，该目录已被 Git 忽略，不要提交到仓库。
- 队友从 `main` 新建工作分支，提交后向 `main` 开 PR；在 PR 中写明修改了哪个模型或章节，以及重跑后哪些结果变化。
- 校赛提交版 PDF 含有队员姓名（学校封面要求）；COMAP 正式提交时使用匿名版，或在正式队号确定后用 `build_submission.py --cover ""` 重新生成。
