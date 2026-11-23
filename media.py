import os
import random
import urllib.parse
import requests

def sukurti_paveiksleli(aprasymas, failo_vardas):
    os.makedirs("images", exist_ok=True)
    pilnas_kelias = f"images/{failo_vardas}.jpg"
    
    stiliai = [
        "Vibrant risograph print illustration, bold cobalt blue and warm coral colors, grainy paper texture, Monocle magazine art style, no text: ",
        "Cinematic moody photography, dramatic warm stage lighting, bokeh lights, atmospheric Vilnius evening, 35mm film grain, no text: ",
        "Modern surreal editorial collage art, rich emerald and gold accents, architectural silhouettes, artistic composition, no text: "
    ]
    pasirinktas_stilius = random.choice(stiliai)
    seed = random.randint(1, 999999)
    
    uzklausa = urllib.parse.quote(pasirinktas_stilius + aprasymas)
    url = "https://" + "image.pollinations.ai" + f"/prompt/{uzklausa}?width=800&height=800&seed={seed}&nologo=true"
    
    try:
        atsakas = requests.get(url, timeout=45)
        if atsakas.ok and "image" in atsakas.headers.get("Content-Type", ""):
            with open(pilnas_kelias, "wb") as f:
                f.write(atsakas.content)
            return pilnas_kelias
    except Exception:
        pass

    atsarginis = requests.get("https://picsum.photos", timeout=15)
    with open(pilnas_kelias, "wb") as f:
        f.write(atsarginis.content)
    return pilnas_kelias
