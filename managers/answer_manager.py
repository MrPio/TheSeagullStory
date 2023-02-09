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
            raise Exception('Singleton not respected')
        self.knowledge = AnswerManager.knowledge
        self.time_words = ['when', 'after', 'before']


    knowledge = {
        'health': {
            'albert&BLIND': 1,
            'ronald&BLIND': 0,
            'VOYAGE|BOAT|SHIP|SEA&because&SICK|UNWELL|UNHEALTHY': 1,
            'CRAZY': 0,
            'DISABLED': 0,
            '*SICK&when|after&RESTAURANT|PIER': 0,
            '*SICK&before&RESTAURANT|PIER': 1,
        },
        'pier': {
            'alone&in|on|at': 2,
            'FIND|MEET&SEAGULL': 0,
            'before&RESTAURANT': 1,
            'after&RESTAURANT': 0,
            'PLAN&GO': 1,
            'PIER&ACCIDENTALLY': 0,
            'PIER&by&BOAT|SHIP': 1,
            'PIER&by': 0,
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
            'albert&DECIDED&when|after&SWALLOW|TASTE|BITE|ate|eat': 1,
            'albert&DECIDED&when': 0,
            'albert&SHOOT|PISTOL': 1,
        },
        'seagull': {
            'DISH|SEAGULL&COOKED': 1,
            'DISH|SEAGULL&EDIBLE': 1,
            'DISH|SEAGULL&SICK': 0,
            'DISH|SEAGULL&POISONED': 0,
            'on&MENU': 1,
            'ronald&ord': 2,
            'WAITER|CHEF&SURPRISED': 0,
            'already&eaten': 0,
            'first time': 1,
            'taste&familiar': 0,
        },
        'saving_ship': {
            'LESS&PEOPLE|PERSON|persons&0|zero|1|one|2|two|3|three': 0,
            'MORE&PEOPLE|PERSON|persons&0|zero|1|one|2|two': 1,

            'MORE&DAY&0|zero|1|one|2|two': 1,
            'MORE&SECOND|MINUTE|HOUR': 1,
            'MORE&DAY|WEEK|MONTH|YEAR': 0,
            'LESS&DAY&0|zero|1|one|2|two': 0,
            'LESS&SECOND|MINUTE|HOUR': 0,
            'LESS&DAY|WEEK|MONTH|YEAR': 1,

            'LESS|MORE&PEOPLE|PERSON|persons': 2,
            'TRAVEL|USE|TOOK&SHIP|BOAT&2|two': 1,
            'TRAVEL|USE|TOOK&SHIP|BOAT': 0,

            'wrecked': 0,
            'storm': 0,
            'PIRATE': 0,
        },
        'alberts_ship': {
            'LESS&PEOPLE|PERSON|persons&0|zero|1|one|2|two|3|three': 0,
            'MORE&PEOPLE|PERSON|persons&0|zero|1|one|2|two': 1,

            'MORE&DAY&0|zero|1|one': 1,
            'MORE&SECOND|MINUTE|HOUR': 1,
            'MORE&DAY|WEEK|MONTH|YEAR': 0,
            'LESS&DAY&0|zero|1|one': 0,
            'LESS&SECOND|MINUTE|HOUR': 0,
            'LESS&DAY|WEEK|MONTH|YEAR': 1,

            'LESS|MORE&PEOPLE|PERSON|persons': 2,
            'PIRATE': 0,
            'TRAVEL|USE|TOOK&2|two&SHIP|BOAT': 1,
            'TRAVEL|USE|TOOK&SHIP|BOAT': 0,
            'nearby': 0,
            'wrecked': 1,
            'storm': 1,
            'SOMEBODY|WIFE|girlfriend&DIE|DIED': 1,
            'DIE|DIED': 0,
            'EVERYBODY|WIFE|girlfriend&SURVIVE': 0,
            'SURVIVE': 1,
        },
        'wife': {
            'albert|SOMEBODY|any&MARRY|girlfriend|married': 1,
            'ronald&MARRY|girlfriend|married': 0,
            'FAMILY&INVOLVE|member': 1,
            'ACQUAINTANCE': 1,
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
        # when|before|after check
        if '*' in pattern:
            if not any([w in question.lower() for w in self.time_words]):
                raise Exception('when|before|after required!')
            else:
                pattern = pattern.replace('*', '')

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
        if not self.is_yes_no_question(question):
            raise Exception('that\'s not a yes/no question!')
        if tag not in self.knowledge.keys():
            return 2
        for k, v in self.knowledge[tag].items():
            if self.is_compatible(k, question):
                return v if not self.is_negative_question(question) else 1 if v == 0 else 0 if v == 1 else 2
        return 2

    def is_negative_question(self, question):
        negation = ["not", "n't"]
        return any([x in question for x in negation])

    def is_yes_no_question(self, question:str):
        yes_no_words = ["is", "are", "were", "was", "had", "has", "have", "do", "did", "does", "can", "could", "will",
                        "would"]
        _5W = ['when', 'where', 'what', 'how', 'why']
        text = question.lower().lstrip().split(' ')[0]
        if any([x in text for x in _5W]):
            return False
        return any([x in text for x in yes_no_words])
