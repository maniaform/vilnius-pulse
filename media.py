import os
import random
import urllib.parse
import requests

def sukurti_paveiksleli(aprasymas, failo_vardas):
    os.makedirs("images", exist_ok=True)
    pilnas_kelias = f"images/{failo_vardas}.jpg"
    
    # 1 bandymas: DI iliustracija (Pollinations)
    stilius = "Vibrant risograph print illustration, bold cobalt blue and warm coral colors, grainy paper texture, Monocle magazine art style, no text: "
    seed = random.randint(1, 999999)
    uzklausa = urllib.parse.quote(stilius + aprasymas)
    url = "https://" + "image.pollinations.ai" + f"/prompt/{uzklausa}?width=800&height=800&seed={seed}&nologo=true"
    
    try:
        atsakas = requests.get(url, timeout=25)
        if atsakas.ok and "image" in atsakas.headers.get("Content-Type", "") and len(atsakas.content) > 5000:
            with open(pilnas_kelias, "wb") as f:
                f.write(atsakas.content)
            return pilnas_kelias
    except Exception:
        pass

    # 2 bandymas: Tikslinga nuotraukos paieška pagal renginio temą per Tavily
    tavily_key = os.environ.get("TAVILY_API_KEY")
    if tavily_key:
        try:
            tavily_url = "https://" + "://tavily.com" + "/search"
            payload = {
                "api_key": tavily_key,
                "query": aprasymas,
                "include_images": True,
                "max_results": 3
            }
            res = requests.post(tavily_url, json=payload, timeout=15)
            nuotraukos = res.json().get("images", [])
            for img_url in nuotraukos:
                try:
                    img_res = requests.get(img_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                    if img_res.ok and "image" in img_res.headers.get("Content-Type", "") and len(img_res.content) > 10000:
                        with open(pilnas_kelias, "wb") as f:
                            f.write(img_res.content)
                        return pilnas_kelias
                except Exception:
                    continue
        except Exception:
            pass

    return pilnas_kelias
