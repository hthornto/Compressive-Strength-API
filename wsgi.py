from src import create_app
from decouple import config
# from logging import config
import logging

if config("DEBUG") == False:
    logging.basicConfig(filename='concrete-api.log',
                        filemode='w', level=logging.INFO)


create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
