#############yan_photo_download.py#############

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


image_format_ends = [
	'JPEG',
	'JPG',
	'PNG',
	'GIF',
	'TIFF',
	'PSD',
	'PDF',
	'EPS',
	'AI',
	'INDD',
	'RAW',
]

'''
download_image_from_url(
	page_url = page_url,
	photo_folder = '/dcd_data/linkedin/profile_photo',
	curl_file = None,
	redirect = None,
	overwrite = False,
	)
'''


def download_image_from_url(
	page_url,
	photo_folder = None,
	curl_file = None,
	redirect = None,
	overwrite = False,
	):
	url_hash = str_md5(page_url)
	if overwrite is False:
		for e in image_format_ends:
			file_name = '{}/{}.{}'.format(photo_folder, url_hash, e)
			if os.path.exists(file_name):
				print('\n{} already exists'.format(file_name))
				return file_name
	file_name = None
	print('\ndownloading image from {}'.format(page_url))
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
		file_name = '%s.%s'%(url_hash,image_end)
		os.rename(temp_html, file_name)
		if photo_folder is not None:
			os.system("mv {} {}/".format(file_name,photo_folder))
			return "{}/{}".format(
				photo_folder,
				file_name)
		else:
			return file_name
	except:
		return None


'''
from yan_web_page_download import *
file_name = download_image_from_url(
	page_url = 'https://www.citysearch.ae/uf/companies/14090/chilis.jpg',
	curl_file = None,
	redirect = None)
print(file_name)
os.system("mv %s /Downloads/"%(file_name))
file_name = download_image_from_url(
	page_url = 'https://www.gravatar.com/avatar/47c20752720b3597f9370f9dcf5e21b4?s=32&d=identicon&r=PG&f=1',
	curl_file = None,
	redirect = None)
os.system("mv %s /Downloads/"%(file_name))
'''


#############yan_photo_download.py#############