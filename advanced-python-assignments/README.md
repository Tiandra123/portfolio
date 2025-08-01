# Advanced Python Class Assignments

This folder contains projects I completed for my Python courses as part of my MIS Master's program at USU. All projects were developed and tested on AWS EC2 instances using VS Code, or Cloud9.

## Projects Overview

### 1. Cryptocurrency Arbitrage Detector (`crypto_arbitrage.py`)

A network-based arbitrage detection system for cryptocurrency markets using graph theory algorithms.

**Key Features:**
- Real-time price data retrieval from CoinGecko API
- Weighted directed graph construction
- Graph traversal algorithms to find trading paths
- Arbitrage opportunity identification
- Forward and reverse path analysis
- Profit/loss calculations for trading opportunities

**Supported Cryptocurrencies:**
- Bitcoin (BTC), Ethereum (ETH), Litecoin (LTC)
- Ripple (XRP), Cardano (ADA), Bitcoin Cash (BCH), EOS

**Technologies Used:**
- Python
- NetworkX for graph theory operations
- REST APIs for real-time data
- Mathematical analysis for arbitrage detection

**How to Run:**
1. Install required libraries: `pip install networkx requests matplotlib`
2. Run: `python crypto_arbitrage.py`
3. View arbitrage opportunities in the console output

---

### 2. COVID-19 Data Analysis Tool (`covid_analysis.py`)

A comprehensive data analysis tool that retrieves and processes COVID-19 statistics for all US states and territories.

**Key Features:**
- REST API integration with COVID Tracking Project
- Data processing for all 50 states + territories
- Statistical analysis (averages, peaks, trends)
- Date formatting and data validation
- Monthly/yearly trend analysis
- JSON output file generation per state
- Handles missing data and edge cases

**Technologies Used:**
- Python
- REST APIs & JSON processing
- NumPy for statistical calculations
- Data analysis and datetime manipulation

**How to Run:**
1. Install required libraries: `pip install requests numpy`
2. Run: `python covid_analysis.py`
3. Output files will be generated as `[state].json` for each state

---

### 3. Blackjack Game (`blackjack.py`)

A command-line Blackjack implementation featuring complete game logic and user interaction.

**Key Features:**
- User input handling for hit/stay decisions
- Card dealing and score tracking
- House play rules (house hits when score ≤ 17)
- Bust detection and win/loss evaluation
- Game restart functionality
- Five-card Charlie rule implementation

**Technologies Used:**
- Python
- Object-Oriented Programming
- AWS EC2 for development environment

**Note:** This project uses a `DeckOfCards.py` class provided by the instructor.

**How to Run:**
1. Ensure you have the `DeckOfCards.py` file in the same directory
2. Run: `python blackjack.py`

---

### 4. Energy Efficiency Analysis Tool (`energy_analysis.py`) - My First Big Python Project!

A comprehensive energy analysis system that examines electricity generation efficiency across Western US states.

**Key Features:**
- REST API integration with U.S. Energy Information Administration (EIA.gov)
- Multi-state data processing (UT, MT, ID, WY, CO, CA, AZ, NV, OR, WA)
- Analysis of multiple fuel types (coal, petroleum, natural gas, hydroelectric, wind, solar)
- Efficiency calculations (BTU input vs electricity output)
- Automated data updates with date validation
- Null value handling and data cleaning
- JSON export of processed results
- historical data analysis over multiple years

**Technologies Used:**
- Python
- REST APIs & JSON processing
- Data analysis and mathematical calculations
- File I/O operations

**Note:** You'll need to obtain your own API key from EIA.gov to run this project.

**How to Run:**
1. Get API key from https://www.eia.gov/opendata/
2. Replace `[InsertYourOwnAPIKeyHere]` with your key
3. Install required libraries: `pip install requests`
4. Run: `python energy_analysis.py`

---

## Development Environment

All projects were developed using:
- **Platform:** AWS EC2 instances & Cloud9
- **Editor:** VS Code with remote development
- **Python Version:** 3.x
- **Testing:** Manual testing and validation

## Learning Outcomes

These projects demonstrate proficiency in:
- Object-oriented programming principles
- API integration and JSON data handling
- Data analysis and statistical calculations
- Graph theory and network algorithms
- Error handling and edge case management
- Code organization and documentation
- Energy sector data analysis
- Financial market analysis

---

*Part of MIS Master's Program at Utah State University*
