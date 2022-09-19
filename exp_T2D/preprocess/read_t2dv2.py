import os
import sys
import csv
import pandas as pd
from util_t2d import read_table_cols, read_t2d_cells,read_col_gt,read_col_header

t2d_dir = 'D:/论文二/code/SemAIDA-master/SemAIDA-master/AAAI19/T2Dv2'
if not os.path.exists(t2d_dir):
    print('%s does not exist' % t2d_dir)
    sys.exit(1)

if __name__ == '__main__':
    # 读取列，判断列名代表的class
    t1 = read_table_cols() 
    # 1438042986423——95——2015..... -ip-10这些文件不读取
    t2 = read_col_header()
    list1  = list(t2.items())

    # 读取关键列下的所有cell信息
    col_cells,col_texts = read_t2d_cells()
    # 打印mountain的数据 "1146722_1_7558140036342906956","0","True","http://dbpedia.org/ontology/Mountain"
    #print(col_cells['1146722_1_7558140036342906956 0'])
    #test = col_cells['1146722_1_7558140036342906956 0']
    t4 = read_col_gt()
    test_entity = t4['1146722_1_7558140036342906956 0']
    test_text = col_texts['1146722_1_7558140036342906956 0']
    test_cell = col_cells['1146722_1_7558140036342906956 0']
    list_class = list(t4.items())
    list_cell = list(col_cells.items())
    list_text = list(col_texts.items())
    list_res = []
    for i in range(len(list_class)):
        list_res.append([list_class[i],list_cell[i],list_text[i]])
    

    df =  pd.DataFrame(list_res)
    df.to_csv('t2dv2/'+'t2dv2_text.csv',encoding="utf-8")

    print(t2[list_cell[0][0]])
    print('-----------------------------')
    print(list_cell[0])
    print('-----------------------------')
    print(list_text[0])
    col_num = len(col_cells.keys())
    print('     columns #: %d' % col_num)
    
    #print(t4)



