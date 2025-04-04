from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# CONFIGURATION
filename = "ajio_price.csv"
target_items = 20
scroll_step = 1000
scroll_delay = 0.5
brand_marker = "div.brand[aria-label]"
price_marker = "span.price"
off = "span.discount"
brand,price,discount = [], [], []


def initialize_driver(path, website):
    driver = webdriver.Chrome(service=path)
    driver.get(website)

    #input("Press Enter to close browser...") # This stopped browser from crasshing when no code was written

    print(driver.title)
    return driver

def scroll_to_load_items(driver, target_items, scroll_step, scroll_delay, brand_marker):
    # Initial scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    print(last_height)
    while(True):
        # Scrolls by scroll_step pixels to trick Ajio into thinking we human
        for i in range(0,last_height, scroll_step):
            driver.execute_script(f"window.scrollBy(0, {scroll_step})")
            time.sleep(scroll_delay)

        product_names = driver.find_elements(By.CSS_SELECTOR, brand_marker)
        if len(product_names) >= target_items:
            break
    print(f"{len(product_names)} items loaded.")

def get_product_details(driver, target_items, brand_marker, price_marker, off):
    
    product_names = driver.find_elements(By.CSS_SELECTOR, brand_marker)
    prices = driver.find_elements(By.CSS_SELECTOR, price_marker)
    offers = driver.find_elements(By.CSS_SELECTOR, off )

    for i in range(target_items):
        brand.append(product_names[i].text if i < len(product_names) else "N/A") # Offers safety net from "out of index range" error, in case not enough items loaded
        price.append(prices[i].text if i < len(prices) else "N/A")
        discount.append(offers[i].text if i < len(offers) else "N/A")

    return brand,price,discount

def load_existing_data(filename):
    # Check if the file exists
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
         return pd.DataFrame() # Return empty dataframe as placeholder to concatenate data later

def add_new_data(existing_df, new_df):
    existing_cols = len(existing_df.columns)

    # Create new dynamic column names for new data
    new_col_names = [f"Brand_{(existing_cols // 3) + 1}", f"Price_{(existing_cols // 3) + 1}", f"Discount_{(existing_cols // 3) + 1}"]

    # Concatenate with new data
    final_df = pd.concat([existing_df, new_df], axis=1)

    # Rename columns dynamically
    all_col_names = list(existing_df.columns) + new_col_names
    final_df.columns = all_col_names

    # Reset index after adding columns
    final_df.reset_index(drop=True, inplace=True)
    print("Data updated successfully. File created.")

    #print(final_df.columns)  # Check if 'Price' is listed correctly
    return final_df

def get_html(driver):
    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Save page source to inspect manually
    with open("ajio_page.html", "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    print("Page source saved as 'ajio_page.html'. Open it in your browser to inspect markers.")

def compare_prices(existing_df, new_df):
        # Get the last added Price column dynamically
        price_cols = [col for col in existing_df.columns if col.startswith('Price_')]

        # Check if any Price columns exist
        if price_cols:
            old_price_col = price_cols[-1]  # Get the last added Price column
        else:
            old_price_col = None  # No previous Price column found
        
        
        # Check the minimum length to avoid mismatch
        min_length = min(len(existing_df), len(new_df))

        if old_price_col:
            old_prices = existing_df[old_price_col].iloc[:min_length]
            new_prices = new_df["Price"].iloc[:min_length]
        else:
            # No price comparison if it's the first run
            old_prices = ["N/A"] * min_length
            new_prices = new_df["Price"].iloc[:min_length]
            price_changes = ["New Item"] * min_length

        price_changes = []

        # Zip loops through len of smallest  list
        for old, new in zip(old_prices, new_prices):
        
            # Remove ₹ and commas from prices and convert them to float
            old_price = float(old.replace('₹', '').replace(',', ''))

            new_price = float(new.replace('₹', '').replace(',', '').strip())

            # Compare prices
            if new_price > old_price:
                price_changes.append("Increased")
            elif new_price < old_price:
                price_changes.append("Decreased")
            else:
                price_changes.append("No Change")
            
           

        return price_changes

def append_Cost_Column(final_df, existing_df, new_df):
    columns = final_df.columns.tolist()
    if "Cost_Change_" in columns:
        columns.remove("Cost_Change_")
    final_df = final_df[columns]

    #columns.append("Price_Change_")
    price_changes = compare_prices(existing_df,new_df)

    # Pad the remaining rows with "No Data" if lengths don't match
    price_changes += ["No Data"] * (len(final_df) - len(price_changes))

    # Add the results to the last column of final_df
    final_df[f"Cost_Change_"] = price_changes
    #final_df = final_df[columns]
    return final_df

def save_file(final_df, filename):
    final_df.to_csv(filename, mode="w", index=False,header = True, encoding="utf-8-sig")

def send_email(subject, body):
    sender_email = "uvanadhithya@gmail.com"
    receiver_email = "uvanadhithya@gmail.com"
    password = "oorc vfmk nici eqnb"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # Connect to Gmail's SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

def main():
    # Clears lists after each main() call to prevent duplicate entries
    brand.clear()
    price.clear()
    discount.clear()

    website = "https://www.ajio.com/men-jeans/c/830216001"
    path = Service('C:\webdrivers\chromedriver.exe')
    driver = initialize_driver(path, website)

    scroll_to_load_items(driver,target_items,scroll_step,scroll_delay,brand_marker)
    get_product_details(driver,target_items,brand_marker,price_marker,off)

    existing_df = load_existing_data(filename)
    new_df = pd.DataFrame({'Brand': brand, "Price": price, 'Discount': discount})

    final_df = add_new_data(existing_df, new_df)

    final_df = append_Cost_Column(final_df, existing_df,new_df)
    print(final_df.columns)

    price_changes = compare_prices(existing_df, new_df)
    
    # Send email if price changes
    if "Increased" in price_changes or "Decreased" in price_changes:
        body = "\n".join([f"{brand}: {change}" for brand, change in zip(new_df['Brand'], price_changes)])
        send_email("Ajio Price Change Alert!", body)

    save_file(final_df,filename)
    
    get_html(driver)
    driver.quit()
    
main()
