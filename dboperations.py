import MySQLdb as sqldb
import sys
import click
import _mysql
from todolist import settings
import django
import os.path

@click.group()
def sqlDB():
    "perform different sql operations using python"
    pass

def connect():
    "connects to mysql server"
    try:
        database = sqldb.connect('localhost', 'root', 'root')
        return  database
    except sqldb.Error as e:
        return None

def connectToDataBase(dbname):
    "connects to given database of MySQL server"
    try:
        connection = sqldb.connect('localhost', 'root', 'root', dbname)
        return connection
    except sqldb.Error :
        return None

@sqlDB.command("createdb",short_help="creates a database and tables")
def createdb():
    dbname=settings.DATABASES['default']['NAME']
    db = connect()
    if db is None:
        click.echo('Error occured while connecting to datase')
        sys.exit(1)
    click.echo('creating  a database..')
    sqlquery = db.cursor()
    sqlquery.execute(f"CREATE DATABASE IF NOT EXISTS {dbname}")
    db.commit()
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')
    pass


@sqlDB.command("dropdb",short_help="drops a database")
def dropdb():
    dbname = settings.DATABASES['default']['NAME']
    db=connectToDataBase(dbname)
    if db is None:
        click.echo('Error occured while connecting to datase')
        sys.exit(1)
    sqlquery=db.cursor()
    sqlquery.execute(f'DROP DATABASE IF EXISTS {dbname}')
    db.commit()
    click.echo(f"Database {dbname} is dropped")

if __name__=='__main__':
    sqlDB()