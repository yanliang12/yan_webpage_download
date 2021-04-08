# yan_webpage_download

```bash
docker build -t yanliang12/yan_webpage_download:1.0.0 .

docker run -it \
--memory="256g" \
-v /Users/yan/Downloads/:/Downloads/ \
yanliang12/yan_webpage_download:1.0.0

docker exec -it 2c4a8a038042 bash

python3 \
yan_web_page_batch_download.py \
--input_json input_path \
--curl_file curl_info.sh \
--obs_ak xxxxxxxxxxxxx \
--obs_sk xxxxxxxxxxxx \
--obs_server https://obs.xxxxxxx.com \
--obs_bucketName xxxxxxxxxx \
--obs_path xxxxxxxx/xxxxxxxxx \
--page_regex "DOCTYPE html.*?html lang.*?class.*?theme"
```
