#import "layout.typ": *

#set document(title: "Report on Use of AI Tools", author: (), date: none)
#set text(font: ("Times New Roman", "Microsoft YaHei"), size: 12pt, fill: ink, lang: "en")
#set par(justify: true, leading: .66em, spacing: .78em, first-line-indent: (amount: 1.6em, all: false))
#set page(paper: "a4", margin: (left: .85in, right: .85in, top: .95in, bottom: .8in))
#set heading(numbering: none)
#show heading.where(level: 1): it => block(above: 1.1em, below: .8em)[
  #set text(size: 14pt, weight: "bold")
  #it.body
]
#show heading.where(level: 2): it => block(above: 1.0em, below: .6em)[
  #set text(size: 12.5pt, weight: "bold")
  #it.body
]
#show math.equation.where(block: true): set block(above: .8em, below: .8em)

#include "ai.typ"
