import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt


def extract_gold_prices_doji(url):
  """
  Extracts gold prices data from Doji website and returns a pandas DataFrame.

  Args:
      url: The URL of the Doji gold price webpage.

  Returns:
      A pandas DataFrame containing gold prices data, or None if data cannot be extracted.
  """

  response_doji = requests.get(url)
  response_doji.raise_for_status()  # Raise an exception for non-200 status codes

  soup_doji = BeautifulSoup(response_doji.text, features="html.parser")

  # Find the relevant table (may need adjustment based on website structure)
  table_doji = soup_doji.find_all("table")  # Use class name for better targeting

  # Extract headers (skip empty headers)
  header_doji = [th.text.strip() for th in table_doji[0].find_all('th') if th.text.strip()]

  # Extract rows, excluding the first column, and combine with headers
  data_doji = [[cell.text.strip() for cell in row.find_all('td')[1:]]  # Skip first column
        for row in table_doji[0].find_all('tr')[1:]]  # Skip header row
  # Create DataFrame, remove first column (index 0), and print
  df_doji = pd.DataFrame(data_doji, columns=header_doji)
  return df_doji


def transform_gold_prices_doji(df_doji):
  """
  Transforms extracted gold prices data into a clean pandas DataFrame.

  Args:
      data: A list of rows containing gold price data, or None if data cannot be extracted.
      header: A list of column names for the data.

  Returns:
      A pandas DataFrame containing transformed gold prices data, or None if data is not provided.
  """

  # Rename header
  df_doji = df_doji.rename(columns={'Loại vàng': 'Type of gold', 'Giá mua (VNĐ)': 'Buy', 'Giá bán (VNĐ)': 'Sell'})

  # Clean Type of gold column
  df_doji['Type of gold'] = df_doji['Type of gold'].str.replace('- Bán Lẻ', '') 
  df_doji['Type of gold'] = df_doji['Type of gold'].str.strip()

  # Clean Buy column
  df_doji['Buy'] = df_doji['Buy'].str.replace(',', '')
  df_doji['Buy'] = df_doji['Buy'].astype('int')

  # Clean Sell column
  df_doji['Sell'] = df_doji['Sell'].str.replace(',', '')
  df_doji['Sell'] = df_doji['Sell'].astype('int')

  # Add flag Doji
  df_doji['Source'] = 'Doji'

  # Add time collected
  df_doji['Datetime'] = dt.datetime.today()
  df_doji['Datetime'] = df_doji['Datetime'].dt.strftime('%d-%m-%Y %H:%M')
  df_doji['Datetime'] = pd.to_datetime(df_doji['Datetime'], infer_datetime_format=True)

  return df_doji


def load_gold_prices_doji(df_doji):
  """
  Placeholder function for loading the transformed DataFrame.

  Args:
      df_doji: A pandas DataFrame containing transformed gold prices data, or None if data cannot be extracted.

  Prints the DataFrame for demonstration purposes. In a real ETL pipeline,
  this function would likely save the data to a database or other storage.
  """

  #print(df_pnj)
	try:
	    existing_df = pd.read_csv("gold_prices.csv")
	    df_doji= pd.concat([existing_df, df_doji], ignore_index=True)
	except FileNotFoundError:
	    pass  # If file doesn't exist, just create a new one
	# Save back to CSV
	df_doji.to_csv("gold_prices.csv", index=False)


url_doji = "https://baomoi.com/tien-ich/gia-vang-doji.epi"
extracted_data = extract_gold_prices_doji(url_doji)
transformed_data = transform_gold_prices_doji(extracted_data)
print(transformed_data)