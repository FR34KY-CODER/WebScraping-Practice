import time
import re
import pandas as pd
from bs4 import BeautifulSoup

# Selenium-related imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

#############################################
# PART 1: Paginate Through the Search Results
#############################################

# Configure undetected_chromedriver options for pagination using your personal profile.
options1 = uc.ChromeOptions()
options1.add_argument("--start-maximized")
options1.add_argument(r"--user-data-dir=C:\Users\FR34K\AppData\Local\Google\Chrome\User Data")
options1.add_argument("--profile-directory=Default")
# options1.add_argument("--headless")  # Uncomment if desired

base_urls = [
    "https://indiankanoon.org/search/?formInput=doctypes:supremecourt%20year:2025",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202025&pagenum=1",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202025&pagenum=2",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202025&pagenum=3",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202025&pagenum=4",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202025&pagenum=5",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202025&pagenum=6",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202025&pagenum=7",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202025&pagenum=8",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202025&pagenum=9",
    "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202025&pagenum=10",
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
    
    while True:
        time.sleep(5)  # Allow time for lazy-loaded content.
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Extract all case containers by the 'result_title' class.
        case_elements = soup.find_all("div", class_="result_title")
        if not case_elements:
            print("No case elements found on this page.")
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
                print("Error parsing a case:", ex)

        # Try to click the "Next" button using a CSS selector with rel="next".
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "a[rel='next']")
            next_button.click()
            WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, "result_title")))
        except Exception as e:
            print("No more pages or error clicking next:", e)
            break

driver.quit()
print(f"Extracted {len(all_cases)} cases from paginated results.")

#############################################
# PART 2: Extract Detailed Segregated Content from Case Pages (Test Mode)
#############################################

# For testing, process only the first 10 cases.
test_cases = all_cases

def extract_sections_from_case(soup):
    """
    Extracts segregated sections directly from <p> tags using their title attribute,
    with exact case-sensitive matching.
    Expected section titles:
      "Issue", "Precedent Analysis", "Analysis of the law", "Fact",
      "Respondent's Argument", "Petitioner's Argument", "Court's Reasoning", "Conclusion"
    """
    expected_sections = ["Conclusion"]
    sections = {section: "" for section in expected_sections}
    
    # Find all <p> tags that have a title attribute.
    p_tags = soup.find_all("p", title=True)
    for p in p_tags:
        title_attr = p.get("title")
        # Check for an exact match (case-sensitive)
        if title_attr in expected_sections:
            sections[title_attr] += p.get_text(separator="\n", strip=True) + "\n"
    # Clean up extra newlines.
    for section in sections:
        sections[section] = sections[section].strip()
    return sections

# Create a new ChromeOptions object for detailed extraction.
options2 = uc.ChromeOptions()
options2.add_argument("--start-maximized")
options2.add_argument(r"--user-data-dir=C:\Users\FR34K\AppData\Local\Google\Chrome\User Data")
options2.add_argument("--profile-directory=Default")
# options2.add_argument("--headless")  # Uncomment if desired

driver2 = uc.Chrome(options=options2)
segregated_contents = []  # List to store segregated content for each case.


start_all = time.time()
for idx, case in enumerate(test_cases):
    start_case = time.time()
    try:
        driver2.get(case["Link"])
        # Wait until at least one <p> tag is present.
        WebDriverWait(driver2, 40).until(
            EC.presence_of_element_located((By.TAG_NAME, "p"))
        )
        time.sleep(2)  # Extra delay if necessary.
        case_html = driver2.page_source
        soup_case = BeautifulSoup(case_html, "html.parser")
        sections = extract_sections_from_case(soup_case)
        segregated_contents.append(sections)
        elapsed = time.time() - start_case
        print(f"Processed case {idx+1} of {len(test_cases)} in {elapsed:.2f} s")
    except Exception as ex:
        print(f"Error processing case {idx+1}: {ex}")
        segregated_contents.append({section: "" for section in ["Conclusion"]})

driver2.quit()
total_elapsed = time.time() - start_all
print(f"All {len(all_cases)} cases processed in {total_elapsed/60:.2f} minutes")
#############################################
# PART 3: Merge Data and Save to CSV (Test Data)
#############################################

processed_test_cases = []
for idx, case in enumerate(test_cases):
    new_case = case.copy()
    new_case.update(segregated_contents[idx])
    processed_test_cases.append(new_case)

df_test = pd.DataFrame(processed_test_cases)
csv_filename = "supreme_court_cases_conclusions.csv"
df_test.to_csv(csv_filename, index=False, encoding="utf-8")
print(f"✅ Test data with segregated sections saved to {csv_filename}")
