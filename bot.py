import requests
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

    # echte negative Signale
    if "keine termine verfügbar" in html:
        print("kein Termin")
        return

    # bessere positive Signale
    positive_signals = [
        "termin auswählen",
        "verfügbar",
        "freie termine",
        "select appointment"
    ]

    if any(x in html for x in positive_signals):
        notify("🔥 Möglicher Termin sichtbar – bitte sofort prüfen!")
        print("TERMIN SIGNAL")
    else:
        print("kein eindeutiger Termin")


if __name__ == "__main__":
    check()
