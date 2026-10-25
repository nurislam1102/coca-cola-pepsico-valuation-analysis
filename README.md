# The Valuation Gap: Coca-Cola vs. PepsiCo
*A Financial Performance & Relative Valuation Study*

**Research question:** Why do investors value two competing companies differently, and to what extent can financial performance, profitability and growth explain that difference?

## Status
- Dataset, Excel analysis, documentation: **complete and verified**.
- Tableau Public dashboard: **to be built by the owner** with `docs/TABLEAU_BUILD_GUIDE.md` (not built or published by the author of this package). Add the public link here once published: [[`TABLEAU_LINK_HERE`](https://public.tableau.com/authoring/TheValuationGapCoca-ColavsPepsiCo/Dashboard1#1)](https://public.tableau.com/views/TheValuationGapCoca-ColavsPepsiCo/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link).

## Key results (FY2021-FY2025; valuation date Dec 31, 2025)
| | Coca-Cola | PepsiCo |
|---|---|---|
| Revenue CAGR (4 intervals) | 5.53% | 4.27% |
| Avg operating margin | 25.3% | 13.3% |
| Avg net margin | 24.2% | 9.8% |
| Years revenue AND net income rose (of 5) | 3 | 4 |
| GAAP P/E, 2025-12-31 | 23.0x | 23.9x |

See `docs/FINDINGS.md` for the six research answers and cautions.

## Contents
- `data/valuation_gap_tableau.csv`: Tableau data source (10 rows, 26 fields)
- `excel/valuation_gap_financials.xlsx`: inputs with sources, live formulas, summary, verification, checks, limitations
- `docs/`: data dictionary, sources, Tableau build guide, findings, resume bullets, interview prep, validation report
- `scripts/`: Python used to extract, verify and build (needs network access to SEC; the SEC asks for a contact User-Agent)
- `evidence/`: verified-figure list and prices used

## Method
Financials from SEC 10-K filings (XBRL company facts, matched to filing text). P/E = Dec 31 close / that fiscal year's diluted GAAP EPS. CAGR = (end/start)^(1/4) - 1.

## Limitations
Different business mixes (PepsiCo includes snacks) and fiscal calendars; GAAP EPS includes one-off items; single price source and date; no EV/EBITDA or adjusted metrics. Descriptive analysis only.

## Disclosure
Student portfolio project using public data. Not investment advice. Not affiliated with or endorsed by The Coca-Cola Company or PepsiCo, Inc. Prepared with AI assistance (data extraction, calculations and documentation); the owner should review all figures before publication.
