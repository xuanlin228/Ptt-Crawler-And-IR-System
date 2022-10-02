from elasticsearch import Elasticsearch
import json

from pygments import highlight


def query(query):
    es = Elasticsearch()

    index_name = 'c_chat_article'
    type = 'one_to_one'

    # Query DSL
    search_params = {
        "query": {
            "multi_match": {
                "query": query,
                "operator": "and",
                "type": "phrase",
                "fields": ["title", "article"]
            }
        },
        "highlight": {
            "fields": {
                "title": {
                    "pre_tags": ["\033[0;42m"],
                    "post_tags": ["\033[0m"]
                },
                "article": {
                    "pre_tags": ["\033[0;42m"],
                    "post_tags": ["\033[0m"]
                }
            }
        },
        "size": 15
    }
    #Search document
    result = es.search(index=index_name, doc_type=type, body=search_params)
    result_list = result['hits']['hits'][:]

    result = json.dumps(result_list, indent=4, ensure_ascii=False)
    with open('result.json', 'w', encoding='utf-8') as f:
        f.write(result)
        f.write('\n')

    return result_list


def author_query(query):
    es = Elasticsearch()

    index_name = 'c_chat_post'
    type = 'one_to_one'

    # Query DSL
    search_params = {
        "query": {
            "match": {
                "author": query
            }
        },
        "highlight": {
            "fields": {
                "author": {
                    "pre_tags": ["\033[0;41m"],
                    "post_tags": ["\033[0m"]
                }
            }
        }
    }
    #Search document
    result = es.search(index=index_name, doc_type=type, body=search_params)
    result_list = result['hits']['hits'][:]

    result = json.dumps(result_list, indent=4, ensure_ascii=False)
    with open('result.json', 'w', encoding='utf-8') as f:
        f.write(result)
        f.write('\n')

    return result_list


def print_results(results):
    #print("\n共有" + str(len(results)) + "筆搜尋結果\n")

    for i in range(0, len(results)):
        #print(i)
        r = results[i]
        print("score: " + str(r["_score"]))
        print("catalogue:" + r["_source"]["catalogue_title"])
        #print("author:"+r["_source"]["author"])
        print("author:" + r["_source"]["author"])

        if 'title' in r["highlight"]:
            print("title:" + r["highlight"]["title"][0])
        else:
            print("title:" + r["_source"]["title"])

        if 'article' in r["highlight"]:
            print("article:\n" + r["highlight"]["article"][0])
            '''
        else:
            print("article:\n" + r["_source"]["article"])
            '''
        print(
            "=================================================================="
        )


while True:
    search_choice = input("搜尋作者請按a , 搜尋關鍵字請按/ , 結束搜尋請按0: ")
    if search_choice == 'a':
        search_author = input("請輸入作者名: ")
        results = author_query(search_author)
        print_results(results)

    elif search_choice == '/':
        search_keyword = input("請輸入搜尋關鍵字: ")
        results = query(search_keyword)
        print_results(results)

    elif search_choice == '0':
        break
    else:
        print("無相關搜尋指令，請重新輸入")

print("搜尋結束")
