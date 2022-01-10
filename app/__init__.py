from flask import Flask


# Создаю app - экземпляр класса Flask
app = Flask(__name__)
app.secret_key = 'zxc-magnaactor'

# Импорт модуля декорации маршрутов
from app import routes

if __name__ == "__main__":
    app.run(debug=True)

