#import "layout.typ": *
#import "tables.typ": *

#set document(title: "The Last Mile of Broadband", author: (), date: none)
#set text(font: "Libertinus Serif", size: 12pt, fill: ink, lang: "en")
#set par(justify: true, leading: .65em, spacing: .85em)
#set page(
  paper: "us-letter",
  margin: (left: .8in, right: .8in, top: .85in, bottom: .70in),
  header: context {
    grid(columns: (1fr, auto, 1fr), align(left)[#strong[Team \# #sys.inputs.at("team", default: "TEAM NUMBER REQUIRED")]], [Problem D], align(right)[Page #counter(page).display() of #counter(page).final().first()])
    v(3pt)
    line(length: 100%, stroke: .55pt + rule)
  },
)
#set heading(numbering: "1.1")
#show heading.where(level: 1): it => block(above: .7em, below: .9em)[
  #set text(size: 22pt, fill: navy)
  #if it.numbering != none { counter(heading).display() + h(.45em) }#it.body
]
#show heading.where(level: 2): it => block(above: .8em, below: .65em)[
  #set text(size: 15pt, fill: navy)
  #if it.numbering != none { counter(heading).display() + h(.38em) }#it.body
]
#show math.equation.where(block: true): set block(above: .85em, below: .85em)

#include "summary.typ"
#pagebreak()
#outline(title: [Contents], depth: 2, indent: auto)
#pagebreak()

#include "evidence.typ"
#include "deployment.typ"
#include "mechanisms.typ"
#include "outcomes.typ"
#include "memo.typ"
#include "references.typ"

#pagebreak()
#include "ai.typ"

