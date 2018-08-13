import requests
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
'''
chrome_exec_shim = os.environ.get("GOOGLE_CHROME_BIN", "chromedriver")'''
#self.selenium = webdriver.Chrome(executable_path=chrome_exec_shim)
def tohanear(con,pos):
    ntohaPos=con.find('とは')
    if ntohaPos==-1:
        ntohaPos=con.find('は')
    compare=1000
    nearT=None
    for i in pos:
        if abs(i-ntohaPos)<compare:
            compare=abs(i-ntohaPos)
            nearT=i
    incPos=con.find('「')
    if incPos!=-1:
        if (ntohaPos-incPos)>0:
            nearT=incPos
    return nearT



def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext
exist_url='http://api.nicodic.jp/page.exist/json/a/'
nicoDic='http://dic.nicovideo.jp/a/'
CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"

#chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', "chromedriver")

def summary(words):
#words=input()
#first check if the page exist with API
    exist=requests.get(exist_url+words)
    exist=exist.json()
    if exist: 
        redirect=False
        ht=requests.get(nicoDic+words)
        html=ht.text
        if ht.text.find('meta http-equiv="refresh"')!=-1:
            urlPos=ht.text.find('URL=http://dic.nicovideo.jp/a/')
            realurl=''
            while ht.text[urlPos]!='"':
                realurl=realurl+ht.text[urlPos]
                urlPos=urlPos+1
            realurl=realurl.replace('URL=http://dic.nicovideo.jp/a/','')
            html=requests.get(nicoDic+realurl).text
        
        soup=BeautifulSoup(html,features="html.parser")
        title=soup.title.string
        tohaPos=title.find('とは')
        title=title[:tohaPos]
        print(title)
        #now we have title
        #normal page with a organize summary
        divPos=html.find('<div class="article" id="article">')
        h2Pos=html.find('<h2')
        content=html[divPos:h2Pos]
        purecontent=content
        #print (content)

        summaryPos=[h.start() for h in re.finditer(title, content)]
        content=content[tohanear(content,summaryPos):]
        content=cleanhtml(content)
        #if content.find('\n\n')!=-1:
        #    content=content[:content.find('\n\n')]
        if content.find('である。')!=-1:
            content=content[:content.find('である。')+4]
        while content.find('\n\n')!=-1:
            content=content.replace('\n\n','\n')
        if content[len(content)-1]=='\n':
            content=content[:len(content)-1]
        if content.find('掲示板')==-1:
            return content
    
        #not stander
        h2_1Pos=html.find('<h2 id="h2-1">')
        h2_2Pos=html.find('<h2 id="h2-2">')
        contentUnst=html[h2_1Pos:h2_2Pos]
        if contentUnst.find('<table')!=-1:
            tableStart=contentUnst.find('<table')
            tableEnd=contentUnst.find('</table>')+8
            contentUnst=contentUnst.replace(contentUnst[tableStart:tableEnd],'')
        pStart=contentUnst.find('<p>')
        pEnd=contentUnst.find('</p>')+4
        contentUnst=contentUnst[pStart:pEnd]
        return cleanhtml(contentUnst)
    
    return None

