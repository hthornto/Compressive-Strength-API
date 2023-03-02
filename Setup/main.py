import psycopg2
from psycopg2 import extensions
import configparser


class SetupDatabases:
    def __init__(self):
        conn = None

    def setup_databases(self, settings):
        print("Databases")
        if settings["databases"]["main"] is None:
            self.main_database(settings)
            # self.project_database(settings)
        else:
            while True:
                # Main setup menu for database
                print("1. Change main database configuation.")
                # print("2. Add or change Projects/Clients databases settings")
                print("2. return back to main menu")
                answer = input("Please choose from the menu? ")
                if int(answer) == 1:
                    self.create_database_menu(
                        database=settings['databases'])
                """if int(answer) == 2:
                    self.create_database_menu(
                        database=settings['databases'], ismain=False)
                """
                if int(answer) == 2:
                    break
                else:
                    print("Incorrect option chosen please chose from the menu.")

    def main_database(self, settings):

        database = {}

        print(
            "Main database creation and connection. The main database will content concrete information.")
        DB_NAME = input("Name of database? ")
        DB_USER = input("Database username? ")
        DB_PASSWORD = input("Database Password? ")
        DB_HOST = input("Database host? ")
        PORT = input("Database Port number? ")
        DB_DIALECT = input("Database dialect? ")
        while True:
            if DB_NAME is None:
                DB_NAME = input("Name of database is required ")
            elif DB_USER is None:
                DB_USER = input("Database username is required ")
            elif DB_HOST is None:
                DB_HOST = input("Database host is required ")
            elif DB_DIALECT is None:
                DB_DIALECT = input("Database dialect is requied ")
            else:
                break
        database["DB_PASSWORD"] = DB_PASSWORD
        database["DB_USERNAME"] = DB_USER
        database["DB_NAME"] = DB_NAME
        database["DB_DIALECT"] = DB_DIALECT
        database["DB_HOST"] = DB_HOST
        database["DB_PORT"] = PORT

        settings['databases']['main'] = database

    def project_database(self, settings):
        anotherdatabase = input(
            "Do you want to include your clients and projects data with your compressive strength data? ")

        if anotherdatabase.upper() == "NO" or anotherdatabase.upper() == "N":
            DB_NAME = input("Name of database? ")
            DB_USER = input("Database username? ")
            DB_PASSWORD = input("Database Password? ")
            DB_HOST = input("Database host? ")
            PORT = input("Database Port number? ")
            DB_DIALECT = input("Database dialect? ")
            database = {
                "DB_PASSWORD": DB_PASSWORD,
                "DB_USERNAME": DB_USER,
                "DB_NAME": DB_NAME,
                "DB_DIALECT": DB_DIALECT,
                "DB_HOST": DB_HOST,
                "DB_PORT": PORT,
            }
            settings["databases"]['usemain'] = False
            settings['databases']['projects'] = database
        elif anotherdatabase.upper() == "YES" or anotherdatabase.upper() == "Y":
            settings["databases"]['usemain'] = True
        else:
            print("You need to enter yes or no.")

    def create_database_menu(self, database, ismain=True):
        main_database = {}
        while True:
            if ismain:
                print("1. Database name. Current setting:",
                      database['main']['DB_NAME'])
                print("2. Database username Current setting:",
                      database['main']['DB_USERNAME'])
                print("3. Database password Current setting:",
                      database['main']['DB_PASSWORD'])
                print("4. Database host Current setting:",
                      database['main']['DB_HOST'])
                print("5. Database port Current setting:",
                      database['main']['DB_PORT'])
                print("6. Database dialect Current setting:",
                      database['main']['DB_DIALECT'])
                print("7. Return")
            else:
                print("1. Database name. Current setting:",
                      database['project']['DB_NAME'])
                print("2. Database username Current setting:",
                      database['projectprojectprojectprojectproject']['DB_USERNAME'])
                print("3. Database password Current setting:",
                      database['projectprojectprojectproject']['DB_PASSWORD'])
                print("4. Database host Current setting:",
                      database['projectprojectproject']['DB_HOST'])
                print("5. Database port Current setting:",
                      database['projectproject']['DB_PORT'])
                print("6. Database dialect Current setting:",
                      database['project']['DB_DIALECT'])
                print("7. Return")
            answer = input("Please choose an option? ")
            if int(answer) == 1:

                DB_NAME = input("Name of database? ")
                main_database["DB_NAME"] = DB_NAME
            if int(answer) == 2:
                DB_USER = input("Database username? ")
                main_database["DB_USERNAME"] = DB_USER
            if int(answer) == 3:
                DB_PASSWORD = input("Database Password? ")
                main_database["DB_PASSWORD"] = DB_PASSWORD
            if int(answer) == 4:
                DB_HOST = input("Database host? ")
                main_database["DB_HOST"] = DB_HOST
            if int(answer) == 5:
                PORT = input("Database Port number? ")
                main_database["DB_PORT"] = PORT
            if int(answer) == 6:
                DB_DIALECT = input("Database dialect?")
                main_database["DB_DIALECT"] = DB_DIALECT
            if int(answer) == 7:
                break
        if ismain:
            database["main"] = main_database
        else:
            database["projects"] = main_database


class Main:
    def __init__(self):

        config = configparser.ConfigParser()
        config.read("../settings.ini")
        self.settings = {
            "databases": {
                "main": None,
                "projects": None,
                "usemain": "",
            },
            "general": {
                "SECRET_KEY": "",
                "API_PASSWORD": "",
                "API_KEY": "",


            },


        }
        if config.has_section("Databases"):
            self.settings['databases']['usemain'] = config['Databases']
        if config.has_section("Main Database"):
            self.settings["databases"]['main'] = config["Main Database"]
        if config.has_section("Projects Database"):
            self.settings["databases"]['projects'] = config["Projects Database"]
        if config.has_section("General"):
            self.settings['general'] = config["General"]
        # print(config["Projects Database"])
    setup_database = SetupDatabases()

    def run(self):
        while True:
            print("Welcome to a Concrete API and thanks for downloading it")
            print("1. Create secret key")
            print("2. Create ApI Key")
            print("3. Setup databases")
            print("4. Continue")
            print("5. Exit")
            answer = input("Please choose an option? ")
            if int(answer) == 1:
                secret_key = input("Choose an secret key?")
                self.settings['general']['SECRET_KEY'] = secret_key
            elif int(answer) == 2:
                api_key = input("Choose your api key? ")
                self.settings['general']["API_KEY"] = api_key
                api_password = input("Choose an api_password? ")
                self.settings['general']["API_PASSWORD"] = api_password
            elif int(answer) == 3:
                self.setup_database.setup_databases(settings=self.settings)
            elif int(answer) == 4:
                self.setup()
                break
            elif int(answer) == 5:
                break
            else:
                print("Please choose an option? ")

    def setup(self):
        # first create setup databases

        maindatabaseinfo = self.settings['databases']['main']
        conn = psycopg2.connect(
            database="postgres", user=maindatabaseinfo['DB_USERNAME'], password=maindatabaseinfo['DB_PASSWORD'], host=maindatabaseinfo['DB_HOST'], port=maindatabaseinfo['DB_PORT'])
        conn.autocommit = True
        cool = extensions.ConnectionInfo(conn)
        # print(cool)
        cur = conn.cursor()
        sql = "CREATE DATABASE " + maindatabaseinfo['DB_NAME']
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
        if self.settings['databases']['usemain'] == False:
            maindatabaseinfo = self.settings['databases']['projects']
            conn = psycopg2.connect(
                database="postgres", user=maindatabaseinfo['DB_USERNAME'], password=maindatabaseinfo['DB_PASSWORD'], port=maindatabaseinfo['DB_PORT'], host=maindatabaseinfo['DB_HOST'])
            conn.autocommit = True
            cool = extensions.ConnectionInfo(conn)
            # print(cool)
            cur = conn.cursor()
            sql = "CREATE DATABASE" + maindatabaseinfo['DB_NAME']
            cur.execute(sql)
        # first save database configurations
        config = configparser.ConfigParser()
        # config['Databases'] = {}
        print(self.settings['databases']['usemain'])
        config['Databases'] = {
            'usemain': self.settings['databases']['usemain']}
        config['Main Database'] = self.settings['databases']['main']

        if self.settings['databases']['projects'] is not None:
            config['Projects Database'] = self.settings['databases']['projects']
        # second general settings
        # decide on testing or not
        config['General'] = self.settings['general']
        # Create tables
        self.configfile = open('../settings.ini', 'wt')
        config.write(self.configfile)
        conn.close()


Main().run()
