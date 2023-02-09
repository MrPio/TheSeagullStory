import os
import pickle
from time import time_ns

import requests
from bs4 import BeautifulSoup


class SynonymsManager:
    __key = object()
    __instance = None

    def save(self):
        with open('synonyms_manager.pickle', 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load():
        if not os.path.exists('synonyms_manager.pickle'):
            return None
        with open('synonyms_manager.pickle', 'rb') as file:
            return pickle.load(file)

    @staticmethod
    def get_instance():
        if SynonymsManager.__instance is None:
            SynonymsManager.__instance = SynonymsManager.load()
            if SynonymsManager.__instance is None:
                SynonymsManager.__instance = SynonymsManager(SynonymsManager.__key)
        return SynonymsManager.__instance

    def __init__(self, key):
        if SynonymsManager.__key is not key:
            raise 'Singleton not respected'
        self.cache = {}

    def synonyms(self, term: str):
        if term.lower() in self.cache.keys():
            return self.cache[term.lower()]
        print('*** cerco sinonimo ***')
        response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
        soup = BeautifulSoup(response.text, 'lxml')
        soup.find('section', {'class': 'css-17ofzyv e1ccqdb60'})
        syns = [span.text for span in
                soup.findAll('a',
                             {'class': 'css-1kg1yv8 eh475bn0'})]  # 'css-1gyuw4i eh475bn0' for less relevant synonyms
        self.cache[term.lower()] = syns
        self.save()
        return syns
