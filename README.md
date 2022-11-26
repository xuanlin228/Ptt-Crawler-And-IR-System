# Ptt-Crawler-And-IR-System
A ptt crawler to crawl the information from C_Chat, then use the import to Elastic Search to do the query system.

## Background
PTT 為台灣的大型論壇之一，每天都有數千篇文章在上面發表。而八卦板、C_Chat、股票板更是熱門看板，即時在線人數都有數千人至萬人。而PTT只會保留一年的文章，因此有精華區的功能，將舊文保留下來。但精華區使用網頁板觀看時，沒有關鍵字搜尋系統，有諸多不便。因此本次藉由webcrawler 和elasticsearch system，實作一個小型精華區關鍵字索引，方便使用者查找精華區文章。

## Environment
python 3.8.5<br>
Elasticsearch 7.11.2<br>
Java 8u321

## Set up environment
### Install Elasticsearch
1. Download [Elasticsearch](https://www.elastic.co/downloads/past-releases/elasticsearch-7-11-2)
2. Download Java
   * Download [Java jdk](https://www.oracle.com/java/technologies/downloads/#java8-windows)
   * [Set up Java environment variables](https://www.kjnotes.com/devtools/35)
3. Decompress and running Elasticsearch 
   * Decompress the downloaded Elasticsearch compressfile in step 1.
   * open cmd and change directory to Elasticsearch decompressed folder.
   * Running `bin\elasticsearch.bat`

    ```bash 
    > cd Downloads\elasticsearch-7.11.2
    > bin\elasticsearch.bat
    ```
### Install elasticsearch python package
```bash
> pip install elasticsearch==7.11.0
```
    
## Usage
1. change directory to Elasticsearch folder and running `bin\elasticsearch.bat`
    ```bash 
    > cd Downloads\elasticsearch-7.11.2
    > bin\elasticsearch.bat
    ```
2. Run query_elasticsearch.py
     ```bash 
    > python query_elasticsearch.py
    ```
## Result
<img src="https://user-images.githubusercontent.com/83528766/204094273-18c5ec85-b711-47b8-aeb8-27d494342455.png" alt= “Result” width="30%" height="30%">
