import requests
from bs4 import BeautifulSoup


class SynonymsManager:
    __key = object()
    __instance = None

    @staticmethod
    def get_instance():
        if SynonymsManager.__instance is None:
            SynonymsManager.__instance = SynonymsManager(SynonymsManager.__key)
        return SynonymsManager.__instance

    def __init__(self, key):
        if SynonymsManager.__key is not key:
            raise 'Singleton not respected'

    def synonyms(self, term):
        response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
        soup = BeautifulSoup(response.text, 'lxml')
        soup.find('section', {'class': 'css-17ofzyv e1ccqdb60'})
        return [span.text for span in
                soup.findAll('a',
                             {'class': 'css-1kg1yv8 eh475bn0'})]  # 'css-1gyuw4i eh475bn0' for less relevant synonyms
