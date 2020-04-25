import numpy as np
from nltk.corpus import stopwords


class Preprocessor:

    def __init__(self, text):
        self.text = text

    def splitWords(self, data):
        if type(data) == str:
            words = data.split()
        else:
            words = np.array_str(data).split()
        return words

    def toLowerCase(self, data):
        return np.char.lower(data)

    def removeStopWords(self, data):
        words = self.splitWords(data)
        stop_words = set(stopwords.words('english'))
        new_text = ""
        for word in words:
            if word not in stop_words:
                new_text = new_text + " " + word
        return new_text

    def preprocessData(self):
        data = self.text
        data = self.toLowerCase(data)
        data = self.removeStopWords(data)
        return data
