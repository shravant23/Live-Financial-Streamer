import asyncio

from . import config, dedup, extractor, writer


async def download_filing(fetcher, filing):
    # grab the actual document and remember were it landed
    data = await fetcher.get(filing.url)
    if data:
        filing.local_path = writer.save_raw(filing, data)
    return filing


async def process_ticker(fetcher, ticker, seen):
    # one full pass for a single ticker
    cik = config.TICKERS[ticker]
    url = config.SUBMISSIONS_URL.format(cik=cik)
    data = await fetcher.get_json(url)
    if data is None:
        return []

    filings = extractor.extract_filings(ticker, cik, data)
    new = [f for f in filings if f.accession not in seen]
    if not new:
        print(f"{ticker}: nothing new")
        return []

    # cap it so the first run doesnt pull down hundreds of old files
    new = new[:config.MAX_PER_TICKER]
    print(f"{ticker}: {len(new)} new filings, downloading...")

    # download all the documents at the same time
    done = await asyncio.gather(*[download_filing(fetcher, f) for f in new])
    for f in done:
        seen.add(f.accession)
    return list(done)


async def run_once(fetcher, tickers, seen):
    # poll every ticker concurrently
    results = await asyncio.gather(*[process_ticker(fetcher, t, seen) for t in tickers])
    all_new = [f for group in results for f in group]  # flatten
    if all_new:
        writer.append_rows(all_new)
        dedup.save_seen(seen)
    return all_new
