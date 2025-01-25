
import base64
import datetime
import os
from zipfile import is_zipfile

import openpyxl as px
import xlrd
from botocore import model
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.db import transaction

import app.common.message as Message
import app.const as Const
import app.db.sql as SQL
import app.util as Util
import master
from app.db.db_patch import SaasHandler
from app.db.models.store_table import (MasterData, MasterDataGroup,
                                       MasterLanguage, Menu, MenuCategory)
from app.exception.web import WebException
from app.http.api import BaseAPI
from app.http.response import JsonResponse


class MenuUploadApi(BaseAPI):

    def menu_confirm(self, request, params):

        DATA_BASE = 'ami'
        result = []
        excel_data = self.get_excel_data(params)
        for row in excel_data:
            menu_list = {}
            menu_list['no'] = row[0]  # 编号
            menu_list['menu_max'] = row[1] # 菜单分类(大)
            menu_list['menu_min'] = row[2] # 菜单分类(小)
            menu_list['ja_name'] = row[3] # 菜单日文名称
            menu_list['ch_name'] = row[4] # 菜单中文名称
            menu_list['en_name'] = row[5] # 英文名称
            menu_list['fax'] = row[6] # 是否含税
            menu_list['before_price'] = row[7] # 税前价格
            menu_list['after_price'] = row[8] # 税后价格
            menu_list['photo'] = row[9]  # 照片文件
            # 查询编号是否重复
            sql_no = '''
            SELECT
            *
            FROM menu
            WHERE
                no = %(no)s
            '''
            result_no = SQL.sql_to_list(
                sql=sql_no, params={'no': row[0]}, DB_name=DATA_BASE)
            if(len(result_no) > 0):
                menu_list['error_no'] = '1'  # no重复
            else:
                menu_list['error_no'] = '0'  # no不重复
            # 查询名称是否重复
            sql_name = '''
            SELECT
            *
            FROM menu
            WHERE
                name = %(name)s
            '''
            result_name = SQL.sql_to_list(
                sql=sql_name, params={'name': row[3]}, DB_name=DATA_BASE)
            if(len(result_name) > 0):
                menu_list['error_name'] = '1'  # name重复
            else:
                menu_list['error_name'] = '0'  # name不重复

            result.append(menu_list)

        return JsonResponse(result=True, data=result)

    def menu_upload(self, request, params):
        DATA_BASE = 'ami'
        for row in params:
            # 菜品表
            menu = Menu()
            # 小分类与菜品绑定表
            menu_category = MenuCategory()
            # 小分类表
            master_data = MasterData()
            # 大分类表
            master_data_group = MasterDataGroup()
            # 中日英文名称
            master_language = MasterLanguage()
            # 先查询编号与名称是否已存在，存在的进行操作
            # 查询编号是否重复
            sql_no = '''
                SELECT
                *
                FROM menu
                WHERE
                    no = %(no)s
                '''
            result_no = SQL.sql_to_list(
                sql=sql_no, params={'no':row['no']}, DB_name=DATA_BASE)
            if(len(result_no) > 0):
                continue
            # 查询名称是否重复
            sql_name = '''
                SELECT
                *
                FROM menu
                WHERE
                    name = %(name)s
                '''
            result_name = SQL.sql_to_list(
                sql=sql_name, params={'name': row['ja_name']}, DB_name=DATA_BASE)
            if(len(result_name) > 0):
                continue
            # 编号-1	菜单分类(大)-2	菜单分类(小)-3	菜单日文名称-4	菜单中文名称-5
            # 英文名称-6	是否含税-7	税前价格-8	税后价格-9	照片文件-10
            # 查询大分类
            sql_max = '''
                SELECT
                *
                FROM master_data_group
                WHERE
                    display_name = %(display_name)s
                '''
            result_max = SQL.sql_to_list(
                sql=sql_max, params={'display_name': row['menu_max']}, DB_name=DATA_BASE)
            # 大分类编号，小分类会存在相同
            group_id = ''
            if(len(result_max) <= 0):
                # 不存在，进行大分类的添加
                master_data_group.id = master_data_group.next_value()
                master_data_group.name = row['menu_max']
                master_data_group.display_name = row['menu_max']
                master_data_group.domain = 'menu_category'
                master_data_group.enabled = 1
                master_data_group.save()
                group_id = master_data_group.id
            else:
                group_id = result_max[0]['id']
            # 查询小分类
            sql_min = '''
                SELECT
                *
                FROM master_data
                WHERE
                    name = %(name)s
                AND
                    group_id = %(group_id)s
                '''
            result_min = SQL.sql_to_list(
                sql=sql_min, params={'name':  row['menu_min'], 'group_id': group_id}, DB_name=DATA_BASE)
            # 保存小分类的id
            cate_max = ''
            if(len(result_min) <= 0):
                # 不存在，进行小分类的添加
                master_data.id = master_data.next_value()
                master_data.code = 0
                master_data.name =  row['menu_min']
                master_data.display_name =  row['menu_min']
                master_data.group_id = group_id
                master_data.theme_id = 'default'
                master_data.menu_count = 9
                master_data.display_order = 1
                master_data.save()
                cate_max = master_data.id
            else:
                cate_max = result_min[0]['id']
            # 添加菜品 建立与小分类的关联
            menu.id = menu.next_value()
            menu.no = row['no']
            menu.name =  row['ja_name']
            menu.usable = True
            menu.stock_status_id = 31
            menu.takeout = 0
            menu.image = SaasHandler.get_saas_id() + '/menu_images/' + row['photo']
            if  row['fax'] == '是':
                # 税入，添加税入价格
                menu.tax_in = True
                menu.price =  row['after_price']
            else:
                # 税拔，添加税拔价格
                menu.tax_in = False
                menu.price = row['before_price']
            menu.save()
            # 菜品添加完成添加与小分类的关联
            menu_category.display_order = menu.no
            menu_category.category_id = cate_max
            menu_category.menu_id = menu.id
            menu_category.save()
            # 添加完成后添加菜单的多国语言对应
            master_language.name = row['ja_name']
            master_language.ja = row['ja_name']
            master_language.en = row['en_name']
            master_language.zh = row['ch_name']
            master_language.save()

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))


    def get_excel_data(self, params):
        # Exceclファイル内容取込み
        file_type, base64_data = params['file_data'].split(',')

        if "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" not in file_type\
                and "application/vnd.ms-excel" not in file_type:
            return -1, ''

        excel_info = self.read_excel_info(base64.b64decode(base64_data))
        return excel_info


    def read_excel_info(self, excle_file, seek_row=None):
        '''エクセルファイル内容読み込む'''
        # エクセルファイル内容
        result_data = {}

        file_data = ContentFile(excle_file)
        work_book = xlrd.open_workbook(file_contents=file_data.read())

        sheet_names = work_book.sheet_names()

        for sheet_name in sheet_names:
            sh_info = work_book.sheet_by_name(sheet_name)

            max_row = sh_info.nrows             # 最大行数
            max_col = sh_info.ncols             # 最大列数

            data_header = {}
            data_info = []

            need_seek_row = None
            if seek_row and sheet_name in seek_row and seek_row[sheet_name]:
                need_seek_row = seek_row[sheet_name]
            for row in range(max_row):
                data_tmp = {}
                # 該当シートのシークしたい場合
                if need_seek_row and row < need_seek_row:
                    continue
                for col in range(max_col):
                    tag_row = 0
                    if need_seek_row:
                        tag_row = need_seek_row
                    if row == tag_row:
                        data_header[col] = str(sh_info.cell(row, col).value)
                    else:
                        # 列重複の場合、自動的に「_連番」を追加する
                        if data_header[col] in data_tmp:
                            data_header[col] += "_1"

                        data_tmp[col] = sh_info.cell(row, col).value

                if data_tmp:
                    data_info.append(data_tmp)

            result_data = data_info
            break

        return result_data
