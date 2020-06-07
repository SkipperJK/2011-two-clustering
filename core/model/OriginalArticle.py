from mongoengine import connect
from mongoengine.fields import *
from mongoengine.document import *


# __all__ = (
#     "OriginalArticle"
# )

connect(alias="ReadOrigin", db="Sina", host='10.141.212.162', port=27019)
# disconnect(alias='ReadOrigin')

class OriginalArticle(Document):
    meta = {
        'db_alias': 'ReadOrigin',
        'collection': 'article20191121'
    }

    _id = ObjectIdField()
    title = StringField(required=True)
    url = URLField()
    content = StringField(required=True)
    time = DateField()
    media_show = StringField()
    thumb = URLField()
    mediaL = IntField()
    qscore = IntField()

    # sentences = None

if __name__ == '__main__':
    for i, article in enumerate(OriginalArticle.objects):
        print(i, article['title'])
        break
