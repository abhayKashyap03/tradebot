# Project Overview

This project is an autonomous trading bot written in Python. It analyzes stock market data from various sources, applies a trading strategy, and can execute trades automatically. The core of the trading strategy is powered by the Gemini API, which is used to make trading decisions based on a combination of technical and fundamental analysis, as well as news and social media sentiment.

## Main Technologies

*   **Python 3.10**
*   **Conda** for environment management
*   **uv** for package installation
*   **pre-commit** for code quality checks
*   **google-genai** for the core trading strategy
*   **pandas** for data manipulation
*   **requests** for making HTTP requests
*   **robin-stocks** for trading with Robinhood
*   **sec-api** for insider trading data
*   **tweepy** for Twitter data
*   **alpha-vantage** for financial data
*   **newsapi-python** for news articles

## Architecture

The project is structured into the following components:

*   **`tradebot/main.py`**: The main entry point of the application. It initializes the clients, fetches data, performs analysis, and then uses the `StrategyEngine` to make a trading decision.
*   **`tradebot/strategy.py`**: This file contains the `StrategyEngine` class, which uses the Gemini API to decide whether to buy, sell, or hold a stock based on the data provided.
*   **`tradebot/clients/`**: This directory contains the clients for interacting with external services like Robinhood, Alpha Vantage, NewsAPI, and Twitter.
*   **`tradebot/analyzers/`**: This directory contains the logic for performing technical and fundamental analysis on the stock data.
*   **`tradebot/configs/`**: This directory contains the configuration for the application, including API keys and logger settings.

# Building and Running

1.  **Set up the environment:**
    ```bash
    conda env create -f environment.yml
    conda activate tradebot
    ```

2.  **Install dependencies:**
    ```bash
    pip install uv
    uv pip install -e .
    ```

3.  **Set up pre-commit hooks (for development):**
    ```bash
    pre-commit install
    pre-commit run --all-files
    ```

4. **Testing code and new changes (for dev):**
   ```bash
   pytest tests/
   ```

5.  **Run the bot:**
    ```bash
    python -m tradebot.main
    ```

# Development Conventions

*   **Code Style:** The project uses `ruff` for linting and formatting. The configuration is in `.pre-commit-config.yaml`.
*   **Type Hinting:** The project uses `mypy` for static type checking.
*   **Testing:** The project uses `pytest` for testing. Tests are located in the `tests/` directory.
*   **Commits:** Always run `pre-commit` on all files before committing. Commit messages should follow the [Conventional Commits](https.conventionalcommits.org/en/v1.0.0/) specification.
* **Making Changes:** Always confirm with the user before making significant changes or running important commands (including git). Unless the user specifies that you can autonomously run commands and make changes in the prompt, always confirm first.
