from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request
import requests, re, json
from selenium import webdriver
from gensim.summarization import summarize
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
    ##############################################################################
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)
    driver.get(weburl)
    sleep(4)
    driver.get_screenshot_as_file("screenshot.png")
    driver.quit()
    ################################################################################
    ################### Upload the image to Files.io###############################
    ###############################################################################
    files = {
    'file': ('screenshot.png', open('screenshot.png', 'rb')),
    }
    response = requests.post('https://file.io/', files=files)
    json_resp = response.json()
    ssLink = json_resp['link']
    print(ssLink)
    ###############################################################################
    ##############################################################################
    ######################## Get Contact Email ##################################
    ##############################################################################
    ##############################################################################
    allLinks = [];mails=[]
    links = [a.attrs.get('href') for a in soup.select('a[href]') ]
    for i in links:
        if(("contact" in i or "Contact")or("Career" in i or "career" in i))or('about' in i or "About" in i)or('Services' in i or 'services' in i):
            allLinks.append(i)
    allLinks=set(allLinks)
    def findMails(soup_email):
        for name in soup_email.find_all('a'):
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
            soup_email=BeautifulSoup(data,'html.parser')
            findMails(soup_email)

        else:
            newurl=weburl+link
            r=requests.get(newurl)
            data=r.text
            soup_email=BeautifulSoup(data,'html.parser')
            findMails(soup_email)
    print("mails",mails)
    if(len(mails)==0):
        print("NO MAILS FOUND")

    ################################################################################
    ###############################################################################
    ######################### Short Description ##################################
    ###############################################################################
    ###############################################################################
    metas = soup.find_all('meta')
    short_desc = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description']
    short_desc = str(short_desc)
    short_desc = short_desc.strip('[]')
    print("short desc:",short_desc)

    ################################################################################
    ###############################################################################
    ######################### Summarize the content ##################################
    ###############################################################################
    ###############################################################################
    headline1 = soup.find('h1').get_text()
    headline2 = soup.find('h2').get_text()
    headline3 = soup.find('h3').get_text()
    print("h1",headline1)
    print("h2",headline2)
    print("h3",headline3)
    p_tags = soup.find_all('p')
    p_tags_text = [tag.get_text().strip() for tag in p_tags]
    print("p-tags",p_tags_text)
    sentence_list = [sentence for sentence in p_tags_text if not '\n' in sentence]
    sentence_list = [sentence for sentence in sentence_list if '.' in sentence]
    article = ' '.join(sentence_list)
    summary = summarize(article, ratio=0.3)
    if len(summary)==0 :
        p_tags_text = str(p_tags_text)
        p_tags_text = p_tags_text.strip('[]')
        summary = headline1 + (' ') + headline2 + (' ') + headline3
    print('summary:',summary)

    ################################################################################
    ###############################################################################
    ######################### Paid services ##################################
    ###############################################################################
    ###############################################################################
    word = 'pricing'
    words = soup.find(text=lambda text: text and word in text)
    if len(words)>0:
        print(words)
        pricing = "Yes"
    else:
        pricing = "No"
#################################################################################
#################################################################################
######################### Get the JSON Response ##################################
#################################################################################
#################################################################################

    x = {"Title":titleText,"Screenshot Link":ssLink,"Email":mails, "Short Description":short_desc, "Summary":summary, "Paid Services":pricing}
    y = json.dumps(x)
    z = json.loads(y)
    return jsonify(z)


if __name__ == "__main__":
    app.run(debug=True)
