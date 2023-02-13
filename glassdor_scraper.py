from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


def get_jobs(keyword, num_jobs, path, slp_time):

    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=" + keyword + "&sc.keyword=" + keyword + "&locT=&locId=&jobType="

    driver.get(url)
    jobs = []
    driver.find_element(By.CSS_SELECTOR, "li.react-job-listing").click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "modal_closeIcon").click()
    time.sleep(1)
    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "e856ufb2").click()
    time.sleep(1)

    while len(jobs) < num_jobs:
        time.sleep(slp_time)
        job_buttons = driver.find_elements(By.CSS_SELECTOR, "li.react-job-listing")

        for job_button in job_buttons:
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))

            if len(jobs) >= num_jobs:
                break
            job_button.click()
            time.sleep(1)

            try:
                driver.find_element(By.CLASS_NAME, "e856ufb2").click()
            except:
                pass
            time.sleep(1)

            try:
                driver.find_element(By.CLASS_NAME, "modal_closeIcon").click()
            except:
                pass
            time.sleep(1)

            try:
                driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
            except:
                pass
            time.sleep(1)

            collected_successfully = False

            while not collected_successfully:
                try:
                    company_name = driver.find_element(By.CLASS_NAME, "css-xuk5ye").text.split('\n')[0]
                    print(company_name)
                except:
                    company_name = -1

                try:
                    location = driver.find_element(By.CLASS_NAME, "css-56kyx5").text
                    print(location)
                except:
                    location = -1

                try:
                    job_title = driver.find_element(By.CLASS_NAME, "css-1j389vi").text
                    print(job_title)
                except:
                    job_title = -1

                try:
                    job_description = driver.find_element(By.ID, "JobDescriptionContainer").text
                    print(job_description)
                except:
                    job_description = -1

                try:
                    salary_estimate = driver.find_element(By.CLASS_NAME, "e2u4hf18").text
                    print(salary_estimate)
                except:
                    salary_estimate = -1

                try:
                    rating = driver.find_element(By.CLASS_NAME, "css-xuk5ye").text.split('\n')[1]
                    print(rating)
                except:
                    rating = -1

                try:
                    company_industry = driver.find_element(By.ID, "CompanyContainer").text.split('\n')[10]
                    print(company_industry)
                except:
                    company_industry = -1

                try:
                    size = driver.find_element(By.ID, "CompanyContainer").text.split('\n')[2]
                    print(size)
                except:
                    size = -1

                try:
                    founded = driver.find_element(By.ID, "CompanyContainer").text.split('\n')[8]
                    print(founded)
                except:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element(By.ID, "CompanyContainer").text.split('\n')[4]
                    print(type_of_ownership)
                except:
                    type_of_ownership = -1

                try:
                    sector = driver.find_element(By.ID, "CompanyContainer").text.split('\n')[6]
                    print(sector)
                except:
                    sector = -1

                try:
                    revenue = driver.find_element(By.ID, "CompanyContainer").text.split('\n')[12]
                    print(revenue)
                except:
                    revenue = -1
                collected_successfully = True

            jobs.append({"Company Name": company_name,
                         "Location": location,
                         "Job title": job_title,
                         "Job description": job_description,
                         "Salary estimate": salary_estimate,
                         "Rating": rating,
                         "Company industry": company_industry,
                         "Siza": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Sector": sector,
                         "Revenur": revenue
                         })

        try:
            driver.find_element(By.CLASS_NAME, "nextButton").click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))

            break

    return pd.DataFrame(jobs)