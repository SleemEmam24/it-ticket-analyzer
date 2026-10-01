# IT Support Ticket Analyzer

A Python dashboard for exploring IT support workload and flagging tickets for security review. Built with Streamlit, pandas, and SQLite.

## Features

- Filter tickets by category and status.
- View total tickets, open tickets, and average resolution time.
- Compare ticket counts by category.
- Flag security-related tickets with an explanation.
- Download filtered tickets and security review results as CSV files.

## How it works

On the first run, the app imports tickets.csv into a local SQLite database. Later runs read the stored tickets using SQL.

Average resolution time includes resolved tickets only.

Security review uses keyword and category rules. Flags require human review and do not confirm a threat.

## Run locally

Use Python 3.9 or later.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local address displayed in the terminal.

## Sample data

The project includes 12 fictional tickets for demonstration. It contains no real employee or customer information.

Changes to tickets.csv do not automatically update an existing database. To reload the sample data, stop the app, delete the generated tickets.db file, and restart the app.

## What I practiced

- Using pandas to filter and summarize data
- Storing data in SQLite and reading it with SQL
- Building an interactive Streamlit dashboard
- Writing explainable security review rules
- Exporting analysis results to CSV

## Limitations

This is a learning project with a small fictional dataset. It does not use machine learning or connect to a live ticketing system.