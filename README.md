# Hallowell County 宽带部署 · D 题独立修订版

英文论文见 [Problem-D-review.pdf](output/pdf/Problem-D-review.pdf)。本版从 `42d4d804` 派生，公开审阅版使用队号占位符。当前版本的页码、文件指纹和复核结果见 [交付核对](evidence/release.md)。本包供队内使用。

## 阅读和编辑

- [论文主文件](paper/main.typ) 组织英文正文。[摘要](paper/summary.typ)、[委员会备忘录](paper/sec_memo.typ)和 [AI 使用报告](paper/ai.typ) 可分别编辑。
- [Task 1](analysis/task1.py) 处理地图、订阅、路测和申诉，[Task 2](analysis/task2.py) 求解直接部署模型，[Task 3](analysis/task3.py) 比较三种采购机制和枢纽路线敏感性。
- [Task 2 情景](results/task2_scenarios.csv)、[Task 3 情景](results/task3_summary.csv)、[逐镇分配](results/task3_towns.csv) 和 [租金财务表](results/task3_finance.csv) 支持核对模型结论。[参数来源](sources/) 标注测量、参考值和本题假设。
- [图表生成程序](analysis/paper_data.py) 从结果表生成英文图和排版数据。运行全量复现会重建它们。

## 从赛方附件复算

本次运行环境为 Windows、Python 3.12，依赖在 `requirements.txt` 中锁定。下例从本目录执行；将 `$data` 指向队伍收到的原始 CSV 文件夹。

```powershell
py -3.12 -m venv .venv
$py = '.\.venv\Scripts\python.exe'
& $py -m pip install -r requirements.txt
$data = '..\2026年重庆大学数学建模秋季赛题目\2026_CQU_ICM_Problem_D_DATA'
& $py analysis/reproduce.py --data $data
```

输入应包含 `blocks.csv`、`blocksV2.csv`、`road_segments.csv`、`road_segmentsV2.csv`。它们的 SHA-256 见 [输入审计](results/task1_data_audit.json)。全量入口会重算模型，运行独立核查，再编译匿名 PDF。排版使用 Times New Roman 和 Microsoft YaHei。

## 填入正式队号

收到赛方正式队号后，可用下列命令生成带队号的正文和 AI 报告。学校如要求单独封面，需以本届模板和命名要求为准。先把规定的 A4 单页封面导出为 `private/cover.pdf`，再调用带封面的构建命令。身份信息仅出现在规定的位置。队员应在提交前核对本届 AI 披露要求和实际使用记录。

```powershell
$team = 'REPLACE-WITH-TEAM-ID'
& $py analysis/build_paper.py --team $team --output "private/ICM_D$team.pdf"
# 赛方要求封面时使用
& $py analysis/build_submission.py --team $team --cover private/cover.pdf --out "private/ICM_D${team}_cover.pdf"
```
