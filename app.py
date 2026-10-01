import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="IT Ticket Analyzer", layout="wide")

st.title("IT Support Ticket Analyzer")
st.caption("Support workload dashboard using fictional sample tickets.")

# Locate the CSV and database files.
project_folder = Path(__file__).parent
data_path = project_folder / "tickets.csv"
database_path = project_folder / "tickets.db"

# Open the database.
connection = sqlite3.connect(database_path)

try:
    # Check whether the tickets table already exists.
    table = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='tickets'"
    ).fetchone()

    # Import the sample CSV only on the first run.
    if table is None:
        sample_tickets = pd.read_csv(data_path)
        sample_tickets.to_sql("tickets", connection, index=False)

    # Read the stored tickets using SQL.
    tickets = pd.read_sql_query(
        "SELECT * FROM tickets ORDER BY ticket_id",
        connection
    )
finally:
    connection.close()

# Create sidebar filters.
st.sidebar.header("Filter Tickets")

category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(tickets["category"].unique().tolist())
)

status = st.sidebar.selectbox(
    "Status",
    ["All", "Open", "Resolved"]
)

filtered = tickets.copy()

if category != "All":
    filtered = filtered[filtered["category"] == category]

if status != "All":
    filtered = filtered[filtered["status"] == status]

# Calculate summary numbers.
open_count = (filtered["status"] == "Open").sum()
resolved = filtered[filtered["status"] == "Resolved"]
average_hours = resolved["resolution_hours"].mean()

column1, column2, column3 = st.columns(3)

column1.metric("Total Tickets", len(filtered))
column2.metric("Open Tickets", int(open_count))

if resolved.empty:
    column3.metric("Average Resolution Time", "N/A")
else:
    column3.metric(
        "Average Resolution Time",
        str(round(average_hours, 1)) + " hours"
    )

st.caption("Average resolution time includes resolved tickets only.")

# Display a chart and the ticket table.
if filtered.empty:
    st.info("No tickets match these filters.")
else:
    st.subheader("Tickets by Category")
    category_counts = filtered.groupby("category").size()
    st.bar_chart(category_counts)

    st.subheader("Ticket Details")
    st.dataframe(filtered, hide_index=True, width="stretch")

    st.subheader("Security Review")
st.caption(
    "Rules flag tickets for human review. A flag does not confirm a threat. "
    "This section follows the sidebar filters."
)


def security_reason(ticket):
    """Return the reason a ticket needs security review."""
    description = str(ticket["description"]).lower()

    keywords = [
        "phishing",
        "malware",
        "ransomware",
        "unexpected mfa",
        "suspicious login"
    ]

    matches = []

    for keyword in keywords:
        if keyword in description:
            matches.append(keyword)

    if matches:
        return "Matched keywords: " + ", ".join(matches)

    if ticket["category"] == "Security":
        return "Ticket categorized as Security"

    return ""


review = filtered.copy()
review["review_reason"] = review.apply(security_reason, axis=1)
flagged = review[review["review_reason"] != ""]

if flagged.empty:
    st.info("No tickets flagged by these rules in the current selection.")
else:
    st.write("Tickets requiring security review:", len(flagged))
    st.dataframe(flagged, hide_index=True, width="stretch")

st.subheader("Export Results")

st.download_button(
    label="Download Filtered Tickets",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_tickets.csv",
    mime="text/csv"
)

st.download_button(
    label="Download Security Review",
    data=flagged.to_csv(index=False).encode("utf-8"),
    file_name="security_review.csv",
    mime="text/csv"
)