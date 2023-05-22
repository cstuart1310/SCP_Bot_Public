import random
import sys
import time
from twython import Twython, TwythonError
import os
import datetime # Used to identify date / time for logs
import functools 
import operator  

app_key = "aaaaa" # Api Key
app_secret = "aaaaa" # Api secret
oauth_token = "aaaaa" #Access token
oauth_token_secret = "aaaaa" # Access secret

twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)#,timeout=300,retry_count=5,retry_in=30) #Sets up so don't need to rewrite keys 50 billion times
imagepath=""
erase_line = '\x1b[2K' # USed for animated text
cursor_up = '\x1b[1A'
tweet=""



print("\n"*50)#clears the screen

def search_delay(timer):
    while timer>0:        
        searchprint = "Sleeping for "+str(timer)+" seconds"
        print(searchprint)
        timer=timer-1
        sys.stdout.write(cursor_up) #goes up a line
        sys.stdout.write(erase_line) #erases the line
        time.sleep(1)


def source_image(index):
    global imagepath
    imagepath=('images/'+str(index)+".png")
    #print(imagepath)
    if os.path.isfile(imagepath)==True:#if the file path shows an actual file
        print("Image found:"+imagepath)#TESTING

        return True
    else:
        print("No image found")#TESTING
        return False


print("------------------------------------------------------------------------")
current_datetime_full = datetime.datetime.now()#Gets current date time
current_datetime=current_datetime_full.strftime("%Y-%m-%d %H:%M")#Truncates it
current_date=current_datetime_full.strftime("%Y-%m-%d")#current date
                                                
index = random.randint(1,4999)#Picks a random int
print(current_datetime)
print("Index:",index)

titlefile=open("titles.txt","r")
for fileloop, line in enumerate(titlefile):
    if fileloop == index-1:
        tweet=line
#titlelines=titlefile.readlines()    
#tweet=str(titlelines[index-1])
tweet=("-----Today's Daily SCP Article----- \n             "+current_date+"\n \n"+tweet+"http://www.scp-wiki.net/scp-"+str(index))
print(tweet)
#tweet=(tweet,)





if source_image(index)==True:
    search_delay(30)
    print("Included image")
    try:
        image = open(imagepath, 'rb') # Image path   
        image_part = twitter.upload_media(media=image)           
    except:
        print("Error uploading image")
        time.sleep(60)
        image = open(imagepath, 'rb') # Image path   
        image_part = twitter.upload_media(media=image)            
    try:            
        twitter.update_status(status=tweet,media_ids=[image_part['media_id']])
        
    except TwythonError as e:
        print("Error tweeting, sleeping incase timeout")
        print(e)
        #search_delay(120)            
        twitter.update_status(status=tweet,media_ids=[image_part['media_id']])
else:
    print("Did not include an image")
    try:
        twitter.update_status(status=tweet)
    except TwythonError as e:
        print("Error, sleeping incase timeout")
        print(e)
        search_delay(120)
        
        twitter.update_status(status=tweet)
        
print("Tweeted:",tweet)
    

#1138521666294861834-mPzjYSpYhOZnGpVfkeMJNZZaHbzazQ
#o3YyHUWA2ufSCVjUQEbQMEgRSVaYRm6wjBFcDz0qYOu9E
