"""THIS CODE IS TO TEST THE TIME RESPONSE AND OLLAMA RESPONSES,
IT DOENST TRANSFER THE INFORMATION GENERATED BY THE AI TO ANOTHER DOCUMENT, IT JUST
PRINTS IT ON THE TERMINAL"""

import pandas as pd
import ollama
from tqdm import tqdm

# Configuration
EXCEL_FILE = "test_table.xlsx"
MODEL = "llama3:instruct"

# Load data
try:
    df = pd.read_excel(EXCEL_FILE)
    required_cols = ['Investor', 'Recipient', 'Recipient Country', 'Year', 'Sector', 'Amount (US$ mn)']
    if not all(col in df.columns for col in required_cols):
        missing = [col for col in required_cols if col not in df.columns]
        raise ValueError(f"Missing columns: {missing}")
except Exception as e:
    print(f"Error reading file: {e}")
    exit()


# Generate prompt
def generate_investment_description(row):
    prompt = f"""Provide a brief description (max 5 lines) about the investment of {row['Investor']} in {row['Recipient']}, 
    {row['Recipient Country']} in {row['Year']} in the {row['Sector']} sector valued at {row['Amount (US$ mn)']} million USD. 
    Focus on key facts and significance. Use only factual information without additional commentary."""

    try:
        response = ollama.generate(
            model=MODEL,
            prompt=prompt,
        )
        return response['response'].split('\n')[0].strip()
    except Exception as e:
        print(f"Error in row {row.name}: {e}")
        return None


# Main processing
print("Starting description generation...")
for idx, row in tqdm(df.iterrows(), total=min(10, len(df))):  # Process maximum 10 rows for testing
    description = generate_investment_description(row)
    if description:
        print(f"\nRow {idx + 1}:")
        print(description)

print("\nProcess completed!")