#######yan_web_page_download.py#######
import re
import os
import random
import pandas
import urllib
import hashlib 
import requests

from PIL import Image

try:
	import html
except:
	import HTMLParser
	html = HTMLParser.HTMLParser()

def str_md5(input):
	return hashlib.md5(input.encode()).hexdigest()

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


def download_image_from_url(
	page_url,
	curl_file = None,
	redirect = None):
	if redirect is not None:
		page_url = requests.get(page_url).url
	temp_html = "temp_%f"%(random.random())
	try:
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
		image_end = Image.open(temp_html).format
		url_hash = str_md5(page_url)
		file_name = '%s.%s'%(url_hash,image_end)
		os.rename(temp_html, file_name)
		return file_name
	except:
		return None


'''
from yan_web_page_download import *

file_name = download_image_from_url(
	page_url = 'https://kuwaitlocal.com/img/BusinessLogo/logo_folder/sml_08062015164850_Kiran_technical_Co.jpg',
	curl_file = None,
	redirect = None)

os.system("mv %s /Downloads/"%(file_name))

scp jim@10.1.129.77:/home/jim/24837805ad4e9ed02dcea89df0fdc966.JPEG C:\Users\jywan\Desktop\

pegasus@123

file_name = download_image_from_url(
	page_url = 'https://www.gravatar.com/avatar/47c20752720b3597f9370f9dcf5e21b4?s=32&d=identicon&r=PG&f=1',
	curl_file = None,
	redirect = None)

os.system("mv %s /Downloads/"%(file_name))
'''
#######yan_web_page_download.py#######