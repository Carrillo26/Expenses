import json
import pandas as pd
from bs4 import BeautifulSoup

class BcrProcessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self.load_data()

    def load_data(self):
        """Load JSON data."""
        with open(self.filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

    def extract_transactions(self):
        """Extract transaction details from emails."""
        records = []
        for i, email in enumerate(self.data):
            soup = BeautifulSoup(email['content'], 'html.parser')
            tables = soup.find_all('table')
            if tables:
                for table in tables:
                    rows = table.find_all('tr')
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) == 7:
                            record = {
                                'Fecha': cols[0].text.strip(),
                                'Monto': cols[3].text.strip(),
                                'Comercio': cols[5].text.strip(),
                                'Moneda': 'CRC',
                                'Banco': 'BCR', 
                                'Estado': cols[6].text.strip()
                            }
                            records.append(record)
                        elif len(cols) > 0:
                            print(f"Email #{i + 1}: Number of columns: {len(cols)}")
                            print(f"Email #{i + 1}: Row content: {[col.text.strip() for col in cols]}")
            else:
                print(f"Email #{i + 1}: No tables found")
        return records

    def create_dataframe(self, records):
        """Convert records to DataFrame."""
        df = pd.DataFrame(records)
        if df.empty:
            print("DataFrame is empty")
        return df

    def process_emails(self):
        """Process emails and return a DataFrame."""
        records = self.extract_transactions()
        return self.create_dataframe(records)

if __name__ == "__main__":
    processor = BcrProcessor("/path/files/bcr_emails.json")
    df = processor.process_emails()
    print(df)
