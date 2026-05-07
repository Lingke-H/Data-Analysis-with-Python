# VC Growth Curve: Capital Investment and Startup Exit Outcomes

> **NAA1661 Data Scholarship** — University of Nottingham Ningbo China, Spring 2026
> 
> Part D Individual Contribution: **Growth Curve Analysis**

## Overview

This project investigates how capital investment patterns relate to successful exit outcomes (IPO or acquisition) among venture-capital-backed startups. Using the Crunchbase open dataset (~28,000 companies), we decompose "capital investment" into three dimensions — **volume**, **milestones**, and **velocity** — and produce four publication-ready visualisations.

### Research Questions

| # | Question | Figure |
|---|----------|--------|
| — | What does the startup landscape look like? | Fig 1 · TreeMap |
| RQ1 | Does higher total funding predict higher exit rates? | Fig 2 · Stacked Bar |
| RQ2 | Is there a funding-round threshold for exit success? | Fig 3 · Bubble Chart |
| RQ3 | Does funding speed interact with funding amount? | Fig 4 · Heatmap |

## Repository Structure

```
.
├── preview_figures.py          # Main script — generates all 4 figures + HTML preview
├── Reflection.md               # Reflection report (pandoc → PDF)
├── Reflection.pdf              # Rendered PDF
├── Part D 思路.md               # Research design & methodology notes
├── figures_preview.html        # Interactive HTML preview of all figures
├── _fig1_pyecharts.html        # Fig 1 standalone (pyecharts TreeMap)
├── _fig4_heatmap.png           # Fig 4 exported PNG (seaborn)
├── fig{1,2,3,4}_placeholder.png  # Exported figure PNGs for the report
├── Topic Selection/            # Early-stage topic & branch selection docs
├── Lecutres/                   # Weekly lecture materials (weeks 2–5)
├── Datasets/                   # Crunchbase CSV files (gitignored, ~400 MB)
├── NAA1661 Data Scholarship Specification Feb. 2025.pdf
├── Reflection Template.doc
├── Group Presentation Template.pptx
└── seaborn.ipynb               # Exploratory notebook
```

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
python preview_figures.py
# Opens http://localhost:8765/figures_preview.html

# 4. Render reflection to PDF
pandoc Reflection.md -o Reflection.pdf --pdf-engine=pdflatex
```

## Figures

| Figure | Description | Tool |
|--------|-------------|------|
| Fig 1 | Distribution of VC-Backed Startups by Industry and Exit Status | pyecharts TreeMap |
| Fig 2 | Exit Rate Decomposition (IPO vs. Acquisition) by Total Funding Bracket | Plotly stacked bar + dual axis |
| Fig 3 | Exit Rate by Number of Funding Rounds with Threshold Identification | Plotly bubble chart |
| Fig 4 | Exit Rate Heatmap: Funding Velocity × Funding Volume Interaction | seaborn heatmap |

---

# VC 增长曲线：资本投入与初创企业退出结果

> **NAA1661 数据学术** — University of Nottingham Ningbo China，2026 Spring
>
> Part D 个人贡献：**增长曲线分析**

## 概述

本项目研究风险投资（VC）中的资本投入模式与初创企业成功退出（IPO 或被收购）之间的关系。基于 Crunchbase 开源数据集（约 28,000 家企业），我们将「资本投入」分解为三个维度——**融资总量**、**融资轮次**和**融资速度**——并生成四张可发表级别的可视化图表。

### 研究问题

| # | 问题 | 图表 |
|---|------|------|
| — | 初创企业生态全景如何？ | Fig 1 · 矩形树图 |
| RQ1 | 更高的融资总额是否预示更高的退出率？ | Fig 2 · 堆叠柱状图 |
| RQ2 | 是否存在融资轮次的「门槛效应」？ | Fig 3 · 气泡图 |
| RQ3 | 融资速度与融资金额是否存在交互效应？ | Fig 4 · 热力图 |

## 仓库结构

```
.
├── preview_figures.py          # 主脚本——生成全部 4 张图 + HTML 预览
├── Reflection.md               # 反思报告（pandoc → PDF）
├── Reflection.pdf              # 渲染后的 PDF
├── Part D 思路.md               # 研究设计与方法论笔记
├── figures_preview.html        # 全部图表的交互式 HTML 预览
├── _fig1_pyecharts.html        # Fig 1 独立页面（pyecharts 矩形树图）
├── _fig4_heatmap.png           # Fig 4 导出的 PNG（seaborn）
├── fig{1,2,3,4}_placeholder.png  # 报告用的导出图片
├── Topic Selection/            # 前期选题与方向文档
├── Lecutres/                   # 每周讲座材料（第 2–5 周）
├── Datasets/                   # Crunchbase CSV 文件（已 gitignore，约 400 MB）
├── NAA1661 Data Scholarship Specification Feb. 2025.pdf
├── Reflection Template.doc
├── Group Presentation Template.pptx
└── seaborn.ipynb               # 探索性分析 notebook
```

## 技术栈

| 用途 | 工具 |
|------|------|
| 数据处理 | `pandas`、`numpy` |
| 可视化 | `pyecharts`（树图）、`plotly`（柱状图、气泡图）、`seaborn` + `matplotlib`（热力图） |
| 报告渲染 | `pandoc` + LaTeX → PDF |
| 图片导出 | `kaleido`（Plotly）、`matplotlib`（Fig 4） |

## 快速开始

```bash
# 1. 安装依赖
pip install pandas numpy plotly seaborn matplotlib pyecharts kaleido

# 2. 将 Crunchbase CSV 放入 Datasets/ 目录
#    需要: objects.csv, funding_rounds.csv, acquisitions.csv, ipos.csv

# 3. 生成图表 + 交互式预览
python preview_figures.py
# 浏览器打开 http://localhost:8765/figures_preview.html

# 4. 渲染反思报告为 PDF
pandoc Reflection.md -o Reflection.pdf --pdf-engine=pdflatex
```

## 图表说明

| 图表 | 描述 | 工具 |
|------|------|------|
| Fig 1 | 按行业与退出状态划分的 VC 初创企业分布 | pyecharts 矩形树图 |
| Fig 2 | 按融资总额区间分解的退出率（IPO vs. 收购） | Plotly 堆叠柱状图 + 双轴 |
| Fig 3 | 按融资轮次划分的退出率及门槛识别 | Plotly 气泡图 |
| Fig 4 | 融资速度 × 融资总量交互热力图 | seaborn 热力图 |
