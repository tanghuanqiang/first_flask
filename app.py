from flask import  Flask,request,jsonify,abort  #导入Flask类
from flask_restful import Resource,Api,reqparse
from flask_sqlalchemy import SQLAlchemy
import json

app=Flask(__name__)         #实例化并命名为app实例
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='asdfghjkl'
# 创建数据库
db = SQLAlchemy(app)
# 建表
class Tasks(db.Model):
    __tablename__='tasks'
    id=db.Column(db.Integer,primary_key=True)
    description = db.Column(db.TEXT,nullable=False)
    done = db.Column(db.Boolean)
db.create_all()
# 账户
userid ='tanghuanqiang'
password = '1803206379'



parser = reqparse.RequestParser()
parser.add_argument('task', type=str)


# 查看id是否存在
def check_id(todo_id):
    task = Tasks.query.filter(Tasks.id==todo_id).first()
    if task != None:
        return True
    else:
        return False
def get_taskdata_by_id(todo_id):
    task = Tasks.query.get(todo_id)
    data = {
        "id":task.id,
        "description":task.description,
        "done":task.done
    }
    return data

# 日志管理
import logging
from logging.handlers import RotatingFileHandler


def setup_log():
    """配置日志"""

    # 设置日志的记录等级
    logging.basicConfig(level=logging.DEBUG)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
@app.route('/api/logs')
def logs_check():
    from flask import current_app
    current_app.logger.error('error')
    return 'logger'













#  获取单个任务 删除 修改
class Todo(Resource):
    def get(self,todo_id):
        if check_id(todo_id):
            data = get_taskdata_by_id(todo_id)
            return jsonify(data)
        else:
            return jsonify({"result":"False"})

    def delete(self,todo_id):
        if check_id(todo_id):
            c = Tasks.query.filter(Tasks.id == todo_id).first()
            data = json.loads(request.get_data())
            if data['login']['uid'] == userid and data['login']['password'] == password:
                db.session.delete(c)
                db.session.commit()
                return jsonify({"resule":"success"})
        else:
            return jsonify({"result":"False"})
    def put(self,todo_id):
        if check_id(todo_id):
            c = Tasks.query.filter(Tasks.id == todo_id).first()
            data = json.loads(request.get_data())
            if data['login']['uid'] == userid and data['login']['password'] == password:
                c.id = data['data']['id']
                c.description = data['data']['description']
                c.done = bool(data['data']['done'])
                db.session.add(c)
                db.session.commit()
            return jsonify({"resule":"success"})
        else:
            return jsonify({"result":"False"})

class TodoList(Resource):
    def get(self):
        tasks = Tasks.query.all()
        i = 1
        data = {}
        for t in tasks:
            detail = {
                'id': t.id,
                'description': t.description,
                'done': t.done
            }
            string = 'task' + str(i)
            data[string] = detail
            i += 1
        return jsonify(data)


class SpecialTodoList(Resource):
    def get(self,number,page):
        tasks = Tasks.query.all()
        i = 0
        start = int(number)*(int(page)-1) + 1
        end = int(number)*int(page)
        data = {}
        for t in tasks:
            i = i+1
            if i >= start and i<= end:
                detail = {
                    'id': t.id,
                    'description': t.description,
                    'done': t.done
                }
                string = 'task' + str(i)
                data[string] = detail

        return jsonify(data)


class TodoPOST(Resource):
    def post(self):
        data = json.loads(request.get_data())
        if data['login']['uid'] == userid and data['login']['password'] == password:
            data = data['data']
            c = Tasks(id=data['id'],description=data['description'],done=bool(data['done']))
            db.session.add(c)
            db.session.commit()
            return jsonify({"resule":"success"})
        else:
            return jsonify({"result":"False"})
api.add_resource(Todo,'/api/task/<todo_id>')
api.add_resource(TodoList,'/api/tasks')
api.add_resource(TodoPOST,'/api/task')
api.add_resource(SpecialTodoList,'/api/tasks/<number>:<page>')
if __name__=="__main__":
    setup_log()
    app.run(port=5000,host="127.0.0.1",debug=True)   #调用run方法，设定端口号，启动服务

