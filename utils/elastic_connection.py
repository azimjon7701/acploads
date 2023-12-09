from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

request_body = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 1
    },

    'mappings': {
        'distance': {
            'properties': {
                'loc1loc2': {'index': 'not_analyzed', 'type': 'string'},
                'loc2loc1': {'index': 'not_analyzed', 'type': 'string'},
                'distance_value': {'index': 'not_analyzed', 'type': 'float'},
            }
        }
    }
}

es.indices.create(index='distances', body=request_body)
print(es.indices)

#
# doc = {
#     'author': 'kimchy',
#     'text': 'Elasticsearch: cool. bonsai cool.',
#     'timestamp': datetime.now(),
# }
# # resp = es.index(index="test-index", id=1, document=doc)
# # print("13:",resp['result'])
# t1 = datetime.now()
# for i in range(1,1000):
#     resp = es.get(index="test-index", id=1)
# t2 = datetime.now()
# print("16:",resp['_source'])
#
# es.indices.refresh(index="test-index")
#
# resp = es.search(index="test-index", query={"match_all": {}})
# print("Got %d Hits:" % resp['hits']['total']['value'])
# for hit in resp['hits']['hits']:
#     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
#
# print((t2-t1))
