from twython import Twython, TwythonError, TwythonStreamer # Main twython module + error catch
import sys
import time #Used to sleep
import re
import datetime # Used to identify date / time for logs
import os #used for file stuff
import random #used for random quotes
import urllib#USed to check the page so it is a real article

app_key = "aaaaa" # Api Key
app_secret = "aaaaa" # Api secret
oauth_token = "aaaaa" #Access token
oauth_token_secret = "aaaaa" # Access secret
twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)#,timeout=300,retry_count=5,retry_in=30) #Sets up so don't need to rewrite keys 50 billion times

suffixes=['J','JP','EX']
internationals=['RU','KO','CN','FR','PL','ES','TH','JP','DE','IT','UA','PT','CS','INT']




class MyStreamer(TwythonStreamer): #used to search
    def on_success(self, tweet):
        tweetFunc(tweet)
            

    def on_error(self, status_code, data): #on streaming error, normally caused by a timeout
        print(status_code)
        # errorcounter=errorcounter+1
        # errortxt = (" "+current_datetime+"- !!CRASH!! - Tweetcount="+str(tweetcounter)+"-"+" Errorcount="+str(errorcounter)+" Error:"+str(status_code)+"\n"+"\n")
        # log(errortxt)
        print ("--------------------------------------------------------------------------------------------------")                    
        search()

def search():
    #print("Search func")#TESTING
    while True:
        try:
            tweet = MyStreamer(app_key, app_secret,oauth_token, oauth_token_secret)
            tweet.statuses.filter(track='SCP,scp,Scp',tweet_mode='extended')              
        except TwythonError as e:
            print("Crashed: ",e)



def tweetFunc(tweet):
    user_id, text,username,reply_id = get_data(tweet)
    print("User ID:",user_id)
    print("Username:",username)
    print("Reply ID:",reply_id)
    print("User's tweet:",text)

    textSorted=text_sort(text)
    if validate(textSorted,user_id)==True:
        if len(get_index(textSorted))>=1:
            message,imagepath=composeTweet(get_index(textSorted),username)
            if len(message)>2:#If the message has substance to it so versatile knife hmm very sharp have a whiff SNIFFFFFFFFF fuuuuck me thats some good stuff
                image = open(imagepath, 'rb') # Image path
                image_part = twitter.upload_media(media=image)


                try:
                    twitter.update_status(status=message,media_ids=[image_part['media_id']],in_reply_to_status_id=reply_id)
                    print("Tweeted!")
                except Exception as e:
                    try:
                        print("Error Tweeting, retrying")
                        print(e)
                        timed_delay(10)
                        twitter.update_status(status=message,media_ids=[image_part['media_id']],in_reply_to_status_id=reply_id)
                        print("Tweeted!")
                    except Exception as e:
                        print("Error Tweeting for the second time, removing image")
                        print(e)
                        timed_delay(30)
                        twitter.update_status(status=message,in_reply_to_status_id=reply_id)
                        print("Tweeted!")

                print("--------------------------------------------------")


            else:
                print("--------------------------------------------------")
        else:
            print("--------------------------------------------------")

def text_sort(text):
    removables=["'s",'_','-','.','!','?',':',';',",",'(',')','#','"',"'",'*',"[","]","“"]
    for removable in removables:
        text=text.replace(removable,' ')

    text=text.upper()
    text=text.split()
    text.append(' ')
    text.append(' ')

    return text

def get_data(tweet):
    reply_id = (tweet['id'])
    user_id = tweet['user']['id_str']
    username = tweet['user']['screen_name']
    post_id = tweet['id_str'] # Used to reply to the tweet in a thread format
    try:
        reply_id=tweet['retweeted_status']['id']
        print("Tweet is a retweet")
    except:
        print("Not a retweet")
    full_tweet = twitter.show_status(id=reply_id, tweet_mode='extended')
    text=(full_tweet['full_text'])

    return user_id,text,username,reply_id

def validate(text,user_id):
    
    whitelistFile=open("whitelist.txt","r")
    whitelist=whitelistFile.read().splitlines()
    whitelistFile.close()
    if user_id in whitelist:
        if "SCP" in text:
            if isInt(text[text.index("SCP")+1]):
                print("Tweet is valid")
            return True
        else:
            print("Tweet is invalid")
            print("--------------------------------------------------")

            return False
    else:
        print("\n User isn't whitelisted")
        print("--------------------------------------------------")

        return False

def isInt(SCPindex):
    try:
        SCPindex=int(SCPindex)
        return True
    except:
        return False


def get_index(text):
    indexes=[]
    for location, word in enumerate(text, start=0):
        if word=="SCP":
            SCPindex=text[location+1]
            if isInt(SCPindex)==True:
                if len(str(SCPindex))==1:
                    SCPindex=str(SCPindex)
                    SCPindex=("00"+SCPindex)
                elif len(str(SCPindex))==2:
                    SCPindex=str(SCPindex)
                    SCPindex=("0"+SCPindex)

                if text[location+2] in suffixes or text[location+2] in internationals:
                    SCPindex=SCPindex+"-"+text[location+2]
            
                indexes.append(SCPindex)
    
    print("Found:",indexes)
    indexes=removeDuplicates(indexes)

    return indexes

def isReal(SCPurl):#Checks if an article exists
    try:#An article does not exist if an error is found trying to decode the site
        with urllib.request.urlopen(SCPurl) as url:
            site = url.read() #Reads the html code
            site=site.decode("utf-8")#Decodes the site
            if "This page doesn't exist yet!" in site:#Main title of the error site
                print(SCPurl,"is not a real article")
                return False
            else:#If page doesnt exist is not found on the page
                print(SCPurl," is a real article")
                return True
    except Exception as e:#Any other error
        print("Error looking up:",SCPurl)
        print(e)
        return False
            
def getURL(SCPindex):
    url="http://www.scpwiki.com/scp-"+SCPindex
    
    searchSCPindex=SCPindex.split('-')#Splits the index string at the -

    try:
        if searchSCPindex[1] in internationals: #Checks if any intl suffixes are in the index
            url="http://scp-int.wikidot.com/scp-"+SCPindex #Swaps index to the intl site
            
    except:        #Error catching for if the index has no  suffix
        url="http://www.scpwiki.com/scp-"+SCPindex

    if isReal(url)==False:
        url=str("http://scp-"+searchSCPindex[1]+".wikidot.com/scp-"+SCPindex)
        if isReal(url)==False:
            url="SCP-"+SCPindex+":[𝗗𝗔𝗧𝗔 𝗘𝗫𝗣𝗨𝗡𝗚𝗘𝗗]"
        
    return url

def composeTweet(indexes,username):
    tweet="@"+username+" "
    imagepath=""

    if len(indexes)==1:#If only one index in tweet
        tweet = tweet +source_quote(indexes[0])#Get a specific quote
        imagepath=str(source_image(indexes[0],suffix))
    else:
        imagepath="Anomalous_Animation_lores.gif"
     
        

    for SCPindex in indexes:
        tweet=tweet+getURL(SCPindex)+"\n"

    print("Tweet:"+tweet)
    return tweet,imagepath

def source_quote(SCPindex):
    #resets vars from last run
    quote=""
    global suffix
    suffix=""
    if isInt(SCPindex)==False:#If index isn't on its' own (eg has -j at end)
        suffix=(SCPindex.split('-'))
        suffix=suffix[1]
        print("Suffix:",suffix)

    quotefile=('Quotes/quotes'+suffix+".txt")
    if suffix==" ":
        quotefile=("Quotes/quotes.txt")
    print("QuoteFile:",quotefile)
    quotefile=open(quotefile,"r+",errors="ignore")
    quotelines=quotefile.readlines()

    try:
        SCPindex=SCPindex[0:(SCPindex.index('-'))]#Cuts the index to just the string
    except:
        pass

    SCPindex=int(SCPindex)

    try:
        quote=str(quotelines[SCPindex-1]) #finds the correct quote by searching through the lines array(?) and looking for the index-1 (arrays start at 0)
        quote.replace("\n","")
        print("Specific Quote:",quote)

    except Exception as e:
        print("No specific quote found")
        print(e)

    if len(quote)<=3: #if no quote was found in the file
        miscquotefile=open('Quotes/quotesMisc.txt','r')            
        lines=miscquotefile.readlines() #reads all lines
        linecount=len(lines) #reads all lines            
        miscIndex=random.randint(0,linecount-1)
        quote=str(lines[miscIndex]) #finds the correct quote by searching through the lines array(?) and looking for the index-1 (arrays start at 0)
        print("Misc Quote:",quote)   

    return quote

def source_image(index,suffix):
    global imagepath
    print("Suffix:",suffix,"End")
    imagepath=('images_v3/'+suffix+"/"+str(index)+".png")
    if "images_v3//" in imagepath:
        imagepath=("images_v3/Main/"+str(index)+".png")    
    print("Image Path:",imagepath)
    if os.path.isfile(imagepath)==True:#if the file path shows an actual file
        print("Image found:"+imagepath)
        return imagepath
    else:
        print("No image found, using gif")
        imagepath="Anomalous_Animation.gif"
        return imagepath

def removeDuplicates(indexes):#removes duplicates from the list (duh)
    return list(set(indexes))
    


def log(text):

    logfile=open("Annie_log.txt","a")
    logfile.write((text+"\n"))


def timed_delay(timer):
    erase_line = '\x1b[2K' # USed for animated text
    cursor_up = '\x1b[1A'
    while timer>0: 
        searchprint = "Sleeping for "+str(timer)+" seconds"
        print(searchprint)
        timer=timer-1
        sys.stdout.write(cursor_up) #goes up a line
        sys.stdout.write(erase_line) #erases the line
        time.sleep(1)

#main
#search()
print("Started A.N.N.I.E")
while True:
    try:
         search()
    except Exception as e:
        print(e)
        time.sleep(5)
