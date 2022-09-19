import wikipedia
import os
import sys
import argparse
import csv
# from util_limaye import read_cells_by_cols
import pandas as pd


limaye_dir = 'D:/论文二/数据集/Limaye'
t2d_dir = 'D:/论文二/数据集/T2Dv2'
wikipedia_dir = 'D:/论文二/数据集/Wikipedia'

dataset_dir = t2d_dir
def read_line_cells_by_cols(cols):
    col_cells = dict()
    for col in cols:
        col_tmp = col.split(' ')
        filename = col_tmp[0]
        # col_order = int(col_tmp[1])
        col_f = os.path.join(limaye_dir, 'tables_instance', filename)
        cells = list()
        with open(col_f, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if not line == '':
                    tmp_line = line.strip().split('","')
                    tmp_line[0] = tmp_line[0][1:]
                    tmp_line[-1] = tmp_line[-1][:-1]
                    cell = ' '.join(tmp_line)
                    if not cell == '':
                        cells.append(cell)
        col_cells[col] = cells
    return col_cells


# read columns, each of which includes table id and column number, separated by ' '
def read_table_cols():
    tab_cols = list()
    with open(os.path.join(dataset_dir, 'col_class_checked_fg.csv')) as f:
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
    prop_dir = os.path.join(dataset_dir, 'property')
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
    # col_f = os.path.join(t2d_dir, 'tables', filename)
    table_dir = os.path.join(t2d_dir, 'tables')
    for col in cols:
        tab_id = col.split(' ')[0]
        col_id = col.split(' ')[1]
        with open(os.path.join(table_dir, ('%s.json' % tab_id)),encoding='windows-1252') as f:
            tab_line = f.readline()
            tab_line = tab_line.strip()
            col_contents = tab_line.split("[[")[1].split("]]")[0]
            # 读取文件名对应的列
            col_content = col_contents.split('],[')[int(col_id)]
            col_list = col_content.split('","')
            col_list[0] = col_list[0].replace('"', '')
            col_list[-1] = col_list[-1].replace('"', '')
            if col_headers[col] != 'NULL':
                col_list = col_list[1:]
            col_cells[col] = col_list
    return col_cells

# =====================================
# 读取wikipedia的webtalbe数据集的信息
# =====================================
def read_wikipedia_table_cols():
    tab_cols = list()
    col_indexes = list()
    with open(os.path.join(wikipedia_dir, "rected_col_cls_GS.csv")) as f:
        lines = f.readlines()
        for line in lines:
            line_tmp = line.strip().strip('"').split(",")[:-1]
            file_name = ",".join(line_tmp).split(" ")
            tab_cols.append(file_name[0])
            col_indexes.append(int(file_name[1].strip('"')))
    return tab_cols, col_indexes


# 第一步，读取原始表格的数据集
def read_wikipedia_cells():
    cols, col_idxs = read_wikipedia_table_cols()
    # col_header = read_col_header()
    col_cells = dict()
    table_dir = os.path.join(wikipedia_dir, 'tables')
    for i, col in enumerate(cols):
        cells = list()
        with open(os.path.join(table_dir, col)) as f:
            for line in f.readlines():
                tmp_line = line.split(",")[col_idxs[i]]
                # tmp_line = line
                if len(tmp_line) > 0:
                    cells.append(tmp_line)
                else:
                    cells.append("None")
        col_cells[col] = cells  

        # cells = list() #保存该文件下的所有cell
        # 直接读csv数据有点脏,会产生报错
        # cells = pd.read_csv(os.path.join(table_dir,col))
        # col_cells[col] = cells.iloc[:, [col_idxs[i]]].values

    return col_cells
                    

current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
parser = argparse.ArgumentParser()
parser.add_argument(
    '--io_dir',
    type=str,
    default=os.path.join(current_path, 'in_out_t2d'),
    help='Directory of input/output')

FLAGS, unparsed = parser.parse_known_args()



#===================================
# 读取真值文件的所有数据
#===================================

print('Step #1: Read table columns and cells')
cols = []
# with open(os.path.join(FLAGS.io_dir, 'column_gt_fg.csv'), 'r') as f:
with open(os.path.join(FLAGS.io_dir, 'col_class_checked_fg.csv'), 'r') as f:
    for line in f.readlines():
        cols.append(line.strip().split('","')[0][1:])
print('     columns #: %d' % len(cols))
# col_cells = read_line_cells_by_cols(cols)
# col_cells = read_t2d_cells()
# 读取wikiepedia的数据
col_cells = read_wikipedia_cells()



for i, col in enumerate(col_cells):
    filepath = 'wikipedia_abstract_output_wiki/' + col +' wiki_abstract.csv'
    if not os.path.exists(filepath):
        print("current File:%s.csv", col)
        print("%.2f complete File:",i / len(col_cells))
        cells = col_cells[col]
        all_text = []
        cnt = 0
        for cell in cells:
            text_list = []
            text_list.append(cell)
            try:
                temp_entity = wikipedia.search("Baidu")
                temp_string = wikipedia.summary(temp_entity[0]).replace('\n','')
            except:
                temp_string = ""
            if len(temp_string) > 0 :
                text_list.append(temp_string)
            else:
                text_list.append("None")
            all_text.append(text_list)
            cnt += 1
            print("current File cells %.2f complete" % (cnt/ len(cells)))

        #每个cell存一下内容
        with open(filepath, mode = 'w',encoding='utf-8') as f:
            # if len(cell_text) == 0:
            #     f.write('"%s"\n' % col)
            # else:
            #     for t in cell_text:
            #         print(t)
            #         f.write(t)
            writer = csv.writer(f)
            writer.writerows(all_text)
        # df = pd.DataFrame(dic)
        # df.to_csv(index=False)
        print('one cell done:',i)


#=====================
# Limaye抓取wiki文本数据集
#=====================
# for i, col in enumerate(cols):
#     filepath = 'T2Dv2abstract_output_wiki/' + col[:-6]+'wiki_abstract.csv'
#     if not os.path.exists(filepath):
#         cells = col_cells[col]
#         all_text = []
#         cnt = 0
#         for cell in cells:
#             text_list = []
#             text_list.append(cell)
#             try:
#                 temp_string = wikipedia.summary(cell).replace('\n','')
#             except:
#                 temp_string = ""
#             if len(temp_string) > 0 :
#                 text_list.append(temp_string)
#             else:
#                 text_list.append("None")
#             all_text.append(text_list)
#             cnt += 1
#             print("%.2f complete" % (cnt/ len(cells)))

#         #每个cell存一下内容
#         with open(filepath, mode = 'w',encoding='utf-8') as f:
#             # if len(cell_text) == 0:
#             #     f.write('"%s"\n' % col)
#             # else:
#             #     for t in cell_text:
#             #         print(t)
#             #         f.write(t)
#             writer = csv.writer(f)
#             writer.writerows(all_text)
#         # df = pd.DataFrame(dic)
#         # df.to_csv(index=False)
#         print('one cell done:',i)



# print(wikipedia.summary("Thomas Handforth Mei Li"))