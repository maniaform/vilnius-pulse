import os
import urllib.parse
import requests

def sukurti_paveiksleli(aprasymas, failo_vardas):
    os.makedirs("images", exist_ok=True)
    pilnas_kelias = f"images/{failo_vardas}.jpg"
    
    stilius = "Minimalist editorial magazine illustration, clean modern flat vector art, atmospheric Vilnius vibe, no text, no letters: "
    uzklausa = urllib.parse.quote(stilius + aprasymas)
    url = f"https://image.pollinations.ai/prompt/{uzklausa}?width=1280&height=720&nologo=true"
    
    atsakas = requests.get(url, timeout=60)
    atsakas.raise_for_status()
    
    with open(pilnas_kelias, "wb") as f:
        f.write(atsakas.content)
        
    return pilnas_kelias
