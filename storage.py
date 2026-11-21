import os
import json

def nuskaityti_faila(kelias):
    with open(kelias, "r", encoding="utf-8") as f:
        return f.read()

def gauti_istorija():
    if not os.path.exists("articles.json"):
        return [], "Nėra"
    with open("articles.json", "r", encoding="utf-8") as f:
        straipsniai = json.load(f)
    paskutiniai = [s["event_name"] for s in straipsniai[:3]]
    draudziami = ", ".join(paskutiniai) if paskutiniai else "Nėra"
    return straipsniai, draudziami

def issaugoti_straipsni(seni_straipsniai, naujas_straipsnis):
    visi = [naujas_straipsnis] + seni_straipsniai
    with open("articles.json", "w", encoding="utf-8") as f:
        json.dump(visi, f, ensure_ascii=False, indent=2)
