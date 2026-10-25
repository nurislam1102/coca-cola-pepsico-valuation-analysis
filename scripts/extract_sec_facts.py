import json,datetime as dt,sys
CON={"Revenue":["Revenues","RevenueFromContractWithCustomerExcludingAssessedTax"],
"GrossProfit":["GrossProfit"],"OperatingIncome":["OperatingIncomeLoss"],
"NetIncome":["NetIncomeLoss"],"EPS_Diluted":["EarningsPerShareDiluted"],
"Assets":["Assets"],"DebtLT":["LongTermDebtNoncurrent","LongTermDebt"],"DebtST":["DebtCurrent","LoansPayableCurrent","ShortTermBorrowings"],
"Cash":["CashAndCashEquivalentsAtCarryingValue"],"DA":["DepreciationDepletionAndAmortization","DepreciationAndAmortization","DepreciationAmortizationAndAccretionNet"]}
def d(s): return dt.date.fromisoformat(s)
out={}
for tk,cik in [("KO","0000021344"),("PEP","0000077476")]:
    j=json.load(open(f"cf_{cik}.json"))["facts"]; g=j["us-gaap"]
    for k,tags in CON.items():
        for tag in tags:
            if tag not in g: continue
            u=list(g[tag]["units"].values())[0] if "USD/shares" not in g[tag]["units"] else g[tag]["units"]["USD/shares"]
            rows=[x for x in u if x["form"] in("10-K",) and x["end"]>="2019-12-01"]
            inst = k in("Assets","DebtLT","DebtST","Cash")
            if not inst: rows=[x for x in rows if 340<=(d(x["end"])-d(x["start"])).days<=380]
            by={}
            for x in rows: by.setdefault(x["end"],[]).append(x)
            for e,l in sorted(by.items()):
                l.sort(key=lambda x:x["filed"]); out.setdefault((tk,k,tag),[]).append((e,l[0]["val"],l[0]["accn"],l[0]["filed"],l[-1]["val"],l[-1]["accn"]))
for key,v in out.items():
    print(key); [print("   ",r) for r in v]
