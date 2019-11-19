# -- coding: utf-8 --
from flask import Flask
from flask import render_template, request
import dbModule

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    db_class = dbModule.Database()

    #sql = "select id, title, concat(a.addr1, ' ',a.addr2) addr, (select cat3_nm from TB_TYPE_CODE where cat3 = a.cat3) type, \
    sql =  "select id, title, SUBSTRING_INDEX(addr1, ' ', 1) addr, firstimage \
            from TB_DESTINATION a \
            where firstimage != '' \
            ORDER BY RAND() \
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


@app.route('/main', methods=['POST'])
def main():
    id = request.form['id']
    title = request.form['title']
    score = request.form['score']

    db_class = dbModule.Database()

    sql = "select id, title, (select cat3_nm from TB_TYPE_CODE where cat3 = a.cat3) type, concat(a.addr1, ' ',a.addr2) addr \
            from TB_DESTINATION a \
            limit 0, 30"
    row = db_class.executeAll(sql)

    # print(row)

    return render_template('test/index2.html',
                           result=None,
                           resultData=row,
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

