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
        self.time_words=['when','after','before']

    knowledge = {
        'health': {
            'albert&BLIND': 1,
            'ronald&BLIND': 0,
            'VOYAGE|BOAT|SHIP|SEA&because&SICK|UNWELL|UNHEALTHY': 1,
            'CRAZY': 0,
            '*SICK&when|after&RESTAURANT|PIER': 0,
            '*SICK&before&RESTAURANT|PIER': 1,
        },
        'pier': {
            'alone&in|on|at': 2,
            'FIND|MEET&SEAGULL': 0,
            'before&RESTAURANT': 1,
            'after&RESTAURANT': 0
        },
        'suicide': {
            'albert&HAPPY': 0,
            'albert&SAD': 1,
            'ronald&HAPPY': 0,
            'ronald&SAD': 1,
            'ronald&SURPRISED': 0,
            'WAITER&SURPRISED': 1,
            'CUSTOMER&SURPRISED': 1,
            'albert&DECIDED&before': 0,
            'albert&DECIDED&when&SWALLOW|TASTE|BITE': 1,
            'albert&DECIDED&when': 0,
        },
        'seagull': {
            'DISH|SEAGULL&COOKED': 1,
            'DISH|SEAGULL&EDIBLE': 1,
            'DISH|SEAGULL&SICK': 0,
            'DISH|SEAGULL&POISONED': 0,
            'on&MENU': 1,
            'ronald&ord': 2,
            'WAITER|CHEF&SURPRISED': 0
        }
    }


    def is_synonym_present(self, word: str, question: str) -> bool:
        if word.isupper():
            syns = SynonymsManager.get_instance().synonyms(word)
            syns.append(word)
            # print(f'word= {word} q= {question}')
            for syn in syns:
                if syn.lower() in question.lower():
                    # print(f'syn {syn} (in [{syns}] found in question!')
                    return True
        elif word.lower() in question.lower():
            return True
        return False

    def is_compatible(self, pattern: str, question: str) -> bool:
        if '*' in pattern:
            if not any([w in question.lower() for w in self.time_words]):
                return False #TODO
            else:
                pattern=pattern.replace('*','')
        for a in pattern.split('&'):
            found = False
            for o in a.split('|'):
                if self.is_synonym_present(o, question):
                    found = True
            # print(f'a {a} done, result: found={found}')
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
