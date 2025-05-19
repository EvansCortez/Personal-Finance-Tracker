# Personal Finance Tracker

A Python-based personal finance tracker with CLI, GUI (Tkinter), and web (Flask) interfaces.  
Features include transaction recording, spending analysis, visual reporting, and savings suggestions.

## Structure

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

