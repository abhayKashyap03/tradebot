import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetching credentials from environment variables
ROBINHOOD_EMAIL = os.getenv("ROBINHOOD_EMAIL")
ROBINHOOD_PWD = os.getenv("ROBINHOOD_PWD")
AV_API_KEY = os.getenv("AV_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MAX_POSITION_SIZE = 150
MAX_DAILY_TRADES = 6
MAX_PORTFOLIO_SHARE = 17

if not ROBINHOOD_EMAIL or not ROBINHOOD_PWD:
    raise ValueError(
        "Robinhood credentials (email/password) are not set in the .env file."
    )

if not AV_API_KEY:
    raise ValueError("Alpha Vantage API key is not set in the .env file.")

if not NEWS_API_KEY:
    raise ValueError("News API key is not set in the .env file.")

if (
    not TWITTER_API_KEY
    or not TWITTER_API_SECRET
    or not TWITTER_ACCESS_TOKEN
    or not TWITTER_ACCESS_TOKEN_SECRET
    or not TWITTER_BEARER_TOKEN
):
    raise ValueError("Twitter API credentials are not set in the .env file.")

if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is not set in the .env file.")
