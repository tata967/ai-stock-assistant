import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

# Replace this with any stock symbol you want to track
WATCHLIST = ['TCS.NS', 'INFY.NS', 'RELIANCE.NS']
NEWS_KEYWORDS = ['profit', 'loss', 'merger', 'deal', 'growth']

def fetch_news():
    url = "https://news.google.com/search?q=stock+market+india&hl=en-IN&gl=IN&ceid=IN:en"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    headlines = soup.find_all('a', class_='DY5T1d RZIKme')
    return [h.text for h in headlines[:5]]

def analyze_news(news):
    scored = []
    for item in news:
        for word in NEWS_KEYWORDS:
            if word.lower() in item.lower():
                scored.append(item)
                break
    return scored

def send_email(message):
    sender = "your_email@gmail.com"
    receiver = "your_email@gmail.com"
    password = "your_app_password"  # Not Gmail password; use an App Password

    msg = MIMEText(message)
    msg['Subject'] = "📈 Stock AI Alert"
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)

if __name__ == "__main__":
    news = fetch_news()
    alerts = analyze_news(news)
    if alerts:
        message = "\n".join(alerts)
        send_email(message)

