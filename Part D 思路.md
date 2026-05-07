# Part D 数据分析工作流：数据分析六步骤

> **项目主题：** 全球创投版图与初创企业生存分析 (The Geography of Tech Capital)
> **核心问题：** 在 VC 机制下，资本投入如何转化为初创企业的长期商业价值？
> **角色：** Teammate D — 成长曲线分析 (Growth Curve Analysis)
> **技术栈：** Python · `pandas` · `plotly` · `pyecharts` · `numpy` · `scipy`

---

## 目录 (Table of Contents)

- [核心故事线](#核心故事线)
- [Step 1: 问题公式化与变量映射](#step-1-问题公式化与变量映射-problem-formulation--variable-mapping)
  - [1.1 概念框架](#11-概念框架-conceptual-framework)
  - [1.2 自变量定义](#12-自变量定义-independent-variables--the-input-capital-investment)
  - [1.3 因变量定义](#13-因变量定义-dependent-variables--the-output-long-term-commercial-value)
  - [1.4 核心研究问题](#14-核心研究问题-core-research-questions)
  - [1.5 变量关系与预期假设](#15-变量关系与预期假设-hypothesized-relationships)
- [Step 2: 数据采集与筛选](#step-2-数据采集与筛选-data-collection--filtering)
  - [2.1 目标数据源](#21-目标数据源)
  - [2.2 筛选策略](#22-筛选策略)
  - [2.3 行动指南](#23-行动指南)
- [Step 3: 数据清洗与预处理](#step-3-数据清洗与预处理-data-cleaning--preprocessing)
  - [3.1 缺失值处理](#31-缺失值处理-missing-values)
  - [3.2 去重](#32-去重-deduplication)
  - [3.3 极端值处理](#33-极端值处理-outlier-handling)
  - [3.4 融资类型隔离](#34-融资类型隔离-isolating-equity-financing)
  - [3.5 特征工程](#35-特征工程-feature-engineering)
- [Step 4: 探索性数据分析](#step-4-探索性数据分析-exploratory-data-analysis-eda)
  - [4.1 目标](#41-目标)
  - [4.2 描述性统计](#42-描述性统计-descriptive-statistics)
  - [4.3 EDA 可视化清单](#43-eda-可视化清单)
  - [4.4 与队友协作要点](#44-与队友协作要点)
- [Step 5: 核心分析与可视化](#step-5-核心分析与可视化-core-analysis--visualization)
  - [5.1 Fig 1 — EDA 概览（Plotly Subplots）](#51-fig-1--eda-概览plotly-subplots)
  - [5.2 Fig 2 — RQ1 融资总量与退出率（双轴 Bar + Line）](#52-fig-2--rq1-融资总量与退出率双轴-bar--line)
  - [5.3 Fig 3 — RQ2 融资轮次门槛效应（Scatter + 门槛标注）](#53-fig-3--rq2-融资轮次门槛效应scatter--门槛标注)
  - [5.4 Fig 4 — RQ3 融资速度交叉分析（Seaborn Heatmap）](#54-fig-4--rq3-融资速度交叉分析seaborn-heatmap)
- [Step 6: 解读与叙事](#step-6-解读与叙事-interpretation--storytelling)
  - [6.1 Presentation 脚本](#61-presentation-脚本)
  - [6.2 Reflection 写作框架](#62-reflection-写作框架)
  - [6.3 统计局限性](#63-统计局限性-statistical-limitations)
  - [6.4 最终检查清单](#64-最终检查清单-final-checklist)

---

## 核心故事线

**"Following the Money in Tech"** — 我们将跟随资本的脚步来观察科技生态。Part A 从全球地图开场，展示资金的空间分布；Part B 拉长时空，展示资金在不同历史阶段对不同赛道的追捧；Part C 回归现实，用图表揭示这些赛道中公司的真实存活比例；**Part D（本部分）总结收尾：资本的投入究竟如何转化为企业的长期商业价值。**

---

## Step 1: 问题公式化与变量映射 (Problem Formulation & Variable Mapping)

本步骤是整个分析的逻辑地基。我们需要将一个宽泛的商业问题——"资本投入如何转化为长期商业价值"——**操作化 (Operationalize)** 为可量化、可验证的变量关系。

### 1.1 概念框架 (Conceptual Framework)

```
┌─────────────────────────┐          ┌─────────────────────────┐
│   自变量 (Independent)   │          │   因变量 (Dependent)     │
│   Capital Investment     │ ──────▶ │   Long-term Value       │
│                          │         │                          │
│  · Volume  (融资总量)     │         │  · Status  (定性：终局状态)  │
│  · Milestones (融资轮次)  │         │  · Valuation (定量：估值价格)│
│  · Velocity (融资节奏)    │         │                          │
└─────────────────────────┘          └─────────────────────────┘
```

### 1.2 自变量定义 (Independent Variables — The Input: Capital Investment)

> 标注说明：I = 优先使用（数据易得、解释力强）；II = 可选补充（有分析价值但受限于数据可得性或优先级较低）

| 维度 | 优先级 | 变量名 | 数据类型 | 操作化定义 | 说明 |
|------|:------:|--------|----------|-----------|------|
| **Volume（体量）** | I | `Total_Funding_USD` | Continuous (Float) | 公司历史上所有**股权融资**轮次金额的累计总和（美元），**排除债务融资 (Debt) 和政府拨款 (Grant)**。 | 资本投入最直观的度量，反映投资者对企业的累计信心。原始数据中可能包含 `debt_financing` 和 `grant` 类型，必须在清洗阶段剔除。 |
| **Volume（体量）** | I | `Avg_Funding_Per_Round` | Continuous (Float) | 每轮平均融资额 = `Total_Funding_USD / Funding_Rounds`。 | 区分"大笔押注"与"涓涓细流"两种资本注入模式。同样 5000 万总融资，2 轮拿到 vs 8 轮拿到，资本密度截然不同——前者说明投资人高度看好，后者可能反映估值增长缓慢。 |
| **Volume（体量）** | II | `Last_Round_Size_USD` | Continuous (Float) | 最近一轮融资的金额。 | 反映市场对公司**当前状态**最新的估价信号（即"资本动量 Momentum"）。`Total_Funding_USD` 是历史累积，此变量捕捉最新快照。在 `funding_rounds.csv` 中筛选 `is_last_round=1` 的记录取 `raised_amount_usd` 获得（已在 3.5 表关联步骤中完成），但与 `Total_Funding_USD` 存在共线性 (Collinearity)，需谨慎使用。 |
| **Milestones（机制）** | I | `Funding_Rounds` | Discrete (Integer) | 公司完成的**股权融资轮次数**，即成功通过 Seed → A → B → C… 各阶段的次数。 | 每一轮融资都是一次市场对公司价值的"投票"。存活到更高轮次意味着多次通过了投资人的尽职调查 (Due Diligence)，是衡量企业韧性的代理指标 (Proxy)。 |
| **Milestones（机制）** | I | `Last_Round_Type` | Categorical (Ordinal) | 公司最后一轮融资的类型，取值为 `Seed` / `A` / `B` / `C` / `D+` / `PE`。 | 轮次**数量** ≠ 轮次**质量**。4 轮融资但停留在 Series A（多次 Bridge/Extension）与 4 轮到达 Series C，在 VC 阶梯上的"最高海拔"完全不同。此变量直接标记资本进程的质量。 |
| **Milestones（机制）** | II | `Has_PE_Round` | Binary (0/1) | 是否经历过 Private Equity 轮次。 | PE 轮是从 VC 进入 PE 的标志性转折，通常意味着公司已接近盈利或 IPO。但 Crunchbase 数据中 PE 轮标注不一定完整，且样本量可能偏少，作为辅助指标使用。 |
| **Velocity（速度）** | I | `Avg_Time_Between_Rounds` | Continuous (Float, 月) | 相邻两轮融资之间的**平均间隔时间**（月），计算方式为 `(最后一轮日期 - 首轮日期) / (轮次数 - 1)`。 | 融资节奏反映了资本消耗 (Burn Rate) 与业务迭代的速度。间隔短可能意味着业务增长快、市场竞争激烈；间隔长可能意味着公司在"精益运营"或遭遇了融资困难。 |
| **Velocity（速度）** | II | `Time_to_First_Funding` | Continuous (Float, 月) | 从公司成立 (`founded_at`) 到首轮融资的时间间隔。 | 衡量公司在"零外部资本"状态下的生存时长，反映创始团队的自举能力 (Bootstrapping) 和被市场发现的速度。与 `Avg_Time_Between_Rounds` 捕捉的是不同阶段的速度信号，但计算依赖 `founded_at` 字段的准确性（该字段常有缺失）。 |
| **Velocity（速度）** | II | `Funding_Span_Months` | Continuous (Float, 月) | 首轮融资到最后一轮融资的总时间跨度。 | `Avg_Time_Between_Rounds` 是均值，掩盖了总跨度信息。两家公司平均间隔都是 12 个月，但一家 2 轮（跨度 12 月）、另一家 6 轮（跨度 60 月）——后者在资本市场上存续更久。与 `Funding_Rounds` 有较强相关性，适合做补充交叉验证而非主力变量。 |

### 1.3 因变量定义 (Dependent Variables — The Output: Long-term Commercial Value)

| 维度 | 优先级 | 变量名 | 数据类型 | 操作化定义 | 说明 |
|------|:------:|--------|----------|-----------|------|
| **Categorical Status（定性状态）** | I | `Operating_Status` | Categorical (Nominal) | 公司的当前终局状态，取值为 `IPO`、`Acquired`、`Operating`、`Closed` 四类。 | 衡量"长期商业价值"最核心的分类标签。`IPO` 和 `Acquired` 代表成功退出 (Successful Exit)；`Operating` 代表仍在运营（结局未定）；`Closed` 代表失败。 |
| **Categorical Status（定性状态）** | I | `Exit_Success` | Binary (0/1) | 由 `Operating_Status` 派生：`IPO` + `Acquired` → 1（成功退出），`Operating` + `Closed` → 0。 | RQ1 和 RQ2 分析的**直接目标变量**。将四分类简化为二分类后，便于计算退出率、做分组对比，逻辑链更完整。应在变量映射阶段就正式声明，而非仅在特征工程阶段临时构造。 |
| **Continuous Valuation（定量估值）** | I | `Post_Money_Valuation` / `Acquisition_Price` | Continuous (Float) | 最后一轮融资后的投后估值 (Post-money Valuation)，或被收购时的实际交易价格 (Acquisition Price)。 | 衡量"长期商业价值"的连续性指标。由于数据可得性限制，此变量的缺失率通常很高，分析时需谨慎处理。 |
| **Continuous Valuation（定量估值）** | I | `Valuation_to_Funding_Ratio` | Continuous (Float) | 估值倍数 = `Post_Money_Valuation / Total_Funding_USD`。 | 直接衡量**资本效率 (Capital Efficiency)**——"每一美元资本投入创造了多少美元商业价值"。一家融 10 亿估值 12 亿 vs 融 500 万估值 5000 万，后者资本效率远高。这是回答核心问题"资本投入如何**转化为**长期价值"最精准的指标。 |
| **Continuous Valuation（定量估值）** | II | `Time_to_Exit_Months` | Continuous (Float, 月) | 从公司成立到退出事件（IPO 或 Acquired）的时间跨度。 | 量化"长期商业价值"中**"长期"**这个词。同样是 IPO，5 年上市 vs 15 年上市的资本回报时间价值 (Time Value) 完全不同。结合估值可构造"年化价值创造速度"，但仅适用于已退出公司的子集，样本量受限。 |

### 1.4 核心研究问题 (Core Research Questions)

> **设计原则：** 三个 RQ 从资本投入的**三个维度**（总量、轮次、速度）切入同一个因变量（`Exit_Success`），形成「三维度 × 同一 Y」的平行结构。所有图表的 Y 轴含义统一，观众只需理解一个概念即可。

**总研究问题 (Overarching RQ):**
> 在 VC 机制下，什么样的融资模式最可能带来成功退出（IPO 或 Acquired）？

#### RQ1：融了多少钱？— 融资总量与退出概率

| 项目 | 内容 |
|------|------|
| **维度** | Volume（资本体量） |
| **变量** | X = `Total_Funding_USD`（分箱为 `funding_bracket`：<1M / 1-10M / 10-50M / 50-100M / 100-500M / >500M）；Y = `Exit_Success`（Binary 0/1） |
| **统计方法** | `pd.cut` → `groupby` → 条件概率 P(Exit=1 \| Bracket) |
| **研究问题** | 不同融资总量区间的初创公司，成功退出率如何变化？是否存在一个退出率最高的"最优区间"，超过后增幅放缓？ |
| **预期结果** | 退出率先升后平（边际递减），中等融资区间表现最优 |

#### RQ2：融了几轮？— 融资轮次与退出概率的门槛效应

| 项目 | 内容 |
|------|------|
| **维度** | Milestones（资本进程） |
| **变量** | X = `Funding_Rounds`（Discrete Integer, 1–10+）；Y = `Exit_Success`（Binary 0/1） |
| **统计方法** | `groupby` → 逐轮条件概率 → 一阶差分 `.diff()` 定位门槛 |
| **研究问题** | 成功退出率是否在某一特定轮次后出现显著跳跃？该"门槛轮次"是第几轮？ |
| **预期结果** | 第 3–4 轮（约 Series B）处出现退出率跃升，之后趋于平稳 |

#### RQ3：融资多快？— 融资节奏与退出概率

| 项目 | 内容 |
|------|------|
| **维度** | Velocity（资本速度） |
| **变量** | X = `Avg_Time_Between_Rounds`（分箱：<6m / 6-12m / 12-24m / 24-48m / >48m）；Y = `Exit_Success`（Binary 0/1） |
| **统计方法** | `pd.cut` → `groupby` → 条件概率 P(Exit=1 \| Speed Bin) |
| **研究问题** | 融资间隔越短（迭代越快）的公司，退出率是否越高？是否存在一个最优融资节奏区间？ |
| **预期结果** | 间隔 6-24 个月的公司退出率最高；太快（<6m）或太慢（>48m）都不利 |

### 1.5 变量关系与预期假设 (Hypothesized Relationships)

| RQ | 维度 | 自变量 (X) | 因变量 (Y) | 预期关系 | 图表类型 |
|:---:|:---:|-----------|-----------|---------|---------|
| **RQ1** | Volume | `Total_Funding_USD` (bracket) | `Exit_Success` | 先升后平：边际递减效应 | **Fig 2**: 双轴柱状图 + 折线 |
| **RQ2** | Milestones | `Funding_Rounds` | `Exit_Success` | 非线性跳跃：门槛轮次后退出率骤升 | **Fig 3**: 气泡散点图 + 门槛标注 |
| **RQ3** | Velocity | `Avg_Time_Between_Rounds` (bin) | `Exit_Success` | 倒 U 型：中等节奏最优 | **Fig 4**: 交叉热力图 |

> **Fig 1**（EDA 概览）为描述性统计图，不对应特定 RQ，用于建立数据集的基础认知。

---

## Step 2: 数据采集与筛选 (Data Collection & Filtering)

### 2.1 目标数据源

本项目使用 Kaggle 上的 **Crunchbase 多表关系型数据集**（共 12 张表），所有文件位于 `Datasets/` 目录下。四个 Part **共享同一份原始数据集**，各自 JOIN 不同辅助表做分析。

#### 核心数据表（Part D 直接使用）

| 文件名 | 说明 | 粒度 | Part D 关键字段 |
|--------|------|------|----------------|
| **`objects.csv`** | 主实体表（公司、投资机构、人物等） | 一行 = 一个实体 | `id`, `entity_type`, `name`, `category_code`, `status`, `founded_at`, `closed_at`, `country_code`, `city`, `funding_total_usd`, `funding_rounds`, `first_funding_at`, `last_funding_at` |
| **`funding_rounds.csv`** | 逐轮融资记录 | 一行 = 一轮融资 | `object_id`, `funded_at`, `funding_round_type`, `funding_round_code`, `raised_amount_usd`, `post_money_valuation_usd`, `is_first_round`, `is_last_round` |
| **`acquisitions.csv`** | 收购交易记录 | 一行 = 一次收购 | `acquired_object_id`, `price_amount`, `price_currency_code`, `acquired_at` |
| **`ipos.csv`** | IPO 记录 | 一行 = 一次 IPO | `object_id`, `valuation_amount`, `valuation_currency_code`, `public_at` |

#### 辅助数据表（队友共享）

| 文件名 | 说明 | 适用 Part |
|--------|------|-----------|
| **`offices.csv`** | 公司办公地点（含 `latitude` / `longitude`） | **Part A** — Mapbox 密度图 |
| `investments.csv` / `investments_VC.csv` | 投资人 × 公司关联 | 可选 |
| `people.csv` / `relationships.csv` / `degrees.csv` | 创始人 / 团队信息 | 可选 |
| `milestones.csv` / `funds.csv` | 里程碑事件 / 基金层面数据 | 可选 |

#### 表间关联键

```
objects.id ──┬── funding_rounds.object_id
             ├── acquisitions.acquired_object_id
             ├── ipos.object_id
             └── offices.object_id
```

> ⚠️ `id` 格式为 `c:数字`（如 `c:1` 代表一家公司）。`objects.csv` 包含多种 `entity_type`（Company / FinancialOrg / Person），**必须先筛选 `entity_type == 'Company'`**。

### 2.2 筛选策略

```python
import pandas as pd
import numpy as np

# ============================================================
# 加载核心数据表
# ============================================================
objects = pd.read_csv('Datasets/objects.csv')
rounds  = pd.read_csv('Datasets/funding_rounds.csv')
acq     = pd.read_csv('Datasets/acquisitions.csv')
ipos    = pd.read_csv('Datasets/ipos.csv')

print(f"objects: {objects.shape}, rounds: {rounds.shape}, acq: {acq.shape}, ipos: {ipos.shape}")

# ============================================================
# 筛选公司主表
# ============================================================

# 0. 仅保留"公司"实体（排除 FinancialOrg / Person 等）
df = objects[objects['entity_type'] == 'Company'].copy()

# 1. 只保留有明确融资记录的公司
df = df[df['funding_total_usd'].notna() & (df['funding_total_usd'] > 0)]

# 2. 只保留状态明确的公司
df = df[df['status'].isin(['operating', 'ipo', 'acquired', 'closed'])]

# 3. 时间范围：聚焦有足够观察窗口的公司
df['founded_at'] = pd.to_datetime(df['founded_at'], errors='coerce')
df['founded_year'] = df['founded_at'].dt.year
df = df[(df['founded_year'] >= 2005) & (df['founded_year'] <= 2020)]

# 4. 地域：全量保留（与 Part A 地图呼应），或按需筛选
print(f"筛选后公司数: {len(df)}")
print(df['status'].value_counts())
```

### 2.3 行动指南

- 所有 Part **共享 `Datasets/` 目录下的同一份原始数据**，以 `objects.csv` 为核心主表：Part A JOIN `offices.csv` 获取地理坐标；Part B/C 直接使用 `objects.csv` 中的 `category_code` / `status`；Part D JOIN `funding_rounds.csv`、`acquisitions.csv`、`ipos.csv`。
- 加载后先用 `df.shape`、`df.info()`、`df.head()` 快速评估数据规模和质量。
- ⚠️ `objects.csv` 包含多种 `entity_type`，**所有 Part 的第一步都必须 `df = objects[objects['entity_type'] == 'Company']`**，确保分析口径一致。

---

## Step 3: 数据清洗与预处理 (Data Cleaning & Preprocessing)

### 3.1 缺失值处理 (Missing Values)

```python
# 检查公司主表缺失率
missing_report = df.isnull().sum() / len(df) * 100
print(missing_report.sort_values(ascending=False))

# 策略：
# - objects.csv 中 funding_total_usd, status 为核心字段，缺失则删除
# - founded_at 缺失会影响 Velocity 维度变量，但不影响 Volume/Milestones，暂保留
# - 后续 JOIN 的 post_money_valuation_usd, price_amount 等高缺失字段：不做填充，仅在子集分析中使用
df = df.dropna(subset=['funding_total_usd', 'status'])
```

### 3.2 去重 (Deduplication)

```python
# objects.csv 中每家公司有唯一 id（如 c:1），以此去重
df = df.drop_duplicates(subset=['id'], keep='first')
print(f"去重后剩余 {len(df)} 条记录")
```

### 3.3 极端值处理 (Outlier Handling)

```python
import numpy as np

# 使用 Z-score 方法识别极端值（阈值设为 ±5 标准差，因 VC 数据本身高度右偏）
from scipy import stats
z_scores = np.abs(stats.zscore(df['funding_total_usd'].dropna()))

# 标记但不直接删除 — 先观察极端值分布再决定
df['is_outlier'] = z_scores > 5

# 主分析中排除极端值，敏感性分析中保留
df_main = df[~df['is_outlier']]
print(f"排除 {df['is_outlier'].sum()} 个极端值，占比 {df['is_outlier'].mean():.2%}")
```

### 3.4 融资类型隔离 (Isolating Equity Financing)

```python
# funding_rounds.csv 中 funding_round_type 字段标识融资类型
# 常见取值: venture, angel, seed, series-a, series-b, series-c+, private_equity, debt_financing, grant 等
print(rounds['funding_round_type'].value_counts())

equity_types = ['venture', 'angel', 'seed', 'series-a', 'series-b', 'series-c+',
                'private_equity', 'undisclosed']
debt_types = ['debt_financing', 'grant', 'post_ipo_debt', 'post_ipo_equity']

# 仅保留股权类融资轮次（在 rounds 表上操作，而非公司主表）
rounds_equity = rounds[rounds['funding_round_type'].isin(equity_types)].copy()
print(f"股权融资轮次: {len(rounds_equity)} / 总轮次: {len(rounds)}")
```

### 3.5 特征工程 (Feature Engineering)

```python
# ============================================================
# PART A: 表关联 — 从辅助表聚合信息到公司主表
# ============================================================

# --- A1: 从 funding_rounds.csv 聚合逐轮信息 ---
rounds_equity['funded_at'] = pd.to_datetime(rounds_equity['funded_at'], errors='coerce')
rounds_equity['post_money_valuation_usd'] = rounds_equity['post_money_valuation_usd'].replace(0, np.nan)
rounds_equity['raised_amount_usd'] = rounds_equity['raised_amount_usd'].replace(0, np.nan)

# 按公司聚合：提取最后一轮的类型、金额、估值，以及是否有 PE 轮
round_agg = (
    rounds_equity
    .sort_values('funded_at')
    .groupby('object_id')
    .agg(
        last_round_type=('funding_round_type', 'last'),
        last_round_size=('raised_amount_usd', 'last'),
        last_round_valuation=('post_money_valuation_usd', 'last'),
        has_pe_round=('funding_round_type', lambda x: int('private_equity' in x.values)),
    )
    .reset_index()
)
df = df.merge(round_agg, left_on='id', right_on='object_id', how='left')

# --- A2: 合并 acquisitions.csv（收购价格 & 日期）---
acq_sub = acq[['acquired_object_id', 'price_amount', 'acquired_at']].copy()
acq_sub['price_amount'] = acq_sub['price_amount'].replace(0, np.nan)  # 0 = 未披露
acq_sub = acq_sub.rename(columns={
    'acquired_object_id': 'id',
    'price_amount': 'acquisition_price',
    'acquired_at': 'acquisition_date'
})
df = df.merge(acq_sub, on='id', how='left')

# --- A3: 合并 ipos.csv（IPO 估值 & 日期）---
ipos_sub = ipos[['object_id', 'valuation_amount', 'public_at']].copy()
ipos_sub['valuation_amount'] = ipos_sub['valuation_amount'].replace(0, np.nan)
ipos_sub = ipos_sub.rename(columns={
    'object_id': 'id',
    'valuation_amount': 'ipo_valuation',
    'public_at': 'ipo_date'
})
df = df.merge(ipos_sub, on='id', how='left')

print(f"合并后列数: {df.shape[1]}, 公司数: {len(df)}")

# ============================================================
# PART B: 因变量构造 (Dependent Variables)
# ============================================================

# 1. Exit_Success — 成功退出标签 (Binary)
df['exit_success'] = df['status'].isin(['ipo', 'acquired']).astype(int)

# 2. Valuation_to_Funding_Ratio — 资本效率 (Capital Efficiency)
#    使用最后一轮投后估值（来自 funding_rounds.csv）
df['valuation_to_funding_ratio'] = np.where(
    (df['funding_total_usd'] > 0) & (df['last_round_valuation'].notna()),
    df['last_round_valuation'] / df['funding_total_usd'],
    np.nan
)

# 3. Time_to_Exit_Months — 退出耗时 [优先级 II]
#    Acquired → acquisition_date; IPO → ipo_date
df['acquisition_date'] = pd.to_datetime(df['acquisition_date'], errors='coerce')
df['ipo_date'] = pd.to_datetime(df['ipo_date'], errors='coerce')
df['exit_date'] = df['acquisition_date'].fillna(df['ipo_date'])
df['time_to_exit_months'] = np.where(
    df['exit_date'].notna() & df['founded_at'].notna(),
    (df['exit_date'] - df['founded_at']).dt.days / 30,
    np.nan
)

# ============================================================
# PART C: 自变量构造 (Independent Variables)
# ============================================================

# 4. funding_bracket — 融资总量分箱 (Binning for Sub-RQ 1a)
df['funding_bracket'] = pd.cut(
    df['funding_total_usd'],
    bins=[0, 1e6, 1e7, 5e7, 1e8, 5e8, np.inf],
    labels=['<1M', '1-10M', '10-50M', '50-100M', '100-500M', '>500M']
)

# 5. Avg_Funding_Per_Round — 每轮平均融资额 (Volume 维度)
df['avg_funding_per_round'] = np.where(
    df['funding_rounds'] > 0,
    df['funding_total_usd'] / df['funding_rounds'],
    np.nan
)

# 6. Last_Round_Type 标准化排序 (Milestones 维度)
#    last_round_type 已通过 round_agg JOIN 获得
round_order = {'angel': 0, 'seed': 0.5, 'venture': 1,
               'series-a': 2, 'series-b': 3, 'series-c+': 4,
               'private_equity': 5}
df['last_round_type_rank'] = df['last_round_type'].str.lower().map(round_order)

# 7. has_pe_round 已通过 round_agg JOIN 获得 [优先级 II]

# 8. Avg_Time_Between_Rounds — 平均融资间隔 (Velocity 维度)
#    objects.csv 已有 first_funding_at / last_funding_at
df['first_funding_at'] = pd.to_datetime(df['first_funding_at'], errors='coerce')
df['last_funding_at'] = pd.to_datetime(df['last_funding_at'], errors='coerce')
df['avg_time_between_rounds'] = np.where(
    df['funding_rounds'] > 1,
    (df['last_funding_at'] - df['first_funding_at']).dt.days / 30 / (df['funding_rounds'] - 1),
    np.nan
)

# 9. Time_to_First_Funding — 首轮融资耗时 [优先级 II]
df['time_to_first_funding'] = np.where(
    df['first_funding_at'].notna() & df['founded_at'].notna(),
    (df['first_funding_at'] - df['founded_at']).dt.days / 30,
    np.nan
)

# 10. Funding_Span_Months — 融资总跨度 [优先级 II]
df['funding_span_months'] = np.where(
    df['last_funding_at'].notna() & df['first_funding_at'].notna(),
    (df['last_funding_at'] - df['first_funding_at']).dt.days / 30,
    np.nan
)

print(f"特征工程完成，最终变量数: {df.shape[1]}")
```

---

## Step 4: 探索性数据分析 (Exploratory Data Analysis, EDA)

### 4.1 目标

在进入深度分析之前，先对数据的**分布形态 (Distribution)**、**集中趋势 (Central Tendency)** 和**离散程度 (Dispersion)** 建立直觉。

### 4.2 描述性统计 (Descriptive Statistics)

```python
# 核心变量的五数概括（覆盖所有 Priority I 连续变量）
priority_i_vars = ['funding_total_usd', 'avg_funding_per_round',
                   'funding_rounds', 'avg_time_between_rounds']
print(df[priority_i_vars].describe())

# Priority II 连续变量（可选，检查数据可得性）
priority_ii_vars = ['last_round_size_usd', 'time_to_first_funding',
                    'funding_span_months', 'time_to_exit_months']
for col in priority_ii_vars:
    if col in df.columns:
        print(f"\n--- {col} ---")
        print(df[col].describe())

# 各状态类别的频数
print(df['status'].value_counts(normalize=True))

# Exit_Success 基础比例
print(f"\n成功退出率: {df['exit_success'].mean():.2%}")

# Last_Round_Type 分布（Milestones 维度）
print(df['last_round_type'].value_counts())

# 分组描述：各状态下的融资总量 & 资本效率
print(df.groupby('status')[['funding_total_usd', 'avg_funding_per_round']].describe())
print(df.groupby('status')['valuation_to_funding_ratio'].describe())
```

### 4.3 EDA 可视化清单

| 图表 | 工具 | 目的 | 对应变量 | 优先级 |
|------|------|------|---------|:------:|
| **融资总量直方图 (Histogram)** | `plotly.express.histogram` | 观察 `Total_Funding_USD` 的分布形态（预期高度右偏），决定是否需要对数变换 | `funding_total_usd` | I |
| **状态饼图 / 柱状图** | `plotly.express.pie` / `bar` | 了解 IPO / Acquired / Operating / Closed 的基础比例及 `Exit_Success` 的基线概率 | `status`, `exit_success` | I |
| **每轮平均融资额直方图** | `plotly.express.histogram` | 观察 `Avg_Funding_Per_Round` 的分布，识别"大笔押注"与"涓涓细流"两类公司 | `avg_funding_per_round` | I |
| **最后轮次类型柱状图** | `plotly.express.bar` | 了解 `Last_Round_Type` 在各状态分组中的分布差异 | `last_round_type` × `status` | I |
| **箱线图 (Box Plot)** | `plotly.express.box` | 对比不同 `status` 分组下的融资总量和资本效率分布差异 | `status` × `funding_total_usd`, `status` × `valuation_to_funding_ratio` | I |
| **对数散点图 (Log Scatter)** | `plotly.express.scatter` | 初步观察 `funding_total_usd` 与 `funding_rounds` 的关系 | 两个自变量之间 | I |
| **融资间隔直方图** | `plotly.express.histogram` | 观察 `Avg_Time_Between_Rounds` 的分布，按 `status` 着色 | `avg_time_between_rounds` × `status` | I |
| **首轮融资耗时直方图** | `plotly.express.histogram` | 观察 `Time_to_First_Funding` 的分布形态 | `time_to_first_funding` | II |
| **融资跨度 vs 轮次散点图** | `plotly.express.scatter` | 检验 `Funding_Span_Months` 与 `Funding_Rounds` 的共线性 | `funding_span_months` × `funding_rounds` | II |

```python
import plotly.express as px

# 示例 1：融资总量对数直方图（按状态着色）
fig = px.histogram(
    df, x='funding_total_usd', nbins=50,
    log_x=True,
    color='status',
    title='Distribution of Total Funding (Log Scale) by Status',
    labels={'funding_total_usd': 'Total Funding (USD, Log Scale)'}
)
fig.show()

# 示例 2：每轮平均融资额箱线图（按状态分组）
fig = px.box(
    df, x='status', y='avg_funding_per_round',
    log_y=True,
    color='status',
    title='Avg Funding Per Round by Operating Status',
    labels={'avg_funding_per_round': 'Avg Funding Per Round (USD, Log Scale)'}
)
fig.show()

# 示例 3：最后轮次类型 × 退出状态堆叠柱状图
round_status = df.groupby(['last_round_type', 'status']).size().reset_index(name='count')
fig = px.bar(
    round_status, x='last_round_type', y='count', color='status',
    title='Operating Status Distribution by Last Round Type',
    labels={'last_round_type': 'Last Funding Round Type'}
)
fig.show()
```

### 4.4 与队友协作要点

- 与 **Part A** 共享 `objects.csv`，Part A 额外 JOIN `offices.csv`（含 `latitude` / `longitude`）。确保双方对 `entity_type == 'Company'` 和 `funding_total_usd > 0` 的筛选口径一致。
- 与 **Part C** 对齐 `objects.csv` 中 `status` 字段的分类逻辑（存活率的定义需统一：`closed` = 失败，`operating` = 存续，`ipo` + `acquired` = 成功退出）。
- 与 **Part B** 确认 `category_code` 的赛道分类粒度（是否需要合并细分类别）。
- EDA 阶段的发现应在小组会议中分享，以便动态调整各自的分析方向。

---

## Step 5: 核心分析与可视化 (Core Analysis & Visualization)

> **策略：** 4 张图 = 1 EDA 概览 + 3 RQ 分析。每张图使用**不同的图表类型和包**，展示 learning outcomes 的广度。**全部 4 张图写入 Reflection**；从中选 **Fig 2 + Fig 3** 在 Presentation 中讲解（最易口头阐述、视觉冲击最强）。

| Fig | 对应 | 图表类型 | 包 | 技能展示 |
|:---:|:---:|---------|:---:|---------|
| **Fig 1** | EDA 概览 | Subplots（Histogram + Pie） | `plotly.subplots` + `plotly.graph_objects` | Plotly 底层 API、多图布局 |
| **Fig 2** | RQ1 | 双轴 Bar + Line | `plotly.graph_objects` + `make_subplots` | 双 Y 轴、参考线、标注 |
| **Fig 3** | RQ2 | 气泡散点图 + 区域标注 | `plotly.express` | size/color 映射、`add_vline`/`add_vrect` |
| **Fig 4** | RQ3 | 带标注热力图 | `seaborn` + `matplotlib` | `pivot_table`、`sns.heatmap(annot=True)` |

---

### 5.1 Fig 1 — EDA 概览（Plotly Subplots）

**目的：** 建立数据集的基础认知——融资总量的分布形态 + 公司状态的基线比例。

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np

# ============================================================
# Fig 1: Subplots — 左: 融资分布直方图, 右: 状态饼图
# ============================================================
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "histogram"}, {"type": "pie"}]],
    subplot_titles=["Total Funding Distribution (Log Scale)", "Company Status Breakdown"],
    column_widths=[0.6, 0.4]
)

# 左图：按状态着色的对数直方图
colors = {'operating': '#95a5a6', 'acquired': '#3498db', 'ipo': '#2ecc71', 'closed': '#e74c3c'}
for status in ['operating', 'acquired', 'ipo', 'closed']:
    sub = df[df['status'] == status]
    fig.add_trace(
        go.Histogram(x=np.log10(sub['funding_total_usd']),
                     name=status.capitalize(), marker_color=colors[status],
                     opacity=0.7, nbinsx=30),
        row=1, col=1
    )

# 右图：状态饼图
counts = df['status'].value_counts()
fig.add_trace(
    go.Pie(labels=[s.capitalize() for s in counts.index],
           values=counts.values,
           marker_colors=[colors[s] for s in counts.index],
           textinfo='label+percent'),
    row=1, col=2
)

fig.update_layout(
    title_text="Fig 1: Dataset Overview — Funding Distribution & Status Composition",
    height=450, showlegend=True,
    legend=dict(orientation='h', yanchor='bottom', y=-0.2)
)
fig.update_xaxes(title_text="log₁₀(Total Funding USD)", row=1, col=1)
fig.update_yaxes(title_text="Count", row=1, col=1)
fig.show()
```

**一句话结论：** "数据集中 X% 的公司成功退出（IPO + Acquired），融资总量呈对数正态分布。"

---

### 5.2 Fig 2 — RQ1 融资总量与退出率（双轴 Bar + Line）

**目的：** 回答"融了多少钱影响成功率吗？"——用双轴同时展示退出率（主轴）和样本量（副轴），避免少样本区间误导。

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# ============================================================
# 数据准备
# ============================================================
exit_by_bracket = (
    df.groupby('funding_bracket', observed=True)['exit_success']
    .agg(['mean', 'count'])
    .rename(columns={'mean': 'exit_rate', 'count': 'n_companies'})
    .reset_index()
)

overall_rate = df['exit_success'].mean()

# ============================================================
# Fig 2: 双轴 — 柱状图(退出率) + 折线图(样本量)
# ============================================================
fig = make_subplots(specs=[[{"secondary_y": True}]])

# 主轴：退出率柱状图
fig.add_trace(
    go.Bar(x=exit_by_bracket['funding_bracket'],
           y=exit_by_bracket['exit_rate'],
           name='Exit Rate',
           marker_color='#3498db',
           text=[f"{r:.1%}" for r in exit_by_bracket['exit_rate']],
           textposition='outside'),
    secondary_y=False
)

# 副轴：样本量折线
fig.add_trace(
    go.Scatter(x=exit_by_bracket['funding_bracket'],
               y=exit_by_bracket['n_companies'],
               name='Sample Size (n)',
               mode='lines+markers',
               line=dict(color='#e74c3c', dash='dot', width=2),
               marker=dict(size=8)),
    secondary_y=True
)

# 水平参考线：全局平均退出率
fig.add_hline(y=overall_rate, line_dash='dash', line_color='gray',
              annotation_text=f"Overall avg: {overall_rate:.1%}",
              secondary_y=False)

# 峰值标注
peak_idx = exit_by_bracket['exit_rate'].idxmax()
peak = exit_by_bracket.iloc[peak_idx]
fig.add_annotation(
    x=peak['funding_bracket'], y=peak['exit_rate'],
    text=f"Peak: {peak['exit_rate']:.1%}",
    showarrow=True, arrowhead=2, ax=0, ay=-30,
    font=dict(color='#2c3e50', size=12)
)

fig.update_layout(
    title_text="Fig 2 (RQ1): Exit Success Rate by Total Funding Bracket",
    height=500, legend=dict(orientation='h', yanchor='bottom', y=-0.2)
)
fig.update_yaxes(title_text="Exit Success Rate", tickformat='.0%', secondary_y=False)
fig.update_yaxes(title_text="Number of Companies", secondary_y=True)
fig.show()
```

**一句话结论：** "融资在 [X–Y] 区间的公司退出率最高 (Z%)，超过该区间后退出率增幅放缓——不是越多越好。"

---

### 5.3 Fig 3 — RQ2 融资轮次门槛效应（Scatter + 门槛标注）

**目的：** 回答"第几轮是分水岭？"——用气泡大小编码样本量，颜色编码退出率，垂直线+区域标注门槛位置。

```python
import plotly.express as px

# ============================================================
# 数据准备
# ============================================================
exit_by_round = (
    df.groupby('funding_rounds')['exit_success']
    .agg(['mean', 'count'])
    .rename(columns={'mean': 'exit_rate', 'count': 'n_companies'})
    .reset_index()
)
exit_by_round = exit_by_round[exit_by_round['n_companies'] >= 30]

# 一阶差分定位门槛
exit_by_round['delta'] = exit_by_round['exit_rate'].diff()
threshold_round = int(exit_by_round.loc[exit_by_round['delta'].idxmax(), 'funding_rounds'])

# ============================================================
# Fig 3: 气泡散点 + 门槛区域标注
# ============================================================
fig = px.scatter(
    exit_by_round, x='funding_rounds', y='exit_rate',
    size='n_companies', color='exit_rate',
    color_continuous_scale='RdYlGn',
    size_max=40,
    title=f"Fig 3 (RQ2): Exit Rate by Funding Rounds — Threshold at Round {threshold_round}",
    labels={'exit_rate': 'Exit Success Rate', 'funding_rounds': 'Number of Funding Rounds',
            'n_companies': 'Sample Size'}
)

# 门槛左侧灰色区域
fig.add_vrect(x0=0.5, x1=threshold_round - 0.5,
              fillcolor='gray', opacity=0.08,
              annotation_text='Below Threshold', annotation_position='top left')

# 门槛右侧绿色区域
fig.add_vrect(x0=threshold_round - 0.5, x1=exit_by_round['funding_rounds'].max() + 0.5,
              fillcolor='green', opacity=0.05,
              annotation_text='Above Threshold', annotation_position='top right')

# 门槛垂直线
fig.add_vline(x=threshold_round, line_dash='dash', line_color='red', line_width=2)

fig.update_layout(height=500)
fig.update_yaxes(tickformat='.0%')
fig.show()

print(f"门槛轮次: 第 {threshold_round} 轮 (Δ = {exit_by_round.loc[exit_by_round['delta'].idxmax(), 'delta']:.1%})")
```

**一句话结论：** "第 N 轮是分水岭——退出率从该轮前的 X% 跃升至 Y%，增幅达 Z 个百分点。"

---

### 5.4 Fig 4 — RQ3 融资速度交叉分析（Seaborn Heatmap）

**目的：** 回答"融资间隔多长最好？"——同时交叉 RQ1 的融资区间维度，用热力图展示二维交互效应。

```python
import seaborn as sns
import matplotlib.pyplot as plt

# ============================================================
# 数据准备：分箱融资速度
# ============================================================
df['speed_bin'] = pd.cut(
    df['avg_time_between_rounds'],
    bins=[0, 6, 12, 24, 48, np.inf],
    labels=['<6m', '6-12m', '12-24m', '24-48m', '>48m']
)

# 交叉透视表：融资区间 × 融资速度 → 退出率
heatmap_data = df.pivot_table(
    index='funding_bracket',
    columns='speed_bin',
    values='exit_success',
    aggfunc='mean'
)

# 样本量表（用于标注）
count_data = df.pivot_table(
    index='funding_bracket',
    columns='speed_bin',
    values='exit_success',
    aggfunc='count'
).fillna(0).astype(int)

# ============================================================
# Fig 4: Seaborn 带标注热力图
# ============================================================
plt.figure(figsize=(10, 6))

# 构造标注文本：退出率 + 样本量
annot_text = heatmap_data.copy()
for i in range(heatmap_data.shape[0]):
    for j in range(heatmap_data.shape[1]):
        rate = heatmap_data.iloc[i, j]
        n = count_data.iloc[i, j]
        if pd.notna(rate):
            annot_text.iloc[i, j] = f"{rate:.1%}\n(n={n})"
        else:
            annot_text.iloc[i, j] = "—"

ax = sns.heatmap(
    heatmap_data, annot=annot_text.values, fmt='',
    cmap='RdYlGn', linewidths=0.5,
    vmin=0, vmax=heatmap_data.max().max(),
    cbar_kws={'label': 'Exit Success Rate', 'format': '%.0%%'}
)

plt.title("Fig 4 (RQ3): Exit Rate by Funding Speed × Funding Amount", fontsize=13, pad=15)
plt.xlabel("Avg Time Between Rounds", fontsize=11)
plt.ylabel("Total Funding Bracket", fontsize=11)
plt.tight_layout()
plt.show()
```

**一句话结论：** "融资间隔在 6-24 个月的公司退出率最高；该规律在不同融资区间中保持一致。"

**额外亮点：** 这张热力图**同时验证了 RQ1 和 RQ3**——从 Y 轴看是 RQ1（融资区间效应），从 X 轴看是 RQ3（融资速度效应），交叉位置揭示二者的交互关系。

---

## Step 6: 解读与叙事 (Interpretation & Storytelling)

### 6.1 Presentation 脚本

Part D 是你在 Group Presentation 中负责的章节（约 2.5–3 分钟）。从 4 张图中选 **Fig 2 + Fig 3** 进行口头讲解。

| 时间 | 内容 | 展示图 | 你说的话 |
|------|------|:------:|---------|
| 0:00-0:20 | **引入** | — | "前面几位同学展示了资本的全球分布和行业趋势。我来回答最后一个问题：**什么样的融资模式最可能带来成功？** 我们从三个维度来看。" |
| 0:20-1:10 | **RQ1** | **Fig 2** | "这张图的 X 轴是融资总量区间，Y 轴是成功退出率。可以看到退出率**先升后平**——融资在 [X-Y] 区间的公司退出率最高，达到 Z%。超过这个区间后退出率不再上升。虚线是全局平均水平。**不是越多越好。**" |
| 1:10-2:00 | **RQ2** | **Fig 3** | "接下来看融资轮次。每个气泡代表一个轮次，大小是样本量，颜色是退出率。注意**第 N 轮这条红线**——在它左边退出率很低，右边明显跃升。也就是说，**能走到第 N 轮本身就是一种市场筛选信号。**" |
| 2:00-2:30 | **RQ3 + 总结** | — (口头) | "我们还分析了融资速度——间隔 6-24 个月的公司退出率最高，太快或太慢都不好。所以结论是：**适度的融资总量 + 足够的轮次筛选 + 合理的融资节奏**，共同指向最高的成功概率。更多细节请参考我的 Reflection。" |

### 6.2 Reflection 写作框架

个人 Reflection，500-1000 词，**全部 4 张图**。建议分配：

| 部分 | 约词数 | 内容 | 对应图 |
|------|:------:|------|:------:|
| **Introduction** | ~100 | 研究问题 + 数据来源简介 | — |
| **Method** | ~200 | 数据源（Crunchbase 多表 JOIN）、筛选策略、分箱方法、工具 | Fig 1 |
| **Result** | ~350 | RQ1 结果 + RQ2 结果 + RQ3 结果，每个约 100 词 | Fig 2, 3, 4 |
| **Discussion** | ~200 | 解读 + 至少 2 项局限性声明 | — |
| **References** | — | 5-10 个 | — |

> **关键提示：** Result 只陈述事实（"X 区间退出率为 38%"），Discussion 才做解读（"这可能是因为…"）。

### 6.3 统计局限性 (Statistical Limitations)

| 局限性 | 英文术语 | 建议 Reflection 措辞 |
|--------|---------|---------------------|
| **幸存者偏差** | Survivor Bias | "Our dataset suffers from survivor bias — companies that failed before receiving any funding are absent." |
| **相关非因果** | Correlation ≠ Causation | "The correlation between funding volume and exit success does not imply causation. Confounders such as founder quality and market timing may drive both." |
| **时间截断** | Right Censoring | "Companies in 'Operating' status represent right-censored observations whose final outcome is unknown." |

### 6.4 最终检查清单 (Final Checklist)

- [ ] **Fig 1** (Subplots): 直方图 + 饼图双图合一，标题/轴标签完整
- [ ] **Fig 2** (双轴 Bar+Line): 退出率柱 + 样本量线 + 参考线 + 峰值标注
- [ ] **Fig 3** (气泡散点): size=样本量, color=退出率, 门槛区域标注
- [ ] **Fig 4** (Heatmap): `pivot_table` 交叉表 + `annot=True` + colorbar
- [ ] 每张图有**一句话结论 (One-line Takeaway)**
- [ ] 代码可复现：`.ipynb` 从上到下 `Restart & Run All` 无报错
- [ ] Reflection: 500-1000 词，Result 与 Discussion 严格分离
- [ ] 已声明至少 2 项统计局限性
- [ ] 与队友数据口径对齐（`entity_type == 'Company'`、`status` 分类）
- [ ] Presentation 脚本已排练，控制在 2.5-3 分钟内

---

*文档版本：v2.0 | 创建日期：2026-04-28 | 更新日期：2026-05-06 | 适用于 NAA1661 Data Scholarship Final Project*
*v2.0 更新：基于 Reflection 字数限制（500-1000 词）和图片限制（4 张），将 10 个 Sub-RQ 精简为 3 个核心 RQ（Volume / Milestones / Velocity → Exit Success），重新设计 4 张图表（覆盖 plotly.subplots / plotly.graph_objects / plotly.express / seaborn），Step 5-6 完全重写对齐。*