---
title: "Growth Curve Analysis: How Capital Investment Translates into Long-term Commercial Value for VC-backed Startups"
author: "Lingke Huang"
date: "May 2025"
geometry: margin=2.5cm
fontsize: 12pt
linestretch: 1.25
header-includes:
  - \usepackage{titlesec}
  - \titleformat{\section}{\normalfont\large\bfseries}{\thesection.}{0.5em}{}
  - \titleformat{\subsection}{\normalfont\normalsize\bfseries}{\thesubsection}{0.5em}{}
---

# Introduction

Venture capital (VC) is widely regarded as a catalyst for innovation, yet the relationship between capital investment and startup success remains poorly understood. This study investigates a focused research question: *In the VC ecosystem, what patterns of capital investment are most strongly associated with successful exit outcomes (IPO or acquisition)?* We decompose "capital investment" into three measurable dimensions — volume (total funding), milestones (number of funding rounds), and velocity (time between rounds) — and examine how each dimension relates to the binary outcome of exit success. By operationalising a broad business question into testable sub-questions, this analysis aims to move beyond anecdotal claims and let the data reveal the structural patterns behind startup outcomes.

# Method

**Data source.** The analysis draws on the Crunchbase open dataset, a widely cited source in entrepreneurship research (Block & Sandner, 2009). We utilise four relational tables — *objects.csv* (company master), *funding_rounds.csv* (round-level records), *acquisitions.csv*, and *ipos.csv* — joined via the company identifier. After filtering for entities classified as companies, with confirmed funding greater than zero and a valid status label (operating, acquired, ipo, or closed), the working sample comprises 27,874 VC-backed companies across 42 industry categories.

**Feature engineering.** Three independent variables were constructed: (1) total funding, binned into six tiers from under \$1M to over \$500M; (2) number of funding rounds, as a discrete count capped at 10+; and (3) average time between rounds, computed as the mean inter-round interval in months and binned into five speed categories. The dependent variable is a binary indicator of exit success, coded as 1 if the company achieved an IPO or was acquired, and 0 otherwise. The overall baseline exit rate in the sample is 10.1%.

**Tools.** Data wrangling was performed with *pandas* and *NumPy* in Python. Visualisation employed three distinct packages to demonstrate breadth of technical competency: *pyecharts* for the hierarchical TreeMap (Fig 1), *Plotly* with graph_objects and make_subplots for the stacked bar chart and bubble chart (Figs 2–3), and *seaborn* with *Matplotlib* for the annotated heatmap (Fig 4). A unified professional colour palette was applied across all figures for visual coherence.

# Result

**Fig 1 (EDA Overview)** presents a hierarchical TreeMap of the dataset's 12 largest industries, with rectangle area encoding company count and colour encoding company status. Software and Web dominate the ecosystem by volume, while Biotech shows a comparatively higher exit-success proportion, suggesting that industry context moderates the funding–exit relationship.

**Fig 2 (RQ1: Volume)** decomposes exit rate by funding bracket into IPO rate and Acquired rate using a stacked bar chart, with sample size plotted on a secondary axis. Exit rate rises monotonically from 3.0% (under \$1M) to 42.1% (over \$500M). Notably, the composition shifts: in lower brackets, Acquired exits dominate, while in the highest bracket, the IPO rate alone reaches 36.8%. The overall average exit rate (10.1%) serves as a baseline reference line.

**Fig 3 (RQ2: Milestones)** maps exit rate against funding round count using a bubble chart, where bubble size encodes sample size and colour encodes exit rate. A first-difference analysis identifies Round 10 as the threshold where exit rate jumps most sharply (+14.2 percentage points, from 13.0% to 27.3%). The pattern is non-linear: exit rates plateau around Rounds 3–5 at approximately 15%, dip at Round 9, and surge for companies surviving to Round 10 or beyond.

**Fig 4 (RQ3: Velocity × Volume)** uses a cross-tabulated heatmap to simultaneously examine funding speed and funding amount. Companies with inter-round intervals of 6–24 months consistently show the highest exit rates across funding brackets. The pattern holds even when controlling for funding volume, indicating that funding velocity has an independent association with exit success. One cell (over \$500M, interval exceeding 48 months) reaches 100%, though with only n = 1, demanding cautious interpretation.

# Discussion

All three research questions are addressed with empirical evidence. The results suggest that moderate-to-high funding volume, sufficient round milestones, and a measured funding cadence collectively characterise the most successful startups. The monotonic rise observed in Fig 2 challenges the initial hypothesis of diminishing returns — although this may reflect reverse causality, whereby successful companies attract more capital rather than capital causing success. The Round 10 threshold identified in Fig 3 likely reflects a selection effect: companies surviving to late rounds have already passed multiple rounds of investor due diligence (Gompers & Lerner, 2001).

**Limitations.** First, the analysis is correlational, not causal; confounders such as founder quality, market timing, and macroeconomic conditions are unobserved (Cochrane, 2005). Second, the dataset exhibits survivorship bias — companies that failed before receiving any recorded funding are absent, which may inflate observed exit rates. Third, companies currently in "Operating" status represent right-censored observations whose final outcome is unknown, potentially understating the true long-term exit rate. Fourth, small sample sizes in extreme cells limit the generalisability of those specific findings.

**Recommendations.** Future work should incorporate cohort analysis by founding year and explore causal inference techniques such as instrumental variable regression. For practitioners, achieving later funding rounds and maintaining a 6–24 month funding cadence appear to be more informative signals of eventual success than raw funding volume alone.

# References

[1] Block, J. & Sandner, P. (2009). What is the effect of the financial crisis on venture capital financing? Empirical evidence from US Internet start-ups. *Venture Capital*, 11(4), 295–309.

[2] Cochrane, J.H. (2005). The risk and return of venture capital. *Journal of Financial Economics*, 75(1), 3–52.

[3] Gompers, P. & Lerner, J. (2001). The venture capital revolution. *Journal of Economic Perspectives*, 15(2), 145–168.

[4] Kaplan, S.N. & Lerner, J. (2010). It ain't broke: The past, present, and future of venture capital. *Journal of Applied Corporate Finance*, 22(2), 36–47.

[5] Hellmann, T. & Puri, M. (2002). Venture capital and the professionalization of start-up firms. *Journal of Finance*, 57(1), 169–197.

[6] Da Rin, M., Hellmann, T. & Puri, M. (2013). A survey of venture capital research. *Handbook of the Economics of Finance*, 2, 573–648.

[7] Pyecharts Documentation. (2023). *pyecharts — A Python Echarts Plotting Library*. https://pyecharts.org/

[8] Plotly Technologies Inc. (2023). *Plotly Python Open Source Graphing Library*. https://plotly.com/python/

[9] Waskom, M. (2021). seaborn: statistical data visualization. *Journal of Open Source Software*, 6(60), 3021.

\newpage

# Appendix: Figures

*[Insert Fig 1–4 here]*
