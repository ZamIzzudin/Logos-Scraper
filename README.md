<!-- @format -->

# Scrapper Module

## Run The Project

Create a virtual environtment

```python
  python -m venv venv
```

```python
  venv\Scripts\activate
```

```python
  pip install -r requirements.txt
```

Out from Virtual Environtment

```python
  deactivate
```

### Development

```python
  python app.py
```

## API Reference

#### Basically, this scrapper runs automatically because it uses cron (scheduler).

But,

#### Store Scraping Data [MANUALY]

```http
  GET /manual-scrape/
```

## NOTES

#### 1. Database will using MONGO DB

#### 2. You can setup env variabel by following .example.env format

#### 3. You can setup configuration of scraper like (LPSE Domain, Tender Type, SBU and KBLI code spesification) in [config] folder

#### 4. You can setup data output from scrapper in spider file [/server/utils/scrapper/spider/spider.py] (This is also core function from this module)
