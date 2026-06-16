import pandas as pd
from datetime import datetime, timedelta
import random

# ================================================
# LUXURY RESALE INTELLIGENCE AGENT v2
# With built-in AI interpretation engine
# ================================================

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


def interpret_brand(brand, avg_premium, max_premium, min_premium, count, avg_price):
    """Rule-based AI interpretation engine"""
    
    insights = []
    
    # Pricing power signal
    if avg_premium > 100:
        insights.append(f"Extraordinary pricing power: {brand} resale trades at +{avg_premium:.0f}% above retail on average, indicating severe supply scarcity and inelastic demand — classic hallmarks of an 'investment bag' category.")
    elif avg_premium > 30:
        insights.append(f"Strong pricing power: {brand} commands a +{avg_premium:.0f}% resale premium, reflecting healthy secondary demand and brand desirability beyond the primary market.")
    elif avg_premium > 0:
        insights.append(f"Moderate pricing power: {brand} holds a slim +{avg_premium:.0f}% resale premium. Products retain value but lack the scarcity premium of tier-1 collectibles.")
    else:
        insights.append(f"Pricing pressure: {brand} is trading below retail at {avg_premium:.0f}%, suggesting oversaturation or weakening demand in the secondary market.")

    # Volatility signal
    spread = max_premium - min_premium
    if spread > 150:
        insights.append(f"High price dispersion ({min_premium:.0f}% to +{max_premium:.0f}%): Wide variance suggests condition and colorway drive significant value differences — authentication and provenance are critical.")
    elif spread > 80:
        insights.append(f"Moderate price dispersion ({min_premium:.0f}% to +{max_premium:.0f}%): Some items command outsized premiums, likely limited colorways or rare hardware combinations.")

    # Volume signal
    if count > 100:
        insights.append(f"High liquidity: {count} listings in 30 days indicates an active secondary market — buyers can transact without significant search costs.")
    elif count > 50:
        insights.append(f"Moderate liquidity: {count} listings reflects healthy but not excessive secondary supply.")

    # Strategic implication
    if avg_premium > 100:
        insights.append(f"Strategic implication: {brand}'s resale premium signals untapped primary pricing power. A controlled retail price increase of 10-15% would likely have minimal demand impact while improving margin significantly.")
    elif avg_premium > 20:
        insights.append(f"Strategic implication: {brand} should consider a selective resale partnership (e.g. authenticated resale channel) to capture value currently flowing to third-party platforms.")
    else:
        insights.append(f"Strategic implication: {brand} faces margin pressure in secondary markets. Brand heat initiatives — limited drops, collaborations, waitlist mechanics — could restore scarcity premium.")

    return insights


# --- RUN AGENT ---
print("=" * 55)
print("   LUXURY RESALE INTELLIGENCE AGENT")
print(f"   Report Date: {datetime.now().strftime('%B %d, %Y')}")
print("=" * 55)

df = generate_sample_data()

summary = df.groupby("brand").agg(
    listings=("price_usd", "count"),
    avg_resale_price=("price_usd", "mean"),
    avg_retail_price=("retail_usd", "mean"),
    avg_premium_pct=("resale_premium_pct", "mean"),
    max_premium_pct=("resale_premium_pct", "max"),
    min_premium_pct=("resale_premium_pct", "min"),
).round(2)

print("\n📊 RESALE PREMIUM INDEX")
print("-" * 55)
print(f"{'Brand':<10} {'Listings':>8} {'Avg Resale':>12} {'Avg Retail':>12} {'Premium':>10}")
print("-" * 55)
for brand, row in summary.iterrows():
    print(f"{brand:<10} {int(row['listings']):>8} ${row['avg_resale_price']:>11,.0f} ${row['avg_retail_price']:>11,.0f} {row['avg_premium_pct']:>+9.1f}%")

print("\n\n🧠 AI STRATEGY INTERPRETATION")
print("-" * 55)

for brand, row in summary.iterrows():
    print(f"\n▶ {brand.upper()}")
    insights = interpret_brand(
        brand=brand,
        avg_premium=row["avg_premium_pct"],
        max_premium=row["max_premium_pct"],
        min_premium=row["min_premium_pct"],
        count=int(row["listings"]),
        avg_price=row["avg_resale_price"]
    )
    for i, insight in enumerate(insights, 1):
        print(f"\n  {i}. {insight}")

print("\n\n💡 COMPARATIVE SIGNAL")
print("-" * 55)
h = summary.loc["Hermes", "avg_premium_pct"]
c = summary.loc["Chanel", "avg_premium_pct"]
gap = h - c
print(f"\nHermès commands a {gap:.0f} percentage point higher resale premium than Chanel.")
print(f"This gap represents Hermès' structural scarcity advantage —")
print(f"driven by quota systems, waitlists, and controlled distribution.")
print(f"For LVMH/Richemont strategists, this benchmark defines the ceiling")
print(f"of what effective scarcity mechanics can achieve.")

# Save
df.to_excel("raw_listings.xlsx", index=False)
summary.to_excel("price_summary.xlsx")
print(f"\n✅ Full dataset saved to raw_listings.xlsx")
print(f"✅ Summary saved to price_summary.xlsx")