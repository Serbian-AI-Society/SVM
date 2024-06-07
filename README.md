# SVM Team

## Prerequisites
- Docker
- Docker Compose
- Python 3.8 or higher

## Setup
```
pip install pre-commit
pre-commit install
```
```
docker compose -f docker-compose.yml up --build
```

## Scraping
Scraping is done on Google Maps API, it requires their API KEY.
```
export GMAP_API_KEY=<YOUR API KEY>
python3 scraper/main.py
```

## Usage
- Open your browser and go to `http://localhost:8501/`