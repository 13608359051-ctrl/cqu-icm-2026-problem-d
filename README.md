# D 题 · 宽带接入的最后一公里

在自己的 Fork 中上传或编辑成果，再向本仓库的 `main` 分支提交 Pull Request。

目前交付在本地 `team/problem-d-delivery` 分支。等本届校赛确认公开时点、可公开内容和赛题附件授权后，再按上面的协作方式推送与开 PR。

## 论文和复现

- 英文审阅 PDF 位于 [output/pdf/Problem-D-review.pdf](output/pdf/Problem-D-review.pdf)。正文 16 页，AI 披露 5 页，总体流程图在第 3 页，备忘录在第 15 页。页眉以 `TEAM NUMBER REQUIRED` 标明队号待填。
- 可编辑论文位于 [paper/main.typ](paper/main.typ)，各章节为同目录的 `.typ` 文件。正文采用 12 磅 Libertinus Serif。AI 披露附上保留原语言的提示词，Windows 使用 Microsoft YaHei 显示原文，在其他系统可安装 Noto Sans CJK SC。
- 附件由队员从本届校赛发放包取得。将 `--data` 指向含 `blocks.csv`、`blocksV2.csv`、`road_segments.csv`、`road_segmentsV2.csv` 的 `2026_CQU_ICM_Problem_D_DATA` 文件夹。四个文件的校验值和字段核对见 [原始输入审计](results/task1_data_audit.json)。题面 PDF 和 AI 政策从同一发放包取得。

在仓库根目录用 PowerShell 运行。下例按附件目录与本仓库同级设置。

```powershell
py -3.12 -m venv .venv
$py = '.\.venv\Scripts\python.exe'
& $py -m pip install -r requirements.txt
$data = (Resolve-Path '..\2026年重庆大学数学建模秋季赛题目\2026_CQU_ICM_Problem_D_DATA').Path
& $py analysis/reproduce.py --data $data
```

同一 Python 3.12 环境在 macOS 或 Linux 中使用 `.venv/bin/python`。复现命令重建三组计算、所有图表、英文审阅 PDF，并运行三个独立核查程序。模型无抽样或随机分组。依赖文件固定了实际运行版本。逐页栅格检查可另用 Poppler。

## 文件入口

| 任务 | 计算 | 结果及证据 |
|---|---|---|
| Task 1 口径、北部覆盖、质疑 | [task1.py](analysis/task1.py) | `results/task1_*`，[参数和来源](sources/task1_parameters.csv)，[独算](evidence/task1_review.md) |
| Task 2 资格、混合部署、敏感性 | [task2.py](analysis/task2.py) | `results/task2_*`，[参数和来源](sources/task2_parameters.csv)，[独立 Pareto 求解](evidence/task2_independent_review.txt) |
| Task 3 机制、财务、证据覆盖、去公平 | [task3.py](analysis/task3.py) | `results/task3_*`，[参数和来源](sources/task3_parameters.csv)，[独立重建和求解](evidence/task3_independent_review.md) |
| 论文、图表 | [paper_data.py](analysis/paper_data.py)、[build_paper.py](analysis/build_paper.py) | `results/fig_*.svg`，`results/paper_data.json`，[验收记录](evidence/acceptance.csv) |

向量级结果见 `task2_projects.csv`、`task3_actions.csv` 和 `task3_hubs.csv`。求解状态、覆盖和二阶段间隙见 `task2_solver.json` 与 `task3_summary.csv`。修改情景可直接运行对应脚本。若修改使结果或排序变化，同时更新论文中的解释、图表、摘要及备忘录，再跑独立检查。真实队号、文件命名、AI 输出附交要求和提交渠道见 [交付核对](evidence/release.md)。

## 填入经校赛确认的队号

队伍收到正式队号且核对本届 AI 与文件命名要求后，可以在本地生成提交用 PDF。将下面的变量值和文件名换成正式通知要求，并检查更新后的 PDF。

```powershell
$team = 'REPLACE-WITH-CONFIRMED-ID'
& $py analysis/build_paper.py --team $team --output "private/$team.pdf"
```

真实队号版和完整内部提示记录留在 Git 忽略的 `private/`，由队伍管理和递交。
