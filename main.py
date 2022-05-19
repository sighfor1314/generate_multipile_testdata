from generate_testdata import GenerateFile
from data_management import DataManagement
import sys

# Executing generate_not_csv_file()
def not_csv_file(file,file_category):
   if file_category == 'xlsx' or file_category == 'xsx':
      file.generate_not_csv_file(file_category)
   else:
      print('file_category error')

# String of time convert into tuple
def convert_into_tuple(date, start_status):
   start_time = [0, 0, 0, 0, 0, 0]
   end_time = [23, 59, 59, 0, 0, 0]

   date_list = list(date.split('-'))
   for i in range(len(date_list)):
      date_list[i]=int(date_list[i])
   if start_status == "start":
      date_list+=start_time
   else :
      date_list += end_time

   return tuple(date_list)

# Generate csv | xlsx | xls file
def createFile():
   file_name = sys.argv[2] + '.csv'  # set output file_name
   file_category = sys.argv[3]  # file category : csv | xlsx | xls
   open_parameter = sys.argv[4]  # write file method,including
   #    'w'(means: write): overwrite the original file contents
   #    'a'(means: append) : overwrite the original file contents
   start_datetime = convert_into_tuple(sys.argv[5], "start")  # set tuple of start_time （2002-01-01 00：00：00）
   end_datetime = convert_into_tuple(sys.argv[6], "end")  # set tuple of end_time（2002-12-31 23：59：59）
   rows_number = int(sys.argv[7])  # set rows number

   file = GenerateFile(file_name, open_parameter, start_datetime, end_datetime, rows_number)  # Initial instant
   file.generate_csv_file()

   if file_category != 'csv':
      not_csv_file(file, file_category)

# Create database table or add file to sftp
def createTable():
   db_info = sys.argv[2] # set output file_name
   if db_info == 'sftp': #Instant object according to type of database
      sftp_path = sys.argv[3]
      file_name  = sys.argv[4]
      sftp = DataManagement()
      sftp.createSftpFile(db_info, sftp_path, file_name)
   elif db_info =='mysql':
      file_name = sys.argv[3]
      db = DataManagement()
      db.createMysqlTalbe(db_info, file_name)
   elif db_info == 'mssql':
      file_name = sys.argv[3]
      db = DataManagement()
      db.createMssqlTalble(db_info, file_name)
   elif db_info == 'postgres':
      file_name = sys.argv[3]
      db = DataManagement()
      db.createPostgresTable(db_info, file_name)
   elif db_info == 'oracle':
      file_name = sys.argv[3]
      db = DataManagement()
      db.createOracleTable(db_info, file_name)
   else:
      print("Input error,pleasr input correct db_type or sftp")

# Insert data into database or sftp
def insertData():
   db_info = sys.argv[2]  # set output file_name
   # Instant object according to type of database
   if db_info == 'sftp':
      sftp_path = sys.argv[3]
      local_file_path = sys.argv[4]
      sftp_file_name = sys.argv[5]
      sftp = DataManagement()
      sftp.setSftpInsertion(db_info, sftp_path, local_file_path, sftp_file_name)
   elif db_info in['mysql','mssql','postgres','oracle']:
      table_name=sys.argv[3]
      file_name = sys.argv[4]
      db = DataManagement()
      db.setSqlInsertion(db_info, table_name, file_name)
   else:
      print("Input error,pleasr input correct db_type or sftp")

# Delete data from  database or sftp
def deleteData():
   db_info = sys.argv[2]  # set output file_name
   # Instant object according to type of database
   if db_info == 'sftp':
      sftp_path = sys.argv[3]
      file_name = sys.argv[4]
      sftp = DataManagement()
      sftp.setSftpInsertion(db_info, sftp_path, file_name)
   elif db_info in ['mysql','mssql','postgres','oracle']:
      table_name = sys.argv[3]
      condition = sys.argv[4]
      db = DataManagement()
      db.setSqlDeletion(db_info, table_name, condition)
   else:
      print("Input error,pleasr input correct db_type or sftp")
def main():

   implementation_type= sys.argv[1] # Execute function according to implementation_type
   if implementation_type == 'createfile':
      createFile()
   elif implementation_type == 'createtable':
      createTable()
   elif implementation_type == 'insertion':
      insertData()
   elif implementation_type == 'deletion':
      deleteData()
   else:
      print("Input error,only support createfile,createtable,insection,deletion")


if __name__ == '__main__':
   main()