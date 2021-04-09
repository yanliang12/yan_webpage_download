#######yan_web_page_download.py#######
import re
import os
import html
import random
import pandas
import urllib
import hashlib 
import requests

def download_page_from_url(
	page_url,
	curl_file = None,
	redirect = None):
	if redirect is not None:
		page_url = requests.get(page_url).url
	try:
		temp_html = "temp_%f.html"%(random.random())
		if curl_file is None:
			curl_commend_new = u"""
				curl '%s' --compressed -o %s
				"""%(page_url, temp_html)
		else:
			curl_commend = open(curl_file).read()
			'''
			replace the page url of the curl file by the input page url
			'''
			re_curl_firstline = r'^curl \'(?P<page_url>[^\s]+)\' \\\n'
			curl_fristline = re.search(re_curl_firstline,
				curl_commend).group()
			curl_page_url = re.search(re_curl_firstline,
				curl_commend).group('page_url')
			curl_fristline_replaced = re.sub(
				re.escape(curl_page_url),
				page_url,
				curl_fristline)
			curl_commend_new = re.sub(
				re.escape(curl_fristline),
				curl_fristline_replaced,
				curl_commend)
			curl_commend_new += " -o %s"%(temp_html)
		os.system(curl_commend_new)
		try:
			html_date = open(temp_html).read()
		except:
			html_date = open(temp_html, 
				encoding="cp1251", 
				errors='ignore'
				).read()
		html_date = html.unescape(html_date)
		try:
			os.remove(temp_html)
		except:
			pass
		return html_date
	except:
		return None
#######yan_web_page_download.py#######