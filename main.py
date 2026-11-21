from datetime import datetime
from storage import gauti_istorija, issaugoti_straipsni
from agents import rasti_rengini, parasyti_straipsni
from media import sukurti_paveiksleli

def paleisti_redakcija():
    siandien = datetime.now().strftime("%Y-%m-%d")
    print(f"[{siandien}] Pradedamas darbas...")

    seni_straipsniai, draudziami = gauti_istorija()
    print(f"Ignoruojami paskutiniai renginiai: {draudziami}")

    faktai = rasti_rengini(siandien, draudziami)
    print("Redaktorius atrinko renginį.")

    straipsnis = parasyti_straipsni(faktai)
    print(f"Žurnalistas parašė: {straipsnis['title']}")

    failo_id = f"renginys-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    paveikslo_kelias = sukurti_paveiksleli(straipsnis["image_prompt"], failo_id)
    print(f"Paveikslėlis išsaugotas: {paveikslo_kelias}")

    galutinis_irasas = {
        "id": failo_id,
        "date_published": siandien,
        "event_name": straipsnis["event_name"],
        "event_name_en": straipsnis.get("event_name_en", straipsnis["event_name"]),
        "event_date": straipsnis["event_date"],
        "event_date_en": straipsnis.get("event_date_en", straipsnis["event_date"]),
        "location": straipsnis["location"],
        "location_en": straipsnis.get("location_en", straipsnis["location"]),
        "title": straipsnis["title"],
        "title_en": straipsnis.get("title_en", straipsnis["title"]),
        "summary": straipsnis["summary"],
        "summary_en": straipsnis.get("summary_en", straipsnis["summary"]),
        "content": straipsnis["content"],
        "content_en": straipsnis.get("content_en", straipsnis["content"]),
        "image_url": paveikslo_kelias
    }

    issaugoti_straipsni(seni_straipsniai, galutinis_irasas)
    print("Sėkmingai išsaugota į articles.json!")

if __name__ == "__main__":
    paleisti_redakcija()
