import torch
from torch.autograd.grad_mode import no_grad
import torch.nn as nn
from torch.nn.modules import padding
from transformers import BertConfig, BertTokenizer, BertModel, AlbertModel, DistilBertModel, RobertaModel, XLNetModel,  LongformerModel
import numpy as np
import torch.nn.functional as F

model_ckpts = {'bert': "bert-base-uncased",
               'albert': "albert-base-v2",
               'roberta': "roberta-base",
               'xlnet': "xlnet-base-cased",
               'distilbert': "distilbert-base-uncased",
               'longformer': "allenai/longformer-base-4096"}


# 根据模型名称加载
# 第一次会在线加载模型，并且保存至用户子目录"\.cache\torch\transformers\"
class PretrainedModels(nn.Module):
    def __init__(self, task_configs = [],
                 device='cpu',
                 finetuning=True,
                 lm='bert',
                 bert_pt=None,
                 bert_path=None):
        super().__init__()

        # assert len(task_configs) > 0

        # ==================================================================================
        # 预训练模型的加载部分
        # ==================================================================================

        #特定的一些预训练模型的设置
        self.config = BertConfig.from_pretrained(model_ckpts[lm])
        self.config.output_attentions = True
        
        #加载模型
        if bert_path == None:
            if lm == 'bert':
                self.bert = BertModel.from_pretrained(model_ckpts[lm],config = self.config)
            elif lm == 'distilbert':
                self.bert = DistilBertModel.from_pretrained(model_ckpts[lm],config = self.config)
            elif lm == 'albert':
                self.bert = AlbertModel.from_pretrained(model_ckpts[lm],config = self.config)
            elif lm == 'xlnet':
                self.bert = XLNetModel.from_pretrained(model_ckpts[lm],config = self.config)
            elif lm == 'roberta':
                self.bert = RobertaModel.from_pretrained(model_ckpts[lm], config = self.config)
            elif lm == 'longformer':
                self.bert = RobertaModel.from_pretrained(model_ckpts[lm],config = self.config)
        else:
            output_model_file = bert_path
            model_state_dict = torch.load(output_model_file,
                                          map_location=lambda storage, loc: storage)
            if lm == 'bert':
                self.bert = BertModel.from_pretrained(model_ckpts[lm],
                        state_dict=model_state_dict)
            elif lm == 'distilbert':
                self.bert = DistilBertModel.from_pretrained(model_ckpts[lm],
                        state_dict=model_state_dict)
            elif lm == 'albert':
                self.bert = AlbertModel.from_pretrained(model_ckpts[lm],
                        state_dict=model_state_dict)
            elif lm == 'xlnet':
                self.bert = XLNetModel.from_pretrained(model_ckpts[lm],
                        state_dict=model_state_dict)
            elif lm == 'roberta':
                self.bert = RobertaModel.from_pretrained(model_ckpts[lm],
                        state_dict=model_state_dict)       
        self.tokenizer = BertTokenizer.from_pretrained(model_ckpts[lm])
        self.device = device
        self.finetuning = finetuning
        self.task_configs = task_configs
        self.module_dict = nn.ModuleDict({})

        # hard corded for now
        hidden_size = 768
        hidden_dropout_prob = 0.1

    # ====================================================
    # 模型训练相关参数
    # 后续进行添加，目前只是将该bert预训练模型作为特征提取器
    # ====================================================
    
    # def forward

    
    # ========================================================
    # 对于文本和单词的特征提取器
    # ========================================================

    def bert2vector(self, text_list):
        with torch.no_grad():
            inputs = self.tokenizer(text_list, return_tensors = "pt", padding = True)
            ouputs = self.bert(**inputs)
        return ouputs
