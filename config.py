import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash-lite")

RSS_FEEDS = {
    "Anadolu Ajansi Spor": "https://www.aa.com.tr/tr/rss/default?cat=spor",
    "TR Haber Son Dakika": "https://www.trthaber.com/sondakika.rss",
    "BBC Turkce": "https://feeds.bbci.co.uk/turkce/rss.xml",
    "Fotomac Super Lig": "https://www.fotomac.com.tr/rss/superlig.xml",
    "Fotomac Transfer": "https://www.fotomac.com.tr/rss/transfer.xml",
    "Fotomac Futbol": "https://www.fotomac.com.tr/rss/futbol.xml",
    "BBC Sport Football": "https://feeds.bbci.co.uk/sport/football/rss.xml",
    "Sky Sports Football": "https://www.skysports.com/rss/0,,11095,00.xml",
}
