import json
import time
from media import sukurti_paveiksleli
from seo import generuoti_seo_puslapius

with open("articles.json", "r", encoding="utf-8") as f:
    straipsniai = json.load(f)

for art in straipsniai:
    unikalus_id = art.get("id", f"renginys-{int(time.time())}")
    paieskos_fraze = f"{art.get('event_name_en', art.get('event_name', ''))} {art.get('location_en', 'Vilnius')}"
    
    print(f"Ieškoma nuotraukos: {paieskos_fraze}...")
    naujas_kelias = sukurti_paveiksleli(paieskos_fraze, unikalus_id)
    art["image_url"] = naujas_kelias
    time.sleep(2)

atnaujinti = generuoti_seo_puslapius(straipsniai)

with open("articles.json", "w", encoding="utf-8") as f:
    json.dump(atnaujinti, f, ensure_ascii=False, indent=2)

print("Visi paveikslėliai sėkmingai atnaujinti!")
