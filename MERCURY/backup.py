def latest_file():
    import glob
    import os,shutil
    from datetime import datetime
    ti=datetime.now().strftime("%H%M")

    list_of_files = glob.glob('final/*')
    sorted_files = sorted(list_of_files, key=os.path.getctime)
    latest_file=sorted_files[-3]
    #latest_file = max(list_of_files, key=os.path.getctime)
    shutil.copy(latest_file, 'tmp/')
    shutil.copy(latest_file, 'finalbak/'+ti+'.csv')