import praw, re


#API details, look up the praw documentation on how to register these variables
reddit = praw.Reddit(client_id='',
client_secret='',
username='',
password='',
user_agent='')


def subredditScrape(subredditName, dictionary_placeholder):
    subreddit = reddit.subreddit(subredditName)
    #This limit sets how many of the most recent posts you want to search for, right now it only takes the 500 most recent
    new_python = subreddit.new(limit=500)
    emptyDict = dictionary_placeholder

    #Regex for finding stocks
    RE_INT = re.compile(r'^[-+]?([1-9]\d*|0)$')
    
    #Going thorugh each submission
    for submission in new_python:
        #If its not stickied
        if not submission.stickied:
            #Contains a dollar symbol in the title to indicate a stock ticker
            if ('$') in submission.title:
                onlyTicker = submission.title.split(" ")
                for item in onlyTicker:
                    if ('$') in item:
                        #Stripping all unecessary characters
                        item = item.strip('()?:;.[],')
                        #Stock tickers need to be longer than 3 characters4
                        if len(item) > 3:
                            if RE_INT.match(item[-1]) == None and item[-1] != "k" and item[-1] != "$" and item[-2:] != "MM":
                                #If the item is in the dictionary, we append one more to the counter
                                if item in emptyDict.keys():
                                    emptyDict[item] += 1
                                #If not add the new ticker
                                else:
                                    emptyDict[item] = 1

    #Sort the dictionary to be descending
    sorted_dict = dict( sorted(emptyDict.items(),
                           key=lambda item: item[1],
                           reverse=True))

    sorted_dict = {key:val for key, val in sorted_dict.items() if val != 1}

    #Removing all the most common stocks that have already been hyped up and perhaps beyond their prime
    sorted_dict.pop('$GME', None)  
    sorted_dict.pop('$AMC', None) 
    sorted_dict.pop('$BB', None) 
    sorted_dict.pop('$NOK', None)            
    return(sorted_dict)


#All the subreddits we want to scrape
#If you want to add another, just copy the last variable name and add that as the dictionary placeholder in the
WSB = subredditScrape('wallstreetbets', {})
pennyStocks = subredditScrape('pennystocks', WSB)
robinhoodPennyStocks = subredditScrape('RobinHoodPennyStocks', pennyStocks)
WallStreetbetsELITE = subredditScrape('WallStreetbetsELITE', robinhoodPennyStocks)
stocks = subredditScrape('stocks', WallStreetbetsELITE)


for key, values in stocks.items():
    print(key.strip('$'))

for key, values in stocks.items():
    print(values)

