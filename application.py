from flask import Flask, render_template, request
import os
import logging
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO,filename="ImageScraper.log")

application = Flask(__name__)
app=application

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')
@app.route('/review', methods=['POST'])
def index():
    if request.method == 'POST':
        logging.info("Enetered Index Method")   
        try:
            logging.info("Ended Index Method")
            # query to search for images
            query = request.form['content'].replace(" ","")
            logging.info("Search Value: %s" % query)

            # fake user agent to avoid getting blocked by Google
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

            # fetch the search results page
            response=requests.get(f"https://www.flipkart.com/search?q={query}&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&as-pos=1&as-type=RECENT&suggestionId=iphone+14+pro+max%7CMobiles&requestId=43365810-76a8-4c73-80cd-c2e9ec1f66f6&as-backfill=on",verify=False)

             # parse the HTML using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")
            rating=""
            comment=""
            reviewer=""
            key_value_list=[]
            for div in soup.find_all("div", attrs={"class":"row"}):
                for rating in div.find_all("div", attrs={"class":"_1BLPMq"}):
                        for element in rating:
                            if element.string:
                                #print(f"Rating : {element.string.strip()}")
                                rating = element.string.strip()
                for comment in div.find_all("p", attrs={"class":"_2-N8zT"}):
                        for element in comment:
                            if element.string:
                                #print(f"comment : {element.string.strip()}") 
                                comment = element.string.strip()
                for reviewer in div.find_all("p", attrs={"class":"_2sc7ZR" and "_2V5EHH"}):
                        for element in reviewer:
                            if element.string:
                                #print(f"reviewer : {element.string.strip()}") 
                                reviewer = element.string.strip()
                if rating != '' and comment!='' and reviewer!='':
                        key_value_pairs = {"rating": rating , "comment": comment , "reviewer": reviewer}   
                        rating=""
                        comment=""
                        reviewer=""
                        key_value_list.append(key_value_pairs)
            #logging.info("key_value_list: %s" % key_value_list)
            return render_template('result.html',results=key_value_list)            
            #return "image loaded"
        except Exception as e:
            logging.exception("Error:",e)    
            return 'something is wrong'
    else:
        logging.info("Enetered non Post Method")   
        return 'something is wrong'
    return 'something is wrong'   
if __name__ == '__main__':
    app.run(debug=True)