"""Scrape the first ten pages of stackoverflow jobs for python jobs.

- The job title
- The company name
- The location
- The date posted (in whatever date format makes the most sense to you)
- The link to the actual job posting
"""
from bs4 import BeautifulSoup as bs
from datetime import datetime
import os
import requests

DOMAIN = 'https://stackoverflow.com/jobs'


def scrape_for_jobs(response):
    """Scrape a page for Python jobs.

    Returns the url for the next page of jobs.
    """
    content = bs(response.content, 'html.parser')
    jobs = content.find_all('div', class_='-job-summary ')

    all_job_data = []

    for job in jobs:
        languages = job.find('div', class_='-tags')

        if not languages:
            continue

        if 'python' not in languages.get_text():
            continue

        job_data = []

        title = job.find('a', class_='job-link').text
        job_data.append(title if title else '')

        company = job.find('div', class_='-company')
        company_name = company.find('div', class_='-name').text.strip()
        job_data.append(company_name if company_name else '')

        company_location = company.find('div', class_='-location').text.strip('\r\n -')
        job_data.append('"{}"'.format(company_location) if company_location else '')

        date_posted = job.find('p', class_='-posted-date').text.strip()
        job_data.append(date_posted if date_posted else '')

        link = job.find('a', class_='job-link').get('href')
        full_link = DOMAIN + link
        job_data.append(full_link)

        all_job_data.append(job_data)

    save_results(all_job_data)


def save_results(results):
    """Save the scraping results to a file."""
    dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'results')
    output_file = 'Python jobs - {}.csv'.format(datetime.now().strftime('%m-%d-%y'))
    output_path = os.path.join(dir_path, output_file)

    if not os.path.isfile(output_path):
        with open(output_path, 'w') as output:
            output.write('Job Title,Company,Location,Date Posted,Link')

    with open(output_path, 'a') as output:
        data = [','.join(job_data) for job_data in results]
        output.write('\n' + '\n'.join(data))


def get_job_page(page_num):
    """Scrape num page of the job postings."""
    response = requests.get(DOMAIN + '?pg={}'.format(page_num))
    return scrape_for_jobs(response)

if __name__ == '__main__':
    print('Scraping the StackOverflow Job site for Python jobs!')
    for n in range(1, 11):
        print('Scraping page {}...'.format(n))
        get_job_page(n)
    print('Done!')
