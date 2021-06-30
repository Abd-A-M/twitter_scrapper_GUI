'''
Author: Abdullah Melhem
Email:pro.am532016@gmail.com
'''
import arabic_reshaper
import bidi.algorithm
import numpy
import tweepy
from kivy.base import runTouchApp
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager
from kivy.config import Config
from kivy.core.window import Window
from kivymd.uix.screen import Screen
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from language_detector import detect_language as detect
import webbrowser

Config.set('graphics', 'resizable', '0')

consumer_key = 'nQJEcQCIZxYZd3IBCgG4k8RE0'
consumer_key_secret = 'e4ytqpDOdrx5nlkeszPkduqTfbadX7PUiY5OclpWxK0uPYNXF2'
access_token = '58235285-lINP9lnrHfPsLGlgPwBJxjgQIXLtZHIJFxxIL8gzA'
access_token_secret = 'TQXDt2dSUcrO2L1oWYq9tq76lpehNmox7ySkm9b5J7jvI'

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


class MainWindow(Screen):
    overallfeeling = []
    tweets = []
    tweet_sen = []
    searchkey = ""
    lan = ''
    links = []

    def search(self):
        self.lan = detect(self.searchkey)
        if not (self.searchkey).isspace() and self.searchkey != "" and self.lan != 'Arabic':
            searchword = self.searchkey
            public_tweets = api.search(q=searchword, count=1000)
            if searchword != '':
                for tweet in public_tweets:
                    try:
                        name = tweet.user.screen_name
                        t_id = tweet.id
                        full_link = "https://twitter.com/{}/status/{}".format(name, t_id)
                        self.links.append(full_link)
                    except Exception:
                        self.links.append('www.twitter.com')

                    analyzer = SentimentIntensityAnalyzer()
                    sentiment = analyzer.polarity_scores(tweet.text)['compound']
                    self.overallfeeling.append(sentiment)
                    self.tweets.append(tweet.text)
                    self.tweet_sen.append(self.sentimentformat(sentiment))

                meanfeeling = numpy.mean(self.overallfeeling)
                self.ids.label.text = "Overall sentiment:\n" + self.sentimentformat(meanfeeling)
            return True
        elif self.searchkey.isspace() != True and self.searchkey != "" and self.lan == 'Arabic':
            reshaped_text = arabic_reshaper.reshape(self.searchkey)
            searchword = reshaped_text
            public_tweets = api.search(q=searchword, count=1000)
            if searchword != '':
                for tweet in public_tweets:
                    try:
                        name = tweet.user.screen_name
                        t_id = tweet.id
                        full_link = "https://twitter.com/{}/status/{}".format(name, t_id)
                        self.links.append(full_link)
                    except Exception:
                        self.links.append('www.twitter.com')

                    analyzer = SentimentIntensityAnalyzer()
                    sentiment = analyzer.polarity_scores(tweet.text)['compound']
                    self.overallfeeling.append(sentiment)
                    self.tweets.append(tweet.text)
                    self.tweet_sen.append(self.sentimentformat(sentiment))

                meanfeeling = numpy.mean(self.overallfeeling)
                self.ids.label.text = "Overall sentiment:\n" + self.sentimentformat(meanfeeling)
            return True
        else:
            return False

    def sentimentformat(self, sentimentformat):
        sentiment = sentimentformat
        if sentiment > .5:
            return '[Very Positive]'
        elif sentiment > 0:
            return '[Positive]'
        elif sentiment == 0:
            return '[Neutral]'
        elif sentiment < -.5:
            return '[Very Negative]'
        else:
            return '[Negative]'

    def reset(self):
        self.searchkey = self.ids.input.text
        self.ids.input.text = ""
        self.ids.label.text = "Overall sentiment"

    def open_link(self, link):
        splited = link.split("\n")
        webbrowser.open(splited[-1])
        self.reset()

    def drop_menu(self):
        from kivy.uix.dropdown import DropDown
        if self.search() and self.lan != "Arabic":
            self.dropdownlist = DropDown(size_hint=(None, None), size=(1500, 751), pos=(0, 0), auto_dismiss=False)
            for item in self.tweets:
                pos = self.tweets.index(item)
                indiv_op = Button(text=item.replace("\n", " ") + "\n " + self.tweet_sen[pos] + "\n" + self.links[pos],
                                  size_hint=(None, None),
                                  size=(1500, 120), background_color=(23 / 205.0, 180 / 200, 1.5, 0.3))

                indiv_op.bind(on_press=lambda indiv_op: self.dropdownlist.select(indiv_op.text))
                self.dropdownlist.add_widget(indiv_op)
            self.overallfeeling = []
            self.tweets = []
            self.tweet_sen = []
            self.searchkey = ""
            self.dropdownlist.bind(on_select=lambda instance, x: self.open_link(x))
            self.dropdownlist.auto_dismiss = False
            runTouchApp(self.dropdownlist)

        if self.search() and self.lan == "Arabic":
            self.dropdownlist = DropDown(size_hint=(None, None), size=(1500, 751), pos=(0, 0), auto_dismiss=False)
            for item in self.tweets:
                pos = self.tweets.index(item)
                item = arabic_reshaper.reshape(item)
                item = bidi.algorithm.get_display(item)

                indiv_op = Button(text=item.replace("\n", " ") + "\n " + self.tweet_sen[pos] + "\n" + self.links[pos],
                                  size_hint=(None, None),
                                  size=(1500, 120), background_color=(23 / 205.0, 180 / 200, 1.5, 0.3),
                                  font_name="/home/abdullah/PycharmProjects/corsera/arial.ttf")

                indiv_op.bind(on_press=lambda indiv_op: self.dropdownlist.select(indiv_op.text))
                self.dropdownlist.add_widget(indiv_op)
            self.overallfeeling = []
            self.tweets = []
            self.tweet_sen = []
            self.searchkey = ""
            self.dropdownlist.bind(on_select=lambda instance, x: self.open_link(x))
            self.dropdownlist.auto_dismiss=False
            runTouchApp(self.dropdownlist)

        else:
            from kivy.uix.textinput import TextInput
            layout = GridLayout(cols=1, spacing=2)
            self.textinput_addnewdataser = Label(text='Enter The Correct Search Key', size=(578, 50), bold=True,
                                                 color=(200, 110, 23, 0.5))
            closeButton = Button(text="Close", background_color=(200, 110, 23, 0.15), size=(578, 50))
            layout.add_widget(self.textinput_addnewdataser)
            layout.add_widget(closeButton)
            popup = Popup(title='Error !!',
                          content=layout,
                          size_hint=(None, None), size=(600, 250), auto_dismiss=False)
            popup.open()
            closeButton.bind(on_press=popup.dismiss)


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("GUI.kv")


class MyMainApp(App):
    def build(self):
        self.title = 'TweetAnalysis'
        Window.size = (1500, 800)
        return kv


MyMainApp().run()
