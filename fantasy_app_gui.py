import pandas as pd
import numpy as np
import random

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput


class App_layout(GridLayout):
    def __init__(self, **kwargs):
        super(App_layout, self).__init__(**kwargs)
        self.row = 10
        self.cols = 2

        self.name_label = Label(text='NAME')
        self.add_widget(self.name_label)

        self.name = TextInput(multiline=False)
        self.add_widget(self.name)

        self.runs_label = Label(text='RUNS')
        self.add_widget(self.runs_label)

        self.runs = TextInput(multiline=False)
        self.add_widget(self.runs)

        self.high_score_label = Label(text='HIGHEST SCORE')
        self.add_widget(self.high_score_label)

        self.high_score = TextInput(multiline=False)
        self.add_widget(self.high_score)

        self.strike_rate_label = Label(text='STRIKE RATE')
        self.add_widget(self.strike_rate_label)

        self.strike_rate = TextInput(multiline=False)
        self.add_widget(self.strike_rate)

        self.prediction_label = Label(text='PREDICTION', color=(0, 100, 0))

        self.add_widget(self.prediction_label)

        self.prediction = TextInput(multiline=False)
        self.add_widget(self.prediction)

        self.clear_btn = Button(text='Clear', on_press=self.clear_screen)
        self.add_widget(self.clear_btn)

        self.submit_btn = Button(text='SUBMIT', on_press=self.submit)
        self.add_widget(self.submit_btn)

    def clear_screen(self, obj):
        self.name.text = ''
        self.runs.text = ''
        self.high_score.text = ''
        self.strike_rate.text = ''
        self.prediction.text = ''

    def submit(self, obj):
        runs = int(self.runs.text)
        highest_score = int(self.high_score.text)
        strike_rate = float(self.strike_rate.text)

        df = pd.read_csv('Players report.csv')

        X = df[['Runs', 'Highest score', 'SR']]
        X.dropna(inplace=True)

        y = df['Status']
        y.dropna(inplace=True)

        from sklearn.feature_selection import SelectKBest, f_classif
        best = SelectKBest(score_func=f_classif, k='all')
        best.fit(X, y)
        feature_x = best.transform(X)

        from sklearn.preprocessing import LabelEncoder
        encoder = LabelEncoder()
        y_encoder = encoder.fit(y)
        target_y = encoder.transform(y)

        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(feature_x, target_y, test_size=0.3, random_state=42)

        from sklearn.ensemble import RandomForestClassifier
        clf = RandomForestClassifier(n_estimators=1000)
        clf.fit(X_train, y_train)
        predict = clf.predict(X_test)

        query = [[runs, highest_score, strike_rate]]

        result = clf.predict(query)

        result = encoder.inverse_transform(result)
        result = str(result)
        result = ''.join(result)

        self.prediction.disabled = False
        self.prediction.insert_text(result)

        if result in ['selected']:
            self.prediction.background_color = (0, 190, 0)




class Fantasyapp(App):
    def build(self):
        return App_layout()


if __name__ == '__main__':
    Window.size = (500, 500)
    Fantasyapp().run()
