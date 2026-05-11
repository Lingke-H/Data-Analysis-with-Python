"""
Part D — Preview all 4 figures
Run: python preview_figures.py
Opens a local HTML page with all 4 figures.
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import base64, io, os

DATA = "Datasets"

# ============================================================
# 1. Load & merge data
# ============================================================
print("Loading data...")
obj = pd.read_csv(f"{DATA}/objects.csv")
fr  = pd.read_csv(f"{DATA}/funding_rounds.csv")

# Filter companies with funding
df = obj[
    (obj['entity_type'] == 'Company') &
    (obj['funding_total_usd'] > 0)
].copy()

# Status cleanup
df['status'] = df['status'].str.strip().str.lower()
df = df[df['status'].isin(['operating', 'acquired', 'ipo', 'closed'])]
df['exit_success'] = df['status'].isin(['ipo', 'acquired']).astype(int)

print(f"Companies after filter: {len(df)}")
print(f"Status distribution:\n{df['status'].value_counts()}")

# ============================================================
# 2. Feature engineering
# ============================================================
# Funding bracket
bins = [0, 1e6, 1e7, 5e7, 1e8, 5e8, np.inf]
labels = ['<1M', '1-10M', '10-50M', '50-100M', '100-500M', '>500M']
df['funding_bracket'] = pd.cut(df['funding_total_usd'], bins=bins, labels=labels)

# Funding rounds (already in objects.csv)
df['funding_rounds'] = df['funding_rounds'].fillna(0).astype(int)

# Avg time between rounds
df['first_funding_at'] = pd.to_datetime(df['first_funding_at'], errors='coerce')
df['last_funding_at']  = pd.to_datetime(df['last_funding_at'], errors='coerce')
df['funding_span_months'] = (
    (df['last_funding_at'] - df['first_funding_at']).dt.days / 30.44
)
df['avg_time_between_rounds'] = np.where(
    df['funding_rounds'] > 1,
    df['funding_span_months'] / (df['funding_rounds'] - 1),
    np.nan
)

# Speed bin
df['speed_bin'] = pd.cut(
    df['avg_time_between_rounds'],
    bins=[0, 6, 12, 24, 48, np.inf],
    labels=['<6m', '6-12m', '12-24m', '24-48m', '>48m']
)

# ============================================================
# Fig 1: Plotly TreeMap — Industry × Status Hierarchy
# ============================================================
print("Generating Fig 1 (Plotly TreeMap)...")

# --- Unified palette (shared with Figs 2-4) ---
clr_acq   = '#5B8DBE'   # steel blue  — Acquired
clr_ipo   = '#7BC8A4'   # sage green  — IPO
clr_oper  = '#6B7B8D'   # muted slate — Operating
clr_close = '#C0706B'   # muted rose  — Closed
clr_text  = '#3B3B3B'   # dark charcoal
clr_sub   = '#6B7B8D'   # muted slate
clr_ref   = '#B0B0B0'   # neutral grey

status_order = ['operating', 'acquired', 'ipo', 'closed']
status_colors = {
    'operating': clr_oper, 'acquired': clr_acq,
    'ipo': clr_ipo, 'closed': clr_close
}
status_labels = {
    'operating': 'Operating', 'acquired': 'Acquired',
    'ipo': 'IPO', 'closed': 'Closed'
}

# Build hierarchical dataframe for px.treemap: Industry → Status
top12 = df['category_code'].value_counts().head(12).index.tolist()
df_tree = df[df['category_code'].isin(top12)].copy()
df_tree['industry'] = df_tree['category_code'].str.title()
df_tree['status_label'] = df_tree['status'].map(status_labels)

tree_agg = (
    df_tree.groupby(['industry', 'status_label'])
    .agg(count=('id', 'size'))
    .reset_index()
)

# Industry-level stats for hover
industry_stats = (
    df_tree.groupby('industry')
    .agg(total=('id', 'size'), exit_rate=('exit_success', 'mean'))
    .reset_index()
)

# Re-map status colors: maximise hue separation, avoid red-on-red
status_tile_colors = {
    'Operating': '#CC8A83',   # light rose-terracotta
    'Acquired':  '#5B8DBE',   # steel blue
    'IPO':       '#7BC8A4',   # sage green
    'Closed':    '#D4A76A',   # warm amber (NOT rose — avoids red cluster)
}

# Build explicit hierarchy for go.Treemap
ids, labels, parents, values, colors, hovers = [], [], [], [], [], []
industry_order = df_tree['industry'].value_counts().index.tolist()

for ind in industry_order:
    ind_row = industry_stats[industry_stats['industry'] == ind].iloc[0]
    ids.append(ind)
    labels.append(ind)
    parents.append('')
    values.append(0)
    colors.append('#9EAAB8')  # cool silver-grey for industry header
    hovers.append(
        f"<b>{ind}</b><br>"
        f"Total: {int(ind_row['total']):,}<br>"
        f"Exit rate: {ind_row['exit_rate']:.1%}"
    )

    sub = tree_agg[tree_agg['industry'] == ind].sort_values('count', ascending=False)
    for _, row in sub.iterrows():
        st = row['status_label']
        cnt = int(row['count'])
        uid = f"{ind}/{st}"
        ids.append(uid)
        labels.append(st)
        parents.append(ind)
        values.append(cnt)
        colors.append(status_tile_colors[st])
        hovers.append(
            f"<b>{ind} → {st}</b><br>"
            f"Companies: {cnt:,}<br>"
            f"Industry total: {int(ind_row['total']):,}<br>"
            f"Industry exit rate: {ind_row['exit_rate']:.1%}"
        )

fig1 = go.Figure(go.Treemap(
    ids=ids,
    labels=labels,
    parents=parents,
    values=values,
    branchvalues='remainder',
    marker=dict(
        colors=colors,
        cornerradius=3,
        line=dict(width=0.5, color='white'),
    ),
    texttemplate='<b>%{label}</b><br>%{value:,}',
    textfont=dict(size=11, family='Inter, sans-serif', color='white'),
    hovertext=hovers,
    hoverinfo='text',
    tiling=dict(packing='squarify', pad=2),
    pathbar=dict(visible=False),
))

fig1.update_layout(
    title=dict(
        text=(
            f"Fig 1 (EDA): Distribution of VC-Backed Startups by Industry and Exit Status<br>"
            f"<sup style='color:{clr_sub}'>{len(df):,} companies across "
            f"{df['category_code'].nunique()} industries  |  "
            f"Overall exit rate: {df['exit_success'].mean():.1%}  |  "
            f"Median funding: ${df['funding_total_usd'].median()/1e6:.1f}M</sup>"
        ),
        font=dict(size=15, color=clr_text, family='Inter, sans-serif'),
        x=0.5, xanchor='center'
    ),
    font=dict(family='Inter, sans-serif', color=clr_text),
    margin=dict(l=10, r=10, t=90, b=10),
    paper_bgcolor='white',
    # Manual legend via annotations — treemap has no built-in legend
    annotations=[
        dict(
            text=(
                f"<span style='color:{status_tile_colors['Operating']}'>■</span> Operating &nbsp;&nbsp;"
                f"<span style='color:{status_tile_colors['Acquired']}'>■</span> Acquired &nbsp;&nbsp;"
                f"<span style='color:{status_tile_colors['IPO']}'>■</span> IPO &nbsp;&nbsp;"
                f"<span style='color:{status_tile_colors['Closed']}'>■</span> Closed"
            ),
            x=0.5, y=-0.02, xref='paper', yref='paper',
            showarrow=False,
            font=dict(size=12, color=clr_text, family='Inter, sans-serif'),
            xanchor='center'
        )
    ]
)

# ============================================================
# Fig 2: Stacked Bar (IPO vs Acquired) + Line (RQ1)
# ============================================================
print("Generating Fig 2...")

# Compute IPO rate, Acquired rate, and sample size per bracket
exit_detail = (
    df.groupby('funding_bracket', observed=True)
    .agg(
        ipo_rate=('status', lambda x: (x == 'ipo').mean()),
        acq_rate=('status', lambda x: (x == 'acquired').mean()),
        exit_rate=('exit_success', 'mean'),
        n_companies=('exit_success', 'count')
    )
    .reset_index()
)
overall_rate = df['exit_success'].mean()

clr_line  = '#A0522D'   # warm sienna (sample-size line)

fig2 = make_subplots(specs=[[{"secondary_y": True}]])

x_labels = exit_detail['funding_bracket'].astype(str)

# Stacked: Acquired bar (bottom) — bar text only for values > 3%
fig2.add_trace(
    go.Bar(
        x=x_labels, y=exit_detail['acq_rate'],
        name='Acquired Rate',
        marker=dict(color=clr_acq, line=dict(width=0)),
        text=[f"{r:.1%}" if r > 0.03 else '' for r in exit_detail['acq_rate']],
        textposition='inside', textfont=dict(color='white', size=11, family='Inter, sans-serif'),
        hovertemplate='%{x}<br>Acquired: %{y:.1%}<extra></extra>'
    ),
    secondary_y=False
)

# Stacked: IPO bar (top) — bar text only for values > 3%
fig2.add_trace(
    go.Bar(
        x=x_labels, y=exit_detail['ipo_rate'],
        name='IPO Rate',
        marker=dict(color=clr_ipo, line=dict(width=0)),
        text=[f"{r:.1%}" if r > 0.03 else '' for r in exit_detail['ipo_rate']],
        textposition='inside', textfont=dict(color='white', size=11, family='Inter, sans-serif'),
        hovertemplate='%{x}<br>IPO: %{y:.1%}<extra></extra>'
    ),
    secondary_y=False
)

# Line: sample size — clean, no text labels (use hover instead)
fig2.add_trace(
    go.Scatter(
        x=x_labels, y=exit_detail['n_companies'],
        name='Sample Size (n)',
        mode='lines+markers',
        line=dict(color=clr_line, width=2.5, shape='spline'),
        marker=dict(size=7, color='white', line=dict(color=clr_line, width=2)),
        hovertemplate='%{x}<br>n = %{y:,.0f}<extra></extra>'
    ),
    secondary_y=True
)

# Overall avg reference line — subtle
fig2.add_hline(
    y=overall_rate, line_dash='dot', line_color=clr_ref, line_width=1.5,
    annotation_text=f"Avg: {overall_rate:.1%}",
    annotation_position='bottom left',
    annotation_font=dict(size=10, color=clr_sub),
    secondary_y=False
)

# Peak annotation — positioned to avoid overlap
peak_idx = exit_detail['exit_rate'].idxmax()
peak = exit_detail.iloc[peak_idx]
fig2.add_annotation(
    x=str(peak['funding_bracket']),
    y=peak['exit_rate'],
    text=(f"<b>Peak: {peak['exit_rate']:.1%}</b><br>"
          f"<span style='font-size:10px'>IPO {peak['ipo_rate']:.1%} + Acq {peak['acq_rate']:.1%}</span>"),
    showarrow=True, arrowhead=0, arrowwidth=1.5, arrowcolor=clr_sub,
    ax=-70, ay=-50,
    font=dict(color=clr_text, size=11),
    bordercolor=clr_sub, borderwidth=1, borderpad=6,
    bgcolor='rgba(255,255,255,0.92)', opacity=1
)

fig2.update_layout(
    title=dict(
        text="Fig 2 (RQ1): Exit Rate by Funding Bracket — IPO vs Acquired Decomposition",
        font=dict(size=15, color=clr_text, family='Inter, sans-serif'),
        x=0.5, xanchor='center'
    ),
    height=540, barmode='stack',
    plot_bgcolor='#FAFAFA', paper_bgcolor='white',
    margin=dict(l=65, r=65, t=70, b=105),
    legend=dict(
        orientation='h', yanchor='top', y=-0.18, xanchor='center', x=0.5,
        bgcolor='rgba(255,255,255,0.85)', bordercolor=clr_ref, borderwidth=1,
        font=dict(size=11, color=clr_text, family='Inter, sans-serif'),
        itemsizing='constant', itemwidth=40,
        tracegroupgap=20
    ),
    bargap=0.25
)
fig2.update_xaxes(
    title_text='Funding Bracket (USD)',
    title_font=dict(size=11, color=clr_sub),
    tickfont=dict(size=10, color=clr_text),
    showgrid=False, linecolor=clr_ref
)
fig2.update_yaxes(
    title_text="Exit Rate (stacked)", tickformat='.0%',
    title_font=dict(size=11, color=clr_sub),
    tickfont=dict(size=10, color=clr_sub),
    gridcolor='#ECECEC', gridwidth=0.5, showgrid=True,
    secondary_y=False
)
fig2.update_yaxes(
    title_text="Sample Size (n)",
    title_font=dict(size=11, color=clr_line),
    tickfont=dict(size=10, color=clr_line),
    showgrid=False,
    secondary_y=True
)

# ============================================================
# Fig 3: Enhanced Bubble Chart (RQ2) — 10 data points
# ============================================================
print("Generating Fig 3...")

# Cap rounds at 10+ for density
df_r = df[df['funding_rounds'] > 0].copy()
df_r['round_group'] = df_r['funding_rounds'].clip(upper=10)

round_stats = (
    df_r.groupby('round_group')
    .agg(exit_rate=('exit_success', 'mean'), n=('exit_success', 'count'))
    .reset_index()
)
round_stats['round_label'] = round_stats['round_group'].astype(str)
round_stats.loc[round_stats['round_group'] == 10, 'round_label'] = '10+'

# First difference to find threshold
round_stats['delta'] = round_stats['exit_rate'].diff()
threshold_idx = round_stats['delta'].idxmax()
threshold_round = int(round_stats.loc[threshold_idx, 'round_group'])

# Bubble chart: x=round, y=exit_rate, size=n, color=exit_rate
fig3 = go.Figure()

# Trend line (connecting bubbles) — muted
fig3.add_trace(
    go.Scatter(
        x=round_stats['round_group'], y=round_stats['exit_rate'],
        mode='lines',
        line=dict(color='rgba(107,123,141,0.35)', width=2, dash='dot'),
        showlegend=False, hoverinfo='skip'
    )
)

# Custom colorscale matching the palette (muted red → warm gold → sage green)
cscale_fig3 = [[0, '#C0706B'], [0.4, '#D4A76A'], [0.65, '#A8C490'], [1, '#7BC8A4']]

size_scale = np.sqrt(round_stats['n']) / np.sqrt(round_stats['n'].max()) * 55 + 10
fig3.add_trace(
    go.Scatter(
        x=round_stats['round_group'], y=round_stats['exit_rate'],
        mode='markers+text',
        marker=dict(
            size=size_scale,
            color=round_stats['exit_rate'],
            colorscale=cscale_fig3,
            colorbar=dict(
                title=dict(text='Exit Rate', font=dict(size=10, color=clr_sub)),
                tickformat='.0%', tickfont=dict(size=9, color=clr_sub),
                thickness=12, len=0.6, outlinewidth=0,
                x=1.08
            ),
            line=dict(width=1.5, color='white'),
            opacity=0.88
        ),
        text=[f"{r:.1%}" for r in round_stats['exit_rate']],
        textposition='top center',
        textfont=dict(size=10, color=clr_text, family='Inter, sans-serif'),
        customdata=np.stack([round_stats['n'], round_stats['delta'].fillna(0)], axis=-1),
        hovertemplate=(
            'Round %{x}<br>'
            'Exit Rate: %{y:.1%}<br>'
            'n = %{customdata[0]:,.0f}<br>'
            'Δ from prev: %{customdata[1]:.1%}'
            '<extra></extra>'
        ),
        showlegend=False
    )
)

# Sample size labels below each bubble — muted
for _, row in round_stats.iterrows():
    fig3.add_annotation(
        x=row['round_group'], y=row['exit_rate'],
        text=f"n={row['n']:,.0f}",
        showarrow=False, yshift=-int(size_scale[_]) // 2 - 14,
        font=dict(size=8, color=clr_sub)
    )

# Threshold regions — very subtle tints
fig3.add_vrect(
    x0=0.5, x1=threshold_round - 0.5,
    fillcolor='rgba(192,112,107,0.04)', layer='below', line_width=0
)
fig3.add_vrect(
    x0=threshold_round - 0.5, x1=10.5,
    fillcolor='rgba(123,200,164,0.05)', layer='below', line_width=0
)

# Threshold line + annotation
fig3.add_vline(x=threshold_round, line_dash='dash', line_color=clr_line, line_width=1.5)
pre_rate = round_stats.loc[round_stats['round_group'] == threshold_round - 1, 'exit_rate'].values
post_rate = round_stats.loc[round_stats['round_group'] == threshold_round, 'exit_rate'].values
delta_val = round_stats.loc[threshold_idx, 'delta']
fig3.add_annotation(
    x=threshold_round, y=round_stats['exit_rate'].max() * 0.95,
    text=(
        f"<b>Threshold: Round {threshold_round}</b><br>"
        f"Δ = +{delta_val:.1%}<br>"
        f"{pre_rate[0]:.1%} → {post_rate[0]:.1%}" if len(pre_rate) > 0 and len(post_rate) > 0
        else f"<b>Threshold: Round {threshold_round}</b><br>Δ = +{delta_val:.1%}"
    ),
    showarrow=True, arrowhead=0, arrowwidth=1.5, arrowcolor=clr_sub,
    ax=-90, ay=-30,
    font=dict(size=11, color=clr_text),
    bordercolor=clr_sub, borderwidth=1, borderpad=6,
    bgcolor='rgba(255,255,255,0.92)', opacity=1
)

fig3.update_layout(
    title=dict(
        text=f"Fig 3 (RQ2): Exit Rate by Funding Rounds — Threshold at Round {threshold_round}",
        font=dict(size=15, color=clr_text, family='Inter, sans-serif'),
        x=0.5, xanchor='center'
    ),
    height=550,
    plot_bgcolor='#FAFAFA', paper_bgcolor='white',
    margin=dict(l=60, r=100, t=70, b=60),
    xaxis=dict(
        title=dict(text='Number of Funding Rounds', font=dict(size=11, color=clr_sub)),
        tickvals=round_stats['round_group'].tolist(),
        ticktext=round_stats['round_label'].tolist(),
        tickfont=dict(size=10, color=clr_text),
        range=[0.3, 10.7], showgrid=False, linecolor=clr_ref
    ),
    yaxis=dict(
        title=dict(text='Exit Success Rate', font=dict(size=11, color=clr_sub)),
        tickformat='.0%', tickfont=dict(size=10, color=clr_sub),
        gridcolor='#ECECEC', gridwidth=0.5, showgrid=True
    )
)

print(f"  Threshold round: {threshold_round} (Δ = {delta_val:.1%})")
print(f"  Bubbles: {len(round_stats)}, total companies: {df_r.shape[0]}")
# Export peak for HTML
peak = exit_detail.iloc[exit_detail['exit_rate'].idxmax()]

# ============================================================
# Fig 4: Seaborn heatmap (RQ3)
# ============================================================
print("Generating Fig 4...")
df_heat = df.dropna(subset=['funding_bracket', 'speed_bin'])

heatmap_data = df_heat.pivot_table(
    index='funding_bracket',
    columns='speed_bin',
    values='exit_success',
    aggfunc='mean',
    observed=True
)

count_data = df_heat.pivot_table(
    index='funding_bracket',
    columns='speed_bin',
    values='exit_success',
    aggfunc='count',
    observed=True
).fillna(0).astype(int)

# Build annotation strings
annot_arr = heatmap_data.copy().astype(object)
for i in range(heatmap_data.shape[0]):
    for j in range(heatmap_data.shape[1]):
        rate = heatmap_data.iloc[i, j]
        n = count_data.iloc[i, j]
        if pd.notna(rate):
            annot_arr.iloc[i, j] = f"{rate:.1%}\n(n={n})"
        else:
            annot_arr.iloc[i, j] = "—"

# Custom colormap matching the unified palette
cmap_heat = LinearSegmentedColormap.from_list('unified', ['#C0706B', '#D4A76A', '#A8C490', '#7BC8A4'])

fig4_fig, ax4 = plt.subplots(figsize=(10, 6))
fig4_fig.set_facecolor('white')
ax4.set_facecolor('#FAFAFA')

sns.heatmap(
    heatmap_data, annot=annot_arr.values, fmt='',
    cmap=cmap_heat, linewidths=1, linecolor='white',
    vmin=0, vmax=np.nanpercentile(heatmap_data.values, 95),
    cbar_kws={'label': 'Exit Success Rate', 'shrink': 0.8},
    annot_kws={'size': 9, 'color': '#3B3B3B'},
    ax=ax4
)
ax4.set_title("Fig 4 (RQ3): Exit Rate by Funding Speed × Funding Amount",
              fontsize=14, color='#3B3B3B', fontweight='bold', pad=18,
              fontfamily='sans-serif')
ax4.set_xlabel("Avg Time Between Rounds", fontsize=11, color='#6B7B8D', labelpad=10)
ax4.set_ylabel("Total Funding Bracket", fontsize=11, color='#6B7B8D', labelpad=10)
ax4.tick_params(axis='both', labelsize=10, colors='#3B3B3B')
# Style colorbar
cbar = ax4.collections[0].colorbar
cbar.ax.tick_params(labelsize=9, colors='#6B7B8D')
cbar.set_label('Exit Success Rate', fontsize=10, color='#6B7B8D')
plt.tight_layout()

# Save heatmap as PNG
fig4_path = os.path.join(os.path.dirname(__file__) or '.', '_fig4_heatmap.png')
plt.savefig(fig4_path, dpi=150, bbox_inches='tight')
plt.close()

# Read PNG and encode to base64 for HTML embedding
with open(fig4_path, 'rb') as f:
    fig4_b64 = base64.b64encode(f.read()).decode()

# ============================================================
# Export Figs 2-3 as PNG for Reflection PDF
# ============================================================
print("Exporting PNGs for Reflection...")
_dir = os.path.dirname(__file__) or '.'

fig1.write_image(os.path.join(_dir, 'fig1_placeholder.png'), width=1100, height=620, scale=2)
fig2.write_image(os.path.join(_dir, 'fig2_placeholder.png'), width=1100, height=540, scale=2)
fig3.write_image(os.path.join(_dir, 'fig3_placeholder.png'), width=1100, height=550, scale=2)

# Fig 4 already saved; copy to expected name for pandoc
import shutil
shutil.copy2(fig4_path, os.path.join(_dir, 'fig4_placeholder.png'))

print("  ✓ fig1–4 PNGs exported")

# ============================================================
# Combine into a single HTML page
# ============================================================
print("Writing combined HTML...")

# Build HTML by concatenation to avoid f-string mangling pyecharts JS braces
html_parts = []

html_parts.append("""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>Part D — 4 Figures Preview</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
         max-width: 1100px; margin: 0 auto; padding: 20px; background: #fafafa; }
  h1 { text-align: center; color: #2c3e50; }
  .fig-section { background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,.08);
                  padding: 20px; margin: 24px 0; }
  .fig-section h2 { color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 8px; }
  .takeaway { background: #eaf6ff; border-left: 4px solid #3498db; padding: 10px 16px;
               margin-top: 12px; font-style: italic; }
  .badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.8em;
            font-weight: bold; margin-left: 8px; }
  .pres { background: #2ecc71; color: white; }
  .refl { background: #3498db; color: white; }
  img.heatmap { max-width: 100%; border-radius: 4px; }
</style>
</head><body>
<h1>Part D — 4 Figures Preview</h1>
<p style="text-align:center; color:#7f8c8d;">
  <span class="badge refl">Reflection</span> = 全部 4 张 &nbsp;
  <span class="badge pres">Presentation</span> = Fig 2 + Fig 3（建议）
</p>
""")

# Fig 1 — Plotly TreeMap
fig1_html = fig1.to_html(full_html=False, include_plotlyjs='cdn')
html_parts.append(f"""
<div class="fig-section">
  <h2>Fig 1: EDA 概览 — Plotly TreeMap <span class="badge refl">Reflection</span></h2>
  <p style="color:#7f8c8d; font-size:0.9em;">技能: <code>px.treemap</code> 层级矩形树图 · <code>color_discrete_map</code> 状态配色 · <code>textinfo</code> 标签定制 · <code>hovertemplate</code> 交互提示</p>
  <p style="color:#e67e22; font-size:0.85em;">💡 可点击色块下钻查看行业内部构成</p>
  {fig1_html}
  <div class="takeaway">矩形面积 = 公司数量。12 大行业按公司数排列，内部按 Operating(灰) / Acquired(蓝) / IPO(绿) / Closed(红) 分色。Software 和 Web 主导生态，但 Biotech 退出成功率更高。</div>
</div>
""")

# Fig 2-4 — use f-string (plotly/seaborn output is safe)
fig2_html = fig2.to_html(full_html=False, include_plotlyjs=False)
fig3_html = fig3.to_html(full_html=False, include_plotlyjs=False)

html_parts.append(f"""
<div class="fig-section">
  <h2>Fig 2: RQ1 — IPO vs Acquired 退出率分解 <span class="badge refl">Reflection</span> <span class="badge pres">Presentation</span></h2>
  <p style="color:#7f8c8d; font-size:0.9em;">技能: barmode='stack' · secondary_y 双轴 · add_hline 参考线 · add_annotation 峰值标注</p>
  {fig2_html}
  <div class="takeaway">融资在 {peak['funding_bracket']} 区间退出率最高 ({peak['exit_rate']:.1%})；高融资区间中 IPO 占比上升，低融资区间以 Acquired 为主。</div>
</div>

<div class="fig-section">
  <h2>Fig 3: RQ2 — 融资轮次门槛效应（气泡图） <span class="badge refl">Reflection</span> <span class="badge pres">Presentation</span></h2>
  <p style="color:#7f8c8d; font-size:0.9em;">技能: go.Scatter bubble · size/color 双编码 · colorscale='RdYlGn' · add_vrect 区域 · add_vline 门槛 · customdata + hovertemplate</p>
  {fig3_html}
  <div class="takeaway">Round {threshold_round} 是分水岭 (Δ=+{delta_val:.1%})——气泡从红色渐变为绿色，退出率在门槛线处跃升。气泡大小反映样本量。</div>
</div>

<div class="fig-section">
  <h2>Fig 4: RQ3 — 融资速度 × 融资金额 交叉热力图 <span class="badge refl">Reflection</span></h2>
  <img src="data:image/png;base64,{fig4_b64}" class="heatmap" alt="Fig 4 Heatmap">
  <div class="takeaway">融资间隔 6–24 个月的公司退出率最高；该规律在不同融资区间中保持一致。</div>
</div>

</body></html>
""")

html = ''.join(html_parts)

out_path = os.path.join(os.path.dirname(__file__) or '.', 'figures_preview.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ Preview saved to: {out_path}")
print("Starting local server...")

# Serve via simple HTTP server
import http.server, socketserver
PORT = 8765
os.chdir(os.path.dirname(os.path.abspath(__file__)))

handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), handler) as httpd:
    print(f"Serving at http://localhost:{PORT}/figures_preview.html")
    httpd.serve_forever()
