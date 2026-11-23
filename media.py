import os
import re
import random
import requests

def sukurti_paveiksleli(aprasymas, failo_vardas):
    os.makedirs("images", exist_ok=True)
    pilnas_kelias = f"images/{failo_vardas}.jpg"
    
    # Išrenkame 2 pagrindinius angliškus temos žodžius
    svarus = re.sub(r'[^a-zA-Z\s]', '', aprasymas).lower().split()
    ignoruoti = {"vilnius", "lithuania", "festival", "days", "edition", "party", "guided", "tour", "with", "the", "for", "and", "various", "venues"}
    raktiniai = [z for z in svarus if z not in ignoruoti and len(z) > 3][:2]
    
    temos_tagai = ",".join(raktiniai) if raktiniai else "vilnius,architecture"
    lock_id = random.randint(1, 10000)
    
    # LoremFlickr grąžina tikras fotografijas pagal temą, be užrašų ir plakatų
    domenas = "loremflickr" + ".com"
    url = f"https://{domenas}/800/800/{temos_tagai}?lock={lock_id}"
    
    try:
        atsakas = requests.get(url, timeout=20, allow_redirects=True)
        if atsakas.ok and len(atsakas.content) > 10000:
            with open(pilnas_kelias, "wb") as f:
                f.write(atsakas.content)
            print(f"Parsiųsta nuotrauka pagal temas: {temos_tagai}")
            return pilnas_kelias
    except Exception as e:
        print("Klaida siunčiant nuotrauką:", e)

    return pilnas_kelias
