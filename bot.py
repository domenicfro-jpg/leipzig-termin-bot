import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://terminvereinbarung.leipzig.de/m/leipzig-kfz/extern/calendar/?uid=c97bb32a-92b8-41ba-b5c2-f91d0e90019f&wsid=5291bc47-a574-4ab9-b93f-5af9f25d109e&lang=de&set_lang_ui=de&rev=06Ldz&step_goto=0#top"

TARGET = "umschreibung eines fahrzeugs mit auswärtigen kennzeichen"


def notify(msg):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": msg}
    )


def check():
    r = requests.get(URL, timeout=20)
    html = r.text.lower()

    # simple heuristics (API fallback light)
    blocked_signals = [
        "keine termine",
        "nicht verfügbar",
        "fully booked"
    ]

    if any(x in html for x in blocked_signals):
        print("kein Termin")
        return

    # wenn Kalender oder Inhalte geladen
    if "calendar" in html or "datum" in html:
        notify("🔥 Termin möglich: Leipzig Umschreibung verfügbar!")
        print("TERMIN SIGNAL")
    else:
        print("unklar")


if __name__ == "__main__":
    check()
