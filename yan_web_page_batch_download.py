##########yan_web_page_batch_download.py##########
import os
import re
import time
import pandas
import hashlib 
import argparse
import datetime
from os import listdir
from os.path import isfile, join, exists

import yan_obs
import yan_web_page_download 

parser = argparse.ArgumentParser()
parser.add_argument('--input_json')
parser.add_argument('--curl_file')
parser.add_argument('--obs_ak')
parser.add_argument('--obs_sk')
parser.add_argument('--obs_server')
parser.add_argument('--obs_bucketName')
parser.add_argument('--obs_path')
parser.add_argument('--local_path')
parser.add_argument('--page_regex')
parser.add_argument('--redirect')
parser.add_argument('--sleep_second_per_page')
args = parser.parse_args()


try:
	obs_session = yan_obs.create_obs_session(
		obs_ak = args.obs_ak,
		obs_sk = args.obs_sk,
		obs_server = args.obs_server,
		)
except Exception as e:
	obs_session = None
	print(e)


def upload_page_to_obs(
	page_html,
	page_url,
	obs_session,
	obs_bucketName,
	obs_path,
	overwrite = False,
	):
	#####
	company_id_hash = hashlib.md5(page_url.encode()).hexdigest()
	######
	if overwrite is True:
		file_exist =  False
	else:
		file_exist = yan_obs.obs_file_exist(
			obs_bucketName = obs_bucketName,
			file_name = '%s/%s.json'%(obs_path, company_id_hash),
			obs_session = obs_session)
	#####
	if file_exist is False:
		try:
			df = pandas.DataFrame([{
				'page_url':page_url,
				'page_url_hash':company_id_hash,
				'crawling_date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d'),
				'page_html':page_html
				}])
			print(df)
			df.to_json(
				path_or_buf = '%s.json'%(company_id_hash),
				orient = 'records',
				lines = True)
			yan_obs.upload_file_to_obs(
				obs_bucketName = obs_bucketName,
				local_file = '%s.json'%(company_id_hash),
				obs_file_name = '%s/%s.json'%(obs_path, company_id_hash),
				obs_session = obs_session)
			os.remove('%s.json'%(company_id_hash))
			return 'success'
		except Exception as e:
			print('failed to upload %s'%(page_url))
			print(e)
			return e
	else:
		print('%s/%s.json already exists'%(args.obs_path, company_id_hash))
		return 'exist'

def download_page_from_company_url_and_upload_to_obs(
	page_url,
	obs_session,
	obs_bucketName,
	obs_path,
	curl_file = None,
	redirect = None,
	page_regex = None,
	):
	#####
	company_id_hash = hashlib.md5(page_url.encode()).hexdigest()
	######
	file_exist = yan_obs.obs_file_exist(
		obs_bucketName = obs_bucketName,
		file_name = '%s/%s.json'%(obs_path, company_id_hash),
		obs_session = obs_session)
	#####
	if file_exist is False:
		try:
			html_data = yan_web_page_download.download_page_from_url(
				page_url = page_url,
				curl_file = curl_file,
				redirect = redirect,
				)
			if page_regex is not None:
				re.search(page_regex, html_data).group()
			html_head = html_data[0:1]
			df = pandas.DataFrame([{
				'page_url':page_url,
				'page_url_hash':hashlib.md5(page_url.encode()).hexdigest(),
				'crawling_date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d'),
				'page_html':html_data
				}])
			print(df)
			df.to_json(
				path_or_buf = '%s.json'%(company_id_hash),
				orient = 'records',
				lines = True)
			yan_obs.upload_file_to_obs(
				obs_bucketName = obs_bucketName,
				local_file = '%s.json'%(company_id_hash),
				obs_file_name = '%s/%s.json'%(obs_path, company_id_hash),
				obs_session = obs_session)
			os.remove('%s.json'%(company_id_hash))
			return 'success'
		except Exception as e:
			print('failed to download %s'%(page_url))
			print(e)
			return e
	else:
		print('%s/%s.json already exists'%(obs_path, company_id_hash))
		return 'exist'

def download_page_from_company_url(
	page_url,
	obs_session = None,
	obs_bucketName = None,
	obs_path = None,
	local_path = None,
	):
	#####
	company_id_hash = hashlib.md5(page_url.encode()).hexdigest()
	if local_path is not None:
		json_file_path = '%s/%s.json'%(
			local_path,
			company_id_hash
			)
		file_exist = exists(json_file_path)
		if file_exist is False:
			try:
				if args.sleep_second_per_page is not None:
					try:
						print('sleeping for %d s'%(int(args.sleep_second_per_page)))
						time.sleep(int(args.sleep_second_per_page))
					except:
						pass
				html_data = yan_web_page_download.download_page_from_url(
					page_url = page_url,
					curl_file = args.curl_file,
					redirect = args.redirect,
					)
				if args.page_regex is not None:
					re.search(args.page_regex, html_data).group()
				html_head = html_data[0:1]
				df = pandas.DataFrame([{
					'page_url':page_url,
					'page_url_hash':hashlib.md5(page_url.encode()).hexdigest(),
					'crawling_date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d'),
					'page_html':html_data
					}])
				print(df)
				output_json_path = '%s/%s.json'%(
						local_path,
						company_id_hash)
				df.to_json(
					path_or_buf = output_json_path,
					orient = 'records',
					lines = True)
				return 'success'
			except Exception as e:
				print('failed to download %s'%(page_url))
				print(e)
				return e
		else:
			print('%s already exists'%(json_file_path))
			return 'exist'
	####################
	if obs_path is not None:
		######
		file_exist = yan_obs.obs_file_exist(
			obs_bucketName = args.obs_bucketName,
			file_name = '%s/%s.json'%(args.obs_path, company_id_hash),
			obs_session = obs_session)
		#####
		if file_exist is False:
			try:
				if args.sleep_second_per_page is not None:
					try:
						time.sleep(int(args.sleep_second_per_page))
					except:
						pass
				html_data = yan_web_page_download.download_page_from_url(
					page_url = page_url,
					curl_file = args.curl_file,
					redirect = args.redirect,
					)
				if args.page_regex is not None:
					re.search(args.page_regex, html_data).group()
				html_head = html_data[0:1]
				df = pandas.DataFrame([{
					'page_url':page_url,
					'page_url_hash':hashlib.md5(page_url.encode()).hexdigest(),
					'crawling_date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d'),
					'page_html':html_data
					}])
				print(df)
				df.to_json(
					path_or_buf = '%s.json'%(company_id_hash),
					orient = 'records',
					lines = True)
				yan_obs.upload_file_to_obs(
					obs_bucketName = args.obs_bucketName,
					local_file = '%s.json'%(company_id_hash),
					obs_file_name = '%s/%s.json'%(args.obs_path, company_id_hash),
					obs_session = obs_session)
				os.remove('%s.json'%(company_id_hash))
				return 'success'
			except Exception as e:
				print('failed to download %s'%(page_url))
				print(e)
				return e
		else:
			print('%s/%s.json already exists'%(args.obs_path, company_id_hash))
			return 'exist'

def sequential_page_download(
	first_page_url,
	re_next_page_url,
	obs_bucketName = None,
	obs_path = None,
	obs_session = None,
	local_path = None,
	curl_file = None,
	next_page_prefix = None,
	sleep_second_per_page = None,
	):
	next_page_url = first_page_url
	while(next_page_url is not None):
		print('\n\ndownloading from %s'%(next_page_url))
		if sleep_second_per_page is not None:
			try:
				time.sleep(int(sleep_second_per_page))
			except:
				pass
		page_url = next_page_url
		page_html = yan_web_page_download.download_page_from_url(
				page_url = page_url,
				curl_file = curl_file)
		company_id_hash = yan_web_page_download.str_md5(next_page_url)
		############		
		try:
			next_page_url = re.search(re_next_page_url, 
				page_html).group('next_page_url')
			if next_page_prefix is not None:
				next_page_url = '%s%s'%(next_page_prefix,next_page_url)
			print('find next page %s'%(next_page_url))
		except:
			next_page_url = None
			print('reach the last page')
		#################
		df = pandas.DataFrame([{
			'first_page_url':first_page_url,
			'page_url':page_url,
			'next_page_url':next_page_url,
			'page_url_hash':company_id_hash,
			'crawling_date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d'),
			'page_html':page_html
			}])
		print(df)
		if local_path is not None:
			json_path = '%s/%s.json'%(
				local_path,
				company_id_hash)			
			df.to_json(
				path_or_buf = json_path,
				orient = 'records',
				lines = True)
		if obs_session is not None:
			df.to_json(
				path_or_buf = '%s.json'%(company_id_hash),
				orient = 'records',
				lines = True)
			status = yan_obs.upload_file_to_obs(
				obs_bucketName = obs_bucketName,
				local_file = '%s.json'%(company_id_hash),
				obs_file_name = '%s/%s.json'%(obs_path, company_id_hash),
				obs_session = obs_session)
			os.remove('%s.json'%(company_id_hash))

def get_html_data(r):
	print('\n\n')
	if args.obs_path is not None:
		r['status'] = download_page_from_company_url(
			page_url = r['page_url'],
			obs_session = obs_session,
			obs_bucketName = args.obs_bucketName,
			obs_path = args.obs_path,
			)
	else:
		r['status'] = download_page_from_company_url(
			page_url = r['page_url'],
			local_path = args.local_path,
			)
	print(r['status'])
	return r

def main():
	########
	if os.path.isfile(args.input_json):
		input_df = pandas.read_json(
			path_or_buf = args.input_json,
			orient = 'records',
			lines = True)
		input_df = input_df.apply(get_html_data, axis = 1)
	######
	if os.path.isdir(args.input_json):
		files = [join(args.input_json, f) 
			for f in listdir(args.input_json) 
			if isfile(join(args.input_json, f))
			and bool(re.search(r'.+\.json$', f))]
		for f in files:
			print('downloading pages of %s'%(f))
			input_df = pandas.read_json(
			path_or_buf = f,
			orient = 'records',
			lines = True)
			input_df = input_df.apply(get_html_data, axis = 1)
			print('removing %s'%(f))
			os.remove(f)
			print('%s removed'%(f))	

if __name__ == "__main__":
	main()

##########yan_web_page_batch_download.py##########