from managers.synonyms_manager import SynonymsManager


class AnswerManager:
    __key = object()
    __instance = None

    @staticmethod
    def get_instance():
        if AnswerManager.__instance is None:
            AnswerManager.__instance = AnswerManager(AnswerManager.__key)
        return AnswerManager.__instance

    def __init__(self, key):
        if AnswerManager.__key is not key:
            raise 'Singleton not respected'
        self.knowledge = AnswerManager.knowledge

    knowledge = {
        'seagull': {
            'DISH|SEAGULL&COOKED': 1,
            'DISH|SEAGULL&EDIBLE': 1,
            'on&MENU': 1,
            'ronald&ord': 2,
            'WAITER|CHEF&SURPRISED': 0
        }
    }

    def is_synonym_present(self, word: str, question: str) -> bool:
        if word.isupper():
            syns = SynonymsManager.get_instance().synonyms(word)
            syns.append(word)
            print(f'word= {word} q= {question}')
            for syn in syns:
                if syn.lower() in question.lower():
                    print(f'syn {syn} (in [{syns}] found in question!')
                    return True
        elif word.lower() in question.lower():
            return True
        return False

    def is_compatible(self, pattern: str, question: str) -> bool:
        for a in pattern.split('&'):
            found = False
            for o in a.split('|'):
                if self.is_synonym_present(o, question):
                    found = True
            print(f'a {a} done, result: found={found}')
            if not found:
                return False
        return True

    def answer(self, question, tag) -> int:
        if tag not in self.knowledge.keys():
            return 2
        for k, v in self.knowledge[tag].items():
            if self.is_compatible(k, question):
                return v
        return 2
