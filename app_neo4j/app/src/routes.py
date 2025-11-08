from flask import render_template

def configure_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/create')
    def create():
        return render_template('create.html')
    
    @app.route('/get_task')
    def get_task():
        return render_template('get_task.html')

    @app.route('/delete')
    def delete():
        return render_template('delete.html')
    
    @app.route('/edit')
    def edit():
        return render_template('edit.html')