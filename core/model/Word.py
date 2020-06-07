from mongoengine.fields import *
from mongoengine.document import EmbeddedDocument

class Word(EmbeddedDocument):

    id = IntField()
    lemma = StringField()
    cpostag = StringField()
    postag = StringField()
    head_id = IntField()
    head_word = EmbeddedDocumentField("Word")   # 无法这样使用
    dependency = StringField()
    name = StringField()



'''
class Word:

    # 类变量
    id = None
    lemma = ''
    postag = ''
    head = None
    head_word = None
    dependency = ''


    def __init__(self, id, lemma, cpostag, postag, head_id, head_word, dependency, name):
        self.id = id
        self.lemma = lemma
        self.cpostag = cpostag
        self.postag = postag
        self.head_id = head_id
        self.head_word = head_word
        self.dependency = dependency
        self.name = name

'''




