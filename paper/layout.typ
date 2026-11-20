#let ink = rgb("#19272c")
#let navy = rgb("#163a4c")
#let accent = rgb("#176b68")
#let rule = rgb("#9cb4b6")
#let pale = rgb("#edf5f4")
#let cite(..numbers) = text(fill: accent)[\[#numbers.pos().join(", ")\]]
#let lead(body) = block(stroke: (left: 3pt + accent), inset: (left: 12pt, right: 9pt, top: 7pt, bottom: 7pt), fill: pale, width: 100%, body)
#let caption(body) = block(above: 8pt, below: 13pt)[#text(fill: navy, body)]
#let tab(columns, names, rows, left-columns: (0,)) = block(width: 100%)[
  #set par(justify: false, leading: .44em)
  #table(
    columns: columns,
    align: (x, _) => if x in left-columns { left + horizon } else { right + horizon },
    stroke: (x, y) => (bottom: .4pt + rule),
    inset: (x: 6pt, y: 4.2pt),
    fill: (_, y) => if y == 0 { pale },
    table.header(..names.map(n => strong(n))),
    ..rows.flatten().map(x => if type(x) == str { text(x) } else { x }),
  )
]

