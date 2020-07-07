import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?as_and=Python&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&salary=&radius=25&l=&fromage=any&limit={LIMIT}&sort=&psf=advsrch&from=advancedsearch"

def get_last_page():
    result = requests.get(URL)

    # BeautifulSoup helps you extract detail data from html page
    soup = BeautifulSoup(result.text, 'html.parser')

    pagination = soup.find('div', {'class': 'pagination'})

    links = pagination.find_all('a')

    pages = []
    for link in links[:-1]:
        # pages.append(link.find('span').string)
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page

def extract_job(html):
    title = html.find('h2', {'class':'title'}).find('a')['title']

    company = html.find('span', {'class':'company'})
    if company:
        company_anchor = company.find('a')
        if company_anchor:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
        company = company.strip()
    else:
        company = None

    location = html.find('div', {'class': 'recJobLoc'})['data-rc-loc']

    job_id = html['data-jk']

    return {'title': title, 'company': company, 'location': location, 'link': f'https://www.indeed.com/viewjob?jk={job_id}'}

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f'Scrapping Indeed: Page {page}')
        result = requests.get(f'{URL}&start={page*LIMIT}')
        soup = BeautifulSoup(result.text, 'html.parser')

        # find_all() returns all elements of the list, find() returns only the first element
        results = soup.find_all('div', {'class': 'jobsearch-SerpJobCard'})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs