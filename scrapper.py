import requests
from bs4 import BeautifulSoup


# 가장 마지막 페이지 가져오기
def get_last_page(URL):
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, 'html.parser')
  pagination = soup.find("div", class_="s-pagination")
  links = pagination.find_all("a")
  pages = []
  for link in links[:-1]:
    pages.append(int(link.text))
  max_page = pages[-1]
  return max_page

# 직업, 회사명, loaction, 링크 가져오기 (박스별 하나씩)
def extract_job(html):
  #직업명
  title = html.find("a")["title"]
  #회사와 위치 모두!!
  company, location = html.find("h3",class_="fc-black-700").find_all("span",recursive = False)
  company =company.get_text(strip = True)
  location = location.get_text(strip = True)
  # company = html.select_one('h3>span').string
  # final_company = company.replace(" " , "")
  # #location
  # location = html.find("span", class_="fc-black-500").string
  #link
  link = html.find("a")["href"]
  return {"title":title, "company": company, "location":location, "link":f"https://stackoverflow.com{link}"}


# 모든 박스에 대해서 실행
def scrap_jobs(last_page, URL):
  jobs =[]
  for page in range(last_page):
    print(f"Scraping page {page}")
    result =requests.get(f"{URL}&pg={page}")
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all("div",class_="flex--item fl1")
    for result_text in results:
      job = extract_job(result_text)
      jobs.append(job)
  return jobs


def get_jobs(word):
  URL= f"https://stackoverflow.com/jobs?q={word}"
  # 원하는 아무 직업이나 다 검색할 수 있도록 변경
  last_page = get_last_page(URL)
  jobs = scrap_jobs(last_page , URL)
  return jobs