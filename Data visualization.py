import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import MinMaxScaler

# 1. 加载数据
file_path = '/Users/apple/Desktop/startup_valuation_dataset.csv'
df = pd.read_csv(file_path)

# 指标工程
df['revenue_per_employee'] = df['estimated_revenue_usd'] / (df['employee_count'] + 1)
df['valuation_to_funding_ratio'] = df['estimated_valuation_usd'] / (df['funding_amount_usd'] + 1)

# 图 1：极光脉络桑基图
def create_aurora_sankey(df, cols):
    nodes = []
    for col in cols:
        nodes.extend(df[col].unique().tolist())
    nodes = list(set(nodes))
    colors = px.colors.qualitative.Prism + px.colors.qualitative.Safe
    node_colors = [colors[i % len(colors)] for i in range(len(nodes))]
    links = []
    for i in range(len(cols)-1):
        group = df.groupby([cols[i], cols[i+1]]).size().reset_index(name='value')
        for _, row in group.iterrows():
            src_idx = nodes.index(row[cols[i]])
            links.append({
                'source': src_idx,
                'target': nodes.index(row[cols[i+1]]),
                'value': row['value'],
                'color': node_colors[src_idx].replace('rgb', 'rgba').replace(')', ', 0.35)')
            })
    return nodes, links, node_colors

nodes, links, n_colors = create_aurora_sankey(df.sample(2500), ['region', 'industry', 'exited'])
fig1 = go.Figure(data=[go.Sankey(
    node=dict(pad=12, thickness=15, label=nodes, color=n_colors, line=dict(color="white", width=0.3)),
    link=dict(source=[l['source'] for l in links], target=[l['target'] for l in links],
              value=[l['value'] for l in links], color=[l['color'] for l in links])
)])
fig1.update_layout(title_text="资本流向全景：全球初创企业生态链路", template="plotly_dark")



# 图 2：行业实力矩阵雷达图
radar_features = ['estimated_valuation_usd', 'funding_amount_usd', 'estimated_revenue_usd',
                  'employee_count', 'revenue_per_employee', 'valuation_to_funding_ratio']
radar_df = df.groupby('industry')[radar_features].mean()
radar_norm = pd.DataFrame(MinMaxScaler().fit_transform(radar_df), columns=radar_features, index=radar_df.index)
mean_level = radar_norm.mean().tolist()

target_industries = ['Fintech', 'SaaS', 'AI/ML', 'Blockchain', 'Healthcare', 'E-commerce']
fig2 = make_subplots(rows=2, cols=3, specs=[[{'type': 'polar'}]*3]*2, subplot_titles=target_industries)

for i, industry in enumerate(target_industries):
    r, c = i // 3 + 1, i % 3 + 1
    # 叠加平均水平背景
    fig2.add_trace(go.Scatterpolar(r=mean_level + [mean_level[0]], theta=radar_features + [radar_features[0]],
                                  fill='toself', name='平均', fillcolor='rgba(255,255,255,0.1)',
                                  line=dict(color='gray', width=1, dash='dot'), showlegend=False), row=r, col=c)
    # 行业数据
    val = radar_norm.loc[industry].values.tolist()
    fig2.add_trace(go.Scatterpolar(r=val + [val[0]], theta=radar_features + [radar_features[0]],
                                  fill='toself', name=industry, line=dict(width=2)), row=r, col=c)

fig2.update_polars(radialaxis=dict(visible=False), gridshape='linear')
fig2.update_layout(template="plotly_dark", title="核心行业六维效能矩阵深度对比", height=750, showlegend=False)


# 图 3：深度嵌套旭日图
fig3 = px.sunburst(
    df.sample(4000),
    path=['industry', 'funding_round', 'region', 'exited'],
    values='estimated_valuation_usd',
    color='estimated_valuation_usd',
    color_continuous_scale='Picnic', # 更复杂的配色
    title="行业资本结构深度嵌套透析 (下钻式交互)"
)
fig3.update_layout(template="plotly_dark")


# 图 4：3D 自动旋转黑金地球
geo_agg = df.groupby('country').agg({'estimated_valuation_usd':'sum'}).reset_index()

# 修复：使用 go.Choropleth 代替错误的 Choroplethgeo
fig4 = go.Figure(go.Choropleth(
    locations=geo_agg['country'],
    locationmode='country names',
    z=geo_agg['estimated_valuation_usd'],
    colorscale='YlOrRd',
    reversescale=False,
    marker=dict(line=dict(width=0.2, color='white')),
    colorbar=dict(title="总估值", thickness=15)
))

# 3D 球体旋转设置
fig4.update_geos(
    projection_type="orthographic",
    showocean=True, oceancolor="#010915",
    showland=True, landcolor="#111",
    projection_rotation=dict(lon=0, lat=20, roll=0),
    bgcolor='rgba(0,0,0,0)'
)

# 生成旋转帧（实现自动旋转的关键）
frames = [go.Frame(layout=dict(geo_projection_rotation=dict(lon=i, lat=20, roll=0))) for i in range(0, 360, 5)]
fig4.frames = frames

fig4.update_layout(
    template="plotly_dark", height=800,
    title="全球资本巡航：3D 动态旋转分布展示",
    updatemenus=[dict(
        type="buttons", showactive=False, x=0.05, y=0.05,
        buttons=[dict(label="▶ 点击启动全球巡航", method="animate",
                     args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True)])]
    )]
)


fig1.show()
fig2.show()
fig3.show()
fig4.show()
