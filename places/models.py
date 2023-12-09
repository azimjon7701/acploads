from django.db import models


class Place(models.Model):
    name = models.CharField(unique=True, max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.CharField(null=True, blank=True, max_length=255)


class Meta:
    ordering = ['name']
    verbose_name = 'Place'
    verbose_name_plural = 'Places'
    es_index_name = 'places_usa'
    es_type_name = 'places'

    es_mapping = {
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
