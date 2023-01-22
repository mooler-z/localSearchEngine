import nltk
import re
import sqlite3
import json
import sys


def word_tokenizer(sentence):
    token = nltk.word_tokenize(sentence)
    classify = nltk.pos_tag(token)
    return classify


def get_important(classified):
    important = ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP',
                 'VBZ', 'JJ']
    filtered = []
    for word in classified:
        if word[1] in important:
            filtered.append(word)
    return filtered


def final_result(sent):
    x = word_tokenizer(sent)
    x = get_important(x)
    x.sort(key=lambda x: x[1])
    x = [i[0] for i in x]
    return x


def get_percentage(header, keys):
    if keys:
        pattern = "|".join([key.lower() for key in keys])
    else:
        return
    results = re.findall(pattern, header.lower())
    if not keys:
        return
    ratio = (len(results)/len(keys)) * 100
    if ratio >= 50:
        return ratio


def get_full_query(arr):
    query = "SELECT url, header from indexes WHERE\
    header LIKE"  # '%{}%'".format(arr[0])
    if not arr:
        arr = []
    for a in arr:
        query += f" '%{a}%' OR "
    else:
        query = query[:-4]
    return query


try:
    conn = sqlite3.connect("/home/ultron/00workSpace/scripting/python_202/project_s/localSearchEngine/temp.db")
    curs = conn.cursor()
except Exception as e:
    print("haha", e)


def select_values(arr):
    query = get_full_query(arr)

    if conn:
        curs.execute(query)
        results = []
        for result in curs.fetchall():
            ratio = get_percentage(result[1], arr)
            if ratio:
                results.append(result + (ratio,))
        results.sort(key=lambda x: x[2])
        results = results[::-1]
        if len(results) > 42:
            return results[:42]
        else:
            return results


def main_func(sent):
    sentence = sent
    keys = select_values(final_result(sentence))

    def getUrl(s):
        # pats = "developer.mozilla|javascript.info|www.w3schools.com"
        pats = "/htmldom|/jQuery|/jsInfo|/mdnWebDocs|/newW3|/mdn|/docker|/lodash|/express|/mongoose|/vueGuide|/sqlite|/python|/flask|/django|/dart|/laravel|/javatpoint|/mongodb|/NodeJs|/matplotlib"
        d = re.search(pats, s).start()
        return s[d+1:]

    def checkEx(s, arr):
        for i in arr:
            if s == i[1]:
                return False
        return True

    keys = [(getUrl(key[0]), key[1]) for key in keys]
    fkey = []
    for key in keys:
        if checkEx(key[1], fkey):
            fkey.append(key)
    keys = [dict(url=i[0], header=i[1]) for i in fkey]
    return keys


with open('results.json', 'w') as res:
    json.dump({"results": main_func(sys.argv[1])}, res)
