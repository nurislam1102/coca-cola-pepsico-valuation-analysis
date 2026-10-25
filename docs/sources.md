# Sources

## SEC filings used (10-K, one per fiscal year)

**Coca-Cola (CIK 21344)**
- FY2021 (period end 2021-12-31), accession 0000021344-22-000009: https://www.sec.gov/Archives/edgar/data/21344/000002134422000009/ko-20211231.htm
- FY2022 (period end 2022-12-31), accession 0000021344-23-000011: https://www.sec.gov/Archives/edgar/data/21344/000002134423000011/ko-20221231.htm
- FY2023 (period end 2023-12-31), accession 0000021344-24-000009: https://www.sec.gov/Archives/edgar/data/21344/000002134424000009/ko-20231231.htm
- FY2024 (period end 2024-12-31), accession 0000021344-25-000011: https://www.sec.gov/Archives/edgar/data/21344/000002134425000011/ko-20241231.htm
- FY2025 (period end 2025-12-31), accession 0001628280-26-010047: https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm

**PepsiCo (CIK 77476)**
- FY2021 (period end 2021-12-25), accession 0000077476-22-000010: https://www.sec.gov/Archives/edgar/data/77476/000007747622000010/pep-20211225.htm
- FY2022 (period end 2022-12-31), accession 0000077476-23-000007: https://www.sec.gov/Archives/edgar/data/77476/000007747623000007/pep-20221231.htm
- FY2023 (period end 2023-12-30), accession 0000077476-24-000008: https://www.sec.gov/Archives/edgar/data/77476/000007747624000008/pep-20231230.htm
- FY2024 (period end 2024-12-28), accession 0000077476-25-000007: https://www.sec.gov/Archives/edgar/data/77476/000007747625000007/pep-20241228.htm
- FY2025 (period end 2025-12-27), accession 0000077476-26-000007: https://www.sec.gov/Archives/edgar/data/77476/000007747626000007/pep-20251227.htm

## Structured data
- SEC XBRL company facts (used to extract figures): https://data.sec.gov/api/xbrl/companyfacts/CIK0000021344.json and https://data.sec.gov/api/xbrl/companyfacts/CIK0000077476.json
- SEC EDGAR filing indexes: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000021344&type=10-K and https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000077476&type=10-K
- FY2021 growth base (FY2020 revenue and net income): FY2020 10-Ks, accessions 0000021344-21-000008 (KO) and 0000077476-21-000007 (PEP), via the company facts above.

## Market prices
- Yahoo Finance chart API (unadjusted daily close): https://query1.finance.yahoo.com/v8/finance/chart/KO and https://query1.finance.yahoo.com/v8/finance/chart/PEP . Human-readable history: https://finance.yahoo.com/quote/KO/history and https://finance.yahoo.com/quote/PEP/history
- Prices used are listed in `evidence/prices_used.csv`. This is a secondary, unaudited source; **spot-check the 10 prices** on a second site (e.g. Nasdaq or the exchange) before publishing.

## Verification evidence
- `evidence/verified_figures.json`: the 50 figure-year pairs matched to the text of the 10-K documents above (FY2025 and FY2023 10-Ks per company, each showing three years).
