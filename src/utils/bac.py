import json
import pandas as pd
from bs4 import BeautifulSoup

class BacProcessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self.load_data()
    
    def load_data(self):
        """Load JSON data."""
        with open(self.filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

    def extract_transaction_details(self):
        """ """
        records = []
        for email in self.data:
            soup = BeautifulSoup(email['content'], 'html.parser')
            
            commerce = soup.find(text="Comercio:").find_next().text.strip()
            fecha = soup.find(text="Fecha:").find_next().text.strip()
            amount = soup.find(text="Monto:").find_next().text.strip()
            currency = 'CRC'
            state = 'Aprobada'
            
            records.append({
                'Fecha': fecha,
                'Monto': amount,
                'Comercio': commerce,
                'Moneda': currency,
                'Banco': 'BAC Credomatic',
                'Estado': state
            })
        return records

    def create_dataframe(self, records):
        """Convert  to DataFrame."""
        return pd.DataFrame(records)

    def process_emails(self):
        """Process emails and return a DataFrame."""
        records = self.extract_transaction_details()
        return self.create_dataframe(records)

if __name__ == "__main__":
    processor = BacProcessor('/path/files/bac_credomatic_emails.json')
    df = processor.process_emails()
    print(df)
