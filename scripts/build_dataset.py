"""Build the Valuation Gap dataset (KO vs PEP) from SEC companyfacts + Yahoo Finance closes.
Inputs (cached in ./cache): cf_<CIK>.json, sub_<CIK>.json, px_<TICKER>_clean.json, verified.json"""
import json,csv,datetime as dt,pathlib,re
C=pathlib.Path("/tmp/claude-0/vg"); OUT=pathlib.Path("/tmp/claude-0/ValuationGap")
CO={"KO":("The Coca-Cola Company","0000021344"),"PEP":("PepsiCo, Inc.","0000077476")}
YEARS=[2021,2022,2023,2024,2025]
PXDATE={2021:"2021-12-31",2022:"2022-12-30",2023:"2023-12-29",2024:"2024-12-31",2025:"2025-12-31"}
TAG={"Revenue":"Revenues","GrossProfit":"GrossProfit","OperatingIncome":"OperatingIncomeLoss","NetIncome":"NetIncomeLoss","EPS":"EarningsPerShareDiluted","Assets":"Assets"}
def d(s): return dt.date.fromisoformat(s)
rows=[];ver=json.load(open(C/"verified.json"))
for tk,(name,cik) in CO.items():
    cf=json.load(open(C/f"cf_{cik}.json"))["facts"]["us-gaap"]; sub=json.load(open(C/f"sub_{cik}.json"))["filings"]["recent"]
    px=json.load(open(C/f"px_{tk}_clean.json"))
    def pick(k,fy_end_year,inst=False):
        u=cf[TAG[k]]["units"]["USD/shares" if k=="EPS" else "USD"]
        c=[x for x in u if x["form"]=="10-K" and x["end"].startswith(str(fy_end_year)) and (inst or 340<=(d(x["end"])-d(x["start"])).days<=380)]
        c.sort(key=lambda x:x["filed"]); return c[0]   # earliest-filed = as originally reported
    for y in YEARS:
        r={}; 
        for k in TAG: r[k]=pick(k,y,inst=(k=="Assets"))
        acc=r["Revenue"]["accn"]; i=sub["accessionNumber"].index(acc); pdoc=sub["primaryDocument"][i]
        prev_rev=pick("Revenue",y-1)["val"]; prev_ni=pick("NetIncome",y-1)["val"]
        rev,gp,oi,ni=[r[k]["val"]/1e6 for k in("Revenue","GrossProfit","OperatingIncome","NetIncome")]
        eps=r["EPS"]["val"]; price=px[PXDATE[y]][0]
        rows.append(dict(Company=name,Ticker=tk,Fiscal_Year=y,Fiscal_Year_End=r["Revenue"]["end"],
          Prior_Year_Revenue_USD_M=prev_rev/1e6,Revenue_USD_M=rev,Gross_Profit_USD_M=gp,Operating_Income_USD_M=oi,Net_Income_USD_M=ni,
          Prior_Year_Net_Income_USD_M=prev_ni/1e6,Total_Assets_USD_M=r["Assets"]["val"]/1e6,EPS_Diluted_USD=eps,
          Revenue_Growth_Pct=(rev/(prev_rev/1e6)-1)*100,Net_Income_Growth_Pct=(ni/(prev_ni/1e6)-1)*100,
          Gross_Margin_Pct=gp/rev*100,Operating_Margin_Pct=oi/rev*100,Net_Margin_Pct=ni/rev*100,
          Valuation_Date=PXDATE[y],Close_Price_USD=price,PE_Ratio_GAAP=price/eps,
          Is_Headline_Valuation_Date=(y==2025),Source_Accession=acc,
          Source_URL=f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-','')}/{pdoc}",
          Price_Source="Yahoo Finance chart API, unadjusted close",
          Figures_Text_Verified=sum(1 for k in("Revenue","GrossProfit","OperatingIncome","NetIncome","EPS_Diluted") if f"{tk}|{k}|{y}" in ver)))
base={t:{r["Fiscal_Year"]:r for r in rows if r["Ticker"]==t}[2021] for t in CO}
for r in rows:
    b=base[r["Ticker"]]; r["Revenue_Index_FY2021"]=r["Revenue_USD_M"]/b["Revenue_USD_M"]*100; r["Net_Income_Index_FY2021"]=r["Net_Income_USD_M"]/b["Net_Income_USD_M"]*100
cols=["Company","Ticker","Fiscal_Year","Fiscal_Year_End","Revenue_USD_M","Prior_Year_Revenue_USD_M","Gross_Profit_USD_M","Operating_Income_USD_M","Net_Income_USD_M","Prior_Year_Net_Income_USD_M","Total_Assets_USD_M","EPS_Diluted_USD","Revenue_Growth_Pct","Net_Income_Growth_Pct","Gross_Margin_Pct","Operating_Margin_Pct","Net_Margin_Pct","Revenue_Index_FY2021","Net_Income_Index_FY2021","Valuation_Date","Close_Price_USD","PE_Ratio_GAAP","Is_Headline_Valuation_Date","Source_Accession","Source_URL","Price_Source"]
def f(v,c):
    if isinstance(v,float): return f"{v:.4f}" if c.endswith("Pct") or "Index" in c or c=="PE_Ratio_GAAP" else (f"{v:.2f}" if c in("Close_Price_USD","EPS_Diluted_USD") else f"{v:.0f}")
    return str(v).lower() if isinstance(v,bool) else v
with open(OUT/"data/valuation_gap_tableau.csv","w",newline="",encoding="utf-8") as fh:
    w=csv.writer(fh); w.writerow(cols)
    for r in rows: w.writerow([f(r[c],c) for c in cols])
json.dump(rows,open(C/"rows.json","w"),default=str)
print(len(rows),"rows",len(cols),"fields")
for r in rows: print(r["Ticker"],r["Fiscal_Year"],round(r["Revenue_Growth_Pct"],2),round(r["Operating_Margin_Pct"],2),round(r["Net_Margin_Pct"],2),round(r["Net_Income_Growth_Pct"],2),round(r["PE_Ratio_GAAP"],2),r["Figures_Text_Verified"])
