This web application is an RSS feed parser made in Python. The user of this application can enter the link to an RSS feed and a search phrase and will be presented with all the articles from the RSS feed related to that search phrase. 

I created this project becuase I am very interested in the New York Yankees. I wanted a way where I could stay caught up on all the latest Yankees news from ESPN. I started off by making a python application where the user could enter the RSS feed and search phrase in the terminal. I then deicded I could make the application more user friendly with a website where the user could enter any RSS feed and filter the results with a search phrase.

I created this application with Flask and HTML styled with CSS. The link and search phrase from the HTML forms are sent to the Flask portion of the application and used to open and parse the RSS feed. Articles are only included if they have some relation to the search phrase. This is accomplished with a regular expression. When parsing the RSS feed articles are only considered related if the search phrase is present somewhere in the title or description of the article. An HTML template is then returned to the user with all the related articles including their title (hyperlinked), date published, and image if present.
