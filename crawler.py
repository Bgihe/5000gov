import requests
from bs4 import BeautifulSoup
import re
import json
from git import Repo
import os

def writeOilDict(writeDict):
    with open("/Users/steven/Desktop/公司/git/5000gov/winNumber.json", "w+") as output:
        output.write(str(writeDict))

def pushJson():
    dirfile = os.path.abspath('/Users/steven/Desktop/公司/git/5000gov') # code的文件位置，我默认将其存放在根目录下
    repo = Repo(dirfile)
    g = repo.git
    g.push()
    g.add("--all")
    g.commit("-m auto update")
    g.push()
    print("Successful push!")
    print("Successful push!")

response = requests.get("https://vhpi.5000.gov.tw/")
soup = BeautifulSoup(response.text, "html.parser")
pattern1 = re.compile(r"var winNo1 = {(.*?)}$", re.MULTILINE | re.DOTALL)
pattern2 = re.compile(r"var winNo2 = {(.*?)}$", re.MULTILINE | re.DOTALL)
pattern3 = re.compile(r"var winNo3 = {(.*?)}$", re.MULTILINE | re.DOTALL)
pattern4 = re.compile(r"var winNo4 = {(.*?)}$", re.MULTILINE | re.DOTALL)
script = soup.find("script", text=pattern1)

allWinNoList = {'no1': {}, 'no2': {}, 'no3': {}, 'no4': {}}
allWinNoJson = json.dumps(allWinNoList)

search1 = "{" + pattern1.search(str(script)).group(1) + "}"
search2 = "{" + pattern2.search(str(script)).group(1) + "}"
search3 = "{" + pattern3.search(str(script)).group(1) + "}"
search4 = "{" + pattern4.search(str(script)).group(1) + "}"

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