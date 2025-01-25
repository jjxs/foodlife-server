import app.db.sql as SQL
from django.shortcuts import render
import pdfkit
import sys
import os
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
import base64
import time

def output(template_file, data):
    '''pdfフェイル出力'''

    pdf_out = template_file + '.pdf'
    template = loader.get_template(template_file)
    html = template.render(data)  # Renders the template with the context data.

    # pdfkit
    config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF)
    options = {
        'margin-top': 5,
        'margin-left': 5,
        'margin-right': 5
    }

    # pdf file
    pdfkit.from_string(html, pdf_out, configuration=config, options=options)

    # read pdf file
    data = open(pdf_out, "rb").read()
    response = HttpResponse(data)
    response["Content-Disposition"] = 'attachment; filename=' + pdf_out

    # file remove
    os.remove(pdf_out)
    
    # return
    return response

def get_option(request, params={}, template_id='T04R02', sql_id='transaction.t04.info'):
    '''DATA処理'''
    process_id = ''

    # process_id取得
    if 'id' in params:
        process_id = params['id']
    
    # 組織ID
    org_id = request.user.org_id

    # 
    language = request.user.language
    print(request.user)
    data = {
        'ok_img': get_img('ok'),
        'ng_img': get_img('ng'),
        'cr_img': get_img('cr'),
        'un_img': get_img('un'),
        'logo': get_img('logo_' + language),
        'check_list': get_inspection(language, process_id, org_id),
        'attachment': get_attachment(language, process_id)
    }
    result = get_sql(process_id, sql_id)
    if result:
        for k,v in result[0].items():
            key = k.lower()
            data[key] = v
    
        if language=='j':
            data['comment'] = data['comment_jp']
        elif language=='en':
            data['comment'] = data['comment_en']
        else:
            data['comment'] = data['comment_local']

    template_file = template_id + '_pdf_' + language + '.html'
    return template_file,data

def get_inspection(language='', process_id='', org_id='1003', rows=18):
    '''点検項目'''

    inspection_list = {}
    result = get_sql(process_id=process_id, org_id=org_id, sql_id='transaction.inspection')
    for row in result:
        parent_id = row['PARENT_ID']
        mitid = row['MITID']
        if not parent_id:
            parent_id = 0
            if parent_id not in inspection_list:
                inspection_list[mitid] = {}
                inspection_list[mitid]['child'] = {}
        
        # 点検結果[ok/ng/cr/un]
        if parent_id==0:
            inspection_list[mitid]['data'] = {
                'INSPECTION_RESULT': get_img(row['INSPECTION_RESULT']),
                'INSPECTION_CONTENTS': row['INSPECTION_CONTENTS']
            }
        else:
            inspection_list[parent_id]['child'][mitid] = {
                'INSPECTION_RESULT': get_img(row['INSPECTION_RESULT']),
                'INSPECTION_CONTENTS': row['INSPECTION_CONTENTS']
            }
    if len(result)<18:
        inspection_list['__'] = {
            'data': {
                'INSPECTION_CONTENTS': '',
                'INSPECTION_RESULT': ''
            },
            'child':{}
        }
        for i in range(len(result),17):
            inspection_list['__']['child'][i] = {
                'INSPECTION_CONTENTS': '',
                'INSPECTION_RESULT': ''
            }
    return inspection_list

def get_attachment(language='', process_id=''):
    '''attachment file'''

    result = get_sql(process_id,sql_id='transaction.attachment')
    attachment = []
    for item in result:
        file_path = item['FILE_PATH'] + '/' + item['FILE_NAME']
        attachment.append({
            'url': get_img(path=file_path),
            'note': item['NOTE']
        })

    return attachment

def get_img(file_id='',path=''):
    '''get image file data'''
    file_id = str(file_id).lower()
    file_path = path
    if not path:
        file_path = settings.STATIC_ROOT + '/images/' + file_id +'.jpg'

    img = ''
    if os.path.exists(file_path):
        img_data = base64.b64encode( open(file_path, "rb").read() ).decode('ascii')
        img = 'data:image/jpg;base64,{0}'.format(img_data)
    else:
        img = file_id
    return img

def get_sql(process_id, sql_id, org_id=''):
    params = {
        'process_id': process_id
    }
    if org_id:
        params['org_id'] = org_id
    return SQL.sql_to_list(params=params, sql_id=sql_id)
