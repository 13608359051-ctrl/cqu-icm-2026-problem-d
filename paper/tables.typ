#import "layout.typ": tab
#let report = json("../results/paper_data.json")
#let model-fig = "../results/fig_model.svg"
#let coverage-fig = "../results/fig_coverage.svg"
#let tradeoff-fig = "../results/fig_tradeoff.svg"
#let benefit-fig = "../results/fig_benefit.svg"
#let value(name) = report.values.at(name)
#let rows(name) = report.rows.at(name)

