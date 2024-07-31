import sys, os
import psycopg2
import argparse
from configparser import ConfigParser


def switch_database(conn, cursor, config):
    try:
        conn.close()
        print(f"Connection to '{conn.dsn}' closed.")
        conn = psycopg2.connect(dbname = config['dbname'],
                                user = config['user'],
                                password = config['password'],
                                host=config['host'],
                                port=config['port'])
                                
        conn.autocommit = True
        cursor = conn.cursor()
        print(f"Connected to '{conn.dsn}'")
        return conn, cursor
    except OperationalError as e:
        print(f"Error switching database: {e}")


def execute_sql_file(config, sql_file):

    conn = None
    cursor = None

    try:
        # Read the SQL file
        with open(sql_file, 'r') as file:
            sql_commands = file.read()

        # Replace parameters in SQL commands
        sql_commands = sql_commands.replace(':dbname', config['dbname'])
        sql_commands = sql_commands.replace(':user', config['user'])
        sql_commands = sql_commands.replace(':password', f"'{config['password']}'")

        # Connect to default postgres database
        conn = psycopg2.connect(
               dbname="postgres",
               user=config['admin_user'],
               password=config['admin_password'],
               host=config['host'],
               port=config['port']
        )

        print(f"Connected to '{conn.dsn}'")
        conn.autocommit = True
        cursor = conn.cursor()

        # Split commands and execute them one by one
        for command in sql_commands.split(';'):
            if command.strip() != '':
                if command.strip().lower().startswith('\\c'):
                    print(f"Switching to new database {config['dbname']}")
                    conn, cursor = switch_database(conn, cursor, config)
                else: 
                    cursor.execute(command)
                    print(f"Executed: {command.strip()}")
        
        print("All SQL commands executed successfully")

    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
           cursor.close()
        if conn:
           conn.close()


def main():
    parser = argparse.ArgumentParser(description="Create Charging Stations Table in PostgreSQL")
    parser.add_argument("--config", required=True, help="Path to configuration file")

    # Parse the arguments
    args = parser.parse_args()
    if not os.path.exists(args.config):
       print(f"Config file '{args.config}' not found.")
       parser.print_usage()
       exit(1)

    config = Config(args.config)

################################################################################
def main():
    parser = argparse.ArgumentParser(description='Process a cp_id parameter.')
    parser.add_argument("--config", default="./config.cfg", help="Config file path")
    parser.add_argument("--sql", default="./create_database.sql", help="SQL file path")

    # Parse the arguments
    args = parser.parse_args()
    if not os.path.exists(args.config):
       print(f"Config file '{args.config}' not found.")
       parser.print_usage()
       exit(1)
    if not os.path.exists(args.sql):
       print(f"SQL file '{args.sql}' not found.")
       parser.print_usage()
       exit(1)

    config = ConfigParser()
    config.read(args.config)

    section = "postgres"
    if not config.has_section(section):
       print(f"Config file {args.config} does not have '{section}' section.")
       exit(1)
  
    postgresql_config = config[section]
    execute_sql_file(postgresql_config,args.sql)

################################################################################
if __name__ == "__main__":
    main()
