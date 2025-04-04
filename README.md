# Price-Tracker
email is sent to user when price of garment has changed in clothing website
## About
Price Tracker is a smart price monitoring tool built to help users catch the best deals on clothing. It automates the entire process — from scraping the product page to notifying you the moment a price changes.
## Key Features🔧
- **Real-Time Price Monitoring**: Tracks price fluctuations on AJIO product pages.
- **Email Alerts**: Automatically notifies you via email when a tracked item's price changes.
- **Scheduled Tracking**: Runs seamlessly every 10 minutes, so you never miss a price drop.
- **Anti-Bot Evasion**: Smartly mimics human-like scrolling and interaction to bypass bot detection systems used by major e-commerce platforms.
- **Historical Data Logging**: Logs every price change along with brand names, original prices, current prices and discount percentages into a structured CSV file for future reference or analysis.
## Technologies
- Python : Primary programming language
- Pandas : For data manipulation and analysis
- SMTPLIB : For sending emails
- Selenium : Scraping data off of e-commerce websites
- CSV : Database system
## Installation
### Prerequisites
- Python 3.12 or later
- Chrome Driver (same version as chrome)
- Python libraries required:
  - selenium
  - beautiful soup
  - time
  - pandas
  - os
  - smptplib
  - email.mime
  - schedule
### Steps
#### **1. Clone the repository**
```
git clone https://github.com/UvanAdhithya/Price-Tracker.git
cd Price-Tracker
```
#### 2. Set Up a Virtual Environment (Recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
#### 3. Install dependencies
```
pip install -r requirements.txt
```
#### 4.Run the tracker
```
python run_tracker.py
```
## Configuration
### Google Email Acces
1. Visit [Google App Passwords](https://myaccount.google.com/apppasswords)
2. Create a new project and copy the password
3. Paste the password in main.py send_email() module
4. Type sender and reciever email in send_email() module
### Chrome Driver Installation
1. Visit [Google Chrome Labs](https://googlechromelabs.github.io/chrome-for-testing/)
2. Download corresponding chrome driver version
3. Create new folder "webdrivers" in C:
4. Move chromedriver.exe to said folder
### Target website to scrape
Paste url of website in main()
## License
This project is licensed under the GPL-3.0 License. See the LICENSE file for details.

