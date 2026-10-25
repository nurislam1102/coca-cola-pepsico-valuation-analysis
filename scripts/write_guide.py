import json,pathlib
C=pathlib.Path("/tmp/claude-0/vg"); O=pathlib.Path("/tmp/claude-0/ValuationGap"); D=O/"docs"
R=json.load(open(C/"rows.json")); X=json.load(open(C/"stats.json")); S=X["S"]; K,P=S["KO"],S["PEP"]
ko=[r for r in R if r["Ticker"]=="KO"]; pe=[r for r in R if r["Ticker"]=="PEP"]
def line(L,c,fmt): return " / ".join(fmt.format(r[c]) for r in L)
def exp(c,fmt="{:.1f}"): return f"KO {line(ko,c,fmt)}  |  PEP {line(pe,c,fmt)}"
T1=f"Margins, not growth, separate the two businesses. Coca-Cola's 5-yr average operating margin is {K['om']:.1f}% vs PepsiCo's {P['om']:.1f}%, while revenue CAGR differs by only {K['rev_cagr']-P['rev_cagr']:.1f} pp ({K['rev_cagr']:.1f}% vs {P['rev_cagr']:.1f}%)."
T2=f"Revenue growth did not reliably become profit growth. Revenue and net income rose together in {K['both']} of 5 years (KO) and {P['both']} of 5 (PEP)."
T3=f"The valuation gap is small and unstable. On Dec 31, 2025 GAAP P/E was {P['pe25']:.1f}x (PEP) vs {K['pe25']:.1f}x (KO), and the gap changed sign across year-ends. One snapshot; GAAP EPS only; not investment advice."
G=f"""# Tableau Public Build Guide (browser, Mac)

**Status:** the dashboard is NOT built or published. No Tableau tool was available in this session, and publishing needs your Tableau Public sign-in, which must be done by you. Everything else is ready.

Time needed: about 60-90 minutes. No code. You will use ONE file: `data/valuation_gap_tableau.csv` (10 rows).

## 0. Open Tableau Public web authoring
1. Go to https://public.tableau.com and sign in (create a free account if needed).
2. Click **Create** (top right) then **Web Authoring**. If asked to connect: choose **Upload from computer** and select `valuation_gap_tableau.csv`.
3. On the Data Source page, click the small data-type icon above **Fiscal_Year** and change it to **String** (this makes years behave as labels, not sums). Confirm **Valuation_Date** is a Date. Then click the **Sheet 1** tab at the bottom.

Colour choices used everywhere: **Coca-Cola = dark red**, **PepsiCo = navy** (pick the closest swatches in the colour menu; exact hex is optional: KO #A6192E, PEP #1F3864). Font: Tableau default is fine. Rename each sheet by double-clicking its tab.

## 1. Worksheet A: `A_Revenue_Growth`
- **Columns:** `Fiscal_Year` then `Company` (drag both; they nest)
- **Rows:** `Revenue_Growth_Pct` (SUM)
- **Marks:** Bar
- **Color:** `Company` | **Label:** `Revenue_Growth_Pct` (Marks card > Label > Show; Format > Number > Custom `0.0"%"`)
- **Filters:** none needed; add `Company` and `Fiscal_Year` to Filters and **Show Filter** for the dashboard
- **Sort:** Fiscal_Year ascending (default)
- **Axis title:** "YoY revenue growth (%)" | **Title:** "Revenue growth, year over year (FY2021-FY2025)"
- **Tooltip** (Marks > Tooltip), drag `Revenue_USD_M`, `Prior_Year_Revenue_USD_M`, `Source_Accession` to **Detail** first, then use:
  `<Company> FY<Fiscal_Year>`  /  `Revenue growth: <SUM(Revenue_Growth_Pct)>%`  /  `Revenue: $<SUM(Revenue_USD_M)>M vs $<SUM(Prior_Year_Revenue_USD_M)>M prior year`  /  `Source: SEC 10-K <Source_Accession>`
- **Dashboard position:** top-left
- **Check values** ({'Revenue growth %'}): {exp('Revenue_Growth_Pct')}

## 2. Worksheet B: `B_Profitability`
- **Columns:** `Fiscal_Year`
- **Rows:** `Operating_Margin_Pct`, then `Net_Margin_Pct` (drag both to Rows: two stacked panels; this is NOT a dual axis)
- **Marks:** Line (turn on circles: Marks card > Mark type Line, then Path/Shape circle if available) for both panels
- **Color:** `Company` | **Label:** each point or the last year only; Format `0.0"%"`
- **Axes:** right-click each axis > Edit Axis > Fixed **0 to 35** so both panels are comparable
- **Sort:** Fiscal_Year ascending
- **Title:** "Profitability: operating and net margin (% of revenue)"
- **Tooltip:** `<Company> FY<Fiscal_Year>`  /  `Operating margin: <SUM(Operating_Margin_Pct)>%`  /  `Net margin: <SUM(Net_Margin_Pct)>%`  /  `Source: SEC 10-K <Source_Accession>` (put `Source_Accession` on Detail)
- **Dashboard position:** top-right
- **Check values** (operating margin %): {exp('Operating_Margin_Pct')}
- **Check values** (net margin %): {exp('Net_Margin_Pct')}

## 3. Worksheet C: `C_Revenue_vs_NetIncome`
- **Columns:** `Fiscal_Year`
- **Rows:** `Revenue_Index_FY2021`, then `Net_Income_Index_FY2021` (two stacked panels, same axis range, no dual axis)
- **Marks:** Line with circles | **Color:** `Company`
- **Axes:** Fixed **90 to 140** for both panels
- **Label:** last year (FY2025) only: select the FY2025 marks > right-click > Mark Label > Always Show; Format `0`
- **Title:** "Revenue vs net income, indexed (FY2021 = 100)"
- **Tooltip:** `<Company> FY<Fiscal_Year>`  /  `Revenue index: <SUM(Revenue_Index_FY2021)>`  /  `Net income index: <SUM(Net_Income_Index_FY2021)>`  /  `Revenue $<SUM(Revenue_USD_M)>M, net income $<SUM(Net_Income_USD_M)>M`  /  `Source: <Source_Accession>`
- **Dashboard position:** middle-left
- **Check values** (net income index): {exp('Net_Income_Index_FY2021')}

## 4. Worksheet D: `D_Valuation_PE`
- **Columns:** `Company`
- **Rows:** `PE_Ratio_GAAP` (SUM)
- **Marks:** Bar | **Color:** `Company` | **Label:** `PE_Ratio_GAAP`, Format `0.0"x"`
- **Filters:** drag `Fiscal_Year` to Filters > select only **2025** (this is the headline valuation date, Dec 31, 2025). Do NOT show this filter.
- **Title:** "GAAP P/E on Dec 31, 2025 (closing price / FY2025 diluted EPS)"
- **Tooltip:** `<Company>`  /  `P/E: <SUM(PE_Ratio_GAAP)>x`  /  `Close on <Valuation_Date>: $<SUM(Close_Price_USD)>`  /  `FY2025 diluted EPS: $<SUM(EPS_Diluted_USD)>`  /  `Prices: Yahoo Finance; EPS: SEC 10-K <Source_Accession>` (put `Valuation_Date`, `Close_Price_USD`, `EPS_Diluted_USD`, `Source_Accession` on Detail)
- **Dashboard position:** middle-right
- **Check values:** KO {ko[-1]['PE_Ratio_GAAP']:.1f}x, PEP {pe[-1]['PE_Ratio_GAAP']:.1f}x
- **Optional 5th chart `D2_PE_Trend`:** Columns `Fiscal_Year`, Rows `PE_Ratio_GAAP`, Marks Line, Color `Company`, no year filter; title "GAAP P/E at each calendar year-end close". Check values: {exp('PE_Ratio_GAAP')}

## 5. Takeaways panel (E): use Text objects on the dashboard (no worksheet needed)
Paste these three paragraphs (already verified against the data):
1. {T1}
2. {T2}
3. {T3}

## 6. Assemble the dashboard `THE VALUATION GAP`
1. Click **New Dashboard** (icon next to the sheet tabs). Size: **Fixed size, 1200 x 1600** (or Automatic for a flexible layout).
2. Drag a **Text** object to the top. Write line 1 in bold 24 pt: `THE VALUATION GAP`; line 2 in 12 pt grey: `Coca-Cola vs. PepsiCo | Performance, Profitability & Market Valuation`.
3. Under it, drag **Horizontal** containers to make two rows. Drop A (left) + B (right) in row 1, C (left) + D (right) in row 2. Set both rows to about 380 px high.
4. Add **E**: drag a **Text** object below the charts (full width) and paste the three takeaways.
5. Footer **Text** object (10 pt grey): `Data as of: FY2025 10-Ks (filed Feb 2026); prices = closes on Dec 31, 2025. Source: SEC EDGAR, Yahoo Finance. Method: P/E = close / FY diluted GAAP EPS; CAGR over 4 intervals. Different business mixes and fiscal calendars limit comparability. Student project; not investment advice; not affiliated with either company.`
6. **Filters:** click chart A > the small arrow on its `Company` filter card > Apply to Worksheets > **All Using This Data Source**, then do the same for `Fiscal_Year` (leave D's year fixed to 2025; if D changes when you use the year filter, instead apply the year filter to A, B and C only via "Selected Worksheets"). Place the filter cards in a thin row under the title.
7. Remove duplicate legends: keep one Company colour legend (top right). Use **Float** only if needed.
8. Check each chart against the "Check values" above.

## 7. Publish (the one manual step)
1. Click **Publish** (top right) or File > Save to Tableau Public As...
2. Name: `The Valuation Gap: Coca-Cola vs PepsiCo`. Allow the default (public).
3. Open the public link in a private browser window and confirm all four charts load. Copy the URL for LinkedIn and your resume.

## Tips
- If a field you need is under Measures instead of Dimensions, drag it over; if `Fiscal_Year` shows `SUM(...)`, go back to the data source page and set it to String.
- Do not edit the CSV after you start; if you must, re-upload and re-check.
"""
(D/"TABLEAU_BUILD_GUIDE.md").write_text(G)
V=f"""# Validation Report

| Item | Count / result |
|---|---|
| Companies | 2 (KO, PEP) |
| Reporting years | 5 (FY2021-FY2025) + FY2020 used only as a growth base |
| Financial observations (company-year rows in the CSV) | 10 |
| Fields in CSV | 26 |
| Reported inputs keyed per row | 6 (revenue, gross profit, operating income, net income, total assets, diluted EPS) = **60** reported figures, plus 4 prior-year base figures and 10 prices |
| **Independently verified figures** | **{X['nverified']}** (revenue, gross profit, operating income, net income, diluted EPS x 5 years x 2 companies), matched to the text of the FY2025 and FY2023 10-K documents. Not text-matched: 10 total-assets values, 4 FY2020 base values, 10 Yahoo prices |
| Financial KPIs calculated | 7: revenue growth, net income growth, gross margin, operating margin, net margin, revenue CAGR, P/E |
| Other derived fields | Revenue and net income indices (FY2021 = 100) |
| Planned Tableau views | 4 chart worksheets (A to D) + optional D2 + a text takeaways panel. **None built yet** |
| Workbook vs CSV check | Max absolute difference 0.00005 (CSV rounding to 4 decimals); no formula errors after recalculation |

## How the numbers were checked
1. Extracted each figure from SEC XBRL company facts (earliest-filed 10-K value per period).
2. Searched the primary 10-K HTML documents for the exact three-year sequence of each metric as printed in the income statement; every one of the 50 matched.
3. Recomputed growth, margins, CAGR (4 intervals), P/E in Excel with live formulas; compared with the CSV (`Checks` sheet).

## Headline results with sources
- Revenue CAGR FY21-25: KO {K['rev_cagr']:.2f}%, PEP {P['rev_cagr']:.2f}%. Sources: `docs/sources.md`, 10-Ks FY2021 (0000021344-22-000009; 0000077476-22-000010) and FY2025 (0001628280-26-010047; 0000077476-26-000007).
- Avg operating margin: KO {K['om']:.1f}%, PEP {P['om']:.1f}% (5 annual 10-Ks each).
- P/E on 2025-12-31: KO {K['pe25']:.1f}x, PEP {P['pe25']:.1f}x (FY2025 10-K EPS $3.04 / $6.00; closes ${ko[-1]['Close_Price_USD']:.2f} / ${pe[-1]['Close_Price_USD']:.2f}).

## Honest limits
- Prices come from one secondary source; verify them before publishing.
- Total assets and FY2020 base figures are XBRL-only.
- Debt, EV/EBITDA, adjusted EPS and forecasts are deliberately excluded.
"""
(D/"VALIDATION_REPORT.md").write_text(V)
RM=f"""# The Valuation Gap: Coca-Cola vs. PepsiCo
*A Financial Performance & Relative Valuation Study*

**Research question:** Why do investors value two competing companies differently, and to what extent can financial performance, profitability and growth explain that difference?

## Status
- Dataset, Excel analysis, documentation: **complete and verified**.
- Tableau Public dashboard: **to be built by the owner** with `docs/TABLEAU_BUILD_GUIDE.md` (not built or published by the author of this package). Add the public link here once published: `TABLEAU_LINK_HERE`.

## Key results (FY2021-FY2025; valuation date Dec 31, 2025)
| | Coca-Cola | PepsiCo |
|---|---|---|
| Revenue CAGR (4 intervals) | {K['rev_cagr']:.2f}% | {P['rev_cagr']:.2f}% |
| Avg operating margin | {K['om']:.1f}% | {P['om']:.1f}% |
| Avg net margin | {K['nm']:.1f}% | {P['nm']:.1f}% |
| Years revenue AND net income rose (of 5) | {K['both']} | {P['both']} |
| GAAP P/E, 2025-12-31 | {K['pe25']:.1f}x | {P['pe25']:.1f}x |

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
"""
(O/"README.md").write_text(RM)
print("ok")
