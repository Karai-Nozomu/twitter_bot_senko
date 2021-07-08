import tweepy
import time
import pandas as pd
import re
import datetime
import schedule

consumer_key = ""
consumer_secret = ""
key = ""
secret = ""

class senko_san():
    def __init__(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(key, secret)
        self.api = tweepy.API(auth)
        self.my_id = "@yotei_senko_san"
        
    def clasify(self):
        tl = self.api.home_timeline(count=200)
        for tweet in tl:
            if not(self.my_id in tweet.text):
                continue
            if tweet.favorited == False:
                print("reply")
                keyword = re.findall('\'.+?\'', tweet.text)
                if (len(keyword) == 0) or (len(keyword) >= 3):
                    print("Keyword error")
                    self.api.create_favorite(tweet.id)
                    reply = "@" + str(tweet.user.screen_name) + "\n" + "形式を守るのじゃ！！"
                    self.api.update_status(status=reply, in_reply_to_status_id=tweet.id)
                    continue
                title = keyword[0].strip("'")
                tweet.text = tweet.text.replace(title, "")
                if "削除" in tweet.text:
                    self.delete_plan(title, tweet.id, tweet.user.screen_name)
                else:
                    plan_time = keyword[1].strip("'")
                    self.add_plan(title, plan_time, tweet.text, str(tweet.user.screen_name), tweet.id)
                 
    def delete_plan(self, title, tweet_id, user_name):
        data = pd.read_csv("C:/Users/n0216/Documents/senko_san/data.csv")
        if (len(data[data["title"] == title])) == 0:
            print("no plam")
            self.api.create_favorite(tweet_id)
            reply = "@" + user_name + "\n" + title + "は存在しないのじゃ！！"
            self.api.update_status(status=reply, in_reply_to_status_id=tweet_id)
        else:
            print("delete plan")
            data_drop = data.index[data["title"] == title]
            data = data.drop(data_drop)
            data = data.reset_index()
            data = data.drop('index', axis = 1)
            data.to_csv("C:/Users/n0216/Documents/senko_san/data.csv", index = False)
            self.api.create_favorite(tweet_id)
            reply = "@" + user_name + "\n" + title + "を削除したのじゃ！！"
            self.api.update_status(status=reply, in_reply_to_status_id=tweet_id)
        
    def add_plan(self, title, plan_time, tweet_text, user_name, tweet_id):
        try:
            datetime.datetime.strptime(plan_time, "%Y/%m/%d")
        except:
            print("time error")
            self.api.create_favorite(tweet_id)
            reply = "@" + user_name + "\n" + "時間設定が間違っておるのじゃ！！"
            self.api.update_status(status=reply, in_reply_to_status_id=tweet_id)
            return
        data = pd.read_csv("C:/Users/n0216/Documents/senko_san/data.csv")
        add_data = pd.Series([user_name, title, plan_time, '毎日' in tweet_text, '毎週' in tweet_text, 
                              '課題' in tweet_text], index = data.columns, name = len(data))
        data = data.append(add_data)
        data.to_csv("C:/Users/n0216/Documents/senko_san/data.csv", index = False)
        self.api.create_favorite(tweet_id)
        reply = "@" + user_name + "\n" + title + "を" + plan_time + "に追加したのじゃ！！"
        self.api.update_status(status=reply, in_reply_to_status_id=tweet_id)
        print("add plan")
    
    def tweet_plan(self):
        data = pd.read_csv("C:/Users/n0216/Documents/senko_san/data.csv")
        for row in data[data['time'] == (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d")].itertuples():
            reply = "@" + row[1] + "\n" + row[2] + "は明日なのじゃ！！"
            self.api.update_status(status=reply)
            print("tweet plan")
            
    def tweet_plan_morning(self):
        data = pd.read_csv("C:/Users/n0216/Documents/senko_san/data.csv")
        for row in data[data['time'] == (datetime.date.today() + datetime.timedelta(days=3)).strftime("%Y/%m/%d")].itertuples():
            tweet = row[2] + "は３日後なのじゃ！！"
            self.api.update_status(status=tweet)
            
        for row in data[data['time'] == (datetime.date.today() + datetime.timedelta(days=2)).strftime("%Y/%m/%d")].itertuples():
            tweet = row[2] + "は2日後なのじゃ！！"
            self.api.update_status(status=tweet)
            
        for row in data[data['time'] == (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d")].itertuples():
            tweet = row[2] + "は明日なのじゃ！！"
            self.api.update_status(status=tweet)
        
    def tweet_plan_evening(self):
        data = pd.read_csv("C:/Users/n0216/Documents/senko_san/data.csv")
        for row in data[data['time'] == (datetime.date.today() + datetime.timedelta(days=3)).strftime("%Y/%m/%d")].itertuples():
            tweet = row[2] + "は３日後なのじゃ！！"
            self.api.update_status(status=tweet)
            
        for row in data[data['time'] == (datetime.date.today() + datetime.timedelta(days=2)).strftime("%Y/%m/%d")].itertuples():
            tweet = row[2] + "は2日後なのじゃ！！"
            self.api.update_status(status=tweet)
            
        for row in data[data['time'] == (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d")].itertuples():
            tweet = "@" + row[1] + "\n" + row[2] + "は明日なのじゃ！！"
            self.api.update_status(status=tweet)
            if row[5] == False:
                data_drop = data.index[data["title"] == row[2]]
                data = data.drop(data_drop)
                data = data.reset_index()
                data = data.drop('index', axis = 1)
                data.to_csv("C:/Users/n0216/Documents/senko_san/data.csv", index = False)
            elif row[5] == True:
                data = data.replace(row[3], (datetime.date.today() + datetime.timedelta(days=7)).strftime("%Y/%m/%d"))
                
            
            
    def followback(self):

        followers = self.api.followers_ids(self.my_id)
        friends = self.api.friends_ids(self.my_id)

        follow_back = list(set(followers)-set(friends))
        print("list_followback,count:",len(follow_back))

        for i in range(min(len(follow_back),10)):
            try:
                self.api.create_friendship(follow_back[i])
                print("success follow!"+str(follow_back[i]))
            except tweepy.error.Tweeperror:
                print("follow error")
        
def main():
    senko = senko_san()
    schedule.every().day.at("10:30").do(senko.tweet_plan_morning)
    schedule.every().day.at("18:30").do(senko.tweet_plan_evening)
    while True:
        senko.clasify()
        senko.followback()
        schedule.run_pending()
        time.sleep(60)

    
if __name__ == "__main__":
    main()