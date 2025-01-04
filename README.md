# selenium_script
Steps to Set Up Selenium and MongoDB in Python

1. Install Selenium:  
   Run `pip install selenium` and download the WebDriver for your browser from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads).

2. Install MongoDB:  
   Download MongoDB from [mongodb.com](https://www.mongodb.com/try/download/community), install it, and start the server using `mongodb`.

3. Install PyMongo:  
   Install the Python MongoDB driver using `pip install pymongo`.

4. Set Up MongoDB in Python:  
   Use the following code to connect to MongoDB:
   ```from pymongo import MongoClient
   client = MongoClient("mongodb://localhost:27017/")
   db = client['your_database_name']```

5. Run the Script:  
   Ensure MongoDB is running, match the WebDriver to your browser version, and execute the script for web scraping and data storage.

![Screenshot 2025-01-04 183714](https://github.com/user-attachments/assets/7a14005a-c404-4ff1-b667-3b6f4dc5cdde)
