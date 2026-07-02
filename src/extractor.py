from . import config
from .schema import Filing


def extract_filings(ticker, cik, data):
    # edgar gives each field as a seperate list, zip them back into rows
    recent = data["filings"]["recent"]
    forms = recent["form"]
    accessions = recent["accessionNumber"]
    dates = recent["filingDate"]
    docs = recent["primaryDocument"]

    out = []
    for form, acc, date, doc in zip(forms, accessions, dates, docs):
        if form not in config.FORM_TYPES:
            continue  # skip forms we dont care about
        if not doc:
            continue  # some old filings have no primary document
        # accession number has dashes in the list but not in the url
        acc_clean = acc.replace("-", "")
        url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_clean}/{doc}"
        out.append(Filing(
            ticker=ticker,
            cik=cik,
            form_type=form,
            accession=acc,
            filed_date=date,
            primary_doc=doc,
            url=url,
        ))
    return out
