import os
import re
import random
import requests

DRAUDZIAMI_ZODZIAI = {
    "poster", "logo", "flyer", "banner", "sign", "text", "document",
    "map", "cover", "page", "scan", "plakat", "afisha", "ticket",
    "brochure", "leaflet", "certificate", "diagram", "chart", "stamp"
}

def ar_svari_nuotrauka(pavadinimas, plotis, aukstis):
    pav_mazosiomis = pavadinimas.lower()
    if any(z in pav_mazosiomis for z in DRAUDZIAMI_ZODZIAI):
        return False
    if plotis and aukstis:
        santykis = plotis / aukstis
        if santykis < 0.65 or santykis > 2.2:
            return False
    return True

def ieskoti_wikimedia(uzklausa, headers):
    wiki_url = "https://" + "commons.wikimedia.org" + "/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {uzklausa}",
        "gsrnamespace": 6,
        "gsrlimit": 20,
        "prop": "imageinfo",
        "iiprop": "url|size",
        "iiurlwidth": 800,
        "format": "json"
    }
    res = requests.get(wiki_url, params=params, headers=headers, timeout=15)
    puslapiai = list(res.json().get("query", {}).get("pages", {}).values())
    random.shuffle(puslapiai)
    
    for p in puslapiai:
        pavadinimas = p.get("title", "")
        info = p.get("imageinfo", [])
        if info:
            duomenys = info[0]
            plotis = duomenys.get("width", 0)
            aukstis = duomenys.get("height", 0)
            
            if not ar_svari_nuotrauka(pavadinimas, plotis, aukstis):
                continue

            img_url = duomenys.get("thumburl") or duomenys.get("url")
            if img_url and img_url.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                img_res = requests.get(img_url, headers=headers, timeout=15)
                if img_res.ok and len(img_res.content) > 15000:
                    return img_res.content
    return None

def sukurti_paveiksleli(aprasymas, failo_vardas):
    os.makedirs("images", exist_ok=True)
    pilnas_kelias = f"images/{failo_vardas}.jpg"
    headers = {"User-Agent": "VilniusPulseBot/1.0 (https://vercel.app)"}
    
    svarus = re.sub(r'[^a-zA-Z\s]', '', aprasymas).split()
    ignoruoti = {"vilnius", "lithuania", "festival", "days", "edition", "party", "guided", "tour", "with", "the", "for", "and"}
    raktiniai = [z for z in svarus if z.lower() not in ignoruoti and len(z) > 3][:2]
    
    kandidatai = []
    if raktiniai:
        kandidatai.append(" ".join(raktiniai) + " photography")
    kandidatai.extend([
        "Vilnius Old Town architecture",
        "Vilnius Cathedral Square",
        "Symphony orchestra stage",
        "Contemporary art museum interior"
    ])

    for fraze in kandidatai:
        try:
            nuotrauka = ieskoti_wikimedia(fraze, headers)
            if nuotrauka:
                with open(pilnas_kelias, "wb") as f:
                    f.write(nuotrauka)
                print(f"Parsiųsta švari fotografija pagal: {fraze}")
                return pilnas_kelias
        except Exception:
            continue

    return pilnas_kelias
