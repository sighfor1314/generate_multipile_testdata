cx_Oracle.init_oracle_client(lib_dir="/Users/synergies/Downloads/instantclient_19_8")

import cx_Oracle
import pandas as pd
import numpy as np
import pymssql
import mysql.connector
import psycopg2
import pysftp

class DataManagement():
    def setConnection(self, connection_info):
        '''
            goal:
                connection_info 必須選擇 sql_info.ini 中的其中一個 DB 或 sftp
                根據要使用的DB 回傳對應的object
                根據要使用的SFTP 回傳對應的object

            example:
                setConnection("mysql 56")
                setConnection("sftp-qa")
        '''

        ini_file_name = ("sql_info.ini")
        configuration = configparser.ConfigParser()
        configuration.optionxform = str
        configuration.read(ini_file_name)

        #  connection_info  == ORACLE
        if configuration[connection_info]['type'] == 'ORACLE':
            cx_Oracle.init_oracle_client(lib_dir="instantclient_19_8")
            return cx_Oracle.connect(configuration[connection_info]['db-username'], configuration[connection_info]['db-password'],
                                     configuration[connection_info]['db-host'] + ':' + configuration[connection_info]['db-port'] + '/' +
                                     configuration[connection_info]['db-name'])

        #  connection_info  == MYSQL
        elif configuration[connection_info]['type'] == 'MYSQL':
            return  mysql.connector.connect(host=configuration[connection_info]['db-host'], user=configuration[connection_info]['db-username'],
                                           password=configuration[connection_info]['db-password'],
                                           database=configuration[connection_info]['db-name'])

        #  connection_info  == MSSQL
        elif configuration[connection_info]['type'] == 'MSSQL':
            return pymssql.connect(host=configuration[connection_info]['db-host'], user=configuration[connection_info]['db-username'],
                                   password=configuration[connection_info]['db-password'], database=configuration[connection_info]['db-name'])


        #  connection_info == POSTGRESQL
        elif configuration[connection_info]['type'] == 'POSTGRESQL':
            return psycopg2.connect(host=configuration[connection_info]['db-host'], user=configuration[connection_info]['db-username'],
                                    password=configuration[connection_info]['db-password'], database=configuration[connection_info]['db-name'])


        # connection_info == sftp
        elif configuration[connection_info]['type'] == 'sftp':
            return pysftp.Connection(host=configuration[connection_info]['sftp-host'], username=configuration[connection_info]['sftp-username'],
                                     password=configuration[connection_info]['sftp-password'])


    def setSftpInsertion(self, sftp_info, sftp_path, local_file_path, sftp_file_name=None):
        '''
        goal:
           新增、更新檔案到 sftp server
        usage:
            sftp_info 必須選擇 qajarvix.ini 中的其中一個 sftp server（可增加 qajarvix.ini 中的 sftp 資訊）
        example:
            - 新增檔案: 將 file.csv 上傳到 sftp server
            setSftpInsertion("指定的方法", "sftp欲到達的目錄", "local檔案路徑")
            setSftpInsertion("sftp-qa", sftp_path="/upload/Automation", local_file_path="/local/upload/file.csv")
            - 更新檔案: 將 new_file.csv 更新到 sftp server 上的 file.csv
            setSftpInsertion("sftp-qa", sftp_path="/upload/Automation", local_file_path="/local/upload/new_file.csv", sftp_file_name="file.csv")
        '''

        connect = self.setConnection(sftp_info)  #get sftp object
        with connect.cd(sftp_path):  # 移動到sftp檔案目錄
            connect.put(local_file_path, sftp_file_name)  # 上傳local檔案
        connect.close()

    def setSftpDeletion(self,sftp_info,sftp_path,file_name):
        '''
               goal:
                   刪除sftp server檔案
               example:
                    setSftpInsertion("指定的方法", "sftp欲到達的目錄", "欲刪除的檔案名稱")
                    setSftpInsertion('sftp-qa','/upload/Automation','file.csv')
        '''

        connect = self.setConnection(sftp_info) #get sftp object
        with connect.cd(sftp_path):  # 移動到sftp檔案目錄
            connect.remove(file_name)  # 上傳local檔案
        connect.close()

    def setSqlInsertion(self,db_info,table_name, file_path):
        '''
           goal:
               執行 SQL - INSERT INTO %s VALUES (%s)
           example:
               setSqlInsertion("指定資料庫類別", "sql的table_name", "local檔案路徑")
               setSqlInsertion('mssql 1433','customized_table','/local/upload/file.csv')
        '''
        configuration = self.config
        connect = self.setConnection(db_info) # 回傳db object
        cur = connect.cursor() #建立cursor
        try:
            with open(file_path, newline=''):
                data = pd.read_csv(file_path)
                data= data.replace({np.nan:None})
                column_length = len(data.values[0])
                column_count = ""
                '''
                 依照不同的資料庫對 VALUES (%s) 做字串處理
                 oracle為 ：「:1,:2,:3...」
                 其他為： 「%s,%s,%s...」
                '''
                if configuration[db_info]['type'] == 'ORACLE':
                    for i in range(1, column_length + 1):
                        column_count += ':' + str(i)
                        if i != column_length:
                            column_count += ','
                elif configuration[db_info]['type'] in ['POSTGRESQL','MSSQL','MYSQL']:
                    for i in range(1, column_length + 1):
                        column_count += '%s'
                        if i != column_length:
                            column_count += ','
                rows = [tuple(x) for x in data.values]
                sql_insert = "INSERT INTO %s VALUES (%s)" % (table_name, column_count)
                cur.executemany(sql_insert, rows)
                connect.commit()

        finally:
            connect.close()

    def setSqlDeletion(self,db_info, table_name, condition=""):
        '''
              goal:
                  執行 SQL - delete from %s  %s'
              example:
                  setSqlDeletion("指定資料類別", "sql的table_name", "自定sql語法")
                  setSqlDeletion('mssql 1433','customized_table')
                  setSqlDeletion('mssql 1433','customized_table',"where city = 'Taipei' and salary >= 50000")
        '''
        connect = self.setConnection(db_info)
        cur = connect.cursor()
        sql_delete = 'delete from %s  %s' % (table_name, condition)
        cur.execute(sql_delete)
        connect.commit()
        connect.close()

    def createSftpFile(self,sftp_info,sftp_path,file_name):
        connect = self.setConnection(sftp_info)  # 回傳db object
        with connect.cd(sftp_path):  # temporarily chdir to public
            connect.put(file_name)

    def createMysqlTalbe(self,db_info,file_name):
        connect = self.setConnection(db_info)
        cur = connect.cursor()
        cur.execute(
            "CREATE TABLE "+file_name+" ( id INT,'n_int INT','n_longint BIGINT','n_float FLOAT','n_float1 FLOAT',"
                                      "'n_negative_int INT','n_positive_int INT','n_negative_float FLOAT','n_positive_float FLOAT'"
                                      "c_char VARCHAR(255), c_char1 VARCHAR(255),, c_char2 VARCHAR(255), c_char3 VARCHAR(255), c_char4 VARCHAR(255), c_char5 VARCHAR(255),"
                                      " 桃園市_英 VARCHAR(255), 桃園市_中 VARCHAR(255), c_null1 VARCHAR(255),c_null2 VARCHAR(255),c_empty VARCHAR(255),c_constant VARCHAR(255)"
                                      "b_boolean BIT,"
                                      "t_time Date)")
        connect.commit()
        connect.close()

    def createMssqlTalble(self,db_info,talbe_name):
        connect = self.setConnection(db_info)
        cur = connect.cursor()
        '''
            msssql 沒有支援boolean boolean-->BIT 
        '''
        cur.execute("CREATE TABLE "+talbe_name+" ( id INT,'n_int INT','n_longint BIGINT','n_float FLOAT','n_float1 FLOAT',"
                                      "'n_negative_int INT','n_positive_int INT','n_negative_float FLOAT','n_positive_float FLOAT'"
                                      "c_char VARCHAR(255), c_char1 VARCHAR(255),, c_char2 VARCHAR(255), c_char3 VARCHAR(255), c_char4 VARCHAR(255), c_char5 VARCHAR(255),"
                                      " 桃園市_英 VARCHAR(255), 桃園市_中 VARCHAR(255), c_null1 VARCHAR(255),c_null2 VARCHAR(255),c_empty VARCHAR(255),c_constant VARCHAR(255)"
                                      "b_boolean BIT,"
                                      "t_time DATE)")
        connect.commit()
        connect.close()

    def createOracleTable(self,db_info,table_name):
        connect = self.setConnection(db_info)
        cur = connect.cursor()
        cur.execute("CREATE TABLE "+table_name+" ( id INT,'n_int INT','n_longint BIGINT','n_float FLOAT','n_float1 FLOAT',"
                                      "'n_negative_int INT','n_positive_int INT','n_negative_float FLOAT','n_positive_float FLOAT'"
                                      "c_char VARCHAR(255), c_char1 VARCHAR(255),, c_char2 VARCHAR(255), c_char3 VARCHAR(255), c_char4 VARCHAR(255), c_char5 VARCHAR(255),"
                                      " 桃園市_英 VARCHAR(255), 桃園市_中 VARCHAR(255), c_null1 VARCHAR(255),c_null2 VARCHAR(255),c_empty VARCHAR(255),c_constant VARCHAR(255)"
                                      "b_boolean INT,"
                                      "t_time DATE)")
        connect.commit()
        connect.close()

    def createPostgresTable(self,db_info,table_name):
        connect = self.setConnection(db_info)
        cur = connect.cursor()
        cur.execute(
            "CREATE TABLE "+table_name+" ( id INT,'n_int INT','n_longint BIGINT','n_float FLOAT','n_float1 FLOAT',"
                                      "'n_negative_int INT','n_positive_int INT','n_negative_float FLOAT','n_positive_float FLOAT'"
                                      "c_char VARCHAR(255), c_char1 VARCHAR(255),, c_char2 VARCHAR(255), c_char3 VARCHAR(255), c_char4 VARCHAR(255), c_char5 VARCHAR(255),"
                                      " 桃園市_英 VARCHAR(255), 桃園市_中 VARCHAR(255), c_null1 VARCHAR(255),c_null2 VARCHAR(255),c_empty VARCHAR(255),c_constant VARCHAR(255)"
                                      "b_boolean BOOLEAN,"
                                      "t_time DATE)")
        connect.commit()
        connect.close()
