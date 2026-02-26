import pandas as pd
import os

# Folder paths
raw_folder = "raw_excel"
combined_folder = "combined_excel"

# Make sure combined folder exists
os.makedirs(combined_folder, exist_ok=True)

all_dataframes = []

# Loop through all Excel files in raw_excel folder
for file in os.listdir(raw_folder):
    if file.endswith(".xlsx"):
        file_path = os.path.join(raw_folder, file)
        df = pd.read_excel(file_path)
        all_dataframes.append(df)

# Combine all players into one DataFrame
combined_df = pd.concat(all_dataframes, ignore_index=True)

# Save combined file
output_path = os.path.join(combined_folder, "t20_all_players.xlsx")
combined_df.to_excel(output_path, index=False)

print("Combined file created successfully.")
print("Total Rows:", len(combined_df))