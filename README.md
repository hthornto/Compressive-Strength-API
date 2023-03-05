# Concrete-API


#This software has been copyright by the Author and all rights have been reserved by him.
#This software currently can only be downloaded and used and not modified without the permission of the author

#This api is meant to be simple and straight forward.


Setup

1. Found a capablity database. The compatable databases are mysql, postgres, sqlite, and msSQL.
2. Create a database or use setup if using postgresSQL.
3. Create and ini file titled settings.ini or use setup if you are using an postgresSQL database. I am planning on adding the ability to setup other databases within setup. See the section on what is required in the settings file.

Settings.ini file

The program currently requires to sections. [Main Database] and [General]. Below is a sample of the necassary components within the file  and currently the only options.
    
    [Main Database]
    db_password = my_database_password
    db_username = my_database_username
    db_name = my_database_name
    db_dialect = my_sql_dialect
    db_host = my_database_server
    db_port = database_port_number

    [General]
    secret_key = dev
    api_password = api_password
    api_key = my_api_key


Security
    The api has two different necassery components for security. The first security feature is the ability to for only those or have the api password and key. They second security feature is the secret key. It is necassery for sessions.  This allows the user to stay logged in for 30 days.  See the logging in section for logging into the api.

    Logging In
        URL = /api/loginapi
        JSON required
        Methods = post
        
        Fields = {
            api_password = api_password  #Required
            api_key = my_api_key #Required
        }

        The settings.ini file is essential for security purposes
    Logging Out
        URL = /api/loginapi
        Methods = get

Clients

    The fields = {
            "name": String  #required
            "address": String
            "city": Sring
            "state": String(2)  #Two characters long MAX
            "postalcode": String
            "country": String(3)  # Three characters long MAX
        }

    Add a client.
        The url = /api/clients
        Requires json string
        Method = post
    Delete a client
        URL = /api/clients/<id of client>
        Method = delete
    Update client
        URL = /api/clients/<id of client>
        Requires json string
        Method = patch or put
    Show one client
        URL = /api/clients/<id of client>
        Method = get
    Show all clients 
        URL = URL = /api/clients
        Method = get

Projects

    The fields = {
            "name": String #Required
            "client_id": Foreign Key Integer #Required
        }
    Add project
        URL = /api/projects
        JSON required
        Method = post
    Delete project
        URL = /api/projects/<id of project>
        Method = delete
    Update project
        URL = /api/projects/<id of project>
        Json required
        Method = put or patch
    Show a project
        URL = /api/projects/<id of project>
        method = get
    Show all projects
        URL = /api/projects
        method = get
    


Mixused

    The fields = {
            "producer": String  #required Will probably change this to Integer and add another table titled producers. Most grout and morter are made by the contractor and not the a concrete company
            "mix_description": String
            "mix_code": String
            "strength": Integer
            "isMRWH": Boolean  #required
            "isHRWH": Boolean  #required
        }
    Add mixused
        URL = /api/compressive-strength/mix-used
        Requires JSON string to add fields
        Method = post
    Delete mixused
        URL =/api/compressive-strength/mix-used
        Method = delete
    Update mixused
        URL = /api/compressive-strength/mix-used/<id of mixused>
        Requires JSON string
        Method = put or patch
    Show mixused
        URL = /api/compressive-strength/mix-used<id of mixused>
        Method = get
    Show all mixes used
        URL = /api/compressive-strength/mix-used
        Method = get

Mix Designs

    The fields = {
            'mix description': String
            "producer":  String #Required
            "max slump": Float
            "min slump": Float
            "max air content": Float
            "min air content": Float
            "MRWH max slump": Float
            "MRWH min slump": Float
            "HRWH max slump": Float
            "HRWH min slump": Float
            "design_strength": Integer #Required
            "project_id": Integer #Required
            "break_schedule": JSON #requird See the break schedule below this.

        }

        The break schedule fields are = [
            {'age':7, 'hold': False},
            {'age':28, 'hold': False},
            {'age':28, 'hold': False},
            {'age':28, 'hold': False},
            {'age':28, 'hold': True},
        ]
    Add mix design
        URL = /api/mix-design
        JSON is required see fields section to know what is required.
        Method = post
    Delete mix design
        URL= /api/mix-design/<id of mix design>
        Method = delete
    Update mix design
        URL = /api/mix-design/<id of mix design>
        JSON is required
        Method = put or patch
    Show mix design
        URL = /api/mix-design/<id of mix design>
        Method = get
    Show all mix designs
        URL /api/mix-design
        Method = get

Speciemn Types

    The fields = {
            "type": String (Only options "prism", cylinder, cube) #Required may add beams in the future
            'size': String  #Required that about changing this to a float or removing it.  This only helps distringishing between a 4 inch and a six inch cylinder
        }
    Add specimen typs
        URL = /api/compressive-strength/specimen-types
        JSOn required
        Method = post
    Delete specimen types
        URL = /api/compressive-strength/specimen-types<id of specimen type>
        Method = delete
    Update specimen type
        URL = /api/compressive-strength/specimen-types<id of specimen type>
        JSON required
        Method = put or patch
    Show specimen type
        URL = /api/compressive-strength/specimen-types<id of specimen type>
        Method = get
    Show all specimen types
        URL = /api/compressive-strength/specimen-types
        Method = get

Cylinders

    The fields{
            "set_id": Foregin Key Integer #Required
            "max_load": Integer
            "dia1": Float
            "dia2": Float
            "break_strength": Integer  #Should automatically be calculated based upon dia1, dia2, max_load, and cylinder types
            "cylinder_type_id": Foreign key Integer # Required
            "break_type": String  #All break types require a number from 1 to 6 however, a modifer maybe added
            "weight": Float
            "lab_tech_id": Integer #Could connect to another database and use those names
            "recieved": Date 
            "age": Integer #Required
            "hold": Boolean #Required
        }
    Add cylinders
        New compressive-strength specimens can be added one at a time. They are also added when you create a new set of them.
        URL = /api/compressive-strength/cylinders
        Method = post
    Delete cylinders
        URL = /api/compressive-strength/cylinders<id of cylinder>
        Method = delete
    Update cylinders
        Cylinders are updated using multiple update method. This also only for single cylinder to be updated.
        URL = /api/compressive-strength
        Method = put or patch
    Show cylinders
        All cylinders are shown in sets. See the section on Sets

Sets

    The fields = {
        'slump': Float
        'air_content': Float
        'temperature': Integer
        'ticket_number': String
        'mix_id': Foreign key Integer  #Required
        'total_cy': Integer
        'project_id': Integer  #Required  No foreign key if someone decides to use they own database for their projects infomation
        'field_tech_id': Integer
        'mix_used_id':  Foreign Key Integer
        
    }
    Add a set
        URL = /api/compressive-strength
        Json Required
        Method = post
    Delete set
        URL = /api/compressive-strength<id of set>
        Method = delete
    Show all cylinders
        URL = /api/compressive-strength
        Method = get
    Show by project
        URL = /api/compressive-strength/projects/<id of project>
        Method = get
    Show a set
        URL = /api/compressive-strength/<id of set>
        Method = get
    
