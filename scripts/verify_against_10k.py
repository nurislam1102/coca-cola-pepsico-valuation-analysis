import json,re,subprocess,sys,datetime as dt
from bs4 import BeautifulSoup
UA=open('/home/claude/financeflow/.env').read()
UA=[l.split('=',1)[1].strip().strip('"') for l in UA.splitlines() if l.startswith('SEC_USER_AGENT')][0]
def get(u,o):
    r=subprocess.run(["curl","-s","-m","120","-A",UA,"-o",o,"-w","%{http_code}",u],capture_output=True,text=True); return r.stdout
ACC={"KO":("0000021344",["0001628280-26-010047","0000021344-24-000009"]),"PEP":("0000077476",["0000077476-26-000007","0000077476-24-000008"])}
DATA=json.load(open("../vg/ext_data.json"))
res={}
docs={}
for tk,(cik,accs) in ACC.items():
    sub=f"sub_{cik}.json"; print(tk,"sub",get(f"https://data.sec.gov/submissions/CIK{cik}.json",sub))
    s=json.load(open(sub)); rec=s["filings"]["recent"]
    for a in accs:
        i=rec["accessionNumber"].index(a); pd=rec["primaryDocument"][i]
        url=f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{a.replace('-','')}/{pd}"
        f=f"doc_{tk}_{a}.htm"; print(url,get(url,f))
        txt=BeautifulSoup(open(f,errors="ignore").read(),"lxml").get_text(" | ")
        txt=re.sub(r"\s+"," ",txt); docs[(tk,a)]=(url,txt)
json.dump({f"{k[0]}|{k[1]}":v[0] for k,v in docs.items()},open("doc_urls.json","w"))
def fmt(v,eps=False): return f"{v:.2f}" if eps else f"{round(v/1e6):,}"
ok={};miss=[]
for tk,(cik,accs) in ACC.items():
    for m,eps in [("Revenue",0),("GrossProfit",0),("OperatingIncome",0),("NetIncome",0),("EPS_Diluted",1)]:
        yrs=sorted(DATA[tk][m])  # years
        for a in accs:
            txt=docs[(tk,a)][1]
            ys=[y for y in yrs]  # try each window of 3 consecutive years
            for i in range(len(ys)-2):
                w=[DATA[tk][m][y] for y in ys[i:i+3]]
                for order in (w[::-1],w):
                    pat=r"[\s|\$\(]*".join(re.escape(fmt(v,eps)) for v in order)
                    if re.search(pat,txt):
                        for y in ys[i:i+3]: ok[(tk,m,y)]=a
print(len(ok)); 
for tk in ACC:
    for m in ["Revenue","GrossProfit","OperatingIncome","NetIncome","EPS_Diluted"]:
        for y in sorted(DATA[tk][m]):
            if y>="2021" and (tk,m,y) not in ok: miss.append((tk,m,y))
print("missing",miss)
json.dump({"|".join(k):v for k,v in ok.items()},open("verified.json","w"))
