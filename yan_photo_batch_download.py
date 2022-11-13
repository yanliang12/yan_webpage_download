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
import yan_photo_download 

parser = argparse.ArgumentParser()
parser.add_argument('--input_json')
parser.add_argument('--curl_file')
parser.add_argument('--obs_ak')
parser.add_argument('--obs_sk')
parser.add_argument('--obs_server')
parser.add_argument('--obs_bucketName')
parser.add_argument('--obs_path_photo_file')
parser.add_argument('--obs_path_json_file')
parser.add_argument('--redirect')
parser.add_argument('--sleep_second_per_page')
parser.add_argument('--overwrite_exist_file')
args = parser.parse_args()

obs_session = yan_obs.create_obs_session(
	obs_ak = args.obs_ak,
	obs_sk = args.obs_sk,
	obs_server = args.obs_server,
	)

def download_image_from_url_and_upload_to_obs(
	photo_url,
	obs_session,
	obs_bucketName,
	obs_path_photo_file,
	obs_path_json_file,
	curl_file = None,
	redirect = None,
	overwrite_exist_file = None):
	###
	url_hash = yan_web_page_download.str_md5(photo_url)
	if overwrite_exist_file is not None:
		###check if already downloaded
		file_exist = yan_obs.obs_file_exist(
			obs_bucketName = obs_bucketName,
			file_name = '%s/%s.json'%(obs_path_json_file, url_hash),
			obs_session = obs_session)
		if file_exist is True:
			print('photo of %s already downloaed.'%(photo_url))
			return 'exist'
	###download the file
	file_name = yan_web_page_download.download_image_from_url(
		photo_url,
		curl_file,
		redirect)
	if file_name is not None:
		print('downloaded %s successfully'%(str(file_name)))
		###upload to obs
		status = yan_obs.upload_file_to_obs(
			obs_bucketName = obs_bucketName,
			local_file = file_name,
			obs_file_name = '%s/%s'%(obs_path_photo_file, file_name),
			obs_session = obs_session)
		os.remove(file_name)
	else:
		print('failed to download photo')
	###upload record to obs
	df = pandas.DataFrame([{
		'photo_url':photo_url,
		'file_name':file_name,
		'crawling_date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
		}])
	print(df)
	df.to_json(
		path_or_buf = '%s.json'%(url_hash),
		orient = 'records',
		lines = True)
	status = yan_obs.upload_file_to_obs(
		obs_bucketName = obs_bucketName,
		local_file = '%s.json'%(url_hash),
		obs_file_name = '%s/%s.json'%(obs_path_json_file, url_hash),
		obs_session = obs_session)
	os.remove('%s.json'%(url_hash))
	return 'success'

def get_html_data(r):
	print('\n\n')
	r['status'] = download_image_from_url_and_upload_to_obs(
	photo_url = r['photo_url'],
	obs_session = obs_session,
	obs_bucketName = args.obs_bucketName,
	obs_path_photo_file = args.obs_path_photo_file,
	obs_path_json_file = args.obs_path_json_file,
	overwrite_exist_file = args.overwrite_exist_file)
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
			print('downloading pages of %s'%(f))
			input_df = pandas.read_json(
			path_or_buf = f,
			orient = 'records',
			lines = True)
			input_df = input_df.apply(get_html_data, axis = 1)
			print('removing %s'%(f))
			os.remove(f)
			print('%s removed'%(f))