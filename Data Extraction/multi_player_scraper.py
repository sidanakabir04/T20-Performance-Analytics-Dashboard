import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Make sure raw_excel folder exists
os.makedirs("raw_excel", exist_ok=True)

players = {
    "Virat Kohli": "https://stats.espncricinfo.com/ci/engine/player/253802.html?class=3;template=results;type=batting;view=innings",
    "Rohit Sharma": "https://stats.espncricinfo.com/ci/engine/player/34102.html?class=3;template=results;type=batting;view=innings",
    "Suryakumar Yadav": "https://stats.espncricinfo.com/ci/engine/player/423889.html?class=3;template=results;type=batting;view=innings",
    "Hardik Pandya": "https://stats.espncricinfo.com/ci/engine/player/625371.html?class=3;template=results;type=batting;view=innings"
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_player(player_name, url):
    print(f"\nScraping {player_name}...")

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table", class_="engineTable")

    innings_table = None

    for table in tables:
        first_row = table.find("tr")
        if first_row:
            header_cells = [th.text.strip() for th in first_row.find_all(["th", "td"])]
            if "Runs" in header_cells and "Opposition" in header_cells:
                innings_table = table
                break

    if innings_table is None:
        print(f"Could not find innings table for {player_name}")
        return

    rows = innings_table.find_all("tr")

    data = []

    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) < 13:
            continue

        runs_raw = cols[0].text.strip()

        if runs_raw in ["DNB", "TDNB", "-"]:
            continue

        not_out = 1 if "*" in runs_raw else 0
        runs = runs_raw.replace("*", "")

        data.append([
            player_name,
            runs,
            cols[2].text.strip(),
            cols[3].text.strip(),
            cols[4].text.strip(),
            cols[5].text.strip(),
            cols[10].text.strip(),
            cols[11].text.strip(),
            cols[12].text.strip(),
            not_out
        ])

    df = pd.DataFrame(data, columns=[
        "Player", "Runs", "BF", "4s", "6s",
        "SR", "Opposition", "Ground", "Date", "Not_Out"
    ])

    df["Runs"] = pd.to_numeric(df["Runs"], errors="coerce")
    df["BF"] = pd.to_numeric(df["BF"], errors="coerce")
    df["4s"] = pd.to_numeric(df["4s"], errors="coerce")
    df["6s"] = pd.to_numeric(df["6s"], errors="coerce")

    df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y", errors="coerce")
    df["Year"] = df["Date"].dt.year

    file_name = player_name.lower().replace(" ", "_") + "_t20.xlsx"
    file_path = os.path.join("raw_excel", file_name)

    df.to_excel(file_path, index=False)

    print(f"{player_name} saved successfully. Total innings: {len(df)}")

# Run for all players
for name, link in players.items():
    scrape_player(name, link)

print("\nAll players scraped successfully.")