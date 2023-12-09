from elasticsearch import Elasticsearch

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
#
# def create_index():
#     es = connection()
#     index_name = "places_usa"
#
#     try:
#         index_exists = es.indices.exists(index=index_name)
#
#         if not index_exists:
#             es.indices.create(index=index_name, body=mapping)
#             print("Indeks muvaffaqiyatli yaratildi!")
#
#     except Exception as err:
#         print("Elasticsearch xatosi:", err)

def recreate_index(indices_client:Elasticsearch):
    try:
        index_name = "Places"
        if indices_client.exists(index_name):
            indices_client.delete(index=index_name)
        indices_client.create(index=index_name)
        indices_client.close(index=index_name)
        indices_client.put_settings(
            body={
                "analysis": {
                    "char_filter": {
                        "my_pattern": {
                            "type": "pattern_replace",
                            "pattern": "e",
                            "replacement": "i"
                        }
                    },
                    "normalizer": {
                        "my_normalizer": {
                            "type": "custom",
                            # "char_filter": ["quote"],
                            "filter": ["lowercase", "asciifolding"]
                        }
                    }
                }
            },
            index=index_name
        )
        indices_client.open(index=index_name)
        indices_client.put_mapping(
            body=mapping,
            index=index_name,
            include_type_name=True
        )

    except Exception as err:
            print("Elasticsearch xatosi:", err)
