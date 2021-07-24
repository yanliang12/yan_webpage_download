# yan_webpage_download

```bash
docker pull yanliang12/yan_webpage_download:1.0.5
```


download webpages of urls of a json file and upload it to cloud

```bash
python3 \
yan_web_page_batch_download.py \
--input_json [input_json_file] \
--curl_file [curl_file] \
--obs_ak [ak of cloud] \
--obs_sk [sk of cloud] \
--obs_server [cloud server url] \
--obs_bucketName [cloud bucket] \
--obs_path [folder name to upload] \
--page_regex "DOCTYPE html.*?html lang.*?class.*?theme"
```
