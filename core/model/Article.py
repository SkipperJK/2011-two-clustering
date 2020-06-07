from mongoengine import connect
from mongoengine.fields import *
from mongoengine.document import Document
from core.model.Sentence import Sentence


connect(alias="WriteResult", db="SinaNews", host="10.132.141.255", port=27017)

class Article(Document):

    meta = {
        'db_alias': "WriteResult",
        'collection': "result_20191121"
    }

    _id = ObjectIdField()
    title = StringField()
    sentences = EmbeddedDocumentListField(Sentence, default=[])  # 避免将[] 存入






if __name__ == '__main__':
    pass

