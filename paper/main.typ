#import "layout.typ": *
#import "tables.typ": *

#set document(title: "The Last Mile of Broadband", author: (), date: none)
#set text(font: ("Times New Roman", "Microsoft YaHei"), size: 12pt, fill: ink, lang: "en")
#set par(justify: true, leading: .55em, spacing: .5em, first-line-indent: (amount: 1.6em, all: false))
#set page(
  paper: "a4",
  margin: (left: .95in, right: .95in, top: .95in, bottom: .8in),
  header: context {
    if counter(page).get().first() > 1 {
      set text(size: 12pt)
      grid(columns: (1fr, 1fr),
        align(left)[Team \# #sys.inputs.at("team", default: "TEAM NUMBER REQUIRED")],
        align(right)[Page #counter(page).display() of #counter(page).final().first()],
      )
      v(-6pt)
      line(length: 100%, stroke: .5pt + ink)
    }
  },
)
#set heading(numbering: "1.1")
#show heading.where(level: 1): it => block(above: 1.0em, below: .8em)[
  #set text(size: 14pt, weight: "bold")
  #if it.numbering != none { counter(heading).display() + h(.55em) }#it.body
]
#show heading.where(level: 2): it => block(above: .9em, below: .5em)[
  #set text(size: 12pt, weight: "bold")
  #if it.numbering != none { counter(heading).display() + h(.5em) }#it.body
]
#show heading.where(level: 3): it => block(above: .8em, below: .45em)[
  #set text(size: 12pt, weight: "bold")
  #if it.numbering != none { counter(heading).display() + h(.5em) }#it.body
]
#set math.equation(numbering: "(1)")
#show math.equation.where(block: true): set block(above: .7em, below: .7em)

#include "summary.typ"
#pagebreak()
#outline(title: [Contents], depth: 2, indent: auto)
#pagebreak()

#include "sec_intro.typ"
#include "sec_assumptions.typ"
#include "sec_notation.typ"
#include "sec_task1.typ"
#include "sec_task2a.typ"
#include "sec_task2b.typ"
#include "sec_task3.typ"
#include "sec_insights.typ"
#include "sec_eval.typ"
#include "sec_concl.typ"
#include "sec_memo.typ"
#include "references.typ"
