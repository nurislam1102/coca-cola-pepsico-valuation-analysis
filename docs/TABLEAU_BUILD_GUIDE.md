# Tableau Public Build Guide (browser, Mac)

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
- **Check values** (Revenue growth %): KO 17.1 / 11.3 / 6.4 / 2.9 / 1.9  |  PEP 12.9 / 8.7 / 5.9 / 0.4 / 2.3

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
- **Check values** (operating margin %): KO 26.7 / 25.4 / 24.7 / 21.2 / 28.7  |  PEP 14.0 / 13.3 / 13.1 / 14.0 / 12.2
- **Check values** (net margin %): KO 25.3 / 22.2 / 23.4 / 22.6 / 27.3  |  PEP 9.6 / 10.3 / 9.9 / 10.4 / 8.8

## 3. Worksheet C: `C_Revenue_vs_NetIncome`
- **Columns:** `Fiscal_Year`
- **Rows:** `Revenue_Index_FY2021`, then `Net_Income_Index_FY2021` (two stacked panels, same axis range, no dual axis)
- **Marks:** Line with circles | **Color:** `Company`
- **Axes:** Fixed **90 to 140** for both panels
- **Label:** last year (FY2025) only: select the FY2025 marks > right-click > Mark Label > Always Show; Format `0`
- **Title:** "Revenue vs net income, indexed (FY2021 = 100)"
- **Tooltip:** `<Company> FY<Fiscal_Year>`  /  `Revenue index: <SUM(Revenue_Index_FY2021)>`  /  `Net income index: <SUM(Net_Income_Index_FY2021)>`  /  `Revenue $<SUM(Revenue_USD_M)>M, net income $<SUM(Net_Income_USD_M)>M`  /  `Source: <Source_Accession>`
- **Dashboard position:** middle-left
- **Check values** (net income index): KO 100.0 / 97.7 / 109.7 / 108.8 / 134.1  |  PEP 100.0 / 117.0 / 119.1 / 125.7 / 108.2

## 4. Worksheet D: `D_Valuation_PE`
- **Columns:** `Company`
- **Rows:** `PE_Ratio_GAAP` (SUM)
- **Marks:** Bar | **Color:** `Company` | **Label:** `PE_Ratio_GAAP`, Format `0.0"x"`
- **Filters:** drag `Fiscal_Year` to Filters > select only **2025** (this is the headline valuation date, Dec 31, 2025). Do NOT show this filter.
- **Title:** "GAAP P/E on Dec 31, 2025 (closing price / FY2025 diluted EPS)"
- **Tooltip:** `<Company>`  /  `P/E: <SUM(PE_Ratio_GAAP)>x`  /  `Close on <Valuation_Date>: $<SUM(Close_Price_USD)>`  /  `FY2025 diluted EPS: $<SUM(EPS_Diluted_USD)>`  /  `Prices: Yahoo Finance; EPS: SEC 10-K <Source_Accession>` (put `Valuation_Date`, `Close_Price_USD`, `EPS_Diluted_USD`, `Source_Accession` on Detail)
- **Dashboard position:** middle-right
- **Check values:** KO 23.0x, PEP 23.9x
- **Optional 5th chart `D2_PE_Trend`:** Columns `Fiscal_Year`, Rows `PE_Ratio_GAAP`, Marks Line, Color `Company`, no year filter; title "GAAP P/E at each calendar year-end close". Check values: KO 26.3 / 29.0 / 23.9 / 25.3 / 23.0  |  PEP 31.6 / 28.1 / 25.9 / 21.9 / 23.9

## 5. Takeaways panel (E): use Text objects on the dashboard (no worksheet needed)
Paste these three paragraphs (already verified against the data):
1. Margins, not growth, separate the two businesses. Coca-Cola's 5-yr average operating margin is 25.3% vs PepsiCo's 13.3%, while revenue CAGR differs by only 1.3 pp (5.5% vs 4.3%).
2. Revenue growth did not reliably become profit growth. Revenue and net income rose together in 3 of 5 years (KO) and 4 of 5 (PEP).
3. The valuation gap is small and unstable. On Dec 31, 2025 GAAP P/E was 23.9x (PEP) vs 23.0x (KO), and the gap changed sign across year-ends. One snapshot; GAAP EPS only; not investment advice.

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
