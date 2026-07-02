from pydantic import BaseModel


class Filing(BaseModel):
    # one clean row in our final table, pydantic makes sure types are right
    ticker: str
    cik: str
    form_type: str  # 10-K, 10-Q, 8-K etc
    accession: str  # unique id the sec gives every filing
    filed_date: str
    primary_doc: str  # filename of the main document
    url: str  # were to download it from
    local_path: str = ""  # were we saved it on disk, filled in later
