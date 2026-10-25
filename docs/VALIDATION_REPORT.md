# Validation Report

| Item | Count / result |
|---|---|
| Companies | 2 (KO, PEP) |
| Reporting years | 5 (FY2021-FY2025) + FY2020 used only as a growth base |
| Financial observations (company-year rows in the CSV) | 10 |
| Fields in CSV | 26 |
| Reported inputs keyed per row | 6 (revenue, gross profit, operating income, net income, total assets, diluted EPS) = **60** reported figures, plus 4 prior-year base figures and 10 prices |
| **Independently verified figures** | **50** (revenue, gross profit, operating income, net income, diluted EPS x 5 years x 2 companies), matched to the text of the FY2025 and FY2023 10-K documents. Not text-matched: 10 total-assets values, 4 FY2020 base values, 10 Yahoo prices |
| Financial KPIs calculated | 7: revenue growth, net income growth, gross margin, operating margin, net margin, revenue CAGR, P/E |
| Other derived fields | Revenue and net income indices (FY2021 = 100) |
| Planned Tableau views | 4 chart worksheets (A to D) + optional D2 + a text takeaways panel. **None built yet** |
| Workbook vs CSV check | Max absolute difference 0.00005 (CSV rounding to 4 decimals); no formula errors after recalculation |

## How the numbers were checked
1. Extracted each figure from SEC XBRL company facts (earliest-filed 10-K value per period).
2. Searched the primary 10-K HTML documents for the exact three-year sequence of each metric as printed in the income statement; every one of the 50 matched.
3. Recomputed growth, margins, CAGR (4 intervals), P/E in Excel with live formulas; compared with the CSV (`Checks` sheet).

## Headline results with sources
- Revenue CAGR FY21-25: KO 5.53%, PEP 4.27%. Sources: `docs/sources.md`, 10-Ks FY2021 (0000021344-22-000009; 0000077476-22-000010) and FY2025 (0001628280-26-010047; 0000077476-26-000007).
- Avg operating margin: KO 25.3%, PEP 13.3% (5 annual 10-Ks each).
- P/E on 2025-12-31: KO 23.0x, PEP 23.9x (FY2025 10-K EPS $3.04 / $6.00; closes $69.91 / $143.52).

## Honest limits
- Prices come from one secondary source; verify them before publishing.
- Total assets and FY2020 base figures are XBRL-only.
- Debt, EV/EBITDA, adjusted EPS and forecasts are deliberately excluded.
