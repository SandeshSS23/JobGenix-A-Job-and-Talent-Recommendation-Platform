from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv

service = Service('/usr/local/bin/chromedriver')

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=service, options=chrome_options)

base_url = 'https://www.naukri.com/software-developer-jobs?k=software%20developer&nignbevent_src=jobsearchDeskGNB'
def scrape_jobs_from_page(driver, existing_job_ids):
    jobs = []
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_container = soup.find('div', class_='styles_jlc__main__VdwtF')
        job_cards = job_container.find_all('div', class_='srp-jobtuple-wrapper') if job_container else []
        print(f'Found {len(job_cards)} job cards on the page.')

        for index, job_card in enumerate(job_cards, start=1):
            try:
                job_id = job_card.get('data-job-id', 'Not Available')
                if job_id in existing_job_ids:
                    print(f'Skipping already scraped job ID: {job_id}')
                    continue
                
                job_data = {}
                job_data['Job ID'] = job_id
                job_data['Title'] = job_card.find('h2').get_text(strip=True) if job_card.find('h2') else 'Not Available'
                job_data['Company Name'] = job_card.find('a', class_='comp-name').get_text(strip=True) if job_card.find('a', class_='comp-name') else 'Not Available'
                job_data['Experience'] = job_card.find('span', class_='expwdth').get_text(strip=True) if job_card.find('span', class_='expwdth') else 'Not Available'
                job_data['Salary'] = job_card.find('span', class_='sal').get_text(strip=True) if job_card.find('span', class_='sal') else 'Not Available'
                job_data['Location'] = job_card.find('span', class_='locWdth').get_text(strip=True) if job_card.find('span', class_='locWdth') else 'Not Available'
                job_data['Job Description'] = job_card.find('span', class_='job-desc').get_text(strip=True) if job_card.find('span', class_='job-desc') else 'Not Available'
                job_data['Skills'] = ', '.join([li.get_text(strip=True) for li in job_card.find_all('li', class_='tag-li')])
                job_data['Post Date'] = job_card.find('span', class_='job-post-day').get_text(strip=True) if job_card.find('span', class_='job-post-day') else 'Not Available'
                job_data['Job Link'] = job_card.find('a', class_='title')['href'] if job_card.find('a', class_='title') else 'Not Available'

                job_link = job_data['Job Link']
                print(f"Opening job details page for: {job_data['Title']} at {job_data['Company Name']}")
                
                if job_link != 'Not Available':
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(job_link)
                    
                    try:
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'styles_jd-header-title__rZwM1')))
                        print('Details page loaded successfully.')

                        details_page_soup = BeautifulSoup(driver.page_source, 'html.parser')
                        
                        detail_checks = {
                            'Job Title': details_page_soup.find('h1', class_='styles_jd-header-title__rZwM1'),
                            'Company Name': details_page_soup.find('a', class_='styles_jd-header-comp-name__MvqAI'),
                            'Company Rating': details_page_soup.find('span', class_='styles_amb-rating__4UyFL'),
                            'Experience Required': details_page_soup.find('div', class_='styles_jhc__exp__k_giM'),
                            'Salary': details_page_soup.find('div', class_='styles_jhc__salary__jdfEC'),
                            'Job Location': details_page_soup.find('div', class_='styles_jhc__location__W_pVs'),
                            'Job Description': details_page_soup.find('div', class_='styles_JDC__dang-inner-html__h0K4t'),  
                        }
                        
                        for key, element in detail_checks.items():
                            if element:
                                print(f'✅ Found "{key}" on details page.')
                            else:
                                print(f'❌ Could not find "{key}" on details page.')
                        job_data['Title'] = detail_checks['Job Title'].get_text(strip=True) if detail_checks['Job Title'] else job_data['Title']
                        job_data['Company Name'] = detail_checks['Company Name'].get_text(strip=True) if detail_checks['Company Name'] else job_data['Company Name']
                        job_data['Experience'] = detail_checks['Experience Required'].get_text(strip=True) if detail_checks['Experience Required'] else job_data['Experience']
                        job_data['Salary'] = detail_checks['Salary'].get_text(strip=True) if detail_checks['Salary'] else job_data['Salary']
                        job_data['Location'] = detail_checks['Job Location'].get_text(strip=True) if detail_checks['Job Location'] else job_data['Location']
                        job_data['Job Description'] = detail_checks['Job Description'].get_text(strip=True) if detail_checks['Job Description'] else job_data['Job Description']
                        job_data['Data Source'] = 'Details Page'
                        job_data['Job Highlights'] = 'Not Available'
                        job_data['Company Overview'] = 'Not Available'
                        job_data['Industry'] = 'Not Available'                        
                        try:
                            company_overview_element = driver.find_element(By.CLASS_NAME, 'styles_about-company__lOsvW')
                            if company_overview_element:
                                overview_parts = [el.text.strip() for el in company_overview_element.find_elements(By.XPATH, './/p | .//li') if el.text.strip()]
                                job_data['Company Overview'] = ' '.join(overview_parts) if overview_parts else 'Not Available'
                                print('✅ Compiled "Company Overview" into a single paragraph.')
                            else:
                                job_data['Company Overview'] = 'Not Available'
                        except Exception as e:
                            print(f'❌ Could not find "Company Overview" on details page: {e}')

                    
                    except Exception as e:
                        print(f'Error loading details page or extracting data: {e}')
                        job_data['Data Source'] = 'Listing Page'

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                else:
                    job_data['Data Source'] = 'Listing Page'

                jobs.append(job_data)
                print(f"Scraped job {index}: {job_data['Title']} at {job_data['Company Name']} from {job_data['Data Source']}")

            except Exception as e:
                print(f'Error processing job card {index}: {e}')

    except Exception as e:
        print(f'Error finding job cards: {e}')
    
    return jobs

def get_total_jobs():
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_count_text = soup.find('span', class_='styles_count-string__DlPaZ').get_text()
        total_jobs = int(job_count_text.split('of')[-1].strip().replace(',', ''))
        print(f'Total jobs available: {total_jobs}')
        return total_jobs
    except Exception as e:
        print(f'Error fetching total job count: {e}')
        return 0
    
def scrape_all_pages():

    page_number = 1
    csv_file = 'naukri_final_scraping_trial_2.csv'
    csv_columns = ['Job ID', 'Title', 'Company Name', 'Experience', 'Salary', 'Location', 'Job Description', 'Skills', 'Post Date', 'Job Link', 'Data Source', 'Company Overview', 'Industry', 'Job Highlights']
    
    jobs = scrape_jobs_from_page(driver,set())

    existing_job_ids = set()
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_job_ids.add(row['Job ID'])
        print(f'Loaded {len(existing_job_ids)} existing job IDs.')
    except FileNotFoundError:
        print('No existing file found. Starting fresh.')

    driver.get(base_url)
    time.sleep(2)

    total_jobs = get_total_jobs()

    while len(existing_job_ids) < total_jobs:
        print(f'Opening page {page_number}...')
        driver.get(f'https://www.naukri.com/software-developer-jobs-{page_number}')
        time.sleep(2)

        jobs = scrape_jobs_from_page(driver,existing_job_ids)
        if not jobs and len(existing_job_ids) < total_jobs:
            print('No new jobs found on this page. Continuing to the next page.')
            page_number += 1
            continue

        with open(csv_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns)
            writer.writerows(jobs)

        existing_job_ids.update([job['Job ID'] for job in jobs])
        page_number += 1

    print(f'✅ All available job(s) scraped and saved to {csv_file}')

scrape_all_pages()

print('Closing the driver...')
driver.quit()
print('Driver closed.')
