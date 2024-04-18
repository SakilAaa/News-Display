import sqlite3
import math

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
D = 5044
cursor.execute("SELECT * FROM inverted_index")
for row in cursor.fetchall():
    word = row[0]
    doc_id = row[1].split(',')
    d = len(doc_id)
    idf = math.log(D / (1 + d), 10)
    doc_id = [int(i) for i in doc_id]
    for id in doc_id:
        cursor.execute("SELECT * FROM news_news WHERE id = %s" % id)
        result = cursor.fetchall()[0]
        text = result[1] + result[2]
        N = int(result[11])
        n = text.count(word)
        tfidf = n / N * idf
        cursor.execute("INSERT INTO tfidf (word, doc_id, tfidf) VALUES('%s', '%s', %f)" % (word, id, tfidf))
    
conn.commit()
cursor.close()
conn.close()



    