from server import app, db

@app.cli.command('init-db')
def init_db_command():
    db.create_all()
    print('Initialized the database.')
