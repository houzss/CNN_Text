import os
import sys
import argparse
import re

from tqdm import tnrange
from util_t2d import read_t2d_cells

current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
parser = argparse.ArgumentParser()
parser.add_argument(
    '--io_dir',
    type=str,
    default=os.path.join(current_path, 'in_out'),
    help='Directory of input/output')
FLAGS, unparsed = parser.parse_known_args()


#================
# 读取所有行文件名
#================
print('Step #1: reading columns and cells of each column')
# cols = set()
# with open(os.path.join(FLAGS.io_dir, 'column_gt_fg.csv'), 'r') as f:
#     for line in f.readlines():
#         cols.add(line.strip().split('","')[0][1:])
# print('     columns #: %d' % len(cols))
# col_cells = read_cells_by_cols(cols)
col_cells = read_t2d_cells()

#==================
# 读取每个文件名下的抓取的文本
#=================
print('Step #2: read classes of each table')
tab_class_num = dict()
# with open(os.path.join(FLAGS.io_dir, 'column_ent_class.csv'), 'r') as f:
    # for line in f.readlines():
    #     line_tmp = line.strip().split('","')
    #     line_tmp[0] = line_tmp[0][1:]
    #     line_tmp[-1] = line_tmp[-1][:-1]
    #     tab = line_tmp[0]
    #     class_num = set()
    #     for item in line_tmp[1:]:
    #         if 'Wikidata:Q11424' not in item:
    #             class_num.add(item)
    #     tab_class_num[tab] = class_num

# 读取所有的类
col_lookup_classes = dict()
with open(os.path.join(FLAGS.io_dir, 'lookup_col_classes.csv')) as f:
    for line in f.readlines():
        line_tmp = line.strip().split('","')
        if len(line_tmp) > 1:
            col = line_tmp[0][1:]
            line_tmp[-1] = line_tmp[-1][:-1]
            col_lookup_classes[col] = set(line_tmp[1:])
        else:
            col = line_tmp[0][1:-1]
            col_lookup_classes[col] = set()
out_file = os.path.join(FLAGS.io_dir, 'predictions', 'p_text.csv')
if os.path.exists(out_file) and FLAGS.start_index == 0:
    print('     file exists')
    sys.exit(1)
for csvName in col_cells:
    # tFilepath = current_path + "/abstract_output_wiki/"+csvName[:-6]+"wiki_abstract.csv"
    tFilepath = 'D:/EntityMatchingProject/KBGraphSystem/T2Dv2abstract_output_wiki/' + csvName + "wiki_abstract.csv"
    col_class_p = dict()
    for classifier in col_lookup_classes[csvName]:
        tNum = 0
        with open(tFilepath,'r',encoding="utf-8") as f:
            for line in f.readlines():
            # line_tmp = line.strip().split('","')
            # line_tmp[0] = line_tmp[0][1:]
            # line_tmp[-1] = line_tmp[-1][:-1]
            # tab = line_tmp[0]
            #读取每个文件下的所有分类
                if re.search(classifier, line, re.IGNORECASE):
                    tNum += 1
        
        col_class = '"%s","%s"' % (csvName, classifier)
        col_class_p[col_class] = tNum / len(col_cells[csvName])
        with open(out_file, 'a') as f:
            for col_class in col_class_p.keys():
                f.write('%s,"%.2f"\n' % (col_class, col_class_p[col_class]))

# print('Step #3: calculate score')
# col_class_score = list()
# for col in cols:
#     cell_num = len(col_cells[col])
#     tab = col.split(' ')[0]
#     class_nums = tab_class_num[tab]
#     for class_num in class_nums:
#         tmp = class_num.split(':')
#         cls = tmp[0]
#         num = int(tmp[1])
#         score = float(num)/float(cell_num)
#         col_class_score.append('"%s","%s","%.2f"' % (col, cls, score))

# print('Step #4: output')
# out_file = os.path.join(FLAGS.io_dir, 'predictions', 'p_ent_class.csv')
# with open(out_file, 'w') as f:
#     for s in col_class_score:
#         f.write('%s\n' % s)
