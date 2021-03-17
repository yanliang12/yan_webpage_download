# yan_webpage_download

```bash
docker build -t yanliang12/yan_webpage_download:1.0.0 .

docker run -it \
--memory="256g" \
-v /Users/yan/Downloads/:/Downloads/ \
yanliang12/yan_webpage_download:1.0.0

docker exec -it 2c4a8a038042 bash
```
