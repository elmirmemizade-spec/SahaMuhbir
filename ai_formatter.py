import json
import time
import requests
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL


def format_news(news_items):
    if not news_items:
        return _fallback_format([])

    news_text = "\n".join(
        f"- [{item['source']}] {item['title']}: {item['summary'][:200]}"
        for item in news_items[:30]
    )

    prompt = f"""Sen "Saha Muhbir" adinda bir futbol haber botusun.
Gelen futbol haberlerini kisa, etkili ve ilgicekici Discord mesajlarina donustur.

Kurallar:
- Turkce yaz
- Her haber icin kisa bir ozet yaz (1-2 cumle)
- Emoji kullan ama abartma
- Haberleri kategori ayir (Turk futbolu, Avrupa futbolu, Transfer)
- Max 2000 karakter olsun
- Baslik olarak "Saha Muhbir Gunun Futbol Haberleri" kullan

Haberler:
{news_text}

Ciktigi su formatta ver:
{{
  "title": "Baslik",
  "sections": [
    {{"category": "Kategori", "items": ["Haber 1", "Haber 2"]}}
  ]
}}"""

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": OPENROUTER_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 2000,
                },
                timeout=60,
            )

            if response.status_code != 200:
                print(f"[WARN] OpenRouter HTTP {response.status_code} (deneme {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(5)
                continue

            data = response.json()
            raw = data["choices"][0]["message"]["content"].strip()

            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1]
                if raw.endswith("```"):
                    raw = raw[:-3]
                raw = raw.strip()

            return json.loads(raw)

        except (json.JSONDecodeError, KeyError, requests.exceptions.RequestException) as e:
            print(f"[WARN] AI hatasi (deneme {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(5)

    print("[INFO] AI calismadi, fallback kullaniliyor...")
    return _fallback_format(news_items)


def _fallback_format(news_items):
    if not news_items:
        return {"title": "Saha Muhbir - Haber bulunamadi", "sections": []}

    sections = {}
    for item in news_items[:20]:
        source = item.get("source", "Diger")
        if "lig" in source.lower() or "futbol" in source.lower():
            cat = "Turk Futbolu"
        elif "transfer" in source.lower():
            cat = "Transfer"
        else:
            cat = "Genel Futbol"
        sections.setdefault(cat, []).append(f"**{item['title']}** ({source})")

    result_sections = [{"category": cat, "items": items} for cat, items in sections.items()]
    return {"title": "Saha Muhbir Gunun Futbol Haberleri", "sections": result_sections}
