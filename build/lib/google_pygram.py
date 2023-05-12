import pandas as pd
import numpy as np
import requests
import json
import re

"""
NGram Parameters Class
This class is used to store the parameters for the NGram fetches
from the Google NGram API. The following parameters are used:
1. corpus: The corpus to be used for the NGram fetches
2. smoothing: The smoothing parameter to be used for the NGram fetches (0-5)
3. start_year: The start year for the NGram fetches
4. end_year: The end year for the NGram fetches
"""
class GooglePyGramParams():
    corpuses = {
        "English 2019": "26",
        "American English 2019": "en-US-2019",
        "British English 2019": "en-GB-2019",
        "Chinese (simplified) 2019": "zh-Hans-2019",
        "English Fiction": "en-fiction-2019",
        "French 2019": "fr-2019",
        "German 2019": "de-2019",
        "Hebrew 2019": "iw-2019",
        "Italian 2019": "it-2019",
        "Russian 2019": "ru-2019",
        "Spanish 2019": "es-2019",
        "English 2012": "en-2012",
        "British English 2012": "en-GB-2012",
        "American English 2012": "en-US-2012",
        "Chinese (simplified) 2012": "zh-Hans-2012",
        "English Fiction 2012": "en-fiction-2012",
        "French 2012": "fr-2012",
        "German 2012": "de-2012",
        "Hebrew 2012": "iw-2012",
        "Italian 2012": "it-2012",
        "Russian 2012": "ru-2012",
        "Spanish 2012": "es-2012",
        "American English 2009": "en-US-2009",
        "British English 2009": "en-GB-2009",
        "Chinese (simplified) 2009": "zh-Hans-2009",
        "English Fiction 2009": "en-fiction-2009",
        "French 2009": "fr-2009",
        "German 2009": "de-2009",
        "Hebrew 2009": "iw-2009",
        "Italian 2009": "it-2009",
        "Russian 2009": "ru-2009",
        "Spanish 2009": "es-2009"
    }
    def __init__(
            self,
            corpus = "English",
            corpus_year = 2019,
            smoothing = 0,
            start_year = 1800,
            end_year = 2019,
            case_sensitive = True
        ):
        self.set_corpus(corpus, corpus_year)
        self.set_smoothing(smoothing)
        self.set_start_year(start_year)
        self.set_end_year(end_year)
        self.case_sensitive = case_sensitive

    def set_corpus(self, corpus, year = 2019):
        corpus = " ".join([*[w.capitalize() for w in corpus.strip().split(" ")], str(year)])
        if corpus in self.corpuses:
            self.corpus = self.corpuses[corpus]
        else:
            raise ValueError("Corpus not found")

    def set_smoothing(self, smoothing):
        if smoothing >= 0 and smoothing <= 5:
            self.smoothing = smoothing
        else:
            raise ValueError("Smoothing must be between 0 and 5")

    def set_start_year(self, start_year):
        if start_year >= 1800 and start_year <= 2019:
            self.start_year = start_year
        else:
            raise ValueError("Start year must be between 1800 and 2019")

    def set_end_year(self, end_year):
        if end_year >= 1800 and end_year <= 2019:
            self.end_year = end_year
        else:
            raise ValueError("End year must be between 1800 and 2019")

    def set_case_sensitive(self, case_sensitive):
        self.case_sensitive = case_sensitive

"""
NGram class
This class allows you to read an NGram time series from Google NGram
and convert it to a CSV file.
"""
class GooglePyGram():
    def __init__(
            self,
            corpus = "English",
            corpus_year = 2019,
            smoothing = 0,
            start_year = 1800,
            end_year = 2019,
            case_sensitive = True,
            phrases = []
        ):
        self.parameters = GooglePyGramParams(
            corpus = corpus,
            corpus_year = corpus_year,
            smoothing = smoothing,
            start_year = start_year,
            end_year = end_year,
            case_sensitive = case_sensitive
        )
        self.phrases = phrases

    def add_phrase(self, phrase):
        self.phrases.append(phrase)

    def _bake_fetch_url(self):
        url = "https://books.google.com/ngrams/json"
        params = {
            "content": ",".join(self.phrases),
            "year_start": self.parameters.start_year,
            "year_end": self.parameters.end_year,
            "corpus": self.parameters.corpus,
            "smoothing": self.parameters.smoothing
        }
        if self.parameters.case_sensitive:
            params["case_insensitive"] = "true"
        return (url, params)

    def _fetch(self):
        url, params = self._bake_fetch_url()
        response = requests.get(url, params=params)
        if response.status_code == 200:
            text = response.text
            data = json.loads(text)
            return data
        else:
            raise ValueError("Error fetching data")

    def to_df(self):
        data = self._fetch()
        df = pd.DataFrame()
        for year in range(self.parameters.start_year, self.parameters.end_year + 1):
            df.at[year, "year"] = int(year)
        for word in data:
            year = self.parameters.start_year
            for count in word["timeseries"]:
                df.loc[year, word["ngram"]] = count
                year += 1
        return df

    def to_csv(self, filename):
        df = self.to_df()
        df.to_csv(filename)

if __name__ == "__main__":
    gpg = GooglePyGram
    pygram = gpg(
        corpus='English',
        corpus_year=2019,
        start_year=1800,
        end_year=2000,
        smoothing=0,
        case_sensitive=False,
        phrases=['hello', 'world']
    )

    df = pygram.to_df()

    print(df)