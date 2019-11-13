def openHighLow():
    import pandas as pd
    import numpy as np
    import glob
    import os,shutil
    from datetime import datetime,date

    ti=datetime.now().strftime("%H%M")
    td1=date.today()
    def mkdir_path(i):
        if not os.access(i, os.F_OK):
            os.mkdir(i)
    mkdir_path('finalbak/' + str(td1))
    td=str(td1).replace("-","")
    list_of_files = glob.glob('tmp/*')
    
    df=pd.read_csv(list_of_files[0])
    df.drop(['Unnamed: 0'],axis=1,inplace=True)
    df['openHigh'] = np.where((df['open'] == df['dayHigh'])
                     , df['open'], np.nan)
    df['openLow'] = np.where((df['open'] == df['dayLow'])
                     , df['open'], np.nan)
    df.to_csv('tmp/open_high_low'+'.csv')
    #df.to_csv('final.bak/open_high_low'+ti+'.csv')
    oH=df.openHigh
    opHi=df.symbol[~oH.isnull()]
    opHi.to_frame().to_csv('open/openHigh'+'.csv')
    oL=df.openLow
    opLo=df.symbol[~oL.isnull()]
    opLo.to_frame().to_csv('open/openLow'+'.csv')
    print("\n","-"*9,"\n","Open=High","\n","-"*9,"\n"+opHi.to_string(index=False))
    print("\n","-"*9,"\n","Open=Low","\n","-"*9,"\n"+opLo.to_string(index=False))
    
    import pandas as pd
    #df=pd.read_csv("open_high_low2307.csv",index_col=0)
    df2=pd.read_csv("zerodha.csv")
    a=df2.columns
    count=0
    app=[]
    org=[]
    stri=""
    for x in df['symbol'].values:
         for j in a:
             if(x in df2[j].values and x not in app):
                 stri=stri+" "+j
                 count=count+1
         count=0  
         app.append(x)
         org.append(stri)
         stri=""
    ser=pd.Series(org)
    df['ZTimes']=ser
    df['percentoflp']=(df['dayHigh']-df['dayLow'])*100/df['lastPrice']
    df = df.round({"percentoflp": 2})
    new = df['ZTimes'].str.split(" ", expand=True)
    new.drop([0], axis=1, inplace=True)
    new[1] = new[1].str.replace(r'[^\d.]+', '')
    df['ZTimes'], df['ZTimes_name1'], df['ZTimes_name2'] = new[1], new[2], new[3]
    df = df.round({"BSTimes": 1})
    #print(df.columns.tolist())
    df['ZTimes BS'] = df.ZTimes.astype(str).str.cat(df.BS.astype(str), sep=' ')
    df.drop(['BS', 'ZTimes'], axis=1,inplace=True)
    cols = ['symbol', 'ZTimes BS', 'BSTimes', 'openHigh', 'openLow', 'Thousand', 'lastPrice','percentoflp', 'dayHigh', 'dayLow',
            'open', 'totalBuyQuantity', 'totalSellQuantity', 'Time', 'ZTimes_name1', 'ZTimes_name2']
    df = df[cols]
    #print(df.columns.tolist())
    print(df)
    df.to_csv('finalbak/'+str(td1)+'/open_high_low'+td+ti+'.csv',index=False)