import os
os.chdir('C:/Users/Haribabu/Desktop/jupyter')
def mk_dir(g):
    if not os.access(g, os.F_OK):
        os.mkdir(g)
mk_dir('finale')
j=7
for kk in ['BANKNIFTY','NIFTY']:
    import pandas as pd
    dfcepe = pd.DataFrame(columns=['strikePrice', 'lastPrice', 'totalBuyQuantity', 'totalSellQuantity', 'underlyingValue', 'optionType'])
    for ii in ['CE','PE']:
        import requests
        import re
        import datetime
        import time
        import pandas as pd
        import numpy as np
        from bs4 import BeautifulSoup
        result=pd.DataFrame()
        start_time = datetime.datetime.now()
        ti = datetime.datetime.now().strftime("%H%M")
        td1=datetime.date.today()
        mk_dir('finale/'+str(td1))
        td=str(td1).replace("-","")
        Base_url="https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuoteFO.jsp?underlying="+kk+"&instrument=OPTIDX&expiry=14NOV2019&type="+ii
        page=requests.get(Base_url)
        soup=BeautifulSoup(page.content,'html.parser')
        price=soup.find(id='responseDiv')
        a=str(price.text)
        b=a.strip('\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n')
        c=b.replace('false',"\"false\"").replace("null","\"null\"")
        d=eval(c)
        e=d['data'][0]
        df=pd.DataFrame([e])
        df_new=df.loc[:,['strikePrice','lastPrice','totalBuyQuantity','totalSellQuantity','underlyingValue','optionType']]
        a=df_new['underlyingValue']
        import math
        b=math.ceil(float(a[0].replace(',','')))
        x=int(round(b, -2))
        y=[((x-300),(x+300)) for i in range(1)]
        z=[i for a in y for i in a]
        import numpy as np
        aaa=np.linspace(z[0],z[1],j).astype(int)

        Base_url=["https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuoteFO.jsp?underlying="+kk+"&instrument=OPTIDX&expiry=14NOV2019&type="+ii+"&strike="+str(i)+".00" for i in aaa]

        InfoDF = pd.DataFrame()
        for i in Base_url:
            page=requests.get(i)
            soup=BeautifulSoup(page.content,'html.parser')
            price=soup.find(id='responseDiv')
            a=str(price.text)
            b=a.strip('\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n')
            c=b.replace('false',"\"false\"").replace("null","\"null\"")
            d=eval(c)
            e=d['data'][0]
            df=pd.DataFrame([e])
            df_new=df.loc[:,['strikePrice','lastPrice','totalBuyQuantity','totalSellQuantity','underlyingValue','optionType']]
            InfoDF = pd.concat([InfoDF,df_new])
        print(InfoDF)
        dfcepe = pd.concat([dfcepe,InfoDF])
    print(dfcepe)
    dfcepe.index=range(0,len(dfcepe))
    print(type(int(dfcepe.loc[0]['totalSellQuantity'].replace(",",""))))
    dfcepe['BS'],dfcepe['BSTimes']=[" " for i in range(0,len(dfcepe))],[" " for i in range(0,len(dfcepe))]
    for i in range(0,len(dfcepe)):
        g=int(dfcepe.loc[i]['totalSellQuantity'].replace(",", ""))
        h=int(dfcepe.loc[i]['totalBuyQuantity'].replace(",", ""))
        if g > h:
            dfcepe.loc[i]['BS'],dfcepe.loc[i]['BSTimes']='S',round(g/h,2)
        else:
            dfcepe.loc[i]['BS'],dfcepe.loc[i]['BSTimes']='B',round(h/g,2)
    dfcepe.to_csv('finale/'+str(td1)+'/'+kk+td+ti+'.csv',index=False)
    j=j+6
def sendmailattachh():
    import glob, os
    os.chdir('C:/Users/Haribabu/Desktop/jupyter/finale/'+str(td1))
    list_of_files = [ glob.glob('BANK*'), glob.glob('NIFTY*')]
    filename=[sorted(i, key=os.path.getctime)[-1] for i in list_of_files]
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    fromaddr = 'gk972955@gmail.com'
    toaddr = ['muraliponnada19@gmail.com','gk972955@gmail.com']
    password = "abcdefg"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    #msg['To'] = toaddr
    msg['To'] = ", ".join(toaddr)
    msg['Subject'] = "BANKNIFTY"
    body = "Mail Sent by Python Code"
    msg.attach(MIMEText(body, 'plain'))
    for file in filename:
        attachment = open(file, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % file)
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    #s.sendmail(fromaddr, 'terawork9@gmail.com ',text)
    s.quit()
sendmailattachh()