from elasticsearch import Elasticsearch

URL = "http://root:root@localhost:9200"


def connection():
    es = Elasticsearch(URL)
    return es
