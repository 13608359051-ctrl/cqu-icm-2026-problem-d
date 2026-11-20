#import "layout.typ": tab
#let report = json("../results/paper_data.json")
#let workflow-fig = "../results/fig_workflow.svg"
#let coverage-fig = "../results/fig_coverage.svg"
#let signal-fig = "../results/fig_signal.svg"
#let model-fig = "../results/fig_model.svg"
#let tornado-fig = "../results/fig_tornado.svg"
#let pareto-fig = "../results/fig_pareto.svg"
#let cost-fig = "../results/fig_cost.svg"
#let robust-fig = "../results/fig_robust.svg"
#let benefit-fig = "../results/fig_benefit.svg"
#let value(name) = report.values.at(name)
#let rows(name) = report.rows.at(name)
