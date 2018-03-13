#!/usr/bin/env python3


from bs4 import BeautifulSoup as Soup
import requests
from sys import argv
import time
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

try:
    root_url = argv[1]
except:
    print("please input url behind the script!!")
    exit()

#root_url = 'http://web.stanford.edu/class/cs231a/syllabus.html' #course html

		
def get_pdf_links(root_url):
	res = requests.get(root_url)
	soup = Soup(res.text,'html.parser')
	temp = soup.findAll("a")	
	print('url: {}'.format(root_url))
	if not root_url.endswith("/"):     
		index = root_url.rfind("/")
		root_url = root_url[:index+1]
	pdf_links = []
	for link in temp:
		if link['href'].endswith('pdf'):  
			if link['href'].startswith('http'):			
				pdf_links.append(link['href'])
			else:
				pdf_links.append(root_url + link['href'] )	
	
	return pdf_links

def download_pdf(link):
	file_name = link.split('/')[-1]
	print(link+' downloading.....') 
	response = requests.get(link,stream=True)
	with open(file_name,'wb') as pdf:
		for chunk in response.iter_content(chunk_size = 1024):
			if chunk:
				pdf.write(chunk)
				pdf.flush()

def run(root_url):
	pdf_links = get_pdf_links(root_url)
	file_num = len(pdf_links)
	workers = 8

	pool = ThreadPoolExecutor(max_workers = workers)
	with pool as executor:
		future_url = {executor.submit(download_pdf, link): link for link in pdf_links}
		for future in concurrent.futures.as_completed(future_url):
			url = future_url[future]
			try:
				data = future.result()
			except Exception as exc:
				print('{} generated an exception: {}'.format(url, exc))


	print('All {} pdf files downloaded!'.format(file_num))


if __name__ == "__main__":
	run(root_url)
