# Capital, Timing, and Growth: Visualizing What Drives Startup Success

> [中文版见下方 / Chinese version below](#中文版)

> **NAA1661 Data Scholarship** — University of Nottingham Ningbo China, Spring 2026
>
> **Group B** — Python Track

## Overview

This group project explores the global startup ecosystem through data visualisation, investigating what drives startup success from four complementary angles:

| Part | Title | Author | Focus |
|------|-------|--------|-------|
| **A** | Starting Lines: Where Income, Geography, and Industry Shape Startup Ecosystems | — | Country-level startup activity vs. economic indicators |
| **B** | Capital Pulse: A Deep Analysis from Global Flow Paths to Valuation Structures | Hengji Zhao | Cross-continent capital flows and sectoral valuation |
| **C** | Timing Matters: A Survival Analysis of Global Startups Across Founding and Funding Cycles | Lingyi Peng | Funding timing, survival patterns, and failure cycles |
| **D** | Growth Decoded: A Funding Pattern Analysis from Capital Investment to Startup Exit Success | Lingke Huang | Funding volume, milestones, and velocity vs. exit outcomes |

**Core conclusion:** Startup success is not random — it is shaped by geography, capital structure, timing, and funding rhythm. Visualisation made these patterns discoverable from nearly 28,000 startup records.

## Repository Structure

This repository contains the code, data pipeline, documentation, and presentation materials for **Part D** (Growth Curve Analysis), along with shared group presentation assets.

```
.
├── README.md
├── .gitignore
│
├── src/                                # Source code
│   ├── preview_figures.py              # Main script — generates all 4 figures + HTML preview
│   └── seaborn.ipynb                   # Exploratory notebook for Fig 4
│
├── docs/                               # Documentation & writing
│   ├── Reflection.md                   # Reflection report source (pandoc → PDF)
│   ├── Reflection.pdf                  # Rendered reflection PDF
│   ├── Lingke Huang - Data Scholarship Reflection.doc
│   ├── Presentation_Plan.md            # Slide-by-slide presentation plan with scripts
│   ├── Part D 思路.md                   # Research design & methodology notes
│   └── Topic Selection/               # Early-stage topic & branch selection docs
│
├── figures/                            # Exported figure images
│   ├── fig1_placeholder.png            # Fig 1: TreeMap — industry × exit status
│   ├── fig2_placeholder.png            # Fig 2: Stacked bar — exit rate by funding bracket
│   ├── fig3_placeholder.png            # Fig 3: Bubble chart — exit rate by round count
│   ├── fig4_placeholder.png            # Fig 4: Heatmap — velocity × volume interaction
│   └── _fig4_heatmap.png              # Fig 4 high-res export
│
├── output/                             # Generated HTML previews (gitignored)
│   ├── figures_preview.html
│   ├── _fig1_inline.html
│   └── _fig1_pyecharts.html
│
├── course/                             # Course materials & group PPT (gitignored)
│   ├── NAA1661 Data Scholarship Specification Feb. 2025.pdf
│   ├── Group Presentation Template.pptx
│   ├── Data Scholarship Group Presentation Template 2022-2023.pdf
│   ├── Capital, Timing, and Growth-...pptx   # Final group presentation
│   └── Lecutres/                       # Weekly lecture materials
│
└── Datasets/                           # Crunchbase CSVs (~400 MB, gitignored)
    ├── objects.csv
    ├── funding_rounds.csv
    ├── acquisitions.csv
    ├── ipos.csv
    └── ...
```

## Part D — Research Questions & Figures

| # | Question | Dimension | Figure | Tool |
|---|----------|-----------|--------|------|
| — | What does the startup landscape look like? | Overview | Fig 1 · TreeMap | pyecharts |
| RQ1 | Does higher total funding predict higher exit rates? | Volume | Fig 2 · Stacked Bar | Plotly |
| RQ2 | Is there a funding-round threshold for exit success? | Milestones | Fig 3 · Bubble Chart | Plotly |
| RQ3 | Does funding speed interact with funding amount? | Velocity | Fig 4 · Heatmap | seaborn |

### Key Findings

- **Volume:** Exit rate rises from 3% (<$1M) to 42% (>$500M), but exit type shifts — low funding → acquisition, high funding → IPO
- **Milestones:** Exit rate plateaus at ~15% through Rounds 1–5, then jumps +14 percentage points at Round 10 (selection signal)
- **Velocity:** A 6–24 month funding cadence shows the highest exit rates across all funding brackets

**Takeaway:** It's not just how much you raise — it's *how* you raise it.

## Tech Stack

| Purpose | Tools |
|---------|-------|
| Data wrangling | `pandas`, `numpy` |
| Visualisation | `pyecharts` (TreeMap), `plotly` (bar, bubble), `seaborn` + `matplotlib` (heatmap) |
| Report rendering | `pandoc` + LaTeX → PDF |
| Image export | `kaleido` (Plotly), `matplotlib` (Fig 4) |

## Quick Start

```bash
# 1. Install dependencies
pip install pandas numpy plotly seaborn matplotlib pyecharts kaleido

# 2. Place Crunchbase CSVs in Datasets/
#    Required: objects.csv, funding_rounds.csv, acquisitions.csv, ipos.csv

# 3. Generate figures + interactive preview
python src/preview_figures.py
# Opens http://localhost:8765/figures_preview.html

# 4. Render reflection to PDF
pandoc docs/Reflection.md -o docs/Reflection.pdf --pdf-engine=pdflatex
```

## Data Sources

- **Crunchbase Open Dataset** — startup records, funding rounds, acquisitions, IPOs (~28,000 VC-backed companies)
- **World Bank Entrepreneurship Database** — new business density and GDP per capita across 136 economies (used in Part A)
- **Kaggle Startup Growth & Funding Trends** — supplementary startup sample (used in Parts A, C)

---

<a id="中文版"></a>
# 资本、时间与增长：可视化驱动创业成功的因素

> **NAA1661 数据学术** — 宁波诺丁汉大学，2026 Spring
>
> **B 组** — Python 方向

## 概述

本小组项目通过数据可视化探索全球创业生态，从四个互补角度研究创业成功的驱动因素：

| 部分 | 标题 | 作者 | 研究重点 |
|------|------|------|----------|
| **A** | Starting Lines: 收入、地理与行业如何塑造创业生态 | — | 国家层面创业活动与经济指标 |
| **B** | Capital Pulse: 全球资金流向与估值结构深度分析 | 赵恒基 | 跨大洲资本流动与行业估值 |
| **C** | Timing Matters: 全球初创企业的生存分析 | 彭令仪 | 融资时机、生存模式与失败周期 |
| **D** | Growth Decoded: 资本投入模式与退出成功的关联分析 | 黄令科 | 融资总量、轮次与速度对退出的影响 |

**核心结论：** 创业成功并非随机——它受地理、资本结构、时间节奏和融资模式的共同塑造。可视化使我们从近 28,000 条记录中发现了这些规律。

## 仓库结构

本仓库包含 **Part D**（增长曲线分析）的代码、数据流程、文档及小组演示材料。

```
.
├── README.md
├── .gitignore
├── src/                    # 源代码
│   ├── preview_figures.py  # 主脚本——生成全部 4 张图 + HTML 预览
│   └── seaborn.ipynb       # Fig 4 探索性分析 notebook
├── docs/                   # 文档与写作
│   ├── Reflection.md       # 反思报告源文件
│   ├── Reflection.pdf      # 渲染后 PDF
│   ├── Presentation_Plan.md # 逐页演示计划（含脚本与注释）
│   ├── Part D 思路.md       # 研究设计与方法论笔记
│   └── Topic Selection/    # 选题与方向文档
├── figures/                # 导出的图片
├── output/                 # 生成的 HTML 预览（gitignored）
├── course/                 # 课程资料与小组 PPT（gitignored）
└── Datasets/               # Crunchbase CSV（~400 MB，gitignored）
```

## Part D — 研究问题与图表

| # | 问题 | 维度 | 图表 | 工具 |
|---|------|------|------|------|
| — | 初创企业生态全景如何？ | 概览 | Fig 1 · 矩形树图 | pyecharts |
| RQ1 | 更高的融资总额是否预示更高的退出率？ | 融资总量 | Fig 2 · 堆叠柱状图 | Plotly |
| RQ2 | 是否存在融资轮次的「门槛效应」？ | 融资里程碑 | Fig 3 · 气泡图 | Plotly |
| RQ3 | 融资速度与融资金额是否存在交互效应？ | 融资速度 | Fig 4 · 热力图 | seaborn |

### 主要发现

- **融资总量：** 退出率从 3%（<$1M）升至 42%（>$500M），但退出方式转变——低融资 → 被收购，高融资 → IPO
- **融资里程碑：** 退出率在第 1–5 轮持平于 ~15%，在第 10 轮跳升 +14 个百分点（筛选信号）
- **融资速度：** 6–24 个月的融资节奏在所有融资区间中表现最优

**一句话总结：** 重要的不只是融了多少钱，而是*怎么融的*。

## 快速开始

```bash
# 1. 安装依赖
pip install pandas numpy plotly seaborn matplotlib pyecharts kaleido

# 2. 将 Crunchbase CSV 放入 Datasets/
#    需要: objects.csv, funding_rounds.csv, acquisitions.csv, ipos.csv

# 3. 生成图表 + 交互式预览
python src/preview_figures.py

# 4. 渲染反思报告
pandoc docs/Reflection.md -o docs/Reflection.pdf --pdf-engine=pdflatex
```
