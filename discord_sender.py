import requests
from config import DISCORD_WEBHOOK_URL


def send_news(formatted):
    if isinstance(formatted, dict) and "sections" in formatted:
        embeds = _build_embeds(formatted)
        if embeds:
            payload = {"embeds": embeds[:10]}
            resp = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=30)
            _check_response(resp)
        else:
            _send_text(formatted.get("title", "Saha Muhbir"))
    else:
        text = formatted if isinstance(formatted, str) else str(formatted)
        _send_text(text)


def _send_text(text):
    chunks = [text[i:i+2000] for i in range(0, len(text), 2000)]
    for chunk in chunks:
        resp = requests.post(DISCORD_WEBHOOK_URL, json={"content": chunk}, timeout=30)
        _check_response(resp)


def _check_response(resp):
    if resp.status_code in (200, 204):
        print("[OK] Discord'a gonderildi.")
    else:
        print(f"[HATA] Discord: {resp.status_code} - {resp.text[:200]}")


def _build_embeds(formatted):
    embeds = []
    title = formatted.get("title", "Saha Muhbir")
    sections = formatted.get("sections", [])

    embeds.append({
        "title": f"⚽ {title}",
        "description": "Bugunun one cikan futbol haberleri",
        "color": 0x1E3A5F,
    })

    color_map = {
        "turk futbolu": 0xE30A17,
        "avrupa futbolu": 0x003399,
        "transfer": 0xFFD700,
        "genel futbol": 0x5865F2,
    }

    for section in sections:
        category = section.get("category", "Diger")
        items = section.get("items", [])
        desc = "\n".join(f"• {item}" for item in items)
        if len(desc) > 1024:
            desc = desc[:1021] + "..."

        embeds.append({
            "title": f"📰 {category}",
            "description": desc,
            "color": color_map.get(category.lower(), 0x5865F2),
        })

    return embeds
