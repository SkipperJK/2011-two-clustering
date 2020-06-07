from mongoengine.fields import *
from mongoengine.document import EmbeddedDocument
from core.model.Word import Word


class Sentence(EmbeddedDocument):

    sentence = StringField()
    words = EmbeddedDocumentListField(Word, default=None)  # 避免将[]存入，但是当创建实例时不能指定该参数















'''
class Sentence:


    words = None
    def __init__(self, words = None):
        self.words = words

    def get_word_by_id(self, id):
        return self.words[id] if self.words != None else None

'''

