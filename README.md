# D 题 · 宽带接入的最后一公里

D 题英文论文、可编辑源文件、模型代码和复核记录都在本仓库。队友从 `main` 获取当前版本，并通过 Pull Request 提交修改。

## 从哪里开始

| 想做什么 | 打开这里 |
|---|---|
| 阅读论文 | [英文审阅 PDF](output/pdf/Problem-D-review.pdf)。正文 16 页，AI 披露 5 页。第 3 页是总体流程图，第 15 页是备忘录。 |
| 修改论文 | [paper/main.typ](paper/main.typ) 是 Typst 主文件。[章节源文件](paper/) 与主文件在同一目录。 |
| 修改模型或参数 | [Task 1 覆盖审计](analysis/task1.py)、[Task 2 部署优化](analysis/task2.py)、[Task 3 机制比较](analysis/task3.py)。[参数与来源表](sources/) 可追溯各项设定。 |
| 查图表和验收证据 | [结果目录](results/) 包含选址、技术、预算和乡镇结果。[逐项验收表](evidence/acceptance.csv) 和 [题面复核](evidence/final_prompt_check.md) 记录独立检查。 |

## 队友如何修改

有仓库写权限的队友可从 `main` 新建工作分支，提交后向 `main` 开 PR。其他队友可以在自己的 Fork 中编辑，再向本仓库的 `main` 分支提交 PR。在 PR 中写明修改了哪个模型或章节，以及重跑后哪些结果发生变化。

论文文字和公式在 `paper/*.typ`，排版入口是 `analysis/build_paper.py`。模型或口径改变时，先更新相应分析脚本和参数来源表，再执行全量复现。核对生成的图表、摘要和备忘录是否随结果同步更新。

## 从原始附件复现

附件由队员从本届校赛发放包取得。将 `--data` 指向含 `blocks.csv`、`blocksV2.csv`、`road_segments.csv`、`road_segmentsV2.csv` 的 `2026_CQU_ICM_Problem_D_DATA` 文件夹。题面 PDF 和 AI 政策来自同一发放包。四个 CSV 的校验值和字段核对见 [原始输入审计](results/task1_data_audit.json)。

在仓库根目录用 PowerShell 运行。下例按附件目录与本仓库同级设置。

```powershell
py -3.12 -m venv .venv
$py = '.\.venv\Scripts\python.exe'
& $py -m pip install -r requirements.txt
$data = (Resolve-Path '..\2026年重庆大学数学建模秋季赛题目\2026_CQU_ICM_Problem_D_DATA').Path
& $py analysis/reproduce.py --data $data
```

复现命令重建三组计算、所有图表和英文审阅 PDF，并运行三个独立核查程序。依赖文件锁定了运行版本。macOS 或 Linux 使用 `.venv/bin/python`。AI 附录保留原语言提示词，Windows 可用 Microsoft YaHei，其他系统可安装 Noto Sans CJK SC。

## 文件入口

| 任务 | 计算 | 结果及证据 |
|---|---|---|
| Task 1 口径、北部覆盖、质疑 | [task1.py](analysis/task1.py) | `results/task1_*`，[参数和来源](sources/task1_parameters.csv)，[独算](evidence/task1_review.md) |
| Task 2 资格、混合部署、敏感性 | [task2.py](analysis/task2.py) | `results/task2_*`，[参数和来源](sources/task2_parameters.csv)，[独立 Pareto 求解](evidence/task2_independent_review.txt) |
| Task 3 机制、财务、证据覆盖、去公平 | [task3.py](analysis/task3.py) | `results/task3_*`，[参数和来源](sources/task3_parameters.csv)，[独立重建和求解](evidence/task3_independent_review.md) |
| 论文、图表 | [paper_data.py](analysis/paper_data.py)、[build_paper.py](analysis/build_paper.py) | `results/fig_*.svg`，`results/paper_data.json`，[验收记录](evidence/acceptance.csv) |

逐项目结果见 `results/task2_projects.csv`、`results/task3_actions.csv` 和 `results/task3_hubs.csv`。求解状态、覆盖和二阶段间隙见 `results/task2_solver.json` 与 `results/task3_summary.csv`。验收表的上传状态记录的是首次本地验收时点，实际合并记录以 GitHub 的 Pull Request 为准。队号、文件命名和 AI 记录报送事项见 [交付核对](evidence/release.md)。

## 填入经校赛确认的队号

审阅版页眉显示 `TEAM NUMBER REQUIRED`。队伍收到正式队号并核对校赛 AI 披露与文件命名要求后，可在本地生成提交用 PDF。将下面的变量值和文件名换成正式通知要求，并检查更新后的 PDF。

```powershell
$team = 'REPLACE-WITH-CONFIRMED-ID'
& $py analysis/build_paper.py --team $team --output "private/$team.pdf"
```

真实队号版和完整内部提示记录留在 Git 忽略的 `private/`，由队伍管理和递交。
