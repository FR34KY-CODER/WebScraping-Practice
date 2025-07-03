import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

#############################################
# PART 1: Paginate Through Multiple Base URLs
#############################################

options1 = uc.ChromeOptions()
options1.add_argument("--start-maximized")
options1.add_argument(r"C:\Users\FR34K\AppData\Local\Google\Chrome\User Data\Profile 1")
options1.add_argument("--profile-directory=Default")

# List of 10 base URLs to process
base_urls = [
    "https://indiankanoon.org/search/?formInput=doctypes:supremecourt%20year:2021",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202021&pagenum=1",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202022&pagenum=2",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202023&pagenum=3",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202024&pagenum=4",
    "https://indiankanoon.org/search/?formInput=doctypes:supremecourt%20year:2020",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202020&pagenum=1",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202020&pagenum=2",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202020&pagenum=3",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202020&pagenum=4",
    "https://indiankanoon.org/search/?formInput=doctypes:supremecourt%20year:2019",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202019&pagenum=1",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202019&pagenum=2",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202019&pagenum=3",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202019&pagenum=4",
    "https://indiankanoon.org/search/?formInput=doctypes:supremecourt%20year:2018",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202018&pagenum=1",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202018&pagenum=2", 
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202018&pagenum=3",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202018&pagenum=4",
    "https://indiankanoon.org/search/?formInput=doctypes:supremecourt%20year:2017", 
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202017&pagenum=1",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202017&pagenum=2",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202017&pagenum=3",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202017&pagenum=4",
    "https://indiankanoon.org/search/?formInput=doctypes:supremecourt%20year:2016",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202016&pagenum=1",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202016&pagenum=2",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202016&pagenum=3",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202016&pagenum=4",
    "https://indiankanoon.org/search/?formInput=doctypes:supremecourt%20year:2015",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202015&pagenum=1",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202015&pagenum=2",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202015&pagenum=3",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202015&pagenum=4",
    "https://indiankanoon.org/search/?formInput=doctypes:supremecourt%20year:2014",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202014&pagenum=1",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202014&pagenum=2",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202014&pagenum=3",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202014&pagenum=4",
    "https://indiankanoon.org/search/?formInput=doctypes:supremecourt%20year:2013",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202013&pagenum=1",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202013&pagenum=2",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202013&pagenum=3",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202013&pagenum=4",
    "https://indiankanoon.org/search/?formInput=doctypes:supremecourt%20year:2012",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202012&pagenum=1",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202012&pagenum=2",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202012&pagenum=3",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202012&pagenum=4",
    "https://indiankanoon.org/search/?formInput=doctypes:supremecourt%20year:2011",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202011&pagenum=1",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202011&pagenum=2",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202011&pagenum=3",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202011&pagenum=4",
    "https://indiankanoon.org/search/?formInput=doctypes:supremecourt%20year:2010",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202010&pagenum=1",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202010&pagenum=2",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202010&pagenum=3",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202010&pagenum=4",
]


driver = uc.Chrome(options=options1)
all_cases = []  # Stores cases from all URLs

for url in base_urls:
    print(f"Processing URL: {url}")
    driver.get(url)
    
    try:
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CLASS_NAME, "result_title"))
        )
    except Exception as e:
        print(f"Error loading {url}: {e}")
        continue  # Skip to next URL if current fails
    
    # Paginate through all pages of current URL
    while True:
        time.sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        case_elements = soup.find_all("div", class_="result_title")
        for case in case_elements:
            try:
                a_tag = case.find("a")
                title = a_tag.get_text(strip=True)
                href = a_tag.get("href")
                if not href.startswith("http"):
                    href = "https://indiankanoon.org" + href
                date_elem = case.find_next("div", class_="result_subtitle")
                date_text = date_elem.get_text(strip=True) if date_elem else ""
                all_cases.append({
                    "Case Title": title,
                    "Date": date_text,
                    "Link": href
                })
            except Exception as ex:
                print(f"Error parsing case: {ex}")
        
        # Attempt pagination
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "a[rel='next']")
            next_button.click()
            WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.CLASS_NAME, "result_title"))
            )
        except:
            print(f"No more pages on {url}")
            break

driver.quit()
print(f"Total cases collected: {len(all_cases)}")

#############################################
# PART 2: Extract Detailed Content from All Cases
#############################################

def extract_case_content(soup_case):
    # (Keep the original content extraction logic)
    container = soup_case.find("div", class_="doc") or \
                soup_case.find("div", id="doc") or \
                soup_case.find("div", class_="docFragment")
    
    if container:
        return container.get_text(separator="\n", strip=True)
    else:
        paragraphs = soup_case.find_all("p")
        return "\n".join(p.get_text(strip=True) for p in paragraphs) if paragraphs else ""

# Configure driver for detail extraction
options2 = uc.ChromeOptions()
options2.add_argument("--start-maximized")
options2.add_argument(r"--user-data-dir=C:\Users\FR34K\AppData\Local\Google\Chrome\User Data")
options2.add_argument("--profile-directory=Default")

driver2 = uc.Chrome(options=options2)


start_all = time.time()
# Process ALL collected cases
for idx, case in enumerate(all_cases, start = 1):
    start_case = time.time()
    try:
        driver2.get(case["Link"])
        try:
            WebDriverWait(driver2, 40).until(
                EC.presence_of_element_located((By.ID, "doc"))
            )
        except:
            WebDriverWait(driver2, 40).until(
                EC.presence_of_element_located((By.TAG_NAME, "p"))
            )
        
        time.sleep(1.5)
        case_html = driver2.page_source
        soup_case = BeautifulSoup(case_html, "html.parser")
        all_cases[idx]["Case Content"] = extract_case_content(soup_case)
        elapsed = time.time() - start_case
        print(f"Processed {idx+1}/{len(all_cases)} cases in {elapsed:.2f} s")
    except Exception as ex:
        print(f"Failed to process case {idx+1}: {ex}")
        all_cases[idx]["Case Content"] = ""

driver2.quit()
total_elapsed = time.time() - start_all
print(f"Detailed content extraction complete in {total_elapsed/60:.2f} minutes.")  
#############################################
# PART 3: Save Consolidated Data
#############################################

df = pd.DataFrame(all_cases)
csv_filename = "consolidated_supreme_court_cases2.csv"
df.to_csv(csv_filename, index=False, encoding="utf-8")
print(f"✅ All data saved to {csv_filename}")