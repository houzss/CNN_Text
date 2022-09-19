import os
import sys
import argparse
from util_limaye import read_cells_by_cols
from util_kb import lookup_resources
from util_kb import query_complete_classes_of_entity
from util_kb import query_abstract_of_entity
import pandas as pd
import csv

current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
parser = argparse.ArgumentParser()
parser.add_argument(
    '--io_dir',
    type=str,
    default=os.path.join(current_path, 'in_out'),
    help='Directory of input/output')
parser.add_argument(
    '--start_index',
    type=int,
    default=0,
    help='start index')
parser.add_argument(
    '--end_index',
    type=int,
    default=90,
    help='end index')
FLAGS, unparsed = parser.parse_known_args()
if not os.path.exists(FLAGS.io_dir):
    os.mkdir(FLAGS.io_dir)

print('Step #1: Read table columns and cells')
cols = []
with open(os.path.join(FLAGS.io_dir, 'column_gt_fg.csv'), 'r') as f:
    for line in f.readlines():
        cols.append(line.strip().split('","')[0][1:])
print('     columns #: %d' % len(cols))
col_cells = read_cells_by_cols(cols)


print('Step #2: Read existing entities and classes')
ent_file = os.path.join(FLAGS.io_dir, 'lookup_entities.csv')
cls_file = os.path.join(FLAGS.io_dir, 'lookup_classes.csv')
col_cls_file = os.path.join(FLAGS.io_dir, 'lookup_col_classes.csv')
# col_cell_abstact = os.path.join(FLAGS.io_dir, 'file_cell_abstract.csv')
if FLAGS.start_index == 0 and \
        (os.path.exists(ent_file) or os.path.exists(cls_file) or os.path.exists(col_cls_file)):
    print('     Error: files exist')
    sys.exit(1)

ent_cls, cls_count = dict(), dict()
if os.path.exists(ent_file):
    with open(ent_file, 'r') as out_f:
        for line in out_f.readlines():
            line_tmp = line.strip().split('","')
            line_tmp[0] = line_tmp[0][1:]
            line_tmp[-1] = line_tmp[-1][:-1]
            ent_cls[line_tmp[0]] = line_tmp[1:]
if os.path.exists(cls_file):
    with open(cls_file, 'r') as out_f:
        for line in out_f.readlines():
            line_tmp = line.strip().split('","')
            cls_count[line_tmp[0][1:]] = int(line_tmp[1][:-1])
print('     entities # %d, classes # %d' % (len(ent_cls.keys()), len(cls_count.keys())))


print('Step #3: Lookup new entities and classes')
cell_ents_cache = dict()
# cols = cols[5]
# 浏览每一个文件
# for i, col in enumerate(cols):
    # if i < FLAGS.start_index:
    #     continue
    # if i >= FLAGS.end_index:
    #     print('     This part is fully done, %d entities added' % len(ent_cls.keys()))
    #     break
cnt_file = 0
for i, col in enumerate(cols):
    filepath = 'abstract_output/' + col[:-6]+'abstact.csv'
    while not os.path.exists(filepath):
        try:
            cells = col_cells[col]
            col_classes = set()
            # 读取当前文件下的每一个cell的相关abstract
            cell_text = {}
            all_text = []
            cnt = 0
            for cell in cells:
                if cell in cell_ents_cache:
                    cell_ents = cell_ents_cache[cell]
                else:
                    # 每个entity在DBpedia中查到的最像的两个实体
                    cell_ents = lookup_resources(cell)
                    cell_ents_cache[cell] = cell_ents
                text_list = []
                text_list.append(cell)
                for ent in cell_ents:
                    text_list.append(ent)
                    if ent in ent_cls.keys():
                        text = ent_cls[ent]
                    else:
                        text = query_abstract_of_entity(ent)
                        ent_cls[ent] = text
                    if len(text) > 0:
                        text_list.append(text[0].strip('\n'))
                    else:
                        text_list.append("None")
                all_text.append(text_list)
                cell_text[cell] = text_list
                cnt += 1
                print("%.2f cell complete" % (cnt/len(cells)))
                    # for cls in text:
                    #     col_classes.add(cls)
                    #     if cls not in cls_count:
                    #         cls_count[cls] = 1
                    #     else:
                    #         cls_count[cls] += 1

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
            print('one cell done')
            # print ('    column %d done' % i)
        except:
            pass
        continue
