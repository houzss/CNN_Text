"""
This file contains functions related to processing of T2Dv2 table sets
"""
import os
import sys
import json

#t2d_dir = '../T2Dv2'
# t2d_dir = 'D:/论文二/code/SemAIDA-master/SemAIDA-master/AAAI19/T2Dv2'
t2d_dir = 'D:/论文二/数据集/T2Dv2'
if not os.path.exists(t2d_dir):
    print('%s does not exist' % t2d_dir)
    sys.exit(1)





# read columns, each of which includes table id and column number, separated by ' '
def read_table_cols():
    tab_cols = list()
    with open(os.path.join(t2d_dir, 'col_class_checked_fg.csv')) as f:
        lines = f.readlines()
        for line in lines:
            line_tmp = line.strip().split('","')
            line_tmp[0] = line_tmp[0][1:]
            line_tmp[-1] = line_tmp[-1][:-1]
            tab_id = line_tmp[0]
            col_id = line_tmp[1]
            tab_col = '%s %s' % (tab_id, col_id)
            tab_cols.append(tab_col)
    return tab_cols


# read header name of each column
def read_col_header():
    col_headers = dict()
    prop_dir = os.path.join(t2d_dir, 'property')
    for prop_filename in os.listdir(prop_dir):
        with open(os.path.join(prop_dir, prop_filename)) as f:
            tab_id = prop_filename.split('.csv')[0]
            for line in f.readlines():
                line_tmp = line.strip().split('","')
                line_tmp[0] = line_tmp[0][1:]
                line_tmp[-1] = line_tmp[-1][:-1]
                header = line_tmp[1]
                col_id = line_tmp[3]
                col = '%s %s' % (tab_id, col_id)
                col_headers[col] = header
    return col_headers


# read table column number (order) and table column cells
def read_t2d_cells():
    cols = read_table_cols()
    col_headers = read_col_header()
    col_cells = dict()
    col_text = dict()
    table_dir = os.path.join(t2d_dir, 'tables')
    for col in cols:
        tab_id = col.split(' ')[0]
        col_id = col.split(' ')[1]
        with open(os.path.join(table_dir, ('%s.json' % tab_id)), encoding='windows-1252') as f:
            tab_line = f.readline()
            tab_line = tab_line.strip()
            temp_col_contents = tab_line.split('"textBeforeTable":')[1].split('"textAfterTable":')
            textbefore = temp_col_contents[0]
            textafter = temp_col_contents[1].split('"hasKeyColumn":')[0]
            col_contents = tab_line.split("[[")[1].split("]]")[0]
            col_content = col_contents.split('],[')[int(col_id)]
            col_list = col_content.split('","')
            col_list[0] = col_list[0].replace('"', '')
            col_list[-1] = col_list[-1].replace('"', '')
            if col_headers[col] != 'NULL':
                col_list = col_list[1:]
            col_cells[col] = col_list
            col_text[col] = [textbefore,textafter]

    return col_cells,col_text


# read ground truth label of columns
def read_col_gt():
    col_classes = dict()
    with open(os.path.join(t2d_dir, 'col_class_checked_fg.csv'), 'r') as f:
        for line in f.readlines():
            line_tmp = line.strip().split('","')
            line_tmp[0] = line_tmp[0][1:]
            line_tmp[-1] = line_tmp[-1][:-1]
            tab_id = line_tmp[0]
            col_id = line_tmp[1]
            cls_URI = line_tmp[3]
            ori_cls = cls_URI.split('/')[-1]
            col = '%s %s' % (tab_id, col_id)
            col_classes[col] = [ori_cls]
    return col_classes


# read primary key columns
def primary_key_cols():
    pk_col = set()
    pro_dir = os.path.join(t2d_dir, 'property')
    for file_name in os.listdir(pro_dir):
        with open(os.path.join(pro_dir, file_name), 'r') as f:
            for line in f.readlines():
                line_tmp = line.strip().split('","')
                line_tmp[0] = line_tmp[0][1:]
                line_tmp[-1] = line_tmp[-1][:-1]
                if line_tmp[2] == 'True':
                    col_id = line_tmp[3]
                    tab_id = file_name.split('.csv')[0]
                    col = '%s %s' % (tab_id, col_id)
                    pk_col.add(col)
    return pk_col


def read_table_from_json():
    #with open(os.path.join(t2d_dir, 'tables/1146722_1_7558140036342906956.json'), encoding='gb18030', errors='ignore') as f:
    #with open(os.path.join(t2d_dir, 'tables'), 'r', encoding= 'gb18030',errors='ignore') as f:
    # ===============================
    # 只读取有数据的web table的json表格
    # ================================
    cols = read_table_cols() 
    col_tables = dict()  # 返回 文件名 - 相应表格 的字典序
    web_tables_row = []
    web_tables_column = []

    # 获取table的id
    json_dir = os.path.join(t2d_dir, 'tables')
    for col in cols:
        web_table = []
        tab_id = col.split(' ')[0]
        with open(os.path.join(json_dir, ('%s.json' % tab_id)), encoding= 'windows-1252') as f:
            # 读取单个json的所有信息
            load_dict = json.load(f)
            for column in load_dict['relation']:
                web_table.append(column)
            # 行列转换
            web_table2 = [ [ row[i] for row in web_table ] for i in range(len(web_table[0])) ]
        web_tables_column.append(web_table)
        web_tables_row.append(web_table2)
        col_tables[tab_id] = web_table
    return col_tables
            
            
    
        
    
    #for prop_filename in os.listdir(json_dir): # 读取table文件目录下的所有文件
        

if __name__ == '__main__':
    read_table_from_json()
