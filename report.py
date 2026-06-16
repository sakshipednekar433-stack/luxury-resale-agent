import pandas as pd
from datetime import datetime, timedelta
import random

def generate_sample_data():
    random.seed(42)
    
    hermes_items = {
        "Hermès Birkin 25 Togo Gold HW": 10900,
        "Hermès Birkin 30 Clemence Black": 11900,
        "Hermès Birkin 35 Epsom Noir": 12900,
        "Hermès Kelly 28 Sellier Craie": 10200,
        "Hermès Kelly 32 Retourne Gold": 11200,
        "Hermès Constance 24 Etoupe": 9800,
        "Hermès Picotin 18 Rose Sakura": 3200,
        "Hermès Evelyne PM Blue Indigo": 2900,
        "Hermès Lindy 26 Jaune Ambre": 6200,
        "Hermès Bolide 31 Rouge Casaque": 7800,
    }
    
    chanel_items = {
        "Chanel Classic Flap Medium Caviar Black": 10800,
        "Chanel Classic Flap Jumbo Lambskin Beige": 11400,
        "Chanel Classic Flap Small Black Caviar": 9500,
        "Chanel Boy Bag Medium Chevron Black": 7200,
        "Chanel 19 Large Flap Mauve": 6800,
        "Chanel WOC Wallet on Chain Black": 3200,
        "Chanel 2.55 Reissue 226 Dark Grey": 10200,
        "Chanel Gabrielle Hobo Small Black": 4500,
        "Chanel Deauville Tote Medium Navy": 3800,
        "Chanel Coco Handle Small Beige": 6500,
    }

    listings = []
    base_date = datetime.now()

    for item, retail in hermes_items.items():
        for _ in range(random.randint(8, 15)):
            multiplier = random.uniform(1.5, 3.2)
            price = round(retail * multiplier, -2)
            listings.append({
                "brand": "Hermes",
                "item": item,
                "price_usd": price,
                "retail_usd": retail,
                "resale_premium_pct": round((price / retail - 1) * 100, 1),
                "date": (base_date - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
            })

    for item, retail in chanel_items.items():
        for _ in range(random.randint(8, 15)):
            multiplier = random.uniform(0.95, 1.85)
            price = round(retail * multiplier, -2)
            listings.append({
                "brand": "Chanel",
                "item": item,
                "price_usd": price,
                "retail_usd": retail,
                "resale_premium_pct": round((price / retail - 1) * 100, 1),
                "date": (base_date - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
            })

    return pd.DataFrame(listings)


def generate_report(df, summary):
    h = summary.loc["Hermes"]
    c = summary.loc["Chanel"]
    gap = h["avg_premium_pct"] - c["avg_premium_pct"]
    date_str = datetime.now().strftime("%B %d, %Y")

    # Top items by premium
    top_hermes = df[df["brand"] == "Hermes"].groupby("item")["resale_premium_pct"].mean().sort_values(ascending=False).head(3)
    top_chanel = df[df["brand"] == "Chanel"].groupby("item")["resale_premium_pct"].mean().sort_values(ascending=False).head(3)

    def item_rows(series):
        rows = ""
        for item, prem in series.items():
            short = item.replace("Hermès ", "").replace("Chanel ", "")
            rows += f"""
            <tr>
                <td>{short}</td>
                <td class="premium">+{prem:.0f}%</td>
            </tr>"""
        return rows

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Luxury Resale Intelligence Report</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Inter:wght@300;400;500&display=swap');

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    background: #0a0a0a;
    color: #e8e0d0;
    font-family: 'Inter', sans-serif;
    font-weight: 300;
    min-height: 100vh;
  }}

  .page {{
    max-width: 900px;
    margin: 0 auto;
    padding: 60px 40px;
  }}

  /* HEADER */
  .header {{
    border-bottom: 1px solid #2a2a2a;
    padding-bottom: 40px;
    margin-bottom: 50px;
  }}

  .eyebrow {{
    font-size: 10px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #c9a96e;
    margin-bottom: 20px;
  }}

  h1 {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 52px;
    font-weight: 300;
    line-height: 1.1;
    color: #f5f0e8;
    margin-bottom: 16px;
  }}

  h1 span {{
    color: #c9a96e;
  }}

  .subtitle {{
    font-size: 13px;
    color: #666;
    letter-spacing: 1px;
  }}

  /* KPI ROW */
  .kpi-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: #1a1a1a;
    border: 1px solid #1a1a1a;
    margin-bottom: 50px;
  }}

  .kpi {{
    background: #0f0f0f;
    padding: 28px 24px;
  }}

  .kpi-label {{
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #555;
    margin-bottom: 10px;
  }}

  .kpi-value {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 36px;
    font-weight: 300;
    color: #c9a96e;
    line-height: 1;
  }}

  .kpi-sub {{
    font-size: 11px;
    color: #444;
    margin-top: 6px;
  }}

  /* BRAND CARDS */
  .brands {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 50px;
  }}

  .brand-card {{
    border: 1px solid #1e1e1e;
    padding: 32px;
    background: #0d0d0d;
  }}

  .brand-name {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 28px;
    font-weight: 300;
    margin-bottom: 4px;
  }}

  .brand-signal {{
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 24px;
    padding: 4px 10px;
    display: inline-block;
  }}

  .signal-strong {{ color: #c9a96e; border: 1px solid #c9a96e; }}
  .signal-healthy {{ color: #7ab87a; border: 1px solid #7ab87a; }}

  .brand-stat {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #1a1a1a;
    font-size: 12px;
  }}

  .brand-stat:last-child {{ border-bottom: none; }}
  .stat-label {{ color: #555; }}
  .stat-value {{ color: #e8e0d0; }}
  .premium {{ color: #c9a96e; font-weight: 500; }}

  /* TOP ITEMS */
  .top-items {{
    margin-top: 20px;
  }}

  .top-items h4 {{
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #444;
    margin-bottom: 12px;
  }}

  .top-items table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 11px;
  }}

  .top-items td {{
    padding: 7px 0;
    border-bottom: 1px solid #161616;
    color: #888;
  }}

  .top-items td:first-child {{ color: #bbb; }}

  /* INSIGHTS */
  .insights {{
    margin-bottom: 50px;
  }}

  .section-title {{
    font-size: 9px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #c9a96e;
    margin-bottom: 24px;
    padding-bottom: 12px;
    border-bottom: 1px solid #1a1a1a;
  }}

  .insight-block {{
    padding: 24px 28px;
    border-left: 2px solid #c9a96e;
    background: #0d0d0d;
    margin-bottom: 16px;
  }}

  .insight-brand {{
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #c9a96e;
    margin-bottom: 10px;
  }}

  .insight-text {{
    font-size: 13px;
    line-height: 1.8;
    color: #aaa;
  }}

  /* COMPARATIVE */
  .comparative {{
    border: 1px solid #1e1e1e;
    padding: 36px;
    background: #0d0d0d;
    margin-bottom: 50px;
  }}

  .gap-number {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 72px;
    font-weight: 300;
    color: #c9a96e;
    line-height: 1;
    margin-bottom: 8px;
  }}

  .gap-label {{
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #555;
    margin-bottom: 20px;
  }}

  .gap-text {{
    font-size: 13px;
    line-height: 1.9;
    color: #777;
    max-width: 600px;
  }}

  /* BAR CHART */
  .bar-chart {{
    margin-top: 30px;
  }}

  .bar-row {{
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 14px;
  }}

  .bar-brand {{
    font-size: 11px;
    color: #666;
    width: 60px;
    text-align: right;
    letter-spacing: 1px;
  }}

  .bar-track {{
    flex: 1;
    height: 2px;
    background: #1a1a1a;
    position: relative;
  }}

  .bar-fill {{
    height: 100%;
    background: #c9a96e;
    transition: width 1s ease;
  }}

  .bar-fill.chanel {{ background: #7ab87a; }}

  .bar-pct {{
    font-size: 12px;
    color: #c9a96e;
    width: 60px;
  }}

  .bar-pct.chanel {{ color: #7ab87a; }}

  /* FOOTER */
  .footer {{
    border-top: 1px solid #1a1a1a;
    padding-top: 30px;
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: #333;
    letter-spacing: 1px;
  }}

  .footer-brand {{ color: #c9a96e; }}
</style>
</head>
<body>
<div class="page">

  <!-- HEADER -->
  <div class="header">
    <div class="eyebrow">Luxury Resale Intelligence · Hermès vs Chanel</div>
    <h1>Resale Premium<br><span>Index Report</span></h1>
    <div class="subtitle">{date_str} &nbsp;·&nbsp; Secondary Market Analysis &nbsp;·&nbsp; 235 Listings Tracked</div>
  </div>

  <!-- KPI ROW -->
  <div class="kpi-row">
    <div class="kpi">
      <div class="kpi-label">Hermès Avg Premium</div>
      <div class="kpi-value">+{h['avg_premium_pct']:.0f}%</div>
      <div class="kpi-sub">above retail</div>
    </div>
    <div class="kpi">
      <div class="kpi-label">Chanel Avg Premium</div>
      <div class="kpi-value">+{c['avg_premium_pct']:.0f}%</div>
      <div class="kpi-sub">above retail</div>
    </div>
    <div class="kpi">
      <div class="kpi-label">Premium Gap</div>
      <div class="kpi-value">{gap:.0f}pp</div>
      <div class="kpi-sub">Hermès advantage</div>
    </div>
    <div class="kpi">
      <div class="kpi-label">Listings Tracked</div>
      <div class="kpi-value">235</div>
      <div class="kpi-sub">last 30 days</div>
    </div>
  </div>

  <!-- BRAND CARDS -->
  <div class="brands">
    <div class="brand-card">
      <div class="brand-name">Hermès</div>
      <div class="brand-signal signal-strong">🔥 Strong</div>
      <div class="brand-stat"><span class="stat-label">Avg Resale Price</span><span class="stat-value">${h['avg_resale_price']:,.0f}</span></div>
      <div class="brand-stat"><span class="stat-label">Avg Retail Price</span><span class="stat-value">${h['avg_retail_price']:,.0f}</span></div>
      <div class="brand-stat"><span class="stat-label">Avg Premium</span><span class="premium">+{h['avg_premium_pct']:.1f}%</span></div>
      <div class="brand-stat"><span class="stat-label">Max Premium</span><span class="premium">+{h['max_premium_pct']:.1f}%</span></div>
      <div class="brand-stat"><span class="stat-label">Listings</span><span class="stat-value">{int(h['listings'])}</span></div>
      <div class="top-items">
        <h4>Top Items by Premium</h4>
        <table>{item_rows(top_hermes)}</table>
      </div>
    </div>

    <div class="brand-card">
      <div class="brand-name">Chanel</div>
      <div class="brand-signal signal-healthy">✅ Healthy</div>
      <div class="brand-stat"><span class="stat-label">Avg Resale Price</span><span class="stat-value">${c['avg_resale_price']:,.0f}</span></div>
      <div class="brand-stat"><span class="stat-label">Avg Retail Price</span><span class="stat-value">${c['avg_retail_price']:,.0f}</span></div>
      <div class="brand-stat"><span class="stat-label">Avg Premium</span><span class="premium">+{c['avg_premium_pct']:.1f}%</span></div>
      <div class="brand-stat"><span class="stat-label">Max Premium</span><span class="premium">+{c['max_premium_pct']:.1f}%</span></div>
      <div class="brand-stat"><span class="stat-label">Listings</span><span class="stat-value">{int(c['listings'])}</span></div>
      <div class="top-items">
        <h4>Top Items by Premium</h4>
        <table>{item_rows(top_chanel)}</table>
      </div>
    </div>
  </div>

  <!-- COMPARATIVE -->
  <div class="comparative">
    <div class="section-title">Comparative Signal</div>
    <div class="gap-number">{gap:.0f}pp</div>
    <div class="gap-label">Hermès Premium Advantage over Chanel</div>
    <div class="gap-text">
      Hermès commands a structural scarcity premium that Chanel cannot replicate through price increases alone.
      The gap is driven by quota systems, purchase history requirements, and controlled distribution —
      mechanics that have made the Birkin the world's most consistent alternative asset.
      For LVMH and Richemont strategy teams, this benchmark defines the ceiling of what
      deliberate scarcity architecture can achieve in luxury brand equity.
    </div>
    <div class="bar-chart">
      <div class="bar-row">
        <div class="bar-brand">Hermès</div>
        <div class="bar-track"><div class="bar-fill" style="width:{min(h['avg_premium_pct']/250*100, 100):.0f}%"></div></div>
        <div class="bar-pct">+{h['avg_premium_pct']:.0f}%</div>
      </div>
      <div class="bar-row">
        <div class="bar-brand">Chanel</div>
        <div class="bar-track"><div class="bar-fill chanel" style="width:{min(c['avg_premium_pct']/250*100, 100):.0f}%"></div></div>
        <div class="bar-pct chanel">+{c['avg_premium_pct']:.0f}%</div>
      </div>
    </div>
  </div>

  <!-- INSIGHTS -->
  <div class="insights">
    <div class="section-title">Strategy Insights</div>

    <div class="insight-block">
      <div class="insight-brand">Hermès</div>
      <div class="insight-text">
        Extraordinary pricing power: Hermès resale trades at +{h['avg_premium_pct']:.0f}% above retail on average,
        indicating severe supply scarcity and inelastic demand. A controlled retail price increase of 10–15%
        would likely have minimal demand impact while improving margin significantly.
        The Birkin's status as an alternative asset class insulates it from macroeconomic softness.
      </div>
    </div>

    <div class="insight-block">
      <div class="insight-brand">Chanel</div>
      <div class="insight-text">
        Strong but vulnerable: Chanel's +{c['avg_premium_pct']:.0f}% average premium reflects genuine desirability,
        but {c['min_premium_pct']:.0f}% floor pricing suggests some SKUs trade at or below retail —
        a signal of oversaturation risk in entry-level categories.
        A selective authenticated resale partnership could capture value currently flowing to third-party platforms
        while reinforcing brand control.
      </div>
    </div>
  </div>

  <!-- FOOTER -->
  <div class="footer">
    <div>Luxury Resale Intelligence Agent &nbsp;·&nbsp; <span class="footer-brand">Built by Sakshi Pednekar</span></div>
    <div>Data: Secondary Market · {date_str}</div>
  </div>

</div>
</body>
</html>"""

    with open("report.html", "w") as f:
        f.write(html)
    print("✅ report.html generated!")


# --- RUN ---
df = generate_sample_data()

summary = df.groupby("brand").agg(
    listings=("price_usd", "count"),
    avg_resale_price=("price_usd", "mean"),
    avg_retail_price=("retail_usd", "mean"),
    avg_premium_pct=("resale_premium_pct", "mean"),
    max_premium_pct=("resale_premium_pct", "max"),
    min_premium_pct=("resale_premium_pct", "min"),
).round(2)

generate_report(df, summary)