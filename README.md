##  generate_testdata
### Description
<li>For data analysis system, generate a large amount and variety of test data.</li>

### Prerequisites

1. clone to your local directory
```
$ git clone https://github.com/sighfor1314/generate_multipile_testdata.git
```
2. Install Python 3

3. Install pandas
```
$ pip3 install pandas
```
4. Install pandas
```
$ pip3 install xlwt
```
5. Install numpy 
```
$ pip3 install numpy
```
6. Install connect SQL and sftp package 
```
$ pip3 install cx_Oracle
```
```
$ pip3 install mysql.connector
```
```
$ pip3 install pymssql
```
```
$ pip3 install pysftp
```
```
$ pip3 install psycopg2
```
7. Install configparser
```
$ pip3 install configparser
```
3 install mysql.connector

###  Implement generate_testdata 
1. change to generate_testdata directory
```
$ cd generate_testdata/
```
2. Set up information of sql_info.ini 
2. Execute generate_testdata

### Variable description
1. implementation_type :
    * `createfile` : Implement create new file.
    * `createtable` : Implement create new table in DB or sftp
    * `insertion` :  Insert data into DB or sftp if tale existed.
    * `deletion` :  Delete data from DB or sftp if tale existed.
2. filename :　Set output file_name.
3. file category : Support `csv` | `xlsx` | `xls` 
4. open_parameter : Write file method : Support `w` (means: write): overwrite the original file contents  | 
      </br> &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&nbsp; `a`(means: append) : overwrite the original file contents  
5. start_date and end_date: Generate time from start_date to end_date.
6. rows_number : How many rows do you generate.
#####Createfile example: 
```
$  python main.py createfile `filename` `file_type` `open_parameter` `start_date` `end_date` `rows_number`
```
7. database_type : Support `MySQL` | `MSSQL` | `Oracle` | `Postgres` | `SFTP`
8. table_name : Database table name.
9. condition :　SQL statement, where city = 'Taipei' and salary >= 50000
#####Createtable example (database and sftp) :
```
$  python main.py createtable `database_type` `table_name`
```
#####Insertionexample (database) :
```
$  python main.py insertion `database_type` `table_name` `filename`
```
#####Insertion example (sftp) :
```
$  python main.py insertion sftp `sftp_path` `local_file_path` `filename`
```
#####Deletion example (database) :
```
$  python main.py deletion `database_type` `table_name` `condition`
```
#####Deletion example (sftp) :
######only support drop file
```
$  python main.py deletion sftp `sftp_path` `file_name`
```
