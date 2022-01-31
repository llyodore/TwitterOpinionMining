import tkinter as tk
import tweepy
from afinn import Afinn

class CButton:
    def __init__(self,value,button):
        self.value = value
        self.button = button
        
def getTweetsFromKeyword(keyword):
    k = keyword + " -filter:retweets"
    with open("result.txt", "a", encoding="utf-8") as f:
        f.write("!!trend!! = " + keyword + "\n")
        try:
            search_results = api.search(q=k, count=100,result_type="recent", lang="en", tweet_mode ="extended")
            maxid = 0
            for x in range(1,100):
                for i in search_results:
                    if(maxid != i.id):
                        #print(i.retweet_count)
                        #print(i.favorite_count)
                        #print(i.id)
                        #print(i.full_text)
                        f.write("!!id!! = " + str(i.id_str) + "\n")
                        f.write("!!rt!! = " + str(i.retweet_count) + "\n")
                        f.write("!!fav!! = " + str(i.favorite_count) + "\n")
                        f.write(i.full_text)
                        f.write("\n!!tweetEnd!!\n")
                        maxid = i.id
                    else:
                        print(i.id)
                        f.close()
                        return
                    search_results  = api.search(q=k, count=100, result_type="recent", lang="en", tweet_mode ="extended", max_id = maxid-1)
            f.write("!!trendEnd!!\n")
            f.close()
            print("End of search")
            return
        except tweepy.RateLimitError:
            print("Rate limit exceeded")
            f.write("!!trendEnd!!\n")            
            f.close()
            return
        except:
            print("End: file closed or rate limit exceeded")
            return 

           
def readAndScoreTweets():
    afinn = Afinn(language='en')
    with open("result.txt", "r", encoding="utf-8") as f:
        for ligne in f.readlines():
            if("!!trend!! = " in ligne):
                nbTweets = 0
                posTweets = 0
                negTweets = 0
                neuTweets = 0
                score = 0
                idt = 0
                fav = 0
                rt = 0
                text = ""
                trend = ligne.partition("!!trend!! = ")[2]
                print("\nTrend : " + trend)
            elif("!!trendEnd!!" in ligne):
                print("\nResultats sur la tendance " + trend)
                print("Avis neutres : ",neuTweets,"\n")
                print("Avis negatifs : ",negTweets,"\n")
                print("Avis positifs : ",posTweets,"\n")
                if(nbTweets != 0):
                    print("Score moyen : ",score/nbTweets,"\n")
            else:
                if("!!id!! = " in ligne):
                    text = ""
                    idt = ligne.partition("!!id!! = ")[2]
                    idt = int(idt)
                    print("Id : ", idt)
                elif("!!rt!! = " in ligne):
                    rt = ligne.partition("!!rt!! = ")[2]
                    rt = int(rt)
                    print("Rt : ", rt)
                elif("!!fav!! = " in ligne):
                    fav = ligne.partition("!!fav!! = ")[2]
                    fav = int(fav)
                    print("Fav : ", fav)
                elif("!!tweetEnd!!" in ligne):
                    print(text)
                    t_score = afinn.score(text)
                    print("Score : ", t_score, "\n")
                    score += t_score
                    if(t_score > 0):
                        nbTweets += 1
                        posTweets += 1
                    elif(t_score < 0):
                        nbTweets += 1
                        negTweets += 1
                    else:
                        neuTweets += 1
                else:
                    text += ligne


def searchTweets(checkButtons):
     for cb in checkButtons:
         if cb.value.get():
             search = cb.button.cget("text")
             print("Trend:" + search)
             getTweetsFromKeyword(search)

def getTrends(WOEID):
    trendsP = api.trends_place(WOEID) #Renvoi les tendances sous forme de JSON
    data = trendsP[0] #Récupère le contenu du JSON
    trends = data['trends'] #Récupère les éléments 'trends' du JSON
    names = [trend['name'] for trend in trends] #Récupère l'élément 'name' de chaque tendance
    return names
    
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

PARIS_WOEID = 615702
NEW_YORK_WOEID = 2459115

auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


top = tk.Tk()
 
names = getTrends(PARIS_WOEID)

i = 0
j = 0
checkbuttons = []
for name in names:
    checkVar = tk.IntVar()
    checkbox = tk.Checkbutton(top, text = name, variable = checkVar, onvalue = 1, offvalue = 0)
    checkbuttons.append(CButton(checkVar,checkbox))
    checkbox.grid(row=i,column=j)
    i = i +1
    if i == 10:
        i = 0
        j = j + 1
    
searchButton = tk.Button(top, text ="Search tweets", command = lambda: searchTweets(checkbuttons))
searchButton.grid(row = 11,column = 1)

readButton = tk.Button(top, text = "Read and Score tweets", command = readAndScoreTweets)
readButton.grid(row = 11, column = 3)
top.mainloop()
