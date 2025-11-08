from flask import Flask
from routes import configure_routes
from flask_restful import Api
from services.api_tarefas import TaskCreate, TaskList, TaskDeleteByName, TaskEdit

app = Flask(__name__)
api = Api(app)

api.add_resource(TaskCreate, '/criar_tarefa/')
api.add_resource(TaskList, '/task_list/')
api.add_resource(TaskDeleteByName, '/delete_task_by_name')
api.add_resource(TaskEdit, "/edit_task/<int:task_id>")

configure_routes(app)

if __name__ == '__main__':
    app.run(debug=True)