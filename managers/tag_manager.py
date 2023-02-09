import cohere
from cohere.classify import Example


class TagManager:
    __key = object()
    __instance = None
    training = """blind
                Were the two friends a couple?
                Was Albert blind?
                Was any of the two friends blind?
                Albert was blind, but not Ronald.

                pier
                Were the two friends alone in the pier?
                Were the two friends watching for seagulls at the pier?
                Why was Albert at the pier?
                Why were the two friends at the pier?
                When was Albert at the pier?

                suicide
                Was Albert happy when he killed himself?
                Was Ronald surprised when Albert killed himself?
                Did Ronald know Albert was gonna commit suicide?
                Had Albert already decided to commit suicide before entering the restaurant?
                Had Albert already decided to commit suicide when he was at the pier?

                seagull
                Did the seagull taste good?
                Did Albert eat all of the dish?
                Was the waiter surprised by the ordination?
                Did Ronald ordered a dish too?

                ship
                On the ship there were 3 persons
                The persons on the ships weren't Albert's friends
                Was the boat a pirate boat?"""

    @staticmethod
    def get_instance():
        if TagManager.__instance is None:
            TagManager.__instance = TagManager(TagManager.__key)
        return TagManager.__instance

    def __init__(self, key):
        if TagManager.__key is not key:
            raise 'Singleton not respected'
        self.examples = []
        self.synoms = [
            "killed", "suicide", "dish", 'restaurant', 'decided', 'know', 'happy', 'waiter'
        ]
        self.co = cohere.Client('PWPxy6p0d49Sx9IrttJSa3E1YSQhIk7wBuGgQfPb')

        for par in TagManager.training.split('\n\n'):
            key = par.lstrip().split('\n')[0]
            for line in par.split('\n')[1:]:
                if len(line) > 1:
                    self.examples.append(Example(line, key))


    # def generate_phrases_with_synonyms(self):
    #     toadd = []
    #     for train in self.training.keys():
    #         for syn in synoms:
    #             if syn in train:
    #                 for s in SynonymsManager.get_instance().synonyms(syn):
    #                     if (s != syn):
    #                         toadd.append(train.replace(syn, s))
    #     return toadd


    def is_yes_no_question(self, text):
        yes_no_words = ["is", "are", "do", "did", "does", "can", "could", "will", "would"]
        text = text.lower().strip()
        for word in yes_no_words:
            if text.startswith(word):
                return True
        return False


    def ask(self,question: str):
        response = self.co.classify(
            model='large',
            inputs=[question],
            examples=self.examples
        )

        print(question)
        print(response.classifications[0])
        return response.classifications[0].prediction
