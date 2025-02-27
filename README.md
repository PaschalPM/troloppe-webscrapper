# **Troloppe Web Scraper for Agent Listings**

## **Overview**

This project is a web scraper designed for **Troloppe Property Services**, enabling the extraction of real estate agent listings from:

- **Nigerian Property Center**
- **Private Property**

The scraper collects agent details such as names, emails, phone numbers, and profile URLs, saving the data for further analysis and processing.

---

## **Features**

✅ Scrapes real estate agent profiles from targeted property websites\
✅ Extracts and saves agent contact details (name, email, phone, etc.)\
✅ Supports structured storage in **CSV** and **SQLite database**\
✅ Implements locking mechanisms to prevent duplicate downloads\
✅ Modular and extendable for additional property listing sites

---

## **Project Structure**

```
📂 project_root/
│── .gitignore
│── main.py                    # Entry point for the scraper  
│── agent_profile_urls.json     # Cached agent profile URLs  
│── data_access/                # Handles database queries  
│   ├── __init__.py  
│   ├── npc_queries.py  
│── downloaded_files/           # Lock files for tracking downloads  
│── lib/                        # Core scraping logic  
│   ├── browser.py              # Browser automation for scraping  
│   ├── websites_browsers/      # Website-specific scrapers  
│   │   ├── nigerian_property_center/  
│   │   │   ├── __init__.py  
│   │   │   ├── agent_profile.py  
│   │   │   ├── agent_other_details.py  
│   │   ├── private_property.py  
│── storage/                    # Data storage  
│   ├── credentials.py          # Authentication details (not tracked in Git)  
│   ├── csv/                    # CSV files with extracted data  
│   ├── db.sqlite               # SQLite database storing agent listings  
│   ├── tmp.json                # Temporary data store  
│── utils/                      # Utility functions  
│   ├── __init__.py  
│   ├── convert_to_csv.py       # CSV conversion functions  
│   ├── db.py                   # Database helper functions  
│   ├── tmp_store.py            # Temporary storage utilities  
```

---

## **Installation & Setup**

### **1. Clone the Repository**

```bash
git clone https://github.com/your-username/troloppe-webscraper.git
cd troloppe-webscraper
```

### **2. Create a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## **Usage**

### **Running the Scraper**

To start the scraper and extract agent listings, run:

```bash
python main.py
```

### **Output Data**

- **CSV files** are stored in `storage/csv/`
- **Database records** are stored in `storage/db.sqlite`

---

## **Technologies Used**

🔹 **Python** – Core programming language\
🔹 **Selenium / Requests / BeautifulSoup** – Web scraping tools\
🔹 **SQLite & CSV** – Data storage formats

---

## **Future Improvements**

🔹 Add support for more property listing websites\
🔹 Implement an API for fetching scraped data\
🔹 Automate scraper execution with scheduled tasks

---

## **Author**

👨‍💻 **[Your Name]**\
🔗 **Troloppe Property Services**

---

