from twython import Twython, TwythonError
import sys
import time
import datetime # Used to identify date / time for logs


app_key = "aaaaa" # Api Key
app_secret = "aaaaa" # Api secret
oauth_token = "aaaaa" #Access token
oauth_token_secret = "aaaaa" # Access secret

twitter = Twython(app_key,app_secret,oauth_token,oauth_token_secret)


erase_line = '\x1b[2K' # USed for animated text
cursor_up = '\x1b[1A'



def loadCurrent():

    global curFollowers
    global prevfollowercount
    
    whitelist = open("whitelist.txt","r")
    curFollowers=whitelist.read().splitlines()
    whitelist.close()
    
    
    if len(curFollowers) != prevfollowercount:
        print("Loaded",len(curFollowers),"users from file")
        prevfollowercount=len(curFollowers)
        print ("--------------------------------------------------------------------------------------------------")  
    

def findNew():
    global newFollowers
    global unfollowed

    print("Searching for follower changes...")

    foundFollowers=[]
    unfollowed=[]
    newFollowers = []

    newcount=0
    lostcount=0
    next_cursor = -1
    whitelist = open("whitelist.txt","a")

    #print("Finding new followers")#TESTING
    cursorVal=1
    retryCount=0
    while(next_cursor):
        try:
            get_followers = twitter.get_followers_list(screen_name="AnomalousBot",count=200,stringify_ids=True,cursor=next_cursor)
            print("Cursor",cursorVal,":",len(get_followers["users"]))    #TESTING
            cursorVal=cursorVal+1
            for follower in get_followers["users"]:            
                followerId=(str(follower["id"]))#.decode("utf-8"))           
                foundFollowers.append(followerId)
                next_cursor = get_followers["next_cursor"]

        except TwythonError as e:#Shorter delay when fails just on one cursor lookup
            print(e)
            retryCount+=1
            search_delay(70*retryCount)
    #print(foundFollowers)#TESTING

        #does comparisons with the full found array
    for follower in foundFollowers:
        if follower not in curFollowers: #if follower is new
            newFollowers.append(follower)
    #print(newFollowers)

    for follower in curFollowers:
        if follower not in foundFollowers:
            unfollowed.append(follower)

        #clears file and adds foundFollowers into it
    whitelist.truncate(0) #clears the file
    #print("Cleared old followers")#TESTING
    for follower in foundFollowers:
        whitelist.write(follower)
        whitelist.write("\n")            
    whitelist.close()
    
    sys.stdout.write(cursor_up) #goes up a line
    sys.stdout.write(erase_line) #erases the line


def sendMessages():
    global tweetcounter
    global errorcounter

    followtext="Hi! You have followed me, so I will now provide links to any SCPs you mention! Here's more info on how to use this bot: https://t.co/DeiHW5uPKp"
    unfollowtext="Hi! You have unfollowed me, so I will no longer provide you with links to SCPs that you mention. Changed your mind? Just follow me again! (And wait 10 mins)"

    #gets usernames from ID's
    newFollowerUsernames=[]
    unfollowedUsernames=[]
    print("Found",len(newFollowers),"new followers")
    print(newFollowers)

    for Id in newFollowers:
        lookup=twitter.lookup_user(user_id=Id)
        for user in lookup:
            print(Id)
            username=(user["screen_name"])
            print(username)
            newFollowerUsernames.append(username)

    for userId in unfollowed:
        lookup=twitter.lookup_user(user_id=userId)
        for user in lookup:
            print(userId)
            username=(user["screen_name"])
            print(username)
            unfollowedUsernames.append(username)

    
    if len(newFollowerUsernames)>0:
        print("New followers:",newFollowerUsernames)
        for user in newFollowerUsernames:
            message=("@"+user+" "+followtext)
            message=str(message)
            print(message)
            try:
                twitter.update_status(status=message)
                print("Tweeted:",message)
                tweetcounter=tweetcounter+1
                succLog(message,tweetcounter,errorcounter)
                search_delay(60)
            except TwythonError as error:              
                print("Did not tweet",error)
                errorcounter=errorcounter+1
                errorLog(message,tweetcounter,errorcounter,error)
        

def search_delay(timer):
    while timer>0: 
        searchprint = "Sleeping for "+str(timer)+" seconds"
        print(searchprint)
        timer=timer-1
        sys.stdout.write(cursor_up) #goes up a line
        sys.stdout.write(erase_line) #erases the line
        time.sleep(1)


def succLog(message,tweetcounter,errorcounter):
    current_datetime_full = datetime.datetime.now()
    current_datetime=current_datetime_full.strftime("%Y-%m-%d %H:%M")

    logfile = open("Freddy_log.txt","a") #Opens log file to log
    logfile.write(" "+current_datetime+"- Tweeted - Tweetcount="+str(tweetcounter)+"-"+" Errorcount="+str(errorcounter)+" Message:"+message+"\n"+"\n")
    logfile.close()

def errorLog(message,tweetcounter,errorcounter,error):
    current_datetime_full = datetime.datetime.now()
    current_datetime=current_datetime_full.strftime("%Y-%m-%d %H:%M")

    logfile = open("Freddy_log.txt","a") #Opens log file to log
    logfile.write(" "+current_datetime+"- !!ERROR!! - Tweetcount="+str(tweetcounter)+"-"+" Message:"+str(message)+" Errorcount="+str(errorcounter)+" Error:"+str(error)+"\n"+"\n")
    logfile.close()


#main_________________________________

tweetcounter=0
errorcounter=0

prevfollowercount=0



print("\n"*30)
print('''
  ___                              _                  ______       _      
 / _ \                            | |                 | ___ \     | |     
/ /_\ \_ __   ___  _ __ ___   __ _| | ___  _   _ ___  | |_/ / ___ | |_    
|  _  | '_ \ / _ \| '_ ` _ \ / _` | |/ _ \| | | / __| | ___ \/ _ \| __|   
| | | | | | | (_) | | | | | | (_| | | (_) | |_| \__ \ | |_/ / (_) | |_    
\_| |_/_| |_|\___/|_| |_| |_|\__,_|_|\___/ \__,_|___/ \____/ \___/ \__|   
                                                                          
                                                                          
______    _ _                              ______ _           _           
|  ___|  | | |                             |  ___(_)         | |          
| |_ ___ | | | _____      _____ _ __ ______| |_   _ _ __   __| | ___ _ __ 
|  _/ _ \| | |/ _ \ \ /\ / / _ \ '__|______|  _| | | '_ \ / _` |/ _ \ '__|
| || (_) | | | (_) \ V  V /  __/ |         | |   | | | | | (_| |  __/ |   
\_| \___/|_|_|\___/ \_/\_/ \___|_|         \_|   |_|_| |_|\__,_|\___|_|   
                                                                         
V1
                                                                          ''')
print ("--------------------------------------------------------------------------------------------------")  
while True:

    try:
        #print("Finding new users")
        loadCurrent()
        findNew()
        sendMessages()
        search_delay(950)
    except Exception as e:
        print("Error:",e)
        search_delay(360)

