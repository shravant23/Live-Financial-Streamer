# basic settings for the whole app

# sec requires a user agent with contact info or they block you
USER_AGENT = "shravan personal project tshravan2006@gmail.com"

# tech stocks we watch, mapped to there SEC CIK numbers
TICKERS = {
    "AAPL": "0000320193",
    "MSFT": "0000789019",
    "GOOGL": "0001652044",
    "AMZN": "0001018724",
    "NVDA": "0001045810",
    "META": "0001326801",
    "TSLA": "0001318605",
}

# edgar endpoint that lists all recent filings for a company
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"

# filing types we actualy care about
FORM_TYPES = ["10-K", "10-Q", "8-K"]

# sec allows 10 req/sec max, we stay a bit under to be safe
RATE_LIMIT = 8  # tokens added per second
BUCKET_SIZE = 8  # max burst size

MAX_RETRIES = 4  # how many times we retry a failed request
POLL_INTERVAL = 60  # seconds between polls in watch mode
MAX_PER_TICKER = 5  # dont download 100s of old filings on first run

# output paths
DATA_DIR = "data"
RAW_DIR = "data/raw"
SEEN_FILE = "data/seen.json"
CSV_FILE = "data/filings.csv"
