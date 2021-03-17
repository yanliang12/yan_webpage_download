############yan_obs.py############
'''
https://support.huaweicloud.com/intl/en-us/sdk-python-devg-obs/obs_22_0904.html
https://support.huaweicloud.com/sdk-python-devg-obs/obs_22_0500.html
'''

from obs import ObsClient

def create_obs_session(
	obs_ak,
	obs_sk,
	obs_server):
	try:
		obs_session = ObsClient(
		access_key_id = obs_ak,
		secret_access_key = obs_sk,
		server = obs_server
		)
		return obs_session
	except:
		return None

def obs_file_exist(
	obs_bucketName,
	file_name,
	obs_session):
	status = obs_session.getObject(
		bucketName = obs_bucketName, 
		objectKey = file_name)
	if status['reason'] in ('OK'):
		return True
	else:
		return False

def upload_file_to_obs(
	obs_bucketName,
	local_file,
	obs_file_name,
	obs_session):
	try:
		obs_session.putFile(
		bucketName = obs_bucketName, 
		objectKey = obs_file_name, 
		file_path = local_file)
		return True
	except:
		return False
############yan_obs.py############