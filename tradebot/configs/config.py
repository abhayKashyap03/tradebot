import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetching credentials from environment variables
ROBINHOOD_EMAIL = os.getenv("ROBINHOOD_EMAIL")
ROBINHOOD_PWD = os.getenv("ROBINHOOD_PWD")
AV_API_KEY = os.getenv("AV_API_KEY")

if not ROBINHOOD_EMAIL or not ROBINHOOD_PWD:
    raise ValueError(
        "Robinhood credentials (email/password) are not set in the .env file."
    )

if not AV_API_KEY:
    raise ValueError("Alpha Vantage API key is not set in the .env file.")
