from rss_fetcher import fetch_all_feeds
from ai_formatter import format_news
from discord_sender import send_news


def main():
    print("[1/3] RSS feed'ler cekiliyor...")
    news = fetch_all_feeds(hours=24)
    print(f"     {len(news)} haber bulundu.")

    if not news:
        print("[INFO] Son 24 saatte futbol haberi bulunamadi.")
        return

    print("[2/3] AI ile haberler formatlanıyor...")
    formatted = format_news(news)

    print("[3/3] Discord'a gonderiliyor...")
    send_news(formatted)

    print("[DONE] Islem tamamlandi!")


if __name__ == "__main__":
    main()
