import os
import re
import random
import urllib.parse
import requests

def ieskoti_wikimedia(uzklausa, headers):
    wiki_url = "https://" + "commons.wikimedia.org" + "/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {uzklausa}",
        "gsrnamespace": 6,
        "gsrlimit": 15,
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": 800,
        "format": "json"
    }
    res = requests.get(wiki_url, params=params, headers=headers, timeout=15)
    puslapiai = list(res.json().get("query", {}).get("pages", {}).values())
    random.shuffle(puslapiai)
    
    for p in puslapiai:
        info = p.get("imageinfo", [])
        if info:
            img_url = info[0].get("thumburl") or info[0].get("url")
            if img_url and not img_url.lower().endswith((".svg", ".tif", ".tiff")):
                img_res = requests.get(img_url, headers=headers, timeout=15)
                if img_res.ok and len(img_res.content) > 10000:
                    return img_res.content
    return None

def sukurti_paveiksleli(aprasymas, failo_vardas):
    os.makedirs("images", exist_ok=True)
    pilnas_kelias = f"images/{failo_vardas}.jpg"
    headers = {"User-Agent": "VilniusPulseBot/1.0 (https://vercel.app)"}
    
    # 1. Bandome rasti tikslią nuotrauką pagal renginio raktinius žodžius
    svarus = re.sub(r'[^a-zA-Z\s]', '', aprasymas).split()
    ignoruoti = {"vilnius", "lithuania", "festival", "days", "edition", "party", "guided", "tour", "with", "the", "for", "and"}
    raktiniai = [z for z in svarus if z.lower() not in ignoruoti and len(z) > 3][:2]
    
    kandidatai = []
    if raktiniai:
        kandidatai.append(" ".join(raktiniai))
    kandidatai.extend(["Vilnius Old Town", "Vilnius Cathedral", "Symphony orchestra concert", "Modern art gallery"])

    for fraze in kandidatai:
        try:
            nuotrauka = ieskoti_wikimedia(fraze, headers)
            if nuotrauka:
                with open(pilnas_kelias, "wb") as f:
                    f.write(nuotrauka)
                print(f"Parsiųsta nuotrauka pagal: {fraze}")
                return pilnas_kelias
        except Exception:
            continue

    return pilnas_kelias
