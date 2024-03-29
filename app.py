# -- coding: utf-8 --
from flask import Flask, request
from flask import render_template
import dbModule
import requests, json
import ast

app = Flask(__name__)
db_class = dbModule.Database()

@app.route('/', methods=['GET'])
def index():

    #ORDER BY RAND() \
    #sql = "select id, title, concat(a.addr1, ' ',a.addr2) addr, (select cat3_nm from TB_TYPE_CODE where cat3 = a.cat3) type, \
    sql =  "select id, title, SUBSTRING_INDEX(addr1, ' ', 1) addr, firstimage, (select cat3_nm from TB_TYPE_CODE where cat3 = a.cat3) type \
            from TB_DESTINATION a \
            where firstimage != '' \
            limit 0, 32"
    row = db_class.executeAll(sql)

    #print(row)

    return render_template('index.html',
                           result=None,
                           resultData=row,
                           resultUPDATE=None)


# @app.route('/index', methods=['GET'])
# def index():
#     db_class = dbModule.Database()
#
#     #sql = "select id, title, concat(a.addr1, ' ',a.addr2) addr, (select cat3_nm from TB_TYPE_CODE where cat3 = a.cat3) type, \
#     sql =  "select id, title, concat(a.addr1, ' ',a.addr2) addr \
#             from TB_DESTINATION a \
#             limit 0, 30"
#     row = db_class.executeAll(sql)
#
#     #print(row)
#
#     return render_template('test/index2.html',
#                            result=None,
#                            resultData=row,
#                            resultUPDATE=None)


@app.route('/main', methods=['GET', 'POST'])
def main():
    des_id = request.form['des_id']
    score = request.form['score']
    title = request.form['title']
    print(id, score, title)

    url = 'http://125.131.73.94:60042/get_cb_places?titles=' + title + '&scores=' + score
    print(url)
    headers = {'Content-type': 'application/json'}
    response = requests.get(url, headers=headers)
    #print(response.json())

    #한글
    data = json.dumps(response.json(), ensure_ascii=False)
    print(data)


    cb_title = ''
    cb_count = 0
    for d in json.loads(data):
        cb_title += '\'' + d[0] + '\','
        cb_count += 1
        if(cb_count == 20):
            break

    print(cb_title)
    #string = u'\ud0a8\ub354\ub79c\ub4dc'
    #format_strings = ','.join(['%s'] * len(list_of_ids))



    sql = "select id, title, (select cat3_nm from TB_TYPE_CODE where cat3 = a.cat3) type,  \
           if(firstimage != '',firstimage, 'http://placehold.it/500x325') firstimage, SUBSTRING_INDEX(addr1, ' ', 1) addr \
            from TB_DESTINATION a \
            where title in (" + cb_title[:-1] + ") \
            limit 0, 20"
    print(sql)

    row = db_class.executeAll(sql)


    return render_template('main.html',
                           resultData=row,
                           resultScore=data,
                           resultUPDATE=None)


#
# @app.route('/', methods=['GET'])
# def index():
#     return render_template('test/main.html',
#                            result=None,
#                            resultData=None,
#                            resultUPDATE=None)
#
#
# # INSERT 함수 예제
# @app.route('/insert', methods=['GET'])
# def insert():
#     db_class = dbModule.Database()
#
#     sql = "INSERT INTO testDB.testTable(test) \
#                 VALUES('%s')" % ('testData')
#     db_class.execute(sql)
#     db_class.commit()
#
#     return render_template('test/main.html',
#                            result='insert is done!',
#                            resultData=None,
#                            resultUPDATE=None)
#
#
# # SELECT 함수 예제
# @app.route('/select', methods=['GET'])
# def select():
#     db_class = dbModule.Database()
#
#     sql = "SELECT idx, test \
#                 FROM testDB.testTable"
#     row = db_class.executeAll(sql)
#
#     print(row)
#
#     return render_template('test/main.html',
#                            result=None,
#                            resultData=row[0],
#                            resultUPDATE=None)
#
#
# # UPDATE 함수 예제
# @app.route('/update', methods=['GET'])
# def update():
#     db_class = dbModule.Database()
#
#     sql = "UPDATE testDB.testTable \
#                 SET test='%s' \
#                 WHERE test='testData'" % ('update_Data')
#     db_class.execute(sql)
#     db_class.commit()
#
#     sql = "SELECT idx, test \
#                 FROM testDB.testTable"
#     row = db_class.executeAll(sql)
#
#     return render_template('test/main.html',
#                            result=None,
#                            resultData=None,
#                            resultUPDATE=row[0])



if __name__ == '__main__':
    app.run(debug=True)

