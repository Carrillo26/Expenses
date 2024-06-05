import sys
from utils.downloader import EmailsExtractor
from utils.bac import BacProcessor
from utils.bcr import BcrProcessor
from utils.bncr import BncrProcessor
from utils.unifier import unify_dataframes, save_to_excel

def main():
    
    extractor = EmailsExtractor()
    extractor.run()
    
    
    bac_processor = BacProcessor('/path/files/bac_credomatic_emails.json')
    bcr_processor = BcrProcessor('/path/files/bcr_emails.json')
    bncr_processor = BncrProcessor('/path/files/banco_nacional_emails.json')

    bac_df = bac_processor.process_emails()
    bcr_df = bcr_processor.process_emails()
    bncr_df = bncr_processor.process_emails()

    
    unified_df = unify_dataframes(bac_df, bcr_df, bncr_df)
    print(unified_df)

    
    save_to_excel(unified_df, '/path/datasets/gastos.xlsx')

if __name__ == "__main__":
    main()
