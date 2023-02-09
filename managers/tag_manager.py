import cohere
from cohere.classify import Example


class TagManager:
    __key = object()
    __instance = None
    training = """health
Was Albert blind?
Was Albert crazy?
Was Albert sick?
Was any of the two friends blind?
Was any of the two friends sick?
The health condition of the two friends.
The health condition of Albert.
The health condition of Ronald.
Albert was blind, but not Ronald.
Was Albert disabled?

pier
Were the two friends alone in the pier?
Were the two friends watching for seagulls at the pier?
Why was Albert at the pier?
Why were the two friends at the pier?
When was Albert at the pier?
Did they plan to go to the pier?
Did they get to the pier accidentally?
How did they get to the pier?

suicide
Was Albert happy when he killed himself?
Was Ronald surprised when Albert killed himself?
Did Ronald know Albert was gonna commit suicide?
Had Albert already decided to commit suicide before entering the restaurant?
Had Albert already decided to commit suicide when he was at the pier?
Did Albert have a masterplan when he committed suicide?
Did Albert decide to  commit  suicide when he ordered the seagull?
Did Albert decide to  commit  suicide when he ate the seagull?

seagull
Did the seagull taste good?
Did Albert eat all of the dish?
Was the waiter surprised by the ordination?
The waiter brought the seagull to Albert
The seagull wasn't poisoned
Did Ronald ordered a dish too?
Did Ronald also ordered a seagull?
Had Albert already eaten seagull before?
Did the seagull taste like something familiar?

saving_ship
On the ship there were more than 3 people
The people on the ships weren't Albert's friends
Was the boat a pirate boat?
Did Albert travel in exactly one ship?

alberts_ship
Albert, Ronald and Sofia were on a boat trip
Because of a storm Albert's trip boat is wrecked and they cast away on an island. 
Was Albert's ship  attacked?
Was there a storm?
Was the ship wrecked?
Was there any ship nearby?

wife
Was Albert married?
Was any of the two friends married?
Did Albert have a girlfriend?
Was Ronald married?
Was a family member involved?
Did something happened to an acquaintance of Albert?"""

    @staticmethod
    def get_instance():
        if TagManager.__instance is None:
            TagManager.__instance = TagManager(TagManager.__key)
        return TagManager.__instance

    def __init__(self, key):
        if TagManager.__key is not key:
            raise Exception('Singleton not respected')
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
        pass

    # def generate_phrases_with_synonyms(self):
    #     toadd = []
    #     for train in self.training.keys():
    #         for syn in synoms:
    #             if syn in train:
    #                 for s in SynonymsManager.get_instance().synonyms(syn):
    #                     if (s != syn):
    #                         toadd.append(train.replace(syn, s))
    #     return toadd

    def ask(self, question: str):
        response = self.co.classify(
            model='large',
            inputs=[question],
            examples=self.examples
        )

        # print(question)
        print(response.classifications[0])
        return response.classifications[0].prediction
