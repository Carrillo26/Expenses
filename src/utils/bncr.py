import json
import pandas as pd

class BncrProcessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self.load_data()

    def load_data(self):
        """L0ad JSON data."""
        with open(self.filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

    def extract_transactions(self):
        """Extract transaction details from emails."""
        records = []
        for email in self.data:
            content = email['content']

            commerce_start = content.find("realizada en") + len("realizada en")
            commerce_end = content.find("CRI", commerce_start)
            commerce = content[commerce_start:commerce_end].strip().strip('*')
            
            fecha_start = content.find("el", commerce_end) + len("el")
            fecha_end = content.find("a las", fecha_start)
            fecha = content[fecha_start:fecha_end].strip().strip('*')

            time_start = content.find("a las", fecha_end) + len("a las")
            time_end = content.find("\r\n", time_start)
            time = content[time_start:time_end].strip().strip('*')
            fecha = f"{fecha} {time}"
            
            card_start = content.find("MASTERCARD") + len("MASTERCARD")
            card_end = content.find("NRO. AUT:", card_start)
            card_number = content[card_start:card_end].strip()
            
            amount_start = content.find("TOTAL:", card_end) + len("TOTAL:")
            amount_end = content.find('\r\n', amount_start)
            amount = content[amount_start:amount_end].strip()
            
            state = "Rechazada" if "rechazada" in content.lower() else "Aprobada"
            currency = "CRC"
            
            records.append({
                'Fecha': fecha,
                'Monto': amount,
                'Comercio': commerce,
                'Moneda': currency,
                'Banco': 'Banco Nacional',
                'Estado': state,
                'Numero de Tarjeta': card_number
            })
        return records

    def create_dataframe(self, records):
        """Convert records to DataFrame and filter data."""
        df = pd.DataFrame(records)
        filtered_df = df[df['Numero de Tarjeta'] == '111111111111111111111'].drop(columns=['Numero de Tarjeta'])
        if filtered_df.empty:
            print("DataFrame is empty")
        return filtered_df

    def process_emails(self):
        """  """
        records = self.extract_transactions()
        return self.create_dataframe(records)

if __name__ == "__main__":
    processor = BncrProcessor('/path/files/banco_nacional_emails.json')
    df = processor.process_emails()
    print(df)
