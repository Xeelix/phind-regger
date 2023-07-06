## Description

Simple automated registration at phind.com
with [cloudflare bypass](https://github.com/ultrafunkamsterdam/undetected-chromedriver/tree/master) using python
selenium.

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Build

```bash
pyinstaller --onefile --add-data="deepl.zip:." main.py --name phind
```

## Requirements

Chrome browser