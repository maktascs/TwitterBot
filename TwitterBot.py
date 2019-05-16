import tweepy
from tkinter import *
import os
import time
import config
import praw
import urllib.request as ur

from prawcore.exceptions import Redirect
from prawcore.exceptions import ResponseException
from urllib.error import HTTPError

class TwitterBot:
    E1= None
    E2= None
    E3= None
    E4= None
    E5= None
    E6= None
    E7= None
    limit = None
    subR = None
    status = None
    postImgBtn=None
    #Reddit Info
    client_id = config.REDDIT['client_id']
    client_secret =config.REDDIT['client_secret']


    def __init__(self, root):
        frame = Frame(root,bd=1, relief=RIDGE, pady=10,height=300,width=400,padx=10)
        frame.grid_propagate(False)
        frame.grid(row=0,column=0)

        rightFrame = Frame(root,bd = 1 , relief=RIDGE,pady=10,height=300,width=400,padx=10)
        rightFrame.grid_propagate(False)
        rightFrame.grid(row=0,column=1)


        Label(frame, text="Twitter Bot", font=("Helvetica", 16)).grid(columnspan=2)
        Label(frame,text="Search").grid(row=1)
        self.E1 = Entry(frame, width=40)
        self.E1.grid(row=1,column=1)

        Label( frame, text="Number of Tweets").grid(row=2)
        self.E2 = Entry(frame, width=40)
        self.E2.grid(row=2,column=1)

        Label( frame, text="Response").grid(row=3)
        self.E3 = Entry(frame, width=40)
        self.E3.grid(row=3,column=1)

        Label( frame, text="Reply?").grid(row=4)
        self.E4 = IntVar()
        chk4 = Checkbutton(frame, variable=self.E4, width=40)
        chk4.grid(row=4,column=1)

        Label( frame, text="Retweet?").grid(row=5)
        self.E5=IntVar()
        chk5 = Checkbutton(frame, variable=self.E5, width=40)
        chk5.grid(row=5,column=1)

        Label( frame, text="Favorite?").grid(row=6)
        self.E6=IntVar()
        chk6 = Checkbutton(frame, variable=self.E6, width=40)
        chk6.grid(row=6, column=1)

        Label( frame, text="Follow?").grid(row=7)
        self.E7=IntVar()
        chk7 = Checkbutton(frame, variable=self.E7, width=40)
        chk7.grid(row=7,column=1)

        button = Button(frame, width=40, bg="#008080",fg="white", text ="Submit", command = self.main,pady=20).grid(row=8,columnspan=2)
        #button.grid(row=7,columspan=2)
        
        Label(rightFrame, text="Scrape Images from Reddit?",font=("Helvetica", 16)).grid(row=9,columnspan=2)
        Label(rightFrame, text="Enter Subreddit:").grid(row=10)
        self.subR = Entry(rightFrame,width=40)
        self.subR.grid(row=10,column=1)

        Label( rightFrame, text="Enter Limit:").grid(row=11)
        self.limit = Entry(rightFrame, width=40)
        self.limit.grid(row=11,column=1)
        Button(rightFrame,bg="#5cb85c", width=17 ,pady=10,fg="white", text="Open ImagesFolder",command = self.openResults ).grid(row=12)
        Button(rightFrame,bg="#0275d8", width=20 ,pady=10,fg="white",text="Scrape Images", command = lambda:self.scraperMain(self.subR.get(),int(self.limit.get()))).grid(row=12,column=1)
        
        Label(rightFrame, text="Do you want to post images to Twitter?", font=("Helvetica",12)).grid(row=13,columnspan=2)
        Label(rightFrame, text="Status:").grid(row=14)
        self.status = Entry(rightFrame, width=40)
        self.status.grid(row=14,column=1)
        self.postImgBtn =  Button(rightFrame,bg="#d9534f",state=NORMAL, width=30 ,pady=10,fg="white", text="Post Images",command = lambda: self.postImages(self.status.get()) ).grid(row=15, columnspan=2)

    def postImages(self,status=""):
         
            

            
            os.chdir('results')
            i = 1
            
            for image in os.listdir('.'):
                if self.is_img_link(image):
                    api.update_with_media(image, status=status)
                    print ("Posting Image: ",i)
                    i+=1
                    os.remove(image)
                    time.sleep(3)
          

    def openResults(self):
        os.startfile('.\Results')


    def get_img_urls(self,sub, li):
        try:
            r = praw.Reddit(client_id=self.client_id, client_secret=self.client_secret, user_agent='Reddit_Image_Scraper')
            submissions = r.subreddit(sub).hot(limit=li)

            return [submission.url for submission in submissions]

        except Redirect:
            print("Invalid Subreddit!")
            return 0

        except HTTPError:
            print("Too many Requests. Try again later!")
            return 0

        except ResponseException:
            print("Client info is wrong. Check again.")
            return 0

    def scraperMain(self, sub,li):
        self.subR.delete(0,'end')
        self.limit.delete(0,'end')
        file_no = 1
        url_list = self.get_img_urls(sub, li)
        if url_list:

            self.save_list(url_list)
            count, status = self.read_img_links()

            if status == 1:
                print('\nDownload Complete\n{} - Images Downloaded\n{} - Posts Ignored'.format(count, li - count))
            elif status == 0:
                print('\nDownload Incomplete\n{} - Images Downloaded'.format(count))

        self.delete_img_list()

    def save_list(self,img_url_list):
        for img_url in img_url_list:
            file = open('img_links.txt', 'a')
            file.write('{} \n'.format(img_url))
            file.close()

    def delete_img_list(self):
        f = open('img_links.txt', 'r+')
        f.truncate()


    def is_img_link(self, img_link):
        ext = img_link[-4:]
        if ext == '.jpg' or ext == '.png':
            return True
        else:
            return False

    def download_img(self,img_url, img_title, filename):
        opener = ur.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        ur.install_opener(opener)
        try:
            print('Downloading ' + img_title + '....')
            ur.urlretrieve(img_url, filename)
            return 1

        except HTTPError:
            print("Too many Requests. Try again later!")
            return 0


    def read_img_links(self):
        with open('img_links.txt') as f:
            links = f.readlines()

        links = [x.strip() for x in links]
        download_count = 0

        for link in links:
            if not self.is_img_link(link):
                continue

            file_name = link.split('/')[-1]
            file_loc = 'results/{}'.format(file_name)

            if not file_name:
                continue

            download_status = self.download_img(link, file_name, file_loc)
            download_count += 1

            if download_status == 0:
                return download_count, 0

        return download_count, 1


    def main(self):

        
        search = self.E1.get()
        numberOfTweets = self.E2.get()
        numberOfTweets = int(numberOfTweets)
        phrase = self.E3.get()
        reply = self.E4.get()
        retweet = self.E5.get()
        favorite = self.E6.get()
        follow = self.E7.get()

        if reply == 1:
            for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
                try:
                    #Reply
                    print('\nTweet by: @' + tweet.user.screen_name)
                    print('ID: @' + str(tweet.user.id))
                    tweetId = tweet.user.id
                    username = tweet.user.screen_name
                    api.update_status("@" + username + " " + phrase, in_reply_to_status_id = tweetId)
                    print ("Replied with " + phrase)
                    
                except tweepy.TweepError as e:
                    print(e.reason)

                except StopIteration:
                    break


        if retweet == 1: 
            for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
                try:
                    #Retweet
                    tweet.retweet()
                    print('Retweeted the tweet')   

                except tweepy.TweepError as e:
                    print(e.reason)

                except StopIteration:
                    break

        if favorite == 1: 
            for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
                try:
                    #Favorite
                    tweet.favorite()
                    print('Favorited the tweet')   

                except tweepy.TweepError as e:
                    print(e.reason)

                except StopIteration:
                    break

        if follow == 1: 
            for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
                try:
                    #Follow
                    tweet.user.follow()
                    print('Followed the user')
                    
                except tweepy.TweepError as e:
                    print(e.reason)

                except StopIteration:
                    break       

    

if __name__ == "__main__":
    #Twitter Info
    consumer_key = config.TWITTER['consumer_key']
    consumer_secret = config.TWITTER['consumer_secret']
    access_token = config.TWITTER['access_token']
    access_token_secret = config.TWITTER['access_token_secret']

    

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    user = api.me()

    root = Tk()
    root.geometry("850x400+200+200")

    root.title("Twitter Bot")
    twitterBot = TwitterBot(root)
    root.mainloop()

    
    