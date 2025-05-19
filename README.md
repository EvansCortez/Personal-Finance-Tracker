# Personal Finance Tracker

![Finance Dashboard Screenshot](./screenshots/dashboard.png)

A multi-interface Python application for managing personal finances with CLI, GUI (Tkinter), and web (Flask) interfaces. Features transaction recording, spending analysis, visual reporting, and personalized savings suggestions.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.com/EvansCortez/Personal-Finance-Tracker.svg?branch=main)](https://travis-ci.com/EvansCortez/Personal-Finance-Tracker)
[![Coverage Status](https://coveralls.io/repos/github/EvansCortez/Personal-Finance-Tracker/badge.svg?branch=main)](https://coveralls.io/github/EvansCortez/Personal-Finance-Tracker?branch=main)

## Features

- **Multi-Interface Access**
  - Command Line Interface (CLI)
  - Graphical User Interface (Tkinter)
  - Web Application (Flask)

- **Core Functionality**
  - Transaction recording with categories
  - SQLite database storage
  - Initial balance configuration
  - Net savings calculation

- **Financial Insights**
  - Spending by category visualization
  - Monthly spending trends
  - Personalized savings suggestions
  - Budget vs. actual comparisons

- **Advanced Features**
  - Data export (CSV, Excel)
  - Recurring transaction detection
  - Multi-user support (web version)
  - REST API for mobile integration

## Project Structure

```
finance-tracker/
├── app/
│   ├── __init__.py
│   ├── core.py         # Business logic and data access
│   ├── gui.py          # Tkinter interface
│   ├── web.py          # Flask application
│   ├── config.py       # Configuration settings
│   └── templates/      # Flask templates
├── data/               # Database files
├── tests/              # Unit tests
├── requirements.txt    # Dependencies
└── README.md           # Documentation
```

## Quick Start

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the CLI:
   ```
   python app/core.py
   ```

3. Run the GUI:
   ```
   python app/gui.py
   ```

4. Run the web app:
   ```
   python app/web.py
   ```

## Features

- SQLite-based transaction storage
- Spending analysis and visualizations (Matplotlib)
- Budgeting and savings suggestions
- Tkinter GUI and Flask web interface

## License

MIT License

