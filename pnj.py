import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt


def extract_gold_prices_pnj(url):
  """
  Extracts gold prices data from PNJ website and returns a pandas DataFrame.

  Args:
      url: The URL of the PNJ gold price webpage.

  Returns:
      A pandas DataFrame containing gold prices data.
  """

  # Fetch HTML and create BeautifulSoup object
  response_pnj = requests.get(url)
  soup_pnj = BeautifulSoup(response_pnj.content, features="html.parser")

  # Find the first table and its header
  table_pnj = soup_pnj.find('table')
  header_pnj = [th.text.strip() for th in table_pnj.find_all('th')]

  # Extract rows and combine data with headers
  data_pnj = [[cell.text.strip() for cell in row.find_all('td')] for row in table_pnj.find_all('tr')[1:]]  # Skip header row

  # Create DataFrame
  df_pnj = pd.DataFrame(data_pnj, columns=header_pnj)

  return df_pnj

def transform_gold_prices_pnj(df_pnj):
  """
  Transforms extracted gold prices data into a clean pandas DataFrame.

  Args:
      data: A list of rows containing gold price data.
      header: A list of column names for the data.

  Returns:
      A pandas DataFrame containing transformed gold prices data.
  """
  # Rename header
  df_pnj = df_pnj.rename(columns={'Loại vàng | ĐVT: 1.000đ/Chỉ': 'Type of gold', 'Giá mua': 'Buy', 'Giá bán': 'Sell'})

  # Clean Buy column
  df_pnj['Buy'] = df_pnj['Buy'].str.replace(',', '')
  df_pnj['Buy'] = df_pnj['Buy'].astype('int')
  df_pnj['Buy'] = df_pnj['Buy'] * 1000

  # Clean Sell column
  df_pnj['Sell'] = df_pnj['Sell'].str.replace(',', '')
  df_pnj['Sell'] = df_pnj['Sell'].astype('int')
  df_pnj['Sell'] = df_pnj['Sell'] * 1000

  # Add flag PNJ
  df_pnj['Source'] = 'PNJ'

  # Add time collected
  df_pnj['Datetime'] = dt.datetime.today()
  df_pnj['Datetime'] = df_pnj['Datetime'].dt.strftime('%d-%m-%Y %H:%M')
  df_pnj['Datetime'] = pd.to_datetime(df_pnj['Datetime'], infer_datetime_format=True)

  return df_pnj

def load_gold_prices_pnj(df_pnj):
  """
  Placeholder function for loading the transformed DataFrame.

  Args:
      df_pnj: A pandas DataFrame containing transformed gold prices data.

  Prints the DataFrame for demonstration purposes. In a real ETL pipeline,
  this function would likely save the data to a database or other storage.
  """

  #print(df_pnj)
	try:
	    existing_df = pd.read_csv("gold_prices.csv")
	    df_pnj = pd.concat([existing_df, df_pnj], ignore_index=True)
	except FileNotFoundError:
	    pass  # If file doesn't exist, just create a new one
	# Save back to CSV
	df_pnj.to_csv("gold_prices.csv", index=False)



url_pnj = "https://www.pnj.com.vn/blog/gia-vang/?srsltid=AfmBOopmW4cFTI_KJb6uOfLu7o7rWghPljWBgUOJe5zQWz8BvRMc2Bqo&r=1726827414875"
extracted_data = extract_gold_prices_pnj(url_pnj)
tranformed_data = transform_gold_prices_pnj(extracted_data)

print(tranformed_data)