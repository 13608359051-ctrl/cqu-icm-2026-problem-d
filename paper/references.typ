#import "layout.typ": *

#pagebreak()
= References

#let ref(n, body, url: none, label: "Source") = block(above: .55em, below: .65em)[
  #set par(justify: false)
  #grid(columns: (2.2em, 1fr), [\[#n\]], [#body #if url != none { link(url, text(fill: accent, underline(label))) }])
]

#ref(1, [2026 CQU ICM. _Problem D: The Last Mile of Broadband_. Contest problem and supplied synthetic block and road files, 2026.])
#ref(2, [Federal Communications Commission. _2024 Section 706 Report_. FCC 24-27, GN Docket 22-270, March 2024.], url: "https://docs.fcc.gov/public/attachments/FCC-24-27A1.pdf", label: "FCC 24-27")
#ref(3, [Major, D., Teixeira, R., & Mayer, J. “No WAN's Land: Mapping U.S. Broadband Coverage with Millions of Address Queries to ISPs.” _ACM Internet Measurement Conference_, 393–419, 2020.], url: "https://doi.org/10.1145/3419394.3423652", label: "DOI")
#ref(4, [U.S. Bureau of Labor Statistics. _Employer Costs for Employee Compensation, December 2025_. Released March 20, 2026.], url: "https://www.bls.gov/news.release/archives/ecec_03202026.htm", label: "BLS release")
#ref(5, [United States Code of Federal Regulations. _47 CFR § 1.7006_, 2024 edition. See also the FCC Broadband Data Collection guidance, “How to Submit a Successful Fixed Availability Challenge.” #link("https://help.bdc.fcc.gov/hc/en-us/articles/12000296843291-How-to-Submit-a-Successful-Fixed-Availability-Challenge")[FCC guidance].], url: "https://www.govinfo.gov/content/pkg/CFR-2024-title47-vol1/pdf/CFR-2024-title47-vol1-sec1-7006.pdf", label: "Rule text")
#ref(6, [de Souza, M. A., et al. “A Techno-Economic Framework for Installing Broadband Networks in Rural and Remote Areas.” _IEEE Access_ 9, 58421–58447, 2021.], url: "https://doi.org/10.1109/ACCESS.2021.3071919", label: "DOI")
#ref(7, [Valentín-Sívico, J., Canfield, C., Low, S. A., & Gollnick, C. “Evaluating the impact of broadband access and internet use in a small underserved rural community.” _Telecommunications Policy_ 47(4), 102499, 2023.], url: "https://doi.org/10.1016/j.telpol.2023.102499", label: "DOI")
#ref(8, [Fiber Broadband Association & Cartesian. _2025 Fiber Deployment Cost Annual Report_. Figure 2.1, released January 2026.], url: "https://fiberbroadband.org/wp-content/uploads/2026/01/FBA_Cartesian_Fiber-Deployment-Cost-Annual-Report_2025.pdf", label: "Report")
#ref(9, [Pierce County. _Broadband Strategic Plan and Facilitation Study_. Section 4.1, March 2021.], url: "https://www.piercecountywa.gov/DocumentCenter/View/108718/Broadband-Strategic-Plan-and-Facilitation-Study-2021?bidId=", label: "County study")
#ref(10, [Kumar, S. K. A., & Oughton, E. J. “Infrastructure Sharing Strategies for Wireless Broadband.” _IEEE Communications Magazine_ 61(7), 46–52, 2023.], url: "https://doi.org/10.1109/MCOM.005.2200698", label: "DOI")
#ref(11, [Nardotto, M., Valletti, T., & Verboven, F. “Unbundling the Incumbent: Evidence from UK Broadband.” _Journal of the European Economic Association_ 13(2), 330–362, 2015.], url: "https://doi.org/10.1111/jeea.12127", label: "DOI")
#ref(12, [OpenAI. _Codex_, run with GPT-6.2 Sol, November 20, 2026. Model development, coding, figure generation, paper drafting, editing and AI subagent review. See the Report on Use of AI Tools.], url: "https://openai.com/codex/", label: "Tool")
#ref(13, [SciPy Developers. _scipy.optimize.milp_, SciPy 1.16.3. HiGHS-backed mixed-integer linear solver.], url: "https://docs.scipy.org/doc/scipy-1.16.3/reference/generated/scipy.optimize.milp.html", label: "Documentation")
#ref(14, [Federal Communications Commission. _Performance Measures for Connect America High-Cost Universal Service Support_. FCC 19-104, WC Docket 10-90, 2019.], url: "https://docs.fcc.gov/public/attachments/FCC-19-104A1.pdf", label: "FCC order")
#ref(15, [Federal Communications Commission. _Rural Digital Opportunity Fund Phase I Auction: Procedures_. FCC 20-77, 2020.], url: "https://docs.fcc.gov/public/attachments/FCC-20-77A1.pdf", label: "FCC auction procedures")
#ref(16, [Kansas Office of Broadband Development. _Non-Discriminatory Open Access Middle Mile_. Interconnection guidance and FAQs, 2024.], url: "https://www.kansascommerce.gov/program/challenge/middle-mile/", label: "Kansas guidance")
#ref(17, [City of Cambridge. _Digital Equity Initiative_. Public program materials on affordability, devices and skills.], url: "https://www.cambridgema.gov/departments/cambridgepubliclibrary/digitalequityinitiative", label: "Program")

