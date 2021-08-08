from bs4 import BeautifulSoup # reads rss feed
from urllib.request import urlopen
import urllib.error
import re # regular expression
from flask import *
from werkzeug.exceptions import Forbidden

app = Flask(__name__)

# This functions searches an rss feed and returns a list with 
# article information from articles related to the search phrase
def searchRSSFeed(RSSFeedURL, searchPhrase):
    # userAgent = Request(RSSFeedURL, headers={'User-Agent':'Chrome/5.0'})
    # Work on try catch for invalid URLs. also still getting forbidden error
    xmlURL = urlopen(RSSFeedURL)        
    soup = BeautifulSoup(xmlURL, "xml")
    articlesInFeed = soup.find_all("item")
    regExpression = re.compile("(?i)" + searchPhrase)

    # list that holds information of articles related to the search phrase
    relatedArticles = [] 

    for article in articlesInFeed:
        # dictionary that holds information from each article
        articleInfoDict = {}
        # has all information
        if article.title != None and article.link != None and article.image != None and article.pubDate != None and article.description != None: 
            if regExpression.findall(article.title.text) != [] or regExpression.findall(article.description.text) != []:
                articleInfoDict['title'] = article.title.text
                articleInfoDict['link'] = article.link.text
                articleInfoDict['image'] = article.image.text
                articleInfoDict['published'] = article.pubDate.text
                articleInfoDict['description'] = article.description.text
                relatedArticles.append(articleInfoDict)
        # has all except image
        elif article.title != None and article.link != None and article.image == None and article.pubDate != None and article.description != None: 
            if regExpression.findall(article.title.text) != [] or regExpression.findall(article.description.text) != []:
                articleInfoDict['title'] = article.title.text
                articleInfoDict['link'] = article.link.text
                articleInfoDict['published'] = article.pubDate.text
                articleInfoDict['description'] = article.description.text
                relatedArticles.append(articleInfoDict)
        # has all except description
        elif article.title != None and article.link != None and article.image != None and article.pubDate != None and article.description == None: 
            if regExpression.findall(article.title.text) != []:
                articleInfoDict['title'] = article.title.text
                articleInfoDict['link'] = article.link.text
                articleInfoDict['image'] = article.image.text
                articleInfoDict['published'] = article.pubDate.text
                relatedArticles.append(articleInfoDict)
        # has all except image, pubDate, and description
        elif article.title != None and article.link != None and article.image == None and article.pubDate == None and article.description!= None: 
            if regExpression.findall(article.title.text) != []:
                articleInfoDict['title'] = article.title.text
                articleInfoDict['link'] = article.link.text
                articleInfoDict['published'] = article.pubDate.text
                articleInfoDict['description'] = article.description.text
                relatedArticles.append(articleInfoDict)

    return relatedArticles

# api end point
@app.route("/", methods=['GET', 'POST'])
def relatedArticles():
    # load page
    if request.method == "GET":
        return render_template("homePage.html")
    # user search
    elif request.method == "POST": 
        RSSFeed = request.form.get("RSSFeed")
        searchPhrase = request.form.get("searchPhrase")

        try: # If the link is invlaid
            relatedArticles = searchRSSFeed(RSSFeed, searchPhrase)
        except ValueError and urllib.error.HTTPError: 
            return render_template("linkError.html")

        # if there are not related articles
        if relatedArticles == [] and searchPhrase == '': # no related articles
            return render_template("noSearchResultsNoSearchPhrase.html", RSSFeed=RSSFeed)
        elif relatedArticles == []:
            return render_template("noSearchResultsSearchPhrase.html", searchPhrase = searchPhrase, RSSFeed = RSSFeed)
        
        # everything worked
        if 'image' in relatedArticles[0]: # has an image
            return render_template("searchResultsHasImage.html", relatedArticles = relatedArticles, numberOfSearchResults = len(relatedArticles))
        else:
            return render_template("searchResultsNoImage.html", relatedArticles = relatedArticles, numberOfSearchResults = len(relatedArticles))


if __name__ == "__main__":
    app.run()

