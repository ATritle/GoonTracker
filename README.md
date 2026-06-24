\# GoonTracker



Escape From Tarkov Goons tracker aggregator.



\## Features



\- Aggregates multiple Goons trackers

\- Calculates consensus location

\- Stores historical sightings in SQLite

\- FastAPI backend

\- Automatic polling



\## Installation



Create and activate a virtual environment:



```bash

python -m venv venv

venv\\Scripts\\Activate.ps1

```



Install dependencies:



```bash

pip install -r requirements.txt

```



\## Run Poller



```bash

python poller.py

```



\## Run API



```bash

uvicorn api:app --reload

```



\## API Endpoints



\### Current Consensus



```text

/consensus

```



\### Recent Sightings



```text

/current

```



\### Statistics



```text

/stats

```



\## Data Sources



\- Tarkov Goon Tracker

\- TarkovBOT Goons Tracker



\## Tech Stack



\- Python

\- SQLite

\- FastAPI

\- Playwright

\- BeautifulSoup

