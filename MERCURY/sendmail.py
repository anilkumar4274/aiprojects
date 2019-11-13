def sendmailattach():
    # self.datadownload()
    import glob, os
    os.chdir('C:/Users/Haribabu/Desktop/mercurycode/finalbak')
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
    fromaddr = 'gopisai28471@gmail.com
    toaddr = ['muraliponnada19@gmail.com', 'terawork9@gmail.com']
    password = "mdoamd5421"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    # msg['To'] = toaddr
    msg['To'] = ", ".join(toaddr)
    msg['Subject'] = "d=A12.5"
    body = "Mail Sent by Python Code"
    msg.attach(MIMEText(body, 'plain'))
    # for filename in glob.glob(os.path.join('C:/Users/anil/Desktop/mercury/finalbak','*.csv')):#to send specific type of files
    # for filename in os.listdir('C:/Users/gopi/Desktop/mercury/open'):
    # os.chdir('C:/Users/anil/Desktop/mercury/finalbak')
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
    s.sendmail(fromaddr,toaddr,text)
    #s.sendmail(fromaddr, 'terawork9@gmail.com ', text)
    s.quit()
