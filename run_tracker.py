import priceTracker
import schedule
import time

def run_price_tracker():
    print("Running price tracker...")
    priceTracker

# Schedule the script to run every 10 min
schedule.every(10).minutes.do(run_price_tracker)

# Keep the script running for infinity
while True:
    schedule.run_pending()
    time.sleep(30)  # Wait for 1 min before checking again to not overload cpu
