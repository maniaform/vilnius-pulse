import os
import json
import requests
from storage import nuskaityti_faila

API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://" + "api.groq.com" + "/openai/v1/chat/completions"

def siusti_uzklausa(messages, modelis="qwen/qwen3.8-27b", temperature=0.2, json_mode=False, max_tokens=600):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": modelis,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
        
    atsakas = requests.post(GROQ_URL, headers=headers, json=payload)
    if not atsakas.ok:
        print("Groq klaidos detalės:", atsakas.text)
    atsakas.raise_for_status()
    return atsakas.json()["choices"][0]["message"]["content"]

def ieskoti_internete(data_str):
    tavily_key = os.environ.get("TAVILY_API_KEY")
    url = "https://api.tavily.com" + "/search"
    payload = {
        "api_key": tavily_key,
        "query": f"renginiai koncertai parodos festivaliai Vilniuje nuo {data_str}",
        "search_depth": "basic",
        "max_results": 7
    }
    atsakas = requests.post(url, json=payload, timeout=15)
    atsakas.raise_for_status()
    rezultatai = atsakas.json().get("results", [])
    return "\n".join([f"- {r['title']} (URL: {r['url']}): {r['content']}" for r in rezultatai])

def rasti_rengini(data_str, draudziami):
    rasti_duomenys = ieskoti_internete(data_str)
    sablonas = nuskaityti_faila("prompts/redaktorius.txt")
    tekstas = sablonas.replace("{siandienos_data}", data_str)
    tekstas = tekstas.replace("{draudziami_renginiai}", draudziami)
    tekstas += f"\n\nŠtai ką radome internete:\n{rasti_duomenys}"
    
    messages = [{"role": "user", "content": tekstas}]
    return siusti_uzklausa(messages, modelis="qwen/qwen3.8-27b", temperature=0.1, max_tokens=300)

def parasyti_straipsni(faktai):
    sablonas = nuskaityti_faila("prompts/zurnalistas.txt")
    tekstas = sablonas.replace("{faktai}", faktai)
    nurodymas = (
        '\n\nGrąžink TIK gryną JSON objektą be jokio papildomo teksto su šiais raktais: '
        '"event_name", "event_name_en", "event_date", "event_date_en", "location", "location_en", '
        '"title", "title_en", "summary", "summary_en", "content", "content_en", "source_url", "image_prompt".'
    )
    messages = [{"role": "user", "content": tekstas + nurodymas}]
    atsakas = siusti_uzklausa(
        messages, 
        modelis="openai/gpt-oss-120b", 
        temperature=0.5, 
        json_mode=True, 
        max_tokens=3500
    )
    return json.loads(atsakas)
