import random
from twython import Twython, TwythonError
import datetime # Used to identify date / time for logs
app_key = "aaaaa" # Api Key
app_secret = "aaaaa" # Api secret
oauth_token = "aaaaa" #Access token
oauth_token_secret = "aaaaa" # Access secret
twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)#,timeout=300,retry_count=5,retry_in=30) #Sets up so don't need to rewrite keys 50 billion times

taleFile=open("talesOut.txt","r")
taleLines=taleFile.readlines()
index=random.randint(1,len(taleLines))

print("------------------------------------------------------------------------")
current_datetime_full = datetime.datetime.now()#Gets current date time
current_datetime=current_datetime_full.strftime("%Y-%m-%d %H:%M")#Truncates it
current_date=current_datetime_full.strftime("%Y-%m-%d")#current date
                                                
print(index)
fullLine=taleLines[index]
line=fullLine.split("TITLE: ")
taleUrl=line[0]
for title in line:
    title=title.replace("\n","")
print(index,taleUrl,title)

tweet=("-----Today's Daily SCP Tale----- \n             "+current_date+"\n"+title+"\n"+taleUrl)
print(tweet)
twitter.update_status(status=tweet)
