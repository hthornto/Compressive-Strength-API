from src import create_app
from decouple import config

create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
