import os
import json
import time
from media import sukurti_paveiksleli

with open("articles.json", "r", encoding="utf-8") as f:
    straipsniai = json.load(f)

for art in straipsniai:
    kelias = art.get("image_url", "")
    if not kelias:
        continue
        
    failo_vardas = os.path.splitext(os.path.basename(kelias))[0]
    tema = art.get("title_en") or art.get("title", "Vilnius cultural event")
    aprasymas = f"Artistic visual metaphor for: {tema}, Vilnius atmosphere"
    
    print(f"Atnaujinamas: {failo_vardas}...")
    sukurti_paveiksleli(aprasymas, failo_vardas)
    time.sleep(3)

print("Visi paveikslėliai sėkmingai atnaujinti!")
