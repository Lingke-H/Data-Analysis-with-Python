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
- [Step 5: 深度分析与建模](#step-5-深度分析与建模-in-depth-analysis--modeling)
  - [5.1 RQ1 分析：融资总量与退出概率](#51-rq1-分析融资总量与退出概率)
  - [5.2 RQ2 分析：融资轮次的门槛效应](#52-rq2-分析融资轮次的门槛效应)
  - [5.3 RQ3 分析：融资节奏与收购价格](#53-rq3-分析融资节奏与收购价格)
  - [5.4 补充分析](#54-补充分析可选)
    - [5.4.1 资本效率分析](#541-资本效率分析-capital-efficiency--valuation_to_funding_ratio)
    - [5.4.2 Priority II 变量探索](#542-priority-ii-变量探索)
    - [5.4.3 可视化增强](#543-可视化增强可选)
- [Step 6: 解读与叙事](#step-6-解读与叙事-interpretation--storytelling)
  - [6.1 从数据到故事的转化框架](#61-从数据到故事的转化框架)
  - [6.2 Reflection Document 写作指南](#62-reflection-document-写作指南)
  - [6.3 必须声明的统计局限性](#63-必须声明的统计局限性-statistical-limitations)
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

基于上述变量映射，我们的 Part D 分析将围绕以下三个逐层递进的研究问题展开：

> **RQ1（体量 × 状态）：融资总量与退出概率**
> 在不同的 `Total_Funding_USD` 区间内，初创公司达到 `IPO` 或 `Acquired` 状态的概率如何变化？是否存在一个"资本甜蜜点 (Sweet Spot)"？

> **RQ2（机制 × 生存）：融资轮次的门槛效应**
> 初创公司的存活概率是否在到达某一特定融资轮次（例如 Series B）后出现显著跳跃？即是否存在一个 **"Threshold Effect（门槛效应）"**？

> **RQ3（速度 × 估值）：融资节奏与最终价值**
> 融资速度 (`Avg_Time_Between_Rounds`) 与最终的 `Acquisition_Price` 之间存在怎样的相关关系？更快的融资节奏是否对应更高的退出价格？

### 1.5 变量关系与预期假设 (Hypothesized Relationships)

| 研究问题 | 自变量 | 因变量 | 预期关系 | 可视化方案 |
|---------|--------|--------|---------|-----------|
| RQ1 | `Total_Funding_USD`（分箱后） | `Exit_Success_Rate` | 正相关，但可能存在边际递减：初期资金越多退出率越高，超过某阈值后增幅放缓 | **Plotly 分组柱状图** (Grouped Bar Chart) |
| RQ2 | `Funding_Rounds` | `Survival_Rate` by round | 非线性跳跃：早期轮次间存活率陡降，B 轮之后趋于稳定 | **Plotly 折线图** (Line Chart with markers) |
| RQ3 | `Avg_Time_Between_Rounds` | `Acquisition_Price` | 负相关：融资间隔越短（迭代越快），收购价格可能越高 | **Plotly 散点图** (Scatter Plot with trendline) |

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

# 4. funding_bracket — 融资总量分箱 (Binning for RQ1)
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

## Step 5: 深度分析与建模 (In-depth Analysis & Modeling)

> ⚠️ **策略原则：** 本项目面向 Data Scholarship 课程，听众包括非统计背景的同学和评委。因此我们采用 **"描述性统计 + 分组对比 + 可视化叙事"** 的路线，避免使用复杂的机器学习模型。所有发现都必须能用**一句话 + 一张图**向非专业听众解释清楚。

### 5.1 RQ1 分析：融资总量与退出概率

**方法：** 分箱 (Binning) → 分组聚合 (`groupby`) → 计算成功退出率 → 柱状图

```python
# 计算每个融资区间的成功退出率
exit_by_bracket = (
    df.groupby('funding_bracket')['exit_success']
    .agg(['mean', 'count'])
    .rename(columns={'mean': 'exit_rate', 'count': 'n_companies'})
    .reset_index()
)

# 可视化
fig = px.bar(
    exit_by_bracket, x='funding_bracket', y='exit_rate',
    text='n_companies',
    title='RQ1: Exit Success Rate by Funding Bracket',
    labels={'exit_rate': 'Successful Exit Rate', 'funding_bracket': 'Total Funding Bracket'}
)
fig.update_traces(texttemplate='n=%{text}', textposition='outside')
fig.show()
```

**关注点：** 观察是否存在"边际递减效应"——更多资金不一定对应更高的成功率。

**补充维度：** 在 `funding_bracket` 分组基础上，叠加 `Avg_Funding_Per_Round` 的中位数对比，验证"资本密度"是否比"资本总量"更能预测退出结果。

```python
# 补充：各融资区间内的平均每轮融资额中位数
bracket_density = (
    df.groupby('funding_bracket')
    .agg(
        exit_rate=('exit_success', 'mean'),
        median_avg_per_round=('avg_funding_per_round', 'median'),
        n_companies=('exit_success', 'count')
    )
    .reset_index()
)
print(bracket_density)
```

### 5.2 RQ2 分析：融资轮次的门槛效应

**方法：** 计算到达每一轮的公司中，最终存活（非 `Closed`）的比例 → 折线图

```python
# 计算每个轮次的存活率
survival_by_round = (
    df.groupby('funding_rounds')
    .apply(lambda x: pd.Series({
        'survival_rate': (x['status'] != 'closed').mean(),
        'exit_rate': x['exit_success'].mean(),
        'n_companies': len(x)
    }))
    .reset_index()
)

# 仅保留样本量 ≥ 30 的轮次（确保统计意义）
survival_by_round = survival_by_round[survival_by_round['n_companies'] >= 30]

# 可视化
fig = px.line(
    survival_by_round, x='funding_rounds', y='survival_rate',
    markers=True,
    title='RQ2: Survival Rate by Number of Funding Rounds (Threshold Effect)',
    labels={'survival_rate': 'Survival Rate (Non-Closed)', 'funding_rounds': 'Number of Funding Rounds'}
)
fig.add_hline(y=0.8, line_dash="dash", line_color="red", annotation_text="80% Threshold")
fig.show()
```

**关注点：** 寻找曲线上的**拐点 (Inflection Point)**，即存活率从快速上升转为平缓的那个轮次。

**补充维度：** 用 `Last_Round_Type` 替代纯数量的 `Funding_Rounds`，从"轮次质量"角度验证门槛效应。如果数据显示 `Last_Round_Type = Series B` 的存活率出现跳跃，则同时从数量和质量两个角度交叉印证了门槛效应。

```python
# 补充：按 Last_Round_Type 计算存活率与退出率
survival_by_type = (
    df.groupby('last_round_type')
    .apply(lambda x: pd.Series({
        'survival_rate': (x['status'] != 'closed').mean(),
        'exit_rate': x['exit_success'].mean(),
        'n_companies': len(x)
    }))
    .reset_index()
    .sort_values('last_round_type_rank' if 'last_round_type_rank' in df.columns else 'exit_rate')
)

# 可视化：按轮次类型的存活率（有序排列）
fig = px.bar(
    survival_by_type, x='last_round_type', y=['survival_rate', 'exit_rate'],
    barmode='group', text='n_companies',
    title='RQ2 Supplement: Survival & Exit Rate by Last Round Type',
    labels={'value': 'Rate', 'last_round_type': 'Last Funding Round Type'}
)
fig.show()
```

### 5.3 RQ3 分析：融资节奏与收购价格

**方法：** 筛选 `Acquired` 子集 → 计算 `Avg_Time_Between_Rounds` → 散点图 + 趋势线

```python
# 筛选已被收购且有价格数据的公司
# acquisition_price 来自 acquisitions.csv (price_amount)，已在 3.5 中 JOIN 到 df
df_acquired = df[
    (df['status'] == 'acquired') &
    (df['acquisition_price'].notna()) &
    (df['avg_time_between_rounds'].notna())
]
print(f"有收购价格 + 融资间隔数据的公司: {len(df_acquired)}")

# 可视化
fig = px.scatter(
    df_acquired,
    x='avg_time_between_rounds',
    y='acquisition_price',
    log_y=True,  # 收购价格高度右偏，使用对数刻度
    trendline='ols',  # 叠加 OLS 回归趋势线
    hover_data=['name'],  # objects.csv 中的公司名字段为 name
    title='RQ3: Funding Velocity vs. Acquisition Price',
    labels={
        'avg_time_between_rounds': 'Avg. Time Between Rounds (Months)',
        'acquisition_price': 'Acquisition Price (USD, Log Scale)'
    }
)
fig.show()
```

**关注点：** `acquisitions.csv` 中 `price_amount` 大量为 0（未披露），已在 3.5 中替换为 NaN。实际可用样本量可能有限，结论需谨慎表述。

### 5.4 补充分析（可选）

#### 5.4.1 资本效率分析 (Capital Efficiency) — `Valuation_to_Funding_Ratio`

这是对 RQ1-RQ3 最有力的补充收尾。即使不构成独立 RQ，也可以在 Presentation 中作为"最终洞察"展示。

```python
# 筛选有估值数据的公司
df_valued = df[df['valuation_to_funding_ratio'].notna() & (df['valuation_to_funding_ratio'] > 0)]

# 按融资区间计算资本效率中位数
efficiency_by_bracket = (
    df_valued.groupby('funding_bracket')['valuation_to_funding_ratio']
    .median()
    .reset_index()
    .rename(columns={'valuation_to_funding_ratio': 'median_ratio'})
)

fig = px.bar(
    efficiency_by_bracket, x='funding_bracket', y='median_ratio',
    title='Capital Efficiency: Median Valuation-to-Funding Ratio by Bracket',
    labels={'median_ratio': 'Median Valuation / Total Funding', 'funding_bracket': 'Total Funding Bracket'}
)
fig.show()

# 按 Last_Round_Type 查看资本效率
efficiency_by_round = (
    df_valued.groupby('last_round_type')['valuation_to_funding_ratio']
    .median()
    .reset_index()
    .rename(columns={'valuation_to_funding_ratio': 'median_ratio'})
)
fig = px.bar(
    efficiency_by_round, x='last_round_type', y='median_ratio',
    title='Capital Efficiency by Last Round Type',
    labels={'median_ratio': 'Median Valuation / Total Funding'}
)
fig.show()
```

#### 5.4.2 Priority II 变量探索

以下分析依赖于数据可得性，视实际字段完整度决定是否纳入最终 Presentation：

```python
# (a) Time_to_First_Funding × Exit_Success — 首轮融资速度是否预测成功退出？
if 'time_to_first_funding' in df.columns:
    df['first_funding_speed'] = pd.cut(
        df['time_to_first_funding'],
        bins=[0, 6, 12, 24, 60, np.inf],
        labels=['<6m', '6-12m', '1-2y', '2-5y', '>5y']
    )
    speed_exit = df.groupby('first_funding_speed')['exit_success'].agg(['mean', 'count']).reset_index()
    print(speed_exit)

# (b) Has_PE_Round × Exit_Success — 经历 PE 轮的公司是否更容易成功退出？
if 'has_pe_round' in df.columns:
    pe_comparison = df.groupby('has_pe_round')['exit_success'].agg(['mean', 'count'])
    print(pe_comparison)

# (c) Time_to_Exit_Months — 成功退出公司的"速度"分布
if 'time_to_exit_months' in df_exited.columns:
    fig = px.histogram(
        df_exited, x='time_to_exit_months', nbins=30,
        color='status',
        title='Time to Exit Distribution (IPO vs Acquired)',
        labels={'time_to_exit_months': 'Time from Founded to Exit (Months)'}
    )
    fig.show()
```

#### 5.4.3 可视化增强（可选）

- **Pyecharts 主题河流图：** 可与 Part B 协作，叠加融资轮次维度。
- **Plotly Sunburst 图：** 展示 `行业 → 融资区间 → 退出状态` 的层级关系。
- **Plotly 热力图 (Heatmap)：** 展示 `Last_Round_Type` × `Funding_Bracket` 的退出率交叉矩阵。

---

## Step 6: 解读与叙事 (Interpretation & Storytelling)

### 6.1 从数据到故事的转化框架

Part D 是整个 Presentation 的**收尾章节（约 3-4 分钟）**，需要将前三个 Part 的发现汇聚成一个有说服力的结论。建议采用以下叙事结构：

| 时间 | 内容 | 核心图表 | 说辞模板 |
|------|------|---------|---------|
| 0:00-0:30 | **引入** — 回顾前三部分的发现，提出核心问题 | — | "我们已经看到了资本的全球分布、赛道变迁和存活现实。那么最终的问题是：**钱花得值吗？**" |
| 0:30-1:15 | **RQ1** — 融资总量与退出概率；叠加 `Avg_Funding_Per_Round` 的"资本密度"视角 | 分组柱状图 | "融资在 X-Y 区间的公司退出率最高，但超过 Z 后增幅放缓。有趣的是，每轮融资密度高的公司退出率也更高——**投资人的单次押注大小比总融资额更能预测成功。**" |
| 1:15-2:00 | **RQ2** — 展示门槛效应，同时用 `Last_Round_Type` 交叉验证 | 折线图 + 分组柱状图 | "无论从轮次数量还是轮次质量来看，Series B 都是分水岭——存活率从 X% 跃升至 Y%。**能走到 B 轮的公司，已经通过了市场最严格的筛选。**" |
| 2:00-2:45 | **RQ3** — 融资节奏与收购价格 | 散点图 + 趋势线 | "融资节奏越快的公司，往往获得更高的收购价格——**速度就是信号。**" |
| 2:45-3:30 | **Capital Efficiency + 总结** — 用 `Valuation_to_Funding_Ratio` 作为最终收尾洞察 | 资本效率柱状图 | "但最深层的发现是：**融资最多的公司并非资本效率最高的公司。** 中等融资区间反而产生了最高的估值倍数——资本的'转化率'比'绝对量'更值得关注。" |

### 6.2 Reflection Document 写作指南

在最终的 Reflection Document 中，**Result（结果）** 和 **Discussion（讨论）** 必须严格分开：

- **Result 部分：** 只陈述事实性发现，使用客观语言。
  - ✅ "融资总量在 10M-50M 区间的公司成功退出率为 38%，高于其他区间。"
  - ❌ "我认为融资 10M-50M 是最好的策略。"

- **Discussion 部分：** 解读结果的含义，提出可能的解释，并**明确承认局限性**。

### 6.3 必须声明的统计局限性 (Statistical Limitations)

| 局限性 | 英文术语 | 说明 | 建议措辞 |
|--------|---------|------|---------|
| **幸存者偏差** | Survivor Bias | 数据集中记录的公司已是"被看到的"，无数默默失败的公司从未进入数据库。 | "Our dataset inherently suffers from **survivor bias** — companies that failed before receiving any recorded funding are absent from our analysis." |
| **相关非因果** | Correlation ≠ Causation | 融资总量与成功退出之间的关联可能受到第三方变量（如创始人背景、市场时机）的驱动。 | "The observed correlation between funding volume and exit success **does not imply causation**. Confounding variables such as founder experience and market timing may drive both." |
| **数据缺失偏差** | Missing Data Bias | `acquisitions.csv` 中 `price_amount` 和 `funding_rounds.csv` 中 `post_money_valuation_usd` 大量为 0（即未披露），可用子集可能不具代表性。 | "RQ3 的分析仅基于 N 家有公开收购价格的公司，**样本量有限，结论需谨慎推广**。" |
| **时间截断** | Right Censoring | `Operating` 状态的公司结局未定，将其排除或纳入都会引入偏差。 | "Companies currently in 'Operating' status represent **right-censored observations** — their final outcome is yet to be determined." |

### 6.4 最终检查清单 (Final Checklist)

- [ ] 所有图表都有**清晰的标题、轴标签和图例**
- [ ] 每张图表都附有**一句话结论 (One-line Takeaway)**
- [ ] 代码可复现：`.ipynb` 文件从上到下 `Restart & Run All` 无报错
- [ ] Reflection Document 中 Result 与 Discussion 严格分离
- [ ] 已明确声明至少两项统计局限性
- [ ] 与队友的数据口径已对齐（`status` 分类、时间范围、地域范围）
- [ ] Priority I 变量全部完成特征工程并纳入分析（共 9 个）
- [ ] Priority II 变量已检查数据可得性，可用者已纳入补充分析
- [ ] `Valuation_to_Funding_Ratio`（资本效率）已作为 Presentation 收尾洞察呈现

---

*文档版本：v1.2 | 创建日期：2026-04-28 | 更新日期：2026-04-28 | 适用于 NAA1661 Data Scholarship Final Project*
*v1.2 更新：整合实际 Crunchbase 多表数据集（`Datasets/` 目录），所有代码均使用真实表名和字段名。*