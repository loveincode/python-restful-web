#coding=utf-8
#————————————————————————————————————————————
#    程序：python web 实现 RestFul风格
#    作者：loveincode
#    日期：2017.9.22
#————————————————————————————————————————————

#Flask web框架  jsonify json格式处理 abort终止异常处理  make_response 回应 request 请求 
from flask import Flask,jsonify,abort,make_response,request

app = Flask(__name__)

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
    return jsonify({'persons': persons})

# curl -i http://localhost:5000/restful/person/2
@app.route('/restful/person/<int:id>', methods=['GET'])
def get_person(id):
    person = filter(lambda t: t['id'] == id, persons)
    if len(person) == 0:
        abort(404)
    return jsonify({'person': person[0]})

# curl -i -H "Content-Type: application/json" -X POST -d '{"name":"new loveincode"}' http://localhost:5000/restful/person
# curl -i -H "Content-Type: application/json" -X POST -d '{"name":"new loveincode","age":23}' http://localhost:5000/restful/person
# curl -i -H "Content-Type: application/json" -X POST -d '{"name":"new loveincode","age":23,"url":"1234"}' http://localhost:5000/restful/person
@app.route('/restful/person', methods=['POST'])
def create_person():
    if not request.json or not 'name' in request.json:
        abort(400)
    person = {
        'id': persons[-1]['id'] + 1,
        'name': request.json['name'],
		#如果没有提交age参数默认为20
        'age': request.json.get('age', 20),
		#同理如果没提交url，url也是默认值
		'url': request.json.get('url', "默认URL loveincode.cnblogs.com"),
		#该参数初始化FALSE
        'done': False
    }
    persons.append(person)
    return jsonify({'person': person}), 201

# curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/restful/person/2
# curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"update","age":30}' http://localhost:5000/restful/person/2
@app.route('/restful/person/<int:id>', methods=['PUT'])
def update_person(id):
    person = filter(lambda t: t['id'] == id, persons)
    if len(person) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != unicode:
        abort(400)
    if 'age' in request.json and type(request.json['age']) is not int:
        abort(400)
    if 'url' in request.json and type(request.json['url']) != unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    person[0]['name'] = request.json.get('name', person[0]['name'])
    person[0]['age'] = request.json.get('age', person[0]['age'])
    person[0]['url'] = request.json.get('url', person[0]['url'])
    person[0]['done'] = request.json.get('done', person[0]['done'])
    return jsonify({'person': person[0]})

# curl -i -X DELETE http://localhost:5000/restful/person/2
@app.route('/restful/person/<int:id>', methods=['DELETE'])
def delete_person(id):
    person = filter(lambda t: t['id'] == id, persons)
    if len(person) == 0:
        abort(404)
    persons.remove(person[0])
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Request Error'}), 400)

if __name__ == '__main__':
    app.run(debug=True)
