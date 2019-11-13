class live:
    def __init__(self, d, bs='B', aaa=0, th=12.5):
        self.d = d
        self.bs = bs
        self.aaa = 0
        self.th = 12.5

    def loaddata(self):
        import pandas as pd
        df = pd.read_csv('zerodha.csv')

        def oneDArray(x):
            import itertools
            return list(itertools.chain(*x))

        if self.d == 'all':
            x = [df[a].dropna().values.tolist() for a in df.columns.tolist()]
            xx = oneDArray(x)
            y = ['GOLDBEES', 'BANKBEES', 'LIQUIDBEES', 'NIFTYBEES', 'TIFIN', 'BHARATFIN', 'KOTAKNIFTY', 'ICICINIFTY',
                 'M50', 'GUJFLUORO']
            self.c = [item for item in xx if item not in y]
            self.zx = set(self.c)
            self.c = list(self.zx)
            return self.c

        xx = df[self.d].dropna().values.tolist()
        y = ['GOLDBEES', 'BANKBEES', 'LIQUIDBEES', 'NIFTYBEES', 'TIFIN', 'BHARATFIN', 'KOTAKNIFTY', 'ICICINIFTY', 'M50',
             'GUJFLUORO']
        self.c = [item for item in xx if item not in y]
        self.zx = set(self.c)
        self.c = list(self.zx)
        return self.c

    def dircreate(self):
        import os
        global count

        dirNames = ['final', 'table', 'piechart', 'tmp']
        dirName = ['finalbak', 'open']

        def mkdir_path(i):
            if not os.access(i, os.F_OK):
                os.mkdir(i)

        [(mkdir_path(i), mkdir_path(j)) for i in dirNames for j in dirName]
        if count == 0:
            import fdremove as fr
            # [ fr.fremove(i) for i in dirNames ]
            [fr.fpatterns(i) for i in dirNames]
        else:
            pass
        count = count + 1

    def batch(self, iterable, nn=1):
        l = len(iterable)
        for ndx in range(0, l, nn):
            yield iterable[ndx:min(ndx + nn, l)]

    def datadownload(self):
        import pandas as pd
        import numpy as np
        from datetime import datetime
        from nsetools import Nse
        import time
        start_time = datetime.now().replace(microsecond=0)
        self.loaddata()
        self.aaa = 0
        self.dircreate()
        for ss in self.batch(self.c, 8):
            df2 = pd.DataFrame([Nse().get_quote(s) for s in ss],
                               columns=['symbol', 'lastPrice', 'totalBuyQuantity', 'totalSellQuantity', 'open',
                                        'dayHigh', 'dayLow'])
            self.aaa = self.aaa + 1
            # df2.replace(r'^\s*$', np.nan, regex=True,inplace=True)
            # df2 = df2.applymap(lambda x: np.nan if isinstance(x, str) and x.isspace() else x)
            df2 = df2.fillna(1000)
            df2.to_csv('table/table' + str(self.aaa) + '.csv')
            self.dataAnalysis()
            self.piechart()
        import backup
        backup.latest_file()
        import openhighlow as ohl
        ohl.openHighLow()
        global scheduler, count
        count = 0
        count += 1

        if count == 10:
            scheduler.shutdown(wait=False)

        end_time = datetime.now().replace(microsecond=0)
        print('Data Downloading, Analysing, piechart drawing : {}'.format(end_time - start_time))

    def dataAnalysis(self):
        import pandas as pd
        import numpy as np
        from datetime import datetime
        from nsetools import Nse
        import time, glob, os
        start_time = datetime.now().replace(microsecond=0)
        df3 = pd.concat(map(pd.read_csv, glob.glob(os.path.join('', "table/table*.csv"))))
        df3.reset_index(drop=True, inplace=True)
        df3.drop(['Unnamed: 0'], axis=1, inplace=True)
        currentDT = datetime.now()
        df3['Time'] = currentDT.strftime("%H:%M")
        ti = currentDT.strftime("%H%M")
        df3["BS"] = [" " for i in range(len(df3))]
        df3["Thousand"] = [" " for i in range(len(df3))]
        for i in range(len(df3)):
            if df3.loc[i]['totalSellQuantity'] > df3.loc[i]['totalBuyQuantity']:
                df3.at[i, 'BS'] = "S"
                df3.at[i, 'Thousand'] = round((1000 / df3.loc[i]['lastPrice']) * self.th, 1)
            else:
                df3.at[i, 'BS'] = "B"
                df3.at[i, 'Thousand'] = round((1000 / df3.loc[i]['lastPrice']) * self.th, 1)
        df3["BSTimes"] = [
            df3.iloc[i]["totalSellQuantity"] / df3.iloc[i]["totalBuyQuantity"] if df3.loc[i]['totalSellQuantity'] >
                                                                                  df3.loc[i]['totalBuyQuantity'] else
            df3.iloc[i]["totalBuyQuantity"] / df3.iloc[i]["totalSellQuantity"] for i in range(len(df3))]
        df3 = df3.sort_values('BSTimes', ascending=False)
        df3.to_csv('final/final' + str(self.aaa) + '.csv')
        df4 = df3[df3['BS'] == 'B']
        df4.to_csv('final/finalb' + str(self.aaa) + '.csv')
        df5 = df3[df3['BS'] == 'S']
        df5.to_csv('final/finals' + str(self.aaa) + '.csv')
        end_time = datetime.now().replace(microsecond=0)
        # print('Time Taken To Analyse Stocks: {}'.format(end_time - start_time))

    def piechart(self):
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        df = pd.read_csv('final/final' + str(self.aaa) + '.csv')
        plt.pie(df['BSTimes'][:7], labels=df['symbol'][:7], autopct='%1.1f%%', radius=2)
        plt.axis('equal')
        plt.savefig('piechart/piecharts' + str(self.aaa) + '.pdf', transparent=True, bbox_inches='tight', pad_inches=0)
        # plt.show()

    def nsestock(self):
        while True:
            try:
                self.loaddata()
                self.datadownload()
            except:
                print("Looks like there is some exception")
                continue
            else:
                print('Yep Successfully Executed')
                break

    def sendmailattachh(self):
        #self.datadownload()
        import glob, os
        from datetime import date
        t=date.today()
        os.chdir('C:/Users/Haribabu/Desktop/mercurycoded/finalbak/'+str(t))
        list_of_files = glob.glob('open*')
        sorted_files = sorted(list_of_files, key=os.path.getctime)
        filename = sorted_files[-1]
        import smtplib
        import os
        import glob
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        fromaddr = 'gk972955@gmail.com'
        toaddr = ['muraliponnada19@gmail.com','terawork9@gmail.com']
        password = "abcdefg"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        #msg['To'] = toaddr
        msg['To'] = ", ".join(toaddr)
        msg['Subject'] = "d=all"
        body = "Mail Sent by Python Code"
        msg.attach(MIMEText(body, 'plain'))
        # for filename in glob.glob(os.path.join('C:/Users/anil/Desktop/mercury/finalbak','*.csv')):#to send specific type of files
        # for filename in os.listdir('C:/Users/gopi/Desktop/mercury/open'):
        #os.chdir('C:/Users/anil/Desktop/mercury/finalbak')
        attachment = open(filename, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, password)
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        #s.sendmail(fromaddr, 'terawork9@gmail.com ',text)
        s.quit()

import os
os.chdir('C:/Users/Haribabu/Desktop/mercurycoded')
import time
count=0
ob = live(d='all')
ob.datadownload()
time.sleep(30)
ob.sendmailattachh()