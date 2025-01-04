from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pymongo import MongoClient
import uuid
import urllib.parse
import requests
from datetime import datetime

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client['twitter_trends']
collection = db['trending_topics']

# ProxyMesh configuration (use URL encoding for special characters)
proxy_username = "USERNAME_OF_ProxyMesh"
proxy_password = urllib.parse.quote("PASSWORD_OF_ProxyMesh")  # Encode special characters
PROXY_URL = f"http://{proxy_username}:{proxy_password}@us-ca.proxymesh.com:31280"

def get_twitter_trends():
    try:
        with webdriver.Chrome() as driver:
            # Set an explicit wait
            wait = WebDriverWait(driver, 300)  # 30 seconds timeout
            driver.get("https://x.com/i/flow/login")
            
            # Wait for the username field to be visible
            username_input = wait.until(EC.presence_of_element_located((By.NAME, "text")))
            username_input.send_keys("@USERNAME")
            username_input.send_keys(Keys.RETURN)

            # Wait for the password field to be visible
            password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.send_keys("PASSWORD")
            password_input.send_keys(Keys.RETURN)

            # Wait for trending elements to be loaded
            wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div[data-testid='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln38']")
            ))
            
            trends = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3'] span")
            top_5_trends = [trend.text for trend in trends[:5]]

            try:
                proxies = {"http": PROXY_URL, "https": PROXY_URL}
                ip_response = requests.get("http://ipinfo.io/json", proxies=proxies)
                print("Proxy response:", ip_response.text)
                ip_address = ip_response.json().get("ip", "N/A")
            except Exception as e:
                print("Error fetching IP address:", e)
                ip_address = "N/A"

            # Store data in MongoDB
            unique_id = str(uuid.uuid4())
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record = {
                "_id": unique_id,
                "trend_1": top_5_trends[0] if len(top_5_trends) > 0 else None,
                "trend_2": top_5_trends[1] if len(top_5_trends) > 1 else None,
                "trend_3": top_5_trends[2] if len(top_5_trends) > 2 else None,
                "trend_4": top_5_trends[3] if len(top_5_trends) > 3 else None,
                "trend_5": top_5_trends[4] if len(top_5_trends) > 4 else None,
                "timestamp": timestamp,
                "ip_address": ip_address
            }
            collection.insert_one(record)
            return record

    except Exception as e:
        print("Error occurred:", e)
        return {"error": str(e)}

if __name__ == "__main__":
    result = get_twitter_trends()
    print(result)
