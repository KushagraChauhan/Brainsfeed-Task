from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request
import requests, re
from selenium import webdriver
from time import sleep
app = Flask(__name__)

@app.route('/getdata', methods=['GET'])
def getdata():
    weburl = request.args['url']
    content = requests.get(weburl)
    soup = BeautifulSoup(content.text, 'html.parser')
    ################################################################################
    ###############################################################################
    ######################### Get the Title of website ############################
    ###############################################################################
    ###############################################################################
    title = soup.find('title')
    print(title)
    print("=========Text Result==========")
    titleText = title.get_text()
    print(title.get_text())
    ################################################################################
    ###############################################################################
    ######################### Take a SS of the homepage# ###########################
    ###############################################################################
    ###############################################################################
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)
    driver.get(weburl)
    sleep(4)
    driver.get_screenshot_as_file("screenshot.png")
    driver.quit()
    ################################################################################
    ###############################################################################
    ######################### Get Contact Email ##################################
    ###############################################################################
    ###############################################################################
    allLinks = [];mails=[]
    links = [a.attrs.get('href') for a in soup.select('a[href]') ]
    for i in links:
        if(("contact" in i or "Contact")or("Career" in i or "career" in i))or('about' in i or "About" in i)or('Services' in i or 'services' in i):
            allLinks.append(i)
    allLinks=set(allLinks)
    def findMails(soup):
        for name in soup.find_all('a'):
            if(name is not None):
                emailText=name.text
                match=bool(re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',emailText))
                if('@' in emailText and match==True):
                    emailText=emailText.replace(" ",'').replace('\r','')
                    emailText=emailText.replace('\n','').replace('\t','')
                    if(len(mails)==0)or(emailText not in mails):
                        print(emailText)
                    mails.append(emailText)
    for link in allLinks:
        if(link.startswith("http") or link.startswith("www")):
            r=requests.get(link)
            data=r.text
            soup=BeautifulSoup(data,'html.parser')
            findMails(soup)

        else:
            newurl=url+link
            r=requests.get(newurl)
            data=r.text
            soup=BeautifulSoup(data,'html.parser')
            findMails(soup)

    mails=set(mails)
    if(len(mails)==0):
        print("NO MAILS FOUND")
    return jsonify(titleText)


if __name__ == "__main__":
    app.run(debug=True)
