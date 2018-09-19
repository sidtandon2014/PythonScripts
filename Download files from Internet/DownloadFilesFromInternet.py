# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 09:06:59 2018

@author: sitandon
"""

import requests
from requests import get
from bs4 import BeautifulSoup
import pdb
from os import path
import os
import zipfile
import pandas as pd
import threading

folderLocation = ""
r  = requests.get(folderLocation)
data = r.text
soup = BeautifulSoup(data)

for link in soup.find_all('a'):
    fileName = link.get('href')
    if "zip" in fileName:
        fullFilePath = path.join(folderLocation, fileName) 
        destinationPath = path.join("F:\Sid\Learnings\Python\Scripts",fileName)
        content = get(fullFilePath)
        with open(destinationPath, 'wb') as f:
            f.write(content.content)

      
def writeDataToSql(data):
    import pyodbc
    
    try:
        conn_str = "DSN=sqlserver;"
        #conn = mssql.connect(server = ".",database = "TRAI",user= "sa",password = "Pass@123")    
        conn = pyodbc.connect(conn_str)
        
        cur = conn.cursor()
        cur.fast_executemany = True
        query = """INSERT INTO TRAI.dbo.TRAIData([ServiceAreaCode], PhoneNumber, Preferences, OpsType, PhoneType,filename)
                    VALUES (?,?,?,?,?,?)"""
        cur.executemany(query, tuple(map(tuple, data.values)))
        conn.commit()
        cur.close()
        conn.close()
    except:
        print("Error occured")
        cur.close()
        conn.close()
        
def writeBulkDataToSql():
    import pypyodbc
    
    for root, directories, files in os.walk("F:\Sid\Learnings\Python\Scripts\Data"):
        for filename in files:
            if ".csv" in filename:
                try:
                    filePath = path.join(root, filename)
                    conn_str = "DSN=sqlserver;"
                    conn = pypyodbc.connect(conn_str)
                    
                    cur = conn.cursor()
                    query = """
                            BULK INSERT TRAI.dbo.TRAIData
                            FROM '""" + filePath + """' WITH (
                                FIELDTERMINATOR=',',
                                ROWTERMINATOR='\\n'
                                );
                            """
                    cur.execute(query)
                    conn.commit()
                    cur.close()
                    conn.close()
                except:
                    print(filename + ": Error occured")
                    cur.close()
                    conn.close()
    
#--------------Read file
class ConvertToCSV (threading.Thread):
   def __init__(self, data,fileNameWithoutExt, destinationFolder):
      threading.Thread.__init__(self)
      self.data = data
      self.destinationFolder = destinationFolder
      self.fileNameWithoutExt = fileNameWithoutExt
      
   def run(self):
      self.data.to_csv(path.join(self.destinationFolder, self.fileNameWithoutExt + ".csv"),index = False)
      
for root, directories, files in os.walk("F:\Sid\Learnings\Python\Scripts"):
    for filename in files:
        if ".zip" in filename:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            zf = zipfile.ZipFile(filepath) # having First.csv zipped file.
            df = pd.read_csv(zf.open(filename.split(".")[0] + ".csv")) 
            #df.to_csv(path.join("F:\Sid\Learnings\Python\Scripts\Data", filename.split(".")[0] + ".csv"))
            
            fileNameWithoutExt = filename.split(".")[0]
            print("Starting thread for filename: " + fileNameWithoutExt)
            myThread = ConvertToCSV(df,fileNameWithoutExt,"F:\Sid\Learnings\Python\Scripts\Data")
            myThread.start()
            