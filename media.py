import os
import re
import random
import requests

def sukurti_paveiksleli(aprasymas, failo_vardas):
    os.makedirs("images", exist_ok=True)
    pilnas_kelias = f"images/{failo_vardas}.jpg"
    
    # 1. Ieškome tikros nuotraukos per Tavily API (kuris garantuotai veikia iš GitHub)
    tavily_key = os.environ.get("TAVILY_API_KEY")
    if tavily_key:
        try:
            tavily_url = "https://" + "api.tavily" + ".com/search"
            payload = {
                "api_key": tavily_key,
                "query": f"{aprasymas} photography",
                "include_images": True,
                "max_results": 5
            }
            res = requests.post(tavily_url, json=payload, timeout=15)
            nuotraukos = res.json().get("images", [])
            random.shuffle(nuotraukos)
            for img_url in nuotraukos:
                if any(w in img_url.lower() for w in ["logo", "icon", "poster", "banner", ".svg"]):
                    continue
                try:
                    img_res = requests.get(img_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                    if img_res.ok and "image" in img_res.headers.get("Content-Type", "") and len(img_res.content) > 15000:
                        with open(pilnas_kelias, "wb") as f:
                            f.write(img_res.content)
                        print(f"Parsiųsta Tavily nuotrauka: {img_url[:50]}")
                        return pilnas_kelias
                except Exception:
                    continue
        except Exception as e:
            print("Tavily klaida:", e)

    # 2. Atsarginis variantas (visada veikianti estetiška nuotrauka be užrašų)
    try:
        seed = random.randint(1, 10000)
        atsarginis = requests.get(f"https://picsum.photos{seed}/800/800", timeout=15, allow_redirects=True)
        if atsarginis.ok and len(atsarginis.content) > 10000:
            with open(pilnas_kelias, "wb") as f:
                f.write(atsarginis.content)
            print("Parsiųsta atsarginė Picsum nuotrauka")
            return pilnas_kelias
    except Exception:
        pass

    return pilnas_kelias
