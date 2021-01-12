# Tile Fetcher

## Code

### Install the dependencies

```bash
python -m pip install -r requirements.txt 
```

### Download only one image

```bash
python tile_fetcher.py --zoom 2 "https://artsandculture.google.com/asset/christ-before-the-high-priest-gerrit-van-honthorst/6wFp0Y3GxWhwQg"

```

### Download all the images

```bash
python caravaggism.py
```

## Issues

* [urllib.error.HTTPError: HTTP Error 429: Too Many Requests](https://stackoverflow.com/questions/22786068/how-to-avoid-http-error-429-too-many-requests-python)

## References
* https://github.com/gap-decoder/gapdecoder