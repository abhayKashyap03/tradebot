from setuptools import setup, find_packages

setup(
    name="tradebot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-genai",
        "python-dotenv",
        "requests",
        "tweepy",
        "sec-api",
        "robin_stocks",
        "pre-commit",
        "numpy<2.0.0",
        "pandas",
        "pandas-ta",
    ],
)
