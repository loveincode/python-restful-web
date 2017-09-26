#coding=utf-8
#————————————————————————————————————————————
#    程序：python web 实现 RestFul风格
#    作者：loveincode
#    日期：2017.9.22
#————————————————————————————————————————————

#Flask web框架  jsonify json格式处理 abort终止异常处理  make_response 回应 request 请求 
from flask import Flask,jsonify,abort,make_response,request

#cors 跨域访问
from flask_cors import *


app = Flask(__name__);
CORS(app, supports_credentials=True);

file_handler = logging.FileHandler('app.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

#模拟数据库 person 属性 id name age done url
persons = [
    {
        'id': 1,
        'name': u'loveincode',
        'age': 20, 
        'done': False,
		'url':u'loveincode.cnblogs.com'
    },
    {
        'id': 2,
        'name': u'strive',
        'age': 18, 
        'done': False,
		'url':u'loveincode.cnblogs.com'
    }
]

# curl -i http://localhost:5000/restful/persons
@app.route('/restful/persons', methods=['GET'])
def get_persons():
    app.logger.info('enter get_persons');
    response = make_response(jsonify({'persons': persons}));
    response.headers['Access-Control-Allow-Origin'] = '*';
    response.headers['Access-Control-Allow-Methods'] = 'GET';
    return response;
    #return jsonify({'persons': persons})

# curl -i http://localhost:5000/restful/person/2
@app.route('/restful/person/<int:id>', methods=['GET'])
def get_person(id):
    app.logger.info('enter get_person');
    person = filter(lambda t: t['id'] == id, persons)
    if len(person) == 0:
        abort(404)
    response = make_response(jsonify({'person': person[0]}));
    response.headers['Access-Control-Allow-Origin'] = '*';
    response.headers['Access-Control-Allow-Methods'] = 'GET';
    return response;

@app.route('/restful/person', methods=['POST'])
def create_person():
    #if not request.json or not 'name' in request.json:
	#if not request.json :
    #    abort(400)
	#request.form 需要 application/x-www-form-urlencoded或者multipart/form-data
	#request.json 需要 application/json
    app.logger.info('enter create_person');
    if not request.form or not 'name' in request.form:
        abort(400)
    person = {
        'id': persons[-1]['id'] + 1,
        'name': request.form.get('name'),
        #如果没有提交age参数默认为20
        'age': request.form.get('age', 20),
        #同理如果没提交url，url也是默认值
        'url': request.form.get('url', "默认URL loveincode.cnblogs.com"),
        #该参数初始化FALSE
        'done': False
    }
    persons.append(person);
    response = make_response(jsonify({'person': person}), 201);
    response.headers['Access-Control-Allow-Origin'] = '*';
    response.headers['Access-Control-Allow-Methods'] = 'POST';
    return response;

@app.route('/restful/person/<int:id>', methods=['PUT'])
def update_person(id):
    app.logger.info('enter update_person');
    person = filter(lambda t: t['id'] == id, persons)
    if len(person) == 0:
        abort(404)
    #if not request.form:
    #    abort(400)
    #if 'name' in request.form and type(request.form['name']) != unicode:
    #    abort(400)
    #if 'age' in request.form and type(request.form['age']) is not int:
    #    abort(400)
    #if 'url' in request.form and type(request.form['url']) != unicode:
    #    abort(400)
    #if 'done' in request.form and type(request.form['done']) is not bool:
    #    abort(400)
    person[0]['name'] = request.form.get('name', person[0]['name'])
    person[0]['age'] = request.form.get('age', person[0]['age'])
    person[0]['url'] = request.form.get('url', person[0]['url'])
    person[0]['done'] = request.form.get('done', person[0]['done'])
	
    response = make_response(jsonify({'person': person[0]}));
    response.headers['Access-Control-Allow-Origin'] = '*';
    response.headers['Access-Control-Allow-Methods'] = 'PUT';
    return response;
    #return 

# curl -i -X DELETE http://localhost:5000/restful/person/2
@app.route('/restful/person/<int:id>', methods=['DELETE'])
def delete_person(id):
    app.logger.info('enter delete_person');
    person = filter(lambda t: t['id'] == id, persons)
    if len(person) == 0:
        abort(404)
    persons.remove(person[0])
    response = make_response(jsonify({'result': True}));
    response.headers['Access-Control-Allow-Origin'] = '*';
    response.headers['Access-Control-Allow-Methods'] = 'DELETE';
    return response;
    #return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Request Error'}), 400)

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)