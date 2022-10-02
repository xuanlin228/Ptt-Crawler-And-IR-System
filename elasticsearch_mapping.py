from elasticsearch import Elasticsearch, helpers
import json

chat_mapping = {
    "properties": {
        "catalogueTitle": {
            "type": "keyword"
        },
        "title": {
            "type": "text",
            "analyzer": "ik_max_word",
            "search_analyzer": "ik_max_word"
        },
        "author": {
            "type": "keyword"
        },
        "board": {
            "type": "keyword"
        },
        "date": {
            "type": "keyword"
        },
        "article": {
            "type": "text",
            "analyzer": "ik_smart",
            "search_analyzer": "ik_smart"
        }
    }
}

renames_key = {
    'catalogueTitle': 'catalogue_title',
    'title': 'title',
    'author': 'author',
    'board': 'board',
    'date': 'date',
    'article': 'article',
}


# dataset
def read_data():
    with open('data.json', 'r') as f:
        for row in f:
            d = eval(row.strip())
            d = json.dumps(d)
            row = json.loads(d)

            for k, v in renames_key.items():
                for old_name in list(row):
                    if k == old_name:
                        row[v] = row.pop(old_name)
            yield row


def load2_elasticsearch():
    index_name = 'c_chat_article'
    type = 'one_to_one'
    es = Elasticsearch()

    # Create Index
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
    print('Index created!')

    # Put mapping into index
    if not es.indices.exists_type(index=index_name, doc_type=type):
        es.indices.put_mapping(index=index_name,
                               doc_type=type,
                               body=chat_mapping,
                               include_type_name=True)
    print('Mappings created!')

    # Import data to elasticsearch
    success, _ = helpers.bulk(client=es,
                              actions=read_data(),
                              index=index_name,
                              doc_type=type,
                              ignore=400)
    print('success: ', success)


load2_elasticsearch()
