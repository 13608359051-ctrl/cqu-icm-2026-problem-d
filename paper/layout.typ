// Shared typography for the solution document.
// The paper follows the layout of the award-winning ICM-D papers: Times New
// Roman body text, numbered sections, booktabs-style tables, captions above
// tables and below figures, and a running header with the control number.

#let ink = rgb("#000000")
#let grey = rgb("#444444")
#let accent = rgb("#26456b")
#let light = rgb("#f2f2f2")
#let cite(..numbers) = [\[#numbers.pos().join(", ")\]]

// Booktabs-style table: no vertical rules, heavy top/bottom rules, a light
// rule under the header, centred numeric columns.
#let tab(columns, names, rows, left-columns: (0,), size: 11pt) = {
  block(width: 100%)[
    #set text(size: size)
    #set par(justify: false, leading: .5em)
    #table(
      columns: columns,
      stroke: none,
      align: (x, _) => if x in left-columns { left + horizon } else { center + horizon },
      inset: (x: 4.5pt, y: 3.2pt),
      table.hline(stroke: .9pt),
      table.header(..names.map(n => strong(n))),
      table.hline(stroke: .5pt),
      ..rows.flatten().map(x => if type(x) == content { x } else { text(str(x)) }),
      table.hline(stroke: .9pt),
    )
  ]
}

// Captions are numbered manually so that every figure and table can be
// checked against the final PDF. Figure captions sit below the figure and
// table captions above the table, as in the reference papers.
#let figcap(n, body) = block(above: 7pt, below: 15pt, {
  set text(size: 11pt)
  set par(justify: false)
  align(center)[*Figure #n.* #body]
})

#let tabcap(n, body) = block(above: 14pt, below: 4pt, {
  set text(size: 11pt)
  set par(justify: false)
  align(center)[*Table #n.* #body]
})

// Keep a figure and its caption on the same page.
#let fig(path, n, body, width: 100%) = block(breakable: false, width: width)[
  #image(path, width: 100%)
  #figcap(n, body)
]

// Keep a table and its caption on the same page.
#let tabblock(n, caption, columns, names, table-rows, left-columns: (0,), size: 11pt) = block(breakable: false, width: 100%)[
  #tabcap(n, caption)
  #tab(columns, names, table-rows, left-columns: left-columns, size: size)
]

// A short emphasised answer/result paragraph used to make the response to a
// task requirement visible at a glance.
#let answer(body) = block(above: .75em, below: .75em)[
  #set par(first-line-indent: 0pt)
  #text(weight: "bold")[Answer.] #body
]
