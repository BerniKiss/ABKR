import os
import json
import re
import server_files.database_op as db_op

current_database = None
current_db_metadata = None

#adatbazis tarolasa json faljba
DB_FILE = "databases.json"
#BASE_DIR = "databases"

VALID_TYPES = {"int", "float", "bit", "date", "datetime", "varchar"}

def is_valid_column_type(column_type):

    if column_type in VALID_TYPES:
        return True

    if column_type.startswith("varchar"):
        match = re.match(r"varchar\((\d+)\)", column_type)
        return bool(match)  # akkor True

    return False


def get_database_names_from_file(filepath):
    """Reads a JSON file and returns a list of database names."""
    try:
        with open(filepath, 'r') as file:
            database_data = json.load(file)
            database_names = list(database_data.keys())
            return database_names
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filepath}'.")
        return []


def use_database(db_name):
    global current_database


    db_path = os.path.join(DB_FILE, db_name)
    #print(f" Dolgozo konyvtar{BASE_DIR}")


    print(f"Checking if the database exists at: {db_path}")
    databases = load_databases()

    if db_name not in databases:
        return 1

    '''
    if not os.path.exists(db_path):
        print(f"Database '{db_name}' does not exist.")
        return 1
    '''

    current_database = db_name
    print(f"Using database: {current_database}")
    return 0


def load_databases():  # lehet ez nem fog kelleni
    #betolti az adatrbazist
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_databases(databases):
    with open(DB_FILE, "w") as f:
        json.dump(databases, f, indent=4)

def create_database(db_name):

    #databases = load_databases()

    #database_names = get_database_names_from_file(DB_FILE)

    databases = load_databases()

    if db_name in databases:
        return 1

    # hozzaadjuk az uj adatbazist
    databases[db_name] = {"tables": {}}

    # mentjuk a valtozasokat
    save_databases(databases)
    return 0

def drop_database(db_name):
    databases = load_databases()

    if db_name not in databases:
        return 1

    try:
        with open(DB_FILE, "r") as f:
            databases = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{DB_FILE}' not found.")
        return 1
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{DB_FILE}'.")
        return 1

    #db_name = db_op.current_database

    del databases[db_name]
    save_databases(databases)
    if db_name == db_op.current_database:
         db_op.current_database=None
    return 0


