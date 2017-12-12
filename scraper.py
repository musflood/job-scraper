"""Scrape the first ten pages of stackoverflow jobs for python jobs.

- The job title
- The company name
- The location
- The date posted (in whatever date format makes the most sense to you)
- The link to the actual job posting
"""
from bs4 import BeautifulSoup as bs
from datetime.datetime import now
import requests


def scrape_for_jobs(response):
    """Scrape a page for Python jobs.

    Returns the url for the next page of jobs.
    """
    content = bs(response.content, 'html.parser')
    jobs = content.find_all('div', class_='-job-summary ')

    all_job_data = []

    for job in jobs:
        languages = job.find('div', class_='-tags').get_text()

        if 'python' not in languages:
            continue

        job_data = []

        title = job.find('a', class_='job-link').text
        job_data.append(title if title else '')

        company = job.find('div', class_='-company')
        company_name = company.find('div', class_='-name').text.strip()
        job_data.append(company_name if company_name else '')

        company_location = company.find('div', class_='-location').text.strip('\r\n -')
        job_data.append(company_location if company_location else '')

        date_posted = job.find('p', class_='-posted-date').text.strip()
        job_data.append(date_posted if date_posted else '')

        link = job.find('a', class_='job-link').get('href')
        full_link = 'https://stackoverflow.com/jobs' + link
        job_data.append(full_link)

        all_job_data.append(job_data)

    save_results(all_job_data)

    next_page = content.find('a', class_='test-pagination-next').get('href')
    return 'https://stackoverflow.com/jobs' + next_page


def save_results(results):
    """Save the scraping results to a file."""
    output_file = 'Python jobs - {}.csv'.format(now().strftime('%m-%d-%y'))

    with open(output_file, 'a') as output:
        output.write(results)


def scrape_all_pages(num_pages=10):
    """Scrape first num pages of the job postings."""
    url = 'https://stackoverflow.com/jobs'
