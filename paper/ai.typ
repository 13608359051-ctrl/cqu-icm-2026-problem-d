#import "layout.typ": *

= Report on Use of AI Tools

*Tool and model.* OpenAI Codex with GPT-6.2 Sol, November 20, 2026. The coordinating agent and three subagents used the same model. Python, SciPy/HiGHS, Matplotlib, Typst and Poppler executed calculations, plots, typesetting and rendering. The Humanizer workflow was applied within Codex to edit the English prose. No separate language model was used for that step. #cite("12", "13")

*Scope.* The coordinating agent read the problem and policy, searched and checked sources, integrated the models, drew figures from generated results, drafted and edited the English solution and prepared the deliverables. Subagent A authored the data and coverage analysis. Subagent B authored the optimization and sensitivity analysis. Subagent C authored the procurement and effective-use analysis. B independently recalculated A's results, C independently solved B's model, and A independently recalculated C's solutions. The independent checks were performed by separate AI agents. They do not represent human team review.

*Inputs and corresponding outputs.* The available user requests and original subagent assignments are recorded below. The support package contains the full generated work products. The local transcript export retains available visible text. The platform stores other inter-agent exchanges in encrypted records. The team should confirm whether the organizer accepts this output index, the supplementary records and the identity redactions. The team must separately disclose AI use outside this run.

*Accountability.* The audit records identify independently reproduced outputs and limitations. Deployment inputs from the literature were checked against the cited documents. Unobserved county costs, coverage and adoption parameters are explicitly modeled as scenarios. The team has not yet recorded human review or formally submitted this file.

== Output index

- Coverage and data audit. `analysis/task1.py`, `results/task1_*`, and `sources/task1_parameters.csv`.
- Deployment and sensitivity. `analysis/task2.py`, `results/task2_*`, and `sources/task2_parameters.csv`.
- Mechanism analysis. `analysis/task3.py`, `results/task3_*`, and `sources/task3_parameters.csv`.
- Independent verification. `analysis/review_task1.py`, `analysis/verify_task2.py`, `evidence/task3_independent.py`, and the acceptance record.
- Figures and paper. `analysis/paper_data.py`, `results/fig_*.svg`, and the editable files in `paper/`.

#pagebreak()
== Recorded prompts

The excerpts below preserve the wording and language of the requests. Repository and personal workspace identifiers are omitted for anonymous review.

#for entry in json("ai_prompts.json") {
  block(above: 12pt, below: 6pt, sticky: true)[*#entry.title*]
  set text(font: ("Libertinus Serif", "Microsoft YaHei", "Noto Sans CJK SC"))
  set par(justify: false, leading: .48em)
  for line in entry.text.split("\n") {
    if line.trim() != "" { par(text(line)) }
  }
}

