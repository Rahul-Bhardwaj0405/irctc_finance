# # tasks.py
# from celery import shared_task
# import pandas as pd
# import json
# import logging
# from io import StringIO, BytesIO
# from .models import BankData
# from datetime import datetime

# @shared_task
# def process_uploaded_files(file_content, file_name, bank_name, year, month, booking_or_refund):
#     try:
#         # Initialize an empty DataFrame
#         df = pd.DataFrame()

#         # Read the file content into a DataFrame based on file type
#         if file_name.endswith('.csv'):
#             df = pd.read_csv(StringIO(file_content.decode('utf-8')))
#         elif file_name.endswith('.xlsx'):
#             df = pd.read_excel(BytesIO(file_content))
#         elif file_name.endswith('.txt'):
#             df = pd.read_csv(StringIO(file_content.decode('utf-8')), delimiter='\t')
#         elif file_name.endswith('.json'):
#             data = json.loads(file_content)
#             df = pd.json_normalize(data)
#         else:
#             try:
#                 file_str = file_content.decode('utf-8')
#                 delimiter = ',' if ',' in file_str else '\t'
#                 df = pd.read_csv(StringIO(file_str), delimiter=delimiter)
#             except Exception as e:
#                 logging.error(f"Error converting file {file_name} to CSV: {e}")
#                 return
        
#         # Map columns based on the bank_name
#         if bank_name == 'hdfc':
#             required_columns = ['industry_code_ANZSIC', 'industry_name_ANZSIC', 'rme_size_grp']
#         elif bank_name == 'icici':
#             required_columns = ['variable', 'value']
#         # Add conditions for other banks

#         if all(col in df.columns for col in required_columns):
#             date_str = file_name.split('.')[0]
#             date = datetime.strptime(date_str, '%d-%m-%y')

#             for _, row in df.iterrows():
#                 extracted_data = {col: row[col] for col in required_columns}
#                 BankData.objects.create(
#                     bank_name=bank_name,
#                     year=year,
#                     month=month,
#                     booking_or_refund=booking_or_refund,
#                     date=date,
#                     extracted_data=extracted_data
#                 )
#         else:
#             logging.error(f"Required columns are missing in file: {file_name}")

#     except Exception as e:
#         logging.error(f"Error processing file {file_name}: {e}")


# tasks.py
from celery import shared_task
import pandas as pd
import json
import logging
from io import StringIO, BytesIO
from .models import BankData
from datetime import datetime

@shared_task
def process_uploaded_files(file_content, file_name, bank_name, year, month, booking_or_refund):
    try:
        # Initialize an empty DataFrame
        df = pd.DataFrame()

        # Read the file content into a DataFrame based on file type
        if file_name.endswith('.csv'):
            df = pd.read_csv(StringIO(file_content.decode('utf-8')))
        elif file_name.endswith('.xlsx'):
            df = pd.read_excel(BytesIO(file_content))
        elif file_name.endswith('.txt'):
            df = pd.read_csv(StringIO(file_content.decode('utf-8')), delimiter='\t')
        elif file_name.endswith('.json'):
            data = json.loads(file_content)
            df = pd.json_normalize(data)
        else:
            try:
                file_str = file_content.decode('utf-8')
                delimiter = ',' if ',' in file_str else '\t'
                df = pd.read_csv(StringIO(file_str), delimiter=delimiter)
            except Exception as e:
                logging.error(f"Error converting file {file_name} to CSV: {e}")
                return
        
        # Map columns based on the bank_name
        if bank_name == 'hdfc':
            # Assuming 'A' maps to 'industry_code_ANZSIC' and 'a_0' maps to 'rme_size_grp'
            column_mapping = {
                'A': 'industry_code_ANZSIC',
                'industry_name_ANZSIC': 'industry_name_ANZSIC',
                'a_0': 'rme_size_grp'  # Adjust this mapping if different column names are used
            }
        elif bank_name == 'icici':
            column_mapping = {
                'variable': 'variable',
                'value': 'value'
            }
        # Add conditions for other banks as needed

        # Rename the DataFrame columns to match the required column names
        df.rename(columns=column_mapping, inplace=True)

        # Extract required columns after renaming
        required_columns = list(column_mapping.values())

        # Check if the required columns are present after renaming
        if all(col in df.columns for col in required_columns):
            date_str = file_name.split('.')[0]
            try:
                date = datetime.strptime(date_str, '%d-%m-%y')  # Adjust the format if needed
            except ValueError as e:
                logging.error(f"Date parsing error for file {file_name}: {e}")
                return

            for _, row in df.iterrows():
                extracted_data = {col: row[col] for col in required_columns}
                BankData.objects.create(
                    bank_name=bank_name,
                    year=year,
                    month=month,
                    booking_or_refund=booking_or_refund,
                    date=date,
                    extracted_data=extracted_data
                )
        else:
            logging.error(f"Required columns are missing in file: {file_name}")

    except Exception as e:
        logging.error(f"Error processing file {file_name}: {e}")
