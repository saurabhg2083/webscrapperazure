import mysql.connector
from mysql.connector import errorcode
from mysql.connector.errors import *
import logging
import sys
import configparser

logging.basicConfig(filename="sg_logs.log", format='%(asctime)s %(message)s', filemode='w', level=logging.INFO)

class mysqldbconnection:
    def __init__(self, debug=False):
        config = configparser.ConfigParser()
        config.read('mysqlconfig.ini')
        self.host = config['mysqlDB']['host']
        self.dbuser = config['mysqlDB']['user']
        self.dbpass = config['mysqlDB']['pass']
        self.dbname = config['mysqlDB']['db']


        self.port = '3306'
        self.debug = debug
        self.conn = None
        try:
            self.conn = self.get_connector()
        except mysql.connector.Error as err:
            logging.error('Error in Scraping check ', err)
            sys.exit(1)
        if self.debug:
            logging.info('Connected to host.')

        self.cursor = self.conn.cursor()

    def get_connector(self):
        if self.debug:
            print('Connecting to database...')
        # If there is an active connection ,return it
        if isinstance(self.conn, mysql.connector.connection.MySQLConnection):
            if self.debug:
                print('Already connected!')
            return self.conn

        #return mysql.connector.connect(host=str(self.host), user=str(self.dbuser), password=str(self.dbpass), database=str(self.dbname), port=self.port)
        return mysql.connector.connect(host='127.0.0.1',
                                       user='root',
                                       password='',
                                       database='ineuron_scrapper',
                                       port='3306')


    def get_results(self, query):
        try:
            self.cursor.execute(query)
        except InternalError as e:
            if self.debug:
                print('Error in %s: No results for table %s' % (str(e)))
            return []
        return self.cursor.fetchall()

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.commit()
        except Exception as e:
            if self.debug:
                print('Error: %s' % str(e))
            self.rollback()
        finally:
            self.close_connection()

    def commit(self):
        if self.debug:
            print('Commiting changes...')
        self.conn.commit()

    def rollback(self):
        if self.debug:
            print('Rolling back...')
        self.conn.rollback()

    def close_connection(self):
        self.conn.close()
        if self.debug:
            print('Connection closed.')

    def clear_cursor(self):
        if self.debug:
            print('Clearing cursor...')
        self.cursor.fetchall()

