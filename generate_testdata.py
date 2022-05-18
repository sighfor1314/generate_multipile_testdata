import csv
import random
import time
import os
import pandas as pd

class GenerateFile():
    def __init__(self,file_name,open_parameter,start_time,end_time, column_number):
        self.file_name = file_name
        self.open_parameter = open_parameter
        self.start_time = start_time
        self.end_time = end_time
        self.column_number = column_number

    def is_write_mode(self):
        if self.open_parameter=='w':
            return True
        elif self.open_parameter=='a':
            if os.path.isfile(self.file_name) == True: #check file is existed
                with open(self.file_name, 'rt') as csvfile:
                    reader = csv.reader(csvfile)
                    colomn_length = 0
                    for i, rows in enumerate(reader):
                        colomn_length = i
            else:
                return True

            return colomn_length
        else :
            return False

    def generate_csv_file(self):
        taipei=['Songshan District','XinyiDistrict','Daan District','ZhongshanDistrict','ZhongzhengDistrict','Datong District','Wanhua District','Wenshan District','Nangang District','Neihu District','ShilinDistrict','Beitou District']
        taipei_chinese=['松山區','信義區','大安區', '中山區','中正區','大同區', '萬華區', '文山區','南港區', '內湖區','士林區', '北投區'
        ]
        newTaipei=['BanqiaoDistrict','SanchongDistrict','ZhongheDistrict','YongheDistrict','XinzhuangDistrict','XindianDistrict','TuchengDistrict','LuzhouDistrict','XizhiDistrict','ShulinDistrict','TamsuiDistrict ','YinggeDistrict','SanxiaDistrict',
                   'RuifangDistrict','WuguDistrict','TaishanDistrict','LinkouDistrict','ShenkengDistrict','ShidingDistrict','PinglinDistrict','SanzhiDistrict','ShimenDistrict','BaliDistrict','PingxiDistrict','ShuangxiDistrict',
                   'GongliaoDistrict','JinshanDistrict','WanliDistrict','WulaiDistrict'
                   ]
        newTaipei_chinese=['板橋區','三重區','中和區', '永和區', '新莊區', '新店區', '土城區', '蘆洲區','汐止區','樹林區','淡水區','鶯歌區','瑞芳區','五股區','泰山區','林口區','深坑區','石碇區','坪林區','三芝區','石門區','八里區','平溪區', '雙溪區','貢寮區', '金山區','萬里區', '烏來區']
        taoyuan=['TaoyuanDistrict','ZhongliDistrict','DaxiDistrict','YangmeiDistrict','LuzhuDistrict','DayuanDistrict','GuishanDistrict','BadeDistrict','LongtanDistrict','PingzhenDistrict','XinwuDistrict','GuanyinDistrict','FuxingDistrict']
        taoyuan_chinese=['桃園區','中壢區','大溪區','楊梅區','蘆竹區','大園區','龜山區','八德區','龍潭區','平鎮區','新屋區','觀音區','復興區']
        regin=['taipei','newTaipei']
        regin_chinese = ['台北市', '新北市']
        boolean=['true','false']
        taoyuan_null=['TaoyuanDistrict','ZhongliDistrict','DaxiDistrict','YangmeiDistrict','LuzhuDistrict','DayuanDistrict','GuishanDistrict','BadeDistrict','LongtanDistrict','PingzhenDistrict','XinwuDistrict','GuanyinDistrict','FuxingDistrict','','','']
        taoyuan_chinese_null = ['桃園區', '中壢區', '大溪區', '楊梅區', '蘆竹區', '大園區', '龜山區', '八德區', '龍潭區', '平鎮區', '新屋區', '觀音區', '復興區','','','']

        start=time.mktime(self.start_time) # generate start time
        end=time.mktime(self.end_time) # generate end time

        write_mode=self.is_write_mode()
        if write_mode == True:
            colomn_length = 0
        elif write_mode== False:
            print("Only input 'w' or 'a' , please try again")
        else:
            colomn_length = write_mode

        with open(self.file_name, self.open_parameter, newline='') as csvfile:
            writer = csv.writer(csvfile)

            if write_mode== True:
                writer.writerow([
                    'id','n_int','n_longint','n_float','n_float1','n_negative_int','n_positive_int','n_negative_float','n_positive_float',
                    'c_char', 'c_char1', 'c_char2','c_char3','c_char4','c_char5','桃園市_英','桃園市_中','c_null1','c_null2','c_empty','c_constant',
                    'b_boolean',
                    't_time'])

            for i in range(self.column_number):

                date_touple = time.localtime(random.randint(start, end))  # generate date which random from start_time and end_time
                date = time.strftime("%Y-%m-%d", date_touple)  # data tuple convert int to string（example : "2022-05-17"）

                writer.writerow([
                    # ---------------- integer ---------------------
                    colomn_length+i,
                    random.randint(-2147483648,247483647),
                    random.randint(-9223372036854775807,9223372036854775807),
                    random.randint(-2147483648,247483647)+random.random(),
                    random.randint(-9223372036854775807,9223372036854775807) + random.random(),
                    random.randint(0, 247483647),
                    random.randint(-2147483648, 0),
                    random.randint(0, 247483647)+random.random(),
                    random.randint(-2147483648, 0)+random.random(),

                    # ---------------- category ---------------------
                    taipei[random.randint(0,11)],
                    taipei_chinese[random.randint(0,11)],
                    newTaipei[random.randint(0, 19)],
                    newTaipei_chinese[random.randint(0, 19)],
                    regin[random.randint(0,1)],
                    regin_chinese[random.randint(0,1)],
                    taoyuan_null[random.randint(0, 15)],
                    taoyuan_chinese_null[random.randint(0, 15)],
                    taoyuan[random.randint(0, 12)],
                    taoyuan_chinese[random.randint(0, 12)],
                    "",
                    '台灣',

                    # ---------------- boolean ---------------------
                    boolean[random.randint(0,1)],

                    # ---------------- time ---------------------

                    date
                ])

    def generate_not_csv_file(self,file_type):
        read_file = pd.read_csv(self.file_name, encoding='UTF-8')
        read_file.to_excel(self.file_name[:-4]+'.'+file_type, index=None, header=True)
        try:
            os.remove(self.file_name)
        except OSError as e:
            print(e)
