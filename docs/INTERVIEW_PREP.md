# Interview Preparation Notes

## 30-second explanation
"I compared Coca-Cola and PepsiCo using five years of their SEC annual reports. Coca-Cola grew revenue a bit faster (5.5% vs 4.3% a year) and keeps much more profit from each sales dollar (about 25% operating margin vs 13%). But on Dec 31, 2025 their P/E ratios were close, 23.0x vs 23.9x, so strong financials did not simply mean a higher multiple. I built the dataset and a Tableau dashboard to show this, and I am careful to say what the data cannot prove."

## 90-second explanation
"My question was: why do investors value two competing companies differently, and how much can financial performance explain? I collected five fiscal years for Coca-Cola and PepsiCo from their 10-K filings: revenue, gross profit, operating income, net income and diluted EPS, and I matched 50 of those figures to the filed documents. I calculated growth, margins and P/E with a valuation date of Dec 31, 2025.
Findings: Coca-Cola grew revenue faster (5.5% vs 4.3% CAGR over four intervals), and its operating margin is roughly double (25.3% vs 13.3% on average). Revenue growth did not always become profit growth: revenue and net income rose together in only 3 of 5 years for Coca-Cola and 4 of 5 for PepsiCo. On the valuation date PepsiCo's P/E was slightly higher (23.9x vs 23.0x), and the gap flipped sign across year-ends, so margins and growth alone did not explain the ranking.
Limits: different business mixes and fiscal calendars, GAAP EPS with one-off items, a single price date, and I left out EV/EBITDA because I could not define debt consistently. I treat this as descriptive analysis, not investment advice."

## Five likely questions
1. **Why these two companies?** They are direct competitors in beverages but PepsiCo also has a large snack business, so differences in margins and multiples raise a natural analytical question.
2. **How did you make sure the data is right?** I pulled figures from SEC filings, then checked 50 of them (revenue, gross profit, operating income, net income, EPS for 5 years x 2 companies) against the text of the 10-K documents, and recomputed every metric in Excel and compared with the Tableau CSV.
3. **Why did you not use EV/EBITDA?** It needs a consistent debt, cash and share-count definition at one date. The debt line items are tagged differently across years and companies, so I could not verify them, and I chose to exclude it rather than guess.
4. **What would you do differently with more time?** Add adjusted (non-GAAP) EPS from company releases, use forward estimates, add peers, and build EV/EBITDA with carefully defined debt.
5. **Does this show Coke is better or cheaper than Pepsi?** No. It describes performance and one valuation snapshot. It cannot say which is a better investment or why the market priced them as it did.

## Plain-English explainers
- **P/E ratio:** price you pay per $1 of yearly earnings. Here: closing price divided by that year's diluted GAAP EPS. A P/E of 23x means $23 of stock price for each $1 of annual profit per share.
- **Margins:** profit as a percent of sales. Gross margin = (revenue - cost of sales) / revenue; operating margin = operating income / revenue; net margin = net income / revenue. KO's 25% operating margin means about 25 cents of operating profit per sales dollar.
- **Revenue CAGR:** the steady yearly growth rate that links the first and last year. FY2021 to FY2025 is **4 intervals**, so CAGR = (end / start)^(1/4) - 1 (not 5).
- **Performance vs valuation:** performance is what the company earned (from filings, in the past). Valuation is what investors pay for the stock today, which also reflects expectations, risk, interest rates and sentiment. They can move apart.
