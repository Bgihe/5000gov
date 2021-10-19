import requests
from bs4 import BeautifulSoup
import re
import json
from git import Repo
import os
import ast
import time

def writeOilDict(writeDict):
    with open("/Users/steven/Desktop/公司/git/5000gov/winNumber.json", "w+") as output:
        output.write(str(writeDict).replace("'","\""))

def readWinRateDict():
    with open("/Users/steven/Desktop/config.txt", "r") as data:
        dictionary = ast.literal_eval(data.read())
    return dictionary

def pushJson():
    # https://github.com/Bgihe/5000gov.git

    configDict = readWinRateDict()
    print(configDict)
    print(configDict['username'])
    print(configDict['password'])

    dirfile = os.path.abspath('/Users/steven/Desktop/公司/git/5000gov') # code的文件位置，我默认将其存放在根目录下
    try:
        repo = Repo(dirfile)
        g = repo.git
        g.push()
        g.add("--all")
        g.commit("-m auto update")
        g.push("https://" + configDict['username'] + ":" + configDict['password'] + "@github.com/Bgihe/5000gov.git")
        print("Successful push!")
    except:
        print("Nothing to commit")



def startLoop():
    response = requests.get("https://vhpi.5000.gov.tw/")
    soup = BeautifulSoup(response.text, "html.parser")
    pattern1 = re.compile(r"var winNo1 = {(.*?)}$", re.MULTILINE | re.DOTALL)
    pattern2 = re.compile(r"var winNo2 = {(.*?)}$", re.MULTILINE | re.DOTALL)
    pattern3 = re.compile(r"var winNo3 = {(.*?)}$", re.MULTILINE | re.DOTALL)
    pattern4 = re.compile(r"var winNo4 = {(.*?)}$", re.MULTILINE | re.DOTALL)
    script = soup.find("script", text=pattern1)

    allWinNoList = {'no1': {}, 'no2': {}, 'no3': {}, 'no4': {}}
    allWinNoJson = json.dumps(allWinNoList)

    res1 = json.loads("{" + pattern1.search(str(script)).group(1) + "}")
    res2 = json.loads("{" + pattern2.search(str(script)).group(1) + "}")
    res3 = json.loads("{" + pattern3.search(str(script)).group(1) + "}")
    res4 = json.loads("{" + pattern4.search(str(script)).group(1) + "}")

    allWinNoList['no1'] = res1
    allWinNoList['no2'] = res2
    allWinNoList['no3'] = res3
    allWinNoList['no4'] = res4
    print(allWinNoList)

    writeOilDict(allWinNoList)
    pushJson()
    print("sleep 60")
    time.sleep(60)
    startLoop()

startLoop()