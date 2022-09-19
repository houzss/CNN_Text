from calendar import c
import os
import sys
import argparse
from urllib.request import proxy_bypass

current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
parser = argparse.ArgumentParser()

parser.add_argument(
    '--predictions_voting',
    type=str,
    default=os.path.join(current_path, 'in_out/predictions/p_text.csv'),
    help='predictions by voting')

parser.add_argument(
    '--predictions_model',
    type=str,
    default=os.path.join(current_path, 'in_out/predictions/p_cnn_1_2_1.00.csv'),
    help='predictions by ML models')

parser.add_argument(
    '--io_dir',
    type=str,
    default=os.path.join(current_path, 'in_out'),
    help='Directory of input/output')
FLAGS, unparsed = parser.parse_known_args()

p_voting = dict()
with open(FLAGS.predictions_voting) as f:
    for line in f.readlines():
        line_tmp = line.strip().split('","')
        line_tmp[0] = line_tmp[0][1:]
        line_tmp[-1] = line_tmp[-1][:-1]
        col = line_tmp[0]
        cls = line_tmp[1]
        col_cls = '%s:%s' % (col, cls)
        score = float(line_tmp[2])
        p_voting[col_cls] = score

p_model = dict()
with open(FLAGS.predictions_model) as f:
    for line in f.readlines():
        line_tmp = line.strip().split('","')
        line_tmp[0] = line_tmp[0][1:]
        line_tmp[-1] = line_tmp[-1][:-1]
        col = line_tmp[0]
        cls = line_tmp[1]
        col_cls = '%s:%s' % (col, cls)
        score = float(line_tmp[2])
        p_model[col_cls] = score

# 原有方法
# p = dict()
# for col_cls in p_voting:
#     if p_voting[col_cls] >= 0.6:
#         p[col_cls] = p_voting[col_cls]
#     elif p_voting[col_cls] >= 0.25:
#         if col_cls in p_model:
#             p[col_cls] = p_model[col_cls]
#         else:
#             p[col_cls] = p_voting[col_cls]
#     else:
#         p[col_cls] = p_voting[col_cls]

## text方法
p = dict()
for col_cls in p_model.keys():
    p[col_cls] = p_model[col_cls]

# temp_p_voting = dict()
# for col_cls in p_voting.keys():
#     if col_cls in temp_p_voting:
#         temp_p_voting[col_cls] = max(temp_p_voting[col_cls], p_voting[col_cls])
#     else:
#         temp_p_voting[col_cls] = p_voting[col_cls]
    

for col_cls in p_voting.keys():
    # if p_voting[col_cls] >= FLAGS.sigma1 or p_voting[col_cls] < FLAGS.sigma2:
    # if p_voting[col_cls] >= 0.6:
    #     p[col_cls] = p_voting[col_cls]
    if p_voting[col_cls] >= 0.7:
        if col_cls in p_model:
            p[col_cls] = min(p_voting[col_cls] + p_model[col_cls],1)
        else:
            # p[col_cls] = p_voting[col_cls]
            continue


out_file_name = '%s_lookup.csv' % os.path.basename(FLAGS.predictions_model).split('.csv')[0]
with open(os.path.join(FLAGS.io_dir, 'predictions', out_file_name), 'w') as f:
    for col_class in p.keys():
        tmp = col_class.split(':')
        f.write('"%s","%s","%.2f"\n' % (tmp[0], tmp[1], p[col_class]))