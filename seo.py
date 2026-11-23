import os
import re
import json

BASE_URL = "https://vercel.app"

def sukurti_slug(tekstas):
    tekstas = tekstas.lower()
    lt_map = {'ą': 'a', 'č': 'c', 'ę': 'e', 'ė': 'e', 'į': 'i', 'š': 's', 'ų': 'u', 'ū': 'u', 'ž': 'z'}
    for k, v in lt_map.items():
        tekstas = tekstas.replace(k, v)
    tekstas = re.sub(r'[^a-z0-9]+', '-', tekstas).strip('-')
    return tekstas[:60]

def generuoti_seo_puslapius(straipsniai):
    os.makedirs("straipsniai", exist_ok=True)
    sitemap_urls = [f"{BASE_URL}/"]

    for art in straipsniai:
        slug = art.get("slug") or sukurti_slug(art["title"])
        art["slug"] = slug
        failo_kelias = f"straipsniai/{slug}.html"
        pilnas_url = f"{BASE_URL}/{failo_kelias}"
        sitemap_urls.append(pilnas_url)

        pastraipos_lt = "".join([f"<p>{p}</p>" for p in art["content"].split("\n\n") if p.strip()])
        pastraipos_en = "".join([f"<p>{p}</p>" for p in art.get("content_en", art["content"]).split("\n\n") if p.strip()])
        
        schema_data = {
            "@context": "https://schema.org",
            "@type": "Event",
            "name": art["event_name"],
            "startDate": art["event_date"].replace(" ", "T"),
            "location": {
                "@type": "Place",
                "name": art["location"],
                "address": {"@type": "PostalAddress", "addressLocality": "Vilnius", "addressCountry": "LT"}
            },
            "description": art["summary"],
            "image": f"{BASE_URL}/{art['image_url']}"
        }

        bilietu_mygtukas = ""
        if art.get("source_url", "").startswith("http"):
            bilietu_mygtukas = f'<a href="{art["source_url"]}" target="_blank" rel="noopener" class="ticket-btn">Renginio puslapis / Bilietai ↗</a>'

        html = f"""<!DOCTYPE html>
<html lang="lt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{art["title"]} | Vilniaus Pulsas</title>
    <meta name="description" content="{art["summary"]}">
    <meta property="og:title" content="{art["title"]}">
    <meta property="og:description" content="{art["summary"]}">
    <meta property="og:image" content="{BASE_URL}/{art["image_url"]}">
    <meta property="og:url" content="{pilnas_url}">
    <link rel="canonical" href="{pilnas_url}">
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;1,700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../style.css">
    <script type="application/ld+json">{json.dumps(schema_data, ensure_ascii=False)}</script>
</head>
<body>
    <header class="masthead">
        <div class="container masthead-top">
            <a href="../index.html" style="text-decoration:none;"><h1 class="brand-title">Vilniaus <span>Pulsas.</span></h1></a>
            <div class="header-controls">
                <a href="../index.html" class="lang-btn active" style="text-decoration:none;">← Visi renginiai</a>
            </div>
        </div>
    </header>

    <main class="container editorial-layout">
        <article class="featured-card">
            <div class="article-header-row">
                <div class="mini-thumbnail">
                    <img src="../{art["image_url"]}" alt="{art["title"]}">
                </div>
                <div class="header-text-block">
                    <span class="kicker">✦ {art["event_date"]} • {art["location"]}</span>
                    <h1 class="featured-title">{art["title"]}</h1>
                </div>
            </div>
            <p class="featured-summary">{art["summary"]}</p>
            <div class="article-content">{pastraipos_lt}</div>
            
            <hr style="margin: 40px 0; border: none; border-top: 1px solid var(--border-ink);">
            <span class="kicker">🇬🇧 English Version</span>
            <h2 class="featured-title" style="font-size: 1.6rem; margin-bottom: 16px;">{art.get("title_en", "")}</h2>
            <div class="article-content">{pastraipos_en}</div>
        </article>

        <aside class="sidebar">
            <div class="ticket-box">
                <span class="ticket-label">🎟️ Renginio pasas</span>
                <h3 class="ticket-event-name">{art["event_name"]}</h3>
                <div class="ticket-detail"><span>📅</span><span><strong>Kada:</strong> {art["event_date"]}</span></div>
                <div class="ticket-detail"><span>📍</span><span><strong>Kur:</strong> {art["location"]}</span></div>
                {bilietu_mygtukas}
            </div>
        </aside>
    </main>
</body>
</html>"""
        with open(failo_kelias, "w", encoding="utf-8") as f:
            f.write(html)

    # 1. Generuojame sitemap.xml
    xml_eilutes = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://sitemaps.org">']
    for u in sitemap_urls:
        xml_eilutes.append(f"  <url><loc>{u}</loc></url>")
    xml_eilutes.append("</urlset>")
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml_eilutes))

    # 2. Generuojame robots.txt
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")

    return straipsniai
