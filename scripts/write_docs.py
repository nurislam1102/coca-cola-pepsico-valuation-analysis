import json,pathlib,csv,shutil
C=pathlib.Path("/tmp/claude-0/vg"); O=pathlib.Path("/tmp/claude-0/ValuationGap"); D=O/"docs"
R=json.load(open(C/"rows.json")); X=json.load(open(C/"stats.json")); S=X["S"]; K,P=S["KO"],S["PEP"]
ko=[r for r in R if r["Ticker"]=="KO"]; pe=[r for r in R if r["Ticker"]=="PEP"]
hdr=list(csv.reader(open(O/"data/valuation_gap_tableau.csv")))[0]
f1=lambda v:f"{v:.1f}"
ratio=P["rev25"]/K["rev25"]
def tab(L,col,fmt="{:.1f}"): return " | ".join(fmt.format(r[col]) for r in L)
exp=lambda col,fmt="{:.1f}": f"KO: {tab(ko,col,fmt)}  /  PEP: {tab(pe,col,fmt)}"
gap=X["pe_gap"]
# ---- findings
FIND=f"""# Analytical Findings: The Valuation Gap (KO vs PEP)

Data: SEC 10-K filings FY2021-FY2025; prices = closing prices on **2025-12-31**. Student project, public data, not investment advice.

## Answers to the six research questions
1. **Faster revenue growth (FY2021 to FY2025, 4 intervals):** Coca-Cola. Revenue CAGR **{K['rev_cagr']:.2f}%** vs PepsiCo **{P['rev_cagr']:.2f}%** (gap {K['rev_cagr']-P['rev_cagr']:.2f} percentage points). PepsiCo is the larger company: FY2025 revenue ${P['rev25']/1000:.1f}B vs ${K['rev25']/1000:.1f}B ({ratio:.2f}x). Both grew revenue in every year; growth slowed for both (KO {ko[0]['Revenue_Growth_Pct']:.1f}% in FY2021 to {ko[-1]['Revenue_Growth_Pct']:.1f}% in FY2025; PEP {pe[0]['Revenue_Growth_Pct']:.1f}% to {pe[-1]['Revenue_Growth_Pct']:.1f}%).
2. **Stronger margins:** Coca-Cola, clearly. Five-year average operating margin **{K['om']:.1f}%** vs **{P['om']:.1f}%** (+{K['om']-P['om']:.1f} pp); average net margin **{K['nm']:.1f}%** vs **{P['nm']:.1f}%** (+{K['nm']-P['nm']:.1f} pp). FY2025: operating margin {K['om25']:.1f}% vs {P['om25']:.1f}%; net margin {K['nm25']:.1f}% vs {P['nm25']:.1f}%.
3. **Did revenue growth consistently become earnings growth?** No. Revenue rose in all 5 years for both, but net income rose in the same year in only **{K['both']} of 5** years for KO and **{P['both']} of 5** for PEP. KO net income fell in FY2022 ({ko[1]['Net_Income_Growth_Pct']:.1f}%) and FY2024 ({ko[3]['Net_Income_Growth_Pct']:.1f}%); PEP's fell in FY2025 ({pe[-1]['Net_Income_Growth_Pct']:.1f}%).
4. **Higher valuation multiple on the selected date (2025-12-31):** PepsiCo, narrowly. GAAP P/E **{P['pe25']:.1f}x** vs Coca-Cola **{K['pe25']:.1f}x**: a {P['pe25']-K['pe25']:.1f}x gap, PEP at a {X['pe_pct']:.1f}% premium.
5. **What could help explain a valuation gap:** the data show Coca-Cola with much higher margins and faster revenue growth but a P/E that is *not* higher than PepsiCo's on this date, and the sign of the P/E gap flipped across year-ends ({', '.join(f'{y}: {g:+.1f}x' for y,g in gap)} for PEP minus KO). So in this sample, margins and growth alone do **not** line up with the P/E ranking. Possible, untested interpretations: PEP's depressed FY2025 GAAP EPS inflating its P/E; differing expectations about future earnings; business mix; dividend/balance-sheet differences.
6. **What cannot be concluded:** why investors paid these prices; whether either stock was over- or under-valued; anything about future returns. P/E uses GAAP EPS that includes one-off items (e.g. KO 'Other operating charges' of $1,261M/FY2025 and $4,163M/FY2024 per its 10-K). EV/EBITDA and debt-based metrics were excluded (see Limitations). One valuation date is a single snapshot.

## Three dashboard takeaways (observation, then interpretation)
1. **Margins, not growth, separate the two businesses.** Observation: KO's average operating margin is {K['om']:.1f}% vs PEP's {P['om']:.1f}%, while revenue CAGR differs by only {K['rev_cagr']-P['rev_cagr']:.1f} pp. Interpretation (untested): different business mixes (beverage concentrate vs beverages plus snacks).
2. **Revenue growth did not reliably turn into profit growth.** Observation: net income and revenue rose together in {K['both']}/5 (KO) and {P['both']}/5 (PEP) years; FY2021-FY2025 net income CAGR {K['ni_cagr']:.1f}% (KO) vs {P['ni_cagr']:.1f}% (PEP).
3. **The 'valuation gap' is small and unstable at this date.** Observation: on 2025-12-31 PEP's GAAP P/E was {P['pe25']:.1f}x vs KO's {K['pe25']:.1f}x ({X['pe_pct']:.1f}% premium), and the gap changed sign across the five year-ends. Caution: one snapshot, GAAP EPS only.

## Important percentage differences
| Measure | KO | PEP | Difference |
|---|---|---|---|
| Revenue CAGR FY21-25 | {K['rev_cagr']:.2f}% | {P['rev_cagr']:.2f}% | {K['rev_cagr']-P['rev_cagr']:+.2f} pp (KO) |
| Net income CAGR FY21-25 | {K['ni_cagr']:.2f}% | {P['ni_cagr']:.2f}% | {K['ni_cagr']-P['ni_cagr']:+.2f} pp (KO) |
| Avg operating margin | {K['om']:.1f}% | {P['om']:.1f}% | {K['om']-P['om']:+.1f} pp (KO) |
| Avg net margin | {K['nm']:.1f}% | {P['nm']:.1f}% | {K['nm']-P['nm']:+.1f} pp (KO) |
| GAAP P/E 2025-12-31 | {K['pe25']:.1f}x | {P['pe25']:.1f}x | PEP {P['pe25']-K['pe25']:+.1f}x ({X['pe_pct']:+.1f}%) |
"""
(D/"FINDINGS.md").write_text(FIND)
# ---- resume bullets
RB=f"""# Resume Bullet Candidates (all numbers verified in this project)

Use only after you have checked each number against `data/valuation_gap_tableau.csv`. Bullets 1-3 describe work that is **complete**. Bullet 4 describes the Tableau dashboard and is only valid **after you publish it**.

1. Analyzed five fiscal years (FY2021-FY2025) of SEC 10-K data for Coca-Cola and PepsiCo, finding Coca-Cola's average operating margin of {K['om']:.1f}% vs {P['om']:.1f}% and revenue CAGR of {K['rev_cagr']:.1f}% vs {P['rev_cagr']:.1f}%, to assess how profitability and growth relate to relative valuation.
2. Built and reconciled a Tableau-ready dataset (10 company-year records, 26 fields), matching 50 reported income-statement figures to the filed 10-Ks and documenting formulas, accession numbers and comparability limits for FP&A-style review.
3. Compared GAAP P/E at a dated valuation point (Dec 31, 2025: PepsiCo {P['pe25']:.1f}x vs Coca-Cola {K['pe25']:.1f}x) with five-year margin and earnings trends, showing revenue and net income rose together in only {K['both']} of 5 years (KO) and {P['both']} of 5 (PEP), to separate operating performance from market valuation.
4. *(Only after publishing)* Designed a Tableau Public dashboard with 4 chart views and a findings panel comparing growth, margins, earnings trends and P/E for two peer companies, giving recruiters a source-linked view of an equity-research question.

Do not add: investment returns, forecast accuracy, user counts, time saved, or business impact. None were measured.
"""
(D/"RESUME_BULLETS.md").write_text(RB)
# ---- interview
IP=f"""# Interview Preparation Notes

## 30-second explanation
"I compared Coca-Cola and PepsiCo using five years of their SEC annual reports. Coca-Cola grew revenue a bit faster ({K['rev_cagr']:.1f}% vs {P['rev_cagr']:.1f}% a year) and keeps much more profit from each sales dollar (about {K['om']:.0f}% operating margin vs {P['om']:.0f}%). But on Dec 31, 2025 their P/E ratios were close, {K['pe25']:.1f}x vs {P['pe25']:.1f}x, so strong financials did not simply mean a higher multiple. I built the dataset and a Tableau dashboard to show this, and I am careful to say what the data cannot prove."

## 90-second explanation
"My question was: why do investors value two competing companies differently, and how much can financial performance explain? I collected five fiscal years for Coca-Cola and PepsiCo from their 10-K filings: revenue, gross profit, operating income, net income and diluted EPS, and I matched 50 of those figures to the filed documents. I calculated growth, margins and P/E with a valuation date of Dec 31, 2025.
Findings: Coca-Cola grew revenue faster ({K['rev_cagr']:.1f}% vs {P['rev_cagr']:.1f}% CAGR over four intervals), and its operating margin is roughly double ({K['om']:.1f}% vs {P['om']:.1f}% on average). Revenue growth did not always become profit growth: revenue and net income rose together in only {K['both']} of 5 years for Coca-Cola and {P['both']} of 5 for PepsiCo. On the valuation date PepsiCo's P/E was slightly higher ({P['pe25']:.1f}x vs {K['pe25']:.1f}x), and the gap flipped sign across year-ends, so margins and growth alone did not explain the ranking.
Limits: different business mixes and fiscal calendars, GAAP EPS with one-off items, a single price date, and I left out EV/EBITDA because I could not define debt consistently. I treat this as descriptive analysis, not investment advice."

## Five likely questions
1. **Why these two companies?** They are direct competitors in beverages but PepsiCo also has a large snack business, so differences in margins and multiples raise a natural analytical question.
2. **How did you make sure the data is right?** I pulled figures from SEC filings, then checked 50 of them (revenue, gross profit, operating income, net income, EPS for 5 years x 2 companies) against the text of the 10-K documents, and recomputed every metric in Excel and compared with the Tableau CSV.
3. **Why did you not use EV/EBITDA?** It needs a consistent debt, cash and share-count definition at one date. The debt line items are tagged differently across years and companies, so I could not verify them, and I chose to exclude it rather than guess.
4. **What would you do differently with more time?** Add adjusted (non-GAAP) EPS from company releases, use forward estimates, add peers, and build EV/EBITDA with carefully defined debt.
5. **Does this show Coke is better or cheaper than Pepsi?** No. It describes performance and one valuation snapshot. It cannot say which is a better investment or why the market priced them as it did.

## Plain-English explainers
- **P/E ratio:** price you pay per $1 of yearly earnings. Here: closing price divided by that year's diluted GAAP EPS. A P/E of 23x means ${'$'}23 of stock price for each ${'$'}1 of annual profit per share.
- **Margins:** profit as a percent of sales. Gross margin = (revenue - cost of sales) / revenue; operating margin = operating income / revenue; net margin = net income / revenue. KO's {K['om']:.0f}% operating margin means about 25 cents of operating profit per sales dollar.
- **Revenue CAGR:** the steady yearly growth rate that links the first and last year. FY2021 to FY2025 is **4 intervals**, so CAGR = (end / start)^(1/4) - 1 (not 5).
- **Performance vs valuation:** performance is what the company earned (from filings, in the past). Valuation is what investors pay for the stock today, which also reflects expectations, risk, interest rates and sentiment. They can move apart.
"""
(D/"INTERVIEW_PREP.md").write_text(IP)
# ---- data dictionary
fields=[("Company","text","Legal company name"),("Ticker","text","KO or PEP"),("Fiscal_Year","integer","Fiscal year (calendar year in which the fiscal year ends)"),("Fiscal_Year_End","date","Balance-sheet date from the 10-K. KO: Dec 31. PEP: last Saturday of December"),
("Revenue_USD_M","USD millions","Net operating revenues (KO) / Net revenue (PEP), XBRL tag Revenues"),("Prior_Year_Revenue_USD_M","USD millions","Previous fiscal year revenue; used only for growth (FY2021 base comes from the FY2020 10-K XBRL data)"),
("Gross_Profit_USD_M","USD millions","XBRL GrossProfit"),("Operating_Income_USD_M","USD millions","XBRL OperatingIncomeLoss"),("Net_Income_USD_M","USD millions","Net income attributable to the company's shareowners (XBRL NetIncomeLoss)"),
("Prior_Year_Net_Income_USD_M","USD millions","Previous fiscal year net income; used only for growth"),("Total_Assets_USD_M","USD millions","Total assets at fiscal year-end (XBRL Assets; not text-matched)"),("EPS_Diluted_USD","USD per share","Diluted GAAP EPS (XBRL EarningsPerShareDiluted)"),
("Revenue_Growth_Pct","percent","(Revenue / Prior_Year_Revenue - 1) x 100"),("Net_Income_Growth_Pct","percent","(Net_Income / Prior_Year_Net_Income - 1) x 100"),("Gross_Margin_Pct","percent","Gross_Profit / Revenue x 100"),
("Operating_Margin_Pct","percent","Operating_Income / Revenue x 100"),("Net_Margin_Pct","percent","Net_Income / Revenue x 100"),("Revenue_Index_FY2021","index, FY2021 = 100","Revenue / that company's FY2021 revenue x 100 (lets two different-sized companies share one axis)"),
("Net_Income_Index_FY2021","index, FY2021 = 100","Net income / that company's FY2021 net income x 100"),("Valuation_Date","date","Date of the closing price in the row (last trading day of the calendar year: 2021-12-31, 2022-12-30, 2023-12-29, 2024-12-31, 2025-12-31). Each year has its OWN date and price; nothing is repeated across years"),
("Close_Price_USD","USD per share","Unadjusted NYSE close on Valuation_Date (Yahoo Finance chart API; secondary source)"),("PE_Ratio_GAAP","multiple (x)","Close_Price_USD / EPS_Diluted_USD for that fiscal year"),("Is_Headline_Valuation_Date","true/false","True only for the Dec 31, 2025 rows used for the headline P/E chart"),
("Source_Accession","text","SEC accession number of the 10-K for that fiscal year"),("Source_URL","URL","Direct link to that 10-K document on SEC EDGAR"),("Price_Source","text","Source and type of the price")]
assert [f[0] for f in fields]==hdr,(hdr,[f[0] for f in fields])
DD="# Data Dictionary: `valuation_gap_tableau.csv`\n\n10 rows (2 companies x 5 fiscal years), 26 fields, UTF-8, comma-separated, one row per Company x Fiscal_Year. Money is USD millions unless noted. Values are as originally reported in each year's own 10-K (earliest-filed value for the period).\n\n| Field | Unit / type | Definition |\n|---|---|---|\n"+"\n".join(f"| `{a}` | {b} | {c} |" for a,b,c in fields)+"""

## Key conventions
- **CAGR** is not a row field (it would repeat across years). Formula: (FY2025 / FY2021)^(1/4) - 1, because FY2021 to FY2025 spans 4 intervals. Results are in the Excel `Summary` sheet and `FINDINGS.md`.
- **Fiscal years** differ slightly: KO ends Dec 31; PEP ends on the last Saturday of December (Dec 25, 2021; Dec 31, 2022; Dec 30, 2023; Dec 28, 2024; Dec 27, 2025). Period lengths are not adjusted.
- **P/E** pairs a calendar year-end price with that fiscal year's GAAP diluted EPS; PEP's fiscal year-end can be a few days before the price date.
- **Excluded on purpose:** total debt and EV/EBITDA (no consistent, verifiable definition), non-GAAP/adjusted EPS (not an audited line item), forecasts.
"""
(D/"data_dictionary.md").write_text(DD)
# ---- sources
SR="# Sources\n\n## SEC filings used (10-K, one per fiscal year)\n"
for t,L,cik in(("Coca-Cola (CIK 21344)",ko,21344),("PepsiCo (CIK 77476)",pe,77476)):
    SR+=f"\n**{t}**\n"+"".join(f"- FY{r['Fiscal_Year']} (period end {r['Fiscal_Year_End']}), accession {r['Source_Accession']}: {r['Source_URL']}\n" for r in L)
SR+="""
## Structured data
- SEC XBRL company facts (used to extract figures): https://data.sec.gov/api/xbrl/companyfacts/CIK0000021344.json and https://data.sec.gov/api/xbrl/companyfacts/CIK0000077476.json
- SEC EDGAR filing indexes: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000021344&type=10-K and https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000077476&type=10-K
- FY2021 growth base (FY2020 revenue and net income): FY2020 10-Ks, accessions 0000021344-21-000008 (KO) and 0000077476-21-000007 (PEP), via the company facts above.

## Market prices
- Yahoo Finance chart API (unadjusted daily close): https://query1.finance.yahoo.com/v8/finance/chart/KO and https://query1.finance.yahoo.com/v8/finance/chart/PEP . Human-readable history: https://finance.yahoo.com/quote/KO/history and https://finance.yahoo.com/quote/PEP/history
- Prices used are listed in `evidence/prices_used.csv`. This is a secondary, unaudited source; **spot-check the 10 prices** on a second site (e.g. Nasdaq or the exchange) before publishing.

## Verification evidence
- `evidence/verified_figures.json`: the 50 figure-year pairs matched to the text of the 10-K documents above (FY2025 and FY2023 10-Ks per company, each showing three years).
"""
(D/"sources.md").write_text(SR)
# ---- evidence
(O/"evidence").mkdir(exist_ok=True)
shutil.copy(C/"verified.json",O/"evidence/verified_figures.json")
with open(O/"evidence/prices_used.csv","w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["Ticker","Date","Close_USD","EPS_Diluted_USD","PE"]); [w.writerow([r["Ticker"],r["Valuation_Date"],f"{r['Close_Price_USD']:.2f}",r["EPS_Diluted_USD"],f"{r['PE_Ratio_GAAP']:.2f}"]) for r in R]
print("docs ok")
