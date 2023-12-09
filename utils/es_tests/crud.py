import warnings

from elasticsearch import helpers

from connection import connection

warnings.filterwarnings("ignore")

mapping = {
    "settings": {
        "analysis": {
            "analyzer": {
                "whitespace_lowercase": {
                    "tokenizer": "whitespace",
                    "filter": ["lowercase"]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "place_id": {"type": "integer"},
            "name": {"type": "text"},
            "latitude": {"type": "float"},
            "longitude": {"type": "float"},
            "description": {"type": "text"}
        }
    }
}

index_name = "mini_market"

query = {
    "query": {
        "bool": {
            "must": {
                "term": {
                    "item_name": "apple"
                }
            }
        }
    }
}


def create_index():
    es = connection()
    index_name = "places_usa"

    try:
        index_exists = es.indices.exists(index=index_name)

        if not index_exists:
            es.indices.create(index=index_name, body=mapping)
            print("Indeks muvaffaqiyatli yaratildi!")

    except Exception as err:
        print("Elasticsearch xatosi:", err)


def create():
    es = connection()

    try:
        doc = {"item_name": "orange", "price": 200}
        es.index(index=index_name, doc_type="_doc", body=doc)
        print("bitta hujjat qo'shildi!!")
    except Exception as err:
        print("Hujjat yaratishda xato ", err)

    try:
        docs = [
            {"item_name": "apple", "price": 100},
            {"item_name": "mango", "price": 150},
            {"item_name": "mandarin", "price": 200},
            {"item_name": "lemon", "price": 250},
            {"item_name": "chips", "price": 300},
            {"item_name": "chocolate", "price": 550},
            {"item_name": "banana", "price": 220}
        ]
        helpers.bulk(es, docs, index=index_name, doc_type="_doc")
        print("bir nechta hujjatlar qo'shildi!!")
    except Exception as err:
        print("Bir nechta hujjat yaratishda xato ", err)


def read():
    es = connection()

    try:
        results = es.search(index=index_name, body=query)
        print("Qidiruv natijalari:", results)
    except Exception as err:
        print("Qidiruv xatosi :", err)

    range_query = {"query": {"range": {"price": {"gte": 100}}}}

    try:
        results = es.search(index=index_name, body=range_query)
        print("Qidiruv natijalari soni: ", len(results["hits"]["hits"]))
        print("res: ", results)
    except Exception as err:
        print("Natijalar sonini ko'rsatishda xato: ", err)

    try:
        results = es.search(index=index_name, body=range_query, size=1000)
        print(
            "Maxsus oʻlchamli qidiruv natijalari soni", len(results["hits"]["hits"])
        )
    except Exception as err:
        print("Natijalar sonini ko'rsatishda xato ", err)

    try:
        results = helpers.scan(client=es, query=range_query, index=index_name)
        count = 0
        for result in results:
            count += 1
        print("Helpers Scan yordamida qidiruv natijalari soni", count)
    except Exception as err:
        print("Natijalar sonini ko'rsatishda xato", err)


def update():
    es = connection()
    doc_id = ""
    doc_body = {}

    try:
        doc = es.search(index=index_name, body=query)

        for i in range(len(doc["hits"]["hits"])):
            doc_body = doc["hits"]["hits"][i]["_source"]
            doc_id = doc["hits"]["hits"][i]["_id"]

            doc_body["price"] = 50
            es.update(index=index_name, id=doc_id, body={"doc": doc_body})
            print("Hujjat muvaffaqiyatli yangilandi!")
    except Exception as err:
        print("Qidiruv bilan yangilashda xato: ", err)

    try:
        doc_results = helpers.scan(client=es, query=query, index=index_name)

        for doc in doc_results:
            doc_body = doc["_source"]
            doc_id = doc["_id"]

            doc_body["price"] = 22
            es.update(index=index_name, id=doc_id, body={"doc": doc_body})
            print("Hujjat muvaffaqiyatli yangilandi!")
    except Exception as err:
        print("Skanerlash bilan yangilashda xato: ", err)


def delete():
    es = connection()

    query = {"query": {"term": {"product_name": "chips"}}}

    try:
        es.delete_by_query(index=index_name, body=query)
        print("Hujjat soʻrov asosida muvaffaqiyatli oʻchirildi!")
    except Exception as err:
        print("Oʻchirishda xato: ", err)


if __name__ == "__main__":
    create_index()
    # create()
    # time.sleep(1)
    # read()
    # update()
    #     time.sleep(1)
    # delete()
#     time.sleep(1)
#     read()
