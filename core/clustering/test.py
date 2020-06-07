from pymongo import MongoClient
from bson.objectid import ObjectId

conn1 = MongoClient('10.141.212.162', 27019)
db1 = conn1['Sina']
collet1 = db1['article20191121']

conn = MongoClient('10.132.141.255', 27017)
db = conn['SinaNews']
collet = db['result_20191121']


corsor = collet.find({})

'''
5de8ac00ddb6e5130d6ffd5a

'''

for i, article in enumerate(corsor.skip(119235)):
    print(i, article['title'], article['_id'])

    if i > 5: break


problem_arts = ['5de8ac00ddb6e5130d6ffd5a', '5de8ac07ddb6e5130d70f5e5', '5de8ac07ddb6e5130d70faa3']
import json

for num, item in enumerate(problem_arts):
    print(num)
    i = collet.find({'_id': ObjectId(item)})
    for sent in i[0]['sentences']:
        print(sent['sentence'], '++++++++++++')

    print('--------------------------------')

# for i in collet.find({'_id': ObjectId('5de8ac00ddb6e5130d6ffd5a')}):
#     # print(i)
#     i['_id'] = str(i['_id'])
#     print(json.dumps(i, indent=4, ensure_ascii=False))
