from generate_testdata import GenerateFile
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

def main():

   file_name = sys.argv[1]+'.csv' #  set output file_name
   file_category = sys.argv[2] #  file category : csv | xlsx | xls
   open_parameter = sys.argv[3] # open file method,including
                                #    'w'(means: write): overwrite the original file contents
                                #    'a'(means: append) : overwrite the original file contents
   start_datetime=convert_into_tuple(sys.argv[4],"start")  # set tuple of start_time （2002-01-01 00：00：00）
   end_datetime=convert_into_tuple(sys.argv[5],"end") # set tuple of end_time（2002-12-31 23：59：59）
   rows_number = int(sys.argv[6]) # set rows number

   file = GenerateFile(file_name, open_parameter,start_datetime, end_datetime , rows_number) # Initial instant
   file.generate_csv_file()

   if file_category !='csv':
      not_csv_file(file,file_category)

if __name__ == '__main__':
   main()