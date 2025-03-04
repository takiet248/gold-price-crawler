# Gold Price Web Scraper

### 📌 Project Overview
This project is a **Gold Price Web Scraper** designed to extract real-time gold price data from multiple websites, including **Doji** and **PNJ**. The scraper collects essential details such as:
- **Gold Type**
- **Buy Price**
- **Sell Price**

The collected data is then processed and standardized to ensure consistency across sources. Finally, the structured data is stored in a **CSV file** for further analysis and insights.

### 🚀 Features
- ✅ Scrapes live gold prices from multiple sources  
- ✅ Extracts key details: gold type, buy price, and sell price  
- ✅ Processes and unifies data into a standardized format  
- ✅ Saves structured data in a CSV file for easy analysis  
- ✅ Simple, efficient, and easy to use  

### 🛠️ Tech Stack
- **Python** – Main programming language
- **BeautifulSoup** – HTML parsing and web scraping
- **Requests** – Fetching website content
- **Pandas** – Data processing and formatting

### 🔧 Setup & Usage
#### 1️⃣ Install Dependencies
Ensure you have Python installed, then install the required libraries:
```bash
pip install beautifulsoup4 requests pandas
```

#### 2️⃣ Run the Scraper
Execute the script to fetch and save the gold prices:
```bash
python gold_price_scraper.py
```

#### 3️⃣ Output
The extracted data will be saved as `gold_prices.csv`, which can be used for further analysis.


