from flask_restful import Resource
from flask import request, render_template
from services.connection import redis_client
from utils.data_hora import data_hora_atual
import os

UPLOAD_FOLDER = "uploads"

class TaskCreate(Resource):
    def post(self):
        try:
            # Captura os dados textuais
            title = request.form.get("title")
            status = request.form.get("status", "pendente")
            description = request.form.get("description", "")
            data_prev = request.form.get("data_prev", "")

            if not title:
                return {"status": "error", "message": "O título da tarefa é obrigatório"}, 400

            # Gera ID incremental
            task_id = redis_client.incr("task_id_counter")

            # Captura arquivo (se houver)
            file = request.files.get("arquive")
            arquive_name = None
            arquive_path = None

            if file and file.filename != "":
                arquive_name = file.filename
                arquive_path = os.path.join(UPLOAD_FOLDER, f"task_{task_id}_{arquive_name}")
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(arquive_path)

            # Captura data/hora atual
            created_at = data_hora_atual()

            # Salva metadados no Redis
            redis_client.hset(f"task:{task_id}", mapping={
                "id": task_id,
                "title": title,
                "status": status,
                "description": description,
                "data_prev": data_prev,
                "created_at": created_at,
                "arquive": arquive_name or "",
                "arquive_path": arquive_path or ""
            })

            return {
                "status": "success",
                "message": "Tarefa criada com sucesso!",
            }, 201

        except Exception as e:
            return {"status": "error", "message": f"Erro ao criar tarefa: {e}"}, 500

class TaskList(Resource):
    def get(self):
        try:
            tasks = []

            for key in redis_client.scan_iter("task:*"):
                task_data = redis_client.hgetall(key)

                task = {
                    "id": task_data.get("id", ""),
                    "title": task_data.get("title", ""),
                    "status": task_data.get("status", ""),
                    "description": task_data.get("description", ""),
                    "data_prev": task_data.get("data_prev", ""),
                    "created_at": task_data.get("created_at", ""),
                    "arquive": task_data.get("arquive", "")
                }

                tasks.append(task)

            return {"status": "success", "tasks": tasks}, 200

        except Exception as e:
            return {"status": "error", "message": f"Erro ao listar tarefas: {e}"}, 500

class TaskDeleteByName(Resource):
    def delete(self):
        try:
            # Captura o nome enviado no corpo da requisição
            data = request.get_json()
            title_to_delete = data.get("title")

            if not title_to_delete:
                return {"status": "error", "message": "É necessário informar o título da tarefa"}, 400

            deleted = False

            # Percorre todas as tarefas no Redis
            for key in redis_client.scan_iter("task:*"):
                task_data = redis_client.hgetall(key)

                if task_data.get("title") == title_to_delete:
                    redis_client.delete(key)
                    deleted = True

            if deleted:
                return {"status": "success", "message": f"Tarefa '{title_to_delete}' deletada com sucesso!"}, 200
            else:
                return {"status": "error", "message": f"Nenhuma tarefa encontrada com o título '{title_to_delete}'"}, 404

        except Exception as e:
            return {"status": "error", "message": f"Erro ao deletar tarefa: {e}"}, 500
        
class TaskEdit(Resource):
    def put(self, task_id):
        try:
            # Busca a tarefa pelo ID
            key = f"task:{task_id}"
            if not redis_client.exists(key):
                return {"status": "error", "message": f"Tarefa {task_id} não encontrada"}, 404

            # Captura dados enviados
            title = request.form.get("title")
            status = request.form.get("status")
            description = request.form.get("description")
            data_prev = request.form.get("data_prev")

            # Captura novo arquivo (se houver)
            file = request.files.get("arquive")
            arquive_name = None
            arquive_path = None

            if file and file.filename != "":
                arquive_name = file.filename
                arquive_path = os.path.join(UPLOAD_FOLDER, f"task_{task_id}_{arquive_name}")
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(arquive_path)

            # Atualiza os campos no Redis (apenas os que foram enviados)
            updates = {}
            if title: updates["title"] = title
            if status: updates["status"] = status
            if description: updates["description"] = description
            if data_prev: updates["data_prev"] = data_prev
            if arquive_name: updates["arquive"] = arquive_name
            if arquive_path: updates["arquive_path"] = arquive_path

            if updates:
                redis_client.hset(key, mapping=updates)

            # Retorna a tarefa atualizada
            task_data = redis_client.hgetall(key)

            return {
                "status": "success",
                "message": f"Tarefa {task_id} atualizada com sucesso!",
                "task": task_data
            }, 200

        except Exception as e:
            return {"status": "error", "message": f"Erro ao editar tarefa: {e}"}, 500