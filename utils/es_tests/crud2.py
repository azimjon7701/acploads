from connection import connection

titles = [
    {"index": {"_index": "title", "_id": 1}},
    {
        "id": 1,
        "title": "Traditional Marketing vs Digital Marketing",
        "author": 'Amazon',
        "date": "2022-08-31T10:33:23.234Z"
    },
    {"index": {"_index": "title", "_id": 2}},
    {
        "id": 2,
        "title": "Biznesingizni biz bilan rivojlantring",
        "author": 'Thinkland',
        "date": "2022-08-31T10:33:23.234Z"
    },
    {"index": {"_index": "title", "_id": 3}},
    {
        "id": 3,
        "title": "Yuqori sifat ishonchli Hamkor",
        "author": 'Thinkland solutions',
        "date": "2022-08-31T10:33:23.234Z"
    },
    {"index": {"_index": "title", "_id": 4}},
    {
        "id": 4,
        "title": "Siz kutgan mahsulotlar faqat bizda",
        "author": 'Mujohiddin Kamolov',
        "date": "2022-08-31T10:33:23.234Z"
    },
]


def createTitles(body):
    es = connection()
    try:
        resp = es.bulk(index="product", body=body)
        print(resp)
        print("bitta hujjat qo'shildi!!")
    except Exception as err:
        print("Hujjat yaratishda xato ", err)


createTitles(titles)


def countTitles():
    es = connection()
    try:
        resp = es.count(index="product")
        print(resp)
        print("Productlar soni!!")
    except Exception as err:
        print("Productni korsatishda xato ", err)


# countTitles()

def getTitles(id):
    es = connection()
    try:
        resp = es.get(index="product", id=id)
        print(resp)
        print("Productlar olish!!")
    except Exception as err:
        print("Productni olishda xato ", err)


# getTitles(3)


arr = {'took': 15, 'errors': False, 'items': [{'index': {'_index': 'title', '_type': '_doc', '_id': '1', '_version': 11,
                                                         'result': 'updated',
                                                         '_shards': {'total': 2, 'successful': 1, 'failed': 0},
                                                         '_seq_no': 16, '_primary_term': 1, 'status': 200}}, {
                                                  'index': {'_index': 'title', '_type': '_doc', '_id': '2',
                                                            '_version': 3, 'result': 'updated',
                                                            '_shards': {'total': 2, 'successful': 1, 'failed': 0},
                                                            '_seq_no': 17, '_primary_term': 1, 'status': 200}}, {
                                                  'index': {'_index': 'title', '_type': '_doc', '_id': '3',
                                                            '_version': 3, 'result': 'updated',
                                                            '_shards': {'total': 2, 'successful': 1, 'failed': 0},
                                                            '_seq_no': 18, '_primary_term': 1, 'status': 200}}, {
                                                  'index': {'_index': 'title', '_type': '_doc', '_id': '4',
                                                            '_version': 3, 'result': 'updated',
                                                            '_shards': {'total': 2, 'successful': 1, 'failed': 0},
                                                            '_seq_no': 19, '_primary_term': 1, 'status': 200}}]}
