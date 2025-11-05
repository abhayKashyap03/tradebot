# Autonomous Trading Bot

A Python-based application for automated stock market analysis and trading based on a predefined strategy. This bot is designed to run in the background, executing research and trades without manual intervention.

## Key Features

*   **Multi-Source Data Aggregation**: Gathers market data, news, social media sentiment, and insider trading information from various APIs (Alpha Vantage, NewsAPI, Tweepy, SEC-API).
*   **Comprehensive Analysis**: Performs technical analysis (e.g., moving averages), fundamental analysis, and sentiment scoring.
*   **AI-Powered Strategy Engine**: Leverages a Large Language Model (LLM) to synthesize all analyzed data and generate a final trading signal (BUY, SELL, or HOLD).
*   **Secure Configuration**: Manages API keys and secrets safely via a `.env` file, keeping credentials out of the source code.
*   **Structured Logging**: Implements robust logging to monitor all bot activities, decisions, and potential errors.

## Project Status

**Under Development:** This project is in the final stages of development. The core analysis and decision-making engine is complete.

*   **[Complete]** Core Infrastructure (Logging, Configuration)
*   **[Complete]** Data Acquisition Layer
*   **[Complete]** Analysis & Strategy Engine
*   **[Completed]** Trade Execution & Risk Management
*   Overall integration in-progress.

**v2 plans:**
* SLM implementation for sentiment analysis focused on finance
* Continual learning experimentation
* Time-series predictor
* Specialist vs. generalist model implementations
* Backtesting strategies

The bot can currently analyze market data and generate trading signals. However, it is **not yet capable of executing live trades** or performing risk management.

## Getting Started

### Prerequisites

- Conda installed
- Git installed

### Installation

1. Clone the repository:
   ```bash
   git clone https://www.github.com/abhaykashyap03/tradebot.git
   ```

2. Setup virtual env, install packages
   ```bash
   cd tradebot

   conda env create -f environment.yml
   conda activate tradebot

   pip install uv

   uv pip install -e .

   # install pre-commit hooks for dev & contributing
   pre-commit install
   pre-commit run --all-files
   ```
