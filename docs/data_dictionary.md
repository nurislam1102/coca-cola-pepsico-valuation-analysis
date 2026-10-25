# Data Dictionary: `valuation_gap_tableau.csv`

10 rows (2 companies x 5 fiscal years), 26 fields, UTF-8, comma-separated, one row per Company x Fiscal_Year. Money is USD millions unless noted. Values are as originally reported in each year's own 10-K (earliest-filed value for the period).

| Field | Unit / type | Definition |
|---|---|---|
| `Company` | text | Legal company name |
| `Ticker` | text | KO or PEP |
| `Fiscal_Year` | integer | Fiscal year (calendar year in which the fiscal year ends) |
| `Fiscal_Year_End` | date | Balance-sheet date from the 10-K. KO: Dec 31. PEP: last Saturday of December |
| `Revenue_USD_M` | USD millions | Net operating revenues (KO) / Net revenue (PEP), XBRL tag Revenues |
| `Prior_Year_Revenue_USD_M` | USD millions | Previous fiscal year revenue; used only for growth (FY2021 base comes from the FY2020 10-K XBRL data) |
| `Gross_Profit_USD_M` | USD millions | XBRL GrossProfit |
| `Operating_Income_USD_M` | USD millions | XBRL OperatingIncomeLoss |
| `Net_Income_USD_M` | USD millions | Net income attributable to the company's shareowners (XBRL NetIncomeLoss) |
| `Prior_Year_Net_Income_USD_M` | USD millions | Previous fiscal year net income; used only for growth |
| `Total_Assets_USD_M` | USD millions | Total assets at fiscal year-end (XBRL Assets; not text-matched) |
| `EPS_Diluted_USD` | USD per share | Diluted GAAP EPS (XBRL EarningsPerShareDiluted) |
| `Revenue_Growth_Pct` | percent | (Revenue / Prior_Year_Revenue - 1) x 100 |
| `Net_Income_Growth_Pct` | percent | (Net_Income / Prior_Year_Net_Income - 1) x 100 |
| `Gross_Margin_Pct` | percent | Gross_Profit / Revenue x 100 |
| `Operating_Margin_Pct` | percent | Operating_Income / Revenue x 100 |
| `Net_Margin_Pct` | percent | Net_Income / Revenue x 100 |
| `Revenue_Index_FY2021` | index, FY2021 = 100 | Revenue / that company's FY2021 revenue x 100 (lets two different-sized companies share one axis) |
| `Net_Income_Index_FY2021` | index, FY2021 = 100 | Net income / that company's FY2021 net income x 100 |
| `Valuation_Date` | date | Date of the closing price in the row (last trading day of the calendar year: 2021-12-31, 2022-12-30, 2023-12-29, 2024-12-31, 2025-12-31). Each year has its OWN date and price; nothing is repeated across years |
| `Close_Price_USD` | USD per share | Unadjusted NYSE close on Valuation_Date (Yahoo Finance chart API; secondary source) |
| `PE_Ratio_GAAP` | multiple (x) | Close_Price_USD / EPS_Diluted_USD for that fiscal year |
| `Is_Headline_Valuation_Date` | true/false | True only for the Dec 31, 2025 rows used for the headline P/E chart |
| `Source_Accession` | text | SEC accession number of the 10-K for that fiscal year |
| `Source_URL` | URL | Direct link to that 10-K document on SEC EDGAR |
| `Price_Source` | text | Source and type of the price |

## Key conventions
- **CAGR** is not a row field (it would repeat across years). Formula: (FY2025 / FY2021)^(1/4) - 1, because FY2021 to FY2025 spans 4 intervals. Results are in the Excel `Summary` sheet and `FINDINGS.md`.
- **Fiscal years** differ slightly: KO ends Dec 31; PEP ends on the last Saturday of December (Dec 25, 2021; Dec 31, 2022; Dec 30, 2023; Dec 28, 2024; Dec 27, 2025). Period lengths are not adjusted.
- **P/E** pairs a calendar year-end price with that fiscal year's GAAP diluted EPS; PEP's fiscal year-end can be a few days before the price date.
- **Excluded on purpose:** total debt and EV/EBITDA (no consistent, verifiable definition), non-GAAP/adjusted EPS (not an audited line item), forecasts.
