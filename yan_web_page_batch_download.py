##########yan_web_page_batch_download.py##########
import os
import re
import time
import pandas
import hashlib 
import argparse
import datetime
from os import listdir
from os.path import isfile, join

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
parser.add_argument('--page_regex')
args = parser.parse_args()

obs_session = yan_obs.create_obs_session(
	obs_ak = args.obs_ak,
	obs_sk = args.obs_sk,
	obs_server = args.obs_server,
	)

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

def download_page_from_company_url(
	page_url,
	obs_session,
	obs_bucketName,
	obs_path,
	):
	#####
	company_id_hash = hashlib.md5(page_url.encode()).hexdigest()
	######
	file_exist = yan_obs.obs_file_exist(
		obs_bucketName = args.obs_bucketName,
		file_name = '%s/%s.json'%(args.obs_path, company_id_hash),
		obs_session = obs_session)
	#####
	if file_exist is False:
		try:
			html_data = yan_web_page_download.download_page_from_url(
				page_url = page_url,
				curl_file = args.curl_file,
				)
			if args.page_regex is not None:
				re.search(args.page_regex,
					html_data).group()
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

def get_html_data(r):
	print('\n\n')
	r['status'] = download_page_from_company_url(
		page_url = r['page_url'],
		obs_session = obs_session,
		obs_bucketName = args.obs_bucketName,
		obs_path = args.obs_path,
		)
	print(r['status'])
	return r

if __name__ == "__main__":
	########
	if os.path.isfile(args.input_json):
		input_df = pandas.read_json(
			path_or_buf = args.input_json,
			orient = 'records',
			lines = True)
		input_df = input_df.apply(get_html_data, axis = 1)
	######
	if os.path.isdir(args.input_json):
		files = [join(args.input_json, f) for f in listdir(args.input_json) if isfile(join(args.input_json, f))]
		for f in files:
			input_df = pandas.read_json(
			path_or_buf = f,
			orient = 'records',
			lines = True)
			input_df = input_df.apply(get_html_data, axis = 1)

##########yan_web_page_batch_download.py##########