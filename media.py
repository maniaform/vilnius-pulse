import os
import random
import urllib.parse
import requests

def sukurti_paveiksleli(aprasymas, failo_vardas):
    os.makedirs("images", exist_ok=True)
    pilnas_kelias = f"images/{failo_vardas}.jpg"
    headers = {"User-Agent": "VilniusPulseBot/1.0 (https://vercel.app)"}
    
    # 1 bandymas: DI iliustracija (Pollinations)
    stilius = "Vibrant editorial illustration, modern art, bold colors, no text: "
    seed = random.randint(1, 999999)
    uzklausa = urllib.parse.quote(stilius + aprasymas)
    url = "https://" + "image.pollinations.ai" + f"/prompt/{uzklausa}?width=800&height=800&seed={seed}&nologo=true"
    
    try:
        atsakas = requests.get(url, timeout=20, headers=headers)
        if atsakas.ok and "image" in atsakas.headers.get("Content-Type", "") and len(atsakas.content) > 5000:
            with open(pilnas_kelias, "wb") as f:
                f.write(atsakas.content)
            return pilnas_kelias
    except Exception:
        pass

    # 2 bandymas: Tikslinga nuotraukų paieška per Wikimedia Commons (pagal 3 raktinius žodžius)
    try:
        import re
        svarus_zodziai = re.sub(r'[^a-zA-Z0-9\s]', '', aprasymas).split()[:3]
        paieskos_raktas = " ".join(svarus_zodziai) if svarus_zodziai else "Vilnius architecture"
        
        wiki_url = "https://" + "commons.wikimedia.org" + "/w/api.php"
        params = {
            "action": "query",
            "generator": "search",
            "gsrsearch": f"filetype:bitmap {paieskos_raktas}",
            "gsrnamespace": 6,
            "gsrlimit": 5,
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": 800,
            "format": "json"
        }
        res = requests.get(wiki_url, params=params, headers=headers, timeout=15)
        puslapiai = res.json().get("query", {}).get("pages", {})
        for p in puslapiai.values():
            info = p.get("imageinfo", [])
            if info:
               img_url = info[0].get("thumburl") or info[0].get("url")
                if img_url:
                    img_res = requests.get(img_url, headers=headers, timeout=15)
                    if img_res.ok and len(img_res.content) > 10000:
                        with open(pilnas_kelias, "wb") as f:
                            f.write(img_res.content)
                        print(f"Parsiųsta tikra nuotrauka pagal: {paieskos_raktas}")
                        return pilnas_kelias
    except Exception as e:
        print("Paieškos klaida:", e)

    return pilnas_kelias
