#!/usr/bin/env python
# coding: utf-8

# # Base otimizada para importar no Power BI
#conda install qgrid#conda install -c conda-forge parallel
# In[62]:


import pandas as pd
import qgrid
import numpy as np
import glob


# In[63]:


import configparser

config = configparser.RawConfigParser()
config.read('parametros.config')

PARAMETROS = dict(config.items('Padronizacao_conversao'))
PARAMETROS_GERAIS = dict(config.items('Geral'))


# In[64]:


PARAMETROS


# In[65]:


PARAMETROS_GERAIS


# In[66]:


PASTA_DEMONSTRACOES_POR_ANO = PARAMETROS_GERAIS['pasta_raiz_dados']+PARAMETROS['pasta_arquivos_contenados']


# In[67]:


PASTA_DEMONSTRACOES_POR_ANO


# In[ ]:





# ### Como não consegui executar as alterações recentes, utilizei a 1ª base

# In[38]:


def process_ativo(item):
    if item['CD_CONTA_CONTABIL'].strip() == '1':
        return item['VL_SALDO_FINAL']
    return 0


# In[39]:


def process_ativo_circulante(item):
    if item['CD_CONTA_CONTABIL'].strip() == '12':
        return item['VL_SALDO_FINAL']
    return 0


# In[40]:


def process_credito_oper_ps(item):
    if item['CD_CONTA_CONTABIL'].strip() == '123':
        return item['VL_SALDO_FINAL']
    return 0


# In[41]:


def process_passivo(item):
    if item['CD_CONTA_CONTABIL'].strip() == '2':
        return item['VL_SALDO_FINAL']
    return 0


# In[42]:


def process_passivo_circulante(item):
    if item['CD_CONTA_CONTABIL'].strip() == '21':
        return item['VL_SALDO_FINAL']
    return 0


# In[43]:


def process_passivo_nao_circulante(item):
    if item['CD_CONTA_CONTABIL'].strip() == '23':
        return item['VL_SALDO_FINAL']
    return 0


# In[44]:


def process_pl(item):
    if item['CD_CONTA_CONTABIL'].strip() == '25':
        return item['VL_SALDO_FINAL']
    return 0


# In[45]:


def process_receita(item):
    if item['CD_CONTA_CONTABIL'].strip() == '31':
        return item['VL_SALDO_FINAL']
    return 0


# In[46]:


def process_contraprestacao_pre(item):
    if item['CD_CONTA_CONTABIL'][0:3] == '311':
        if item['CD_CONTA_CONTABIL'][5:6] == '1':
            return item['VL_SALDO_FINAL']
    return 0


# In[47]:


def process_contraprestacao_pos(item):
    if item['CD_CONTA_CONTABIL'][0:3] == '311':
        if item['CD_CONTA_CONTABIL'][5:6] == '2':
            return item['VL_SALDO_FINAL']
    return 0


# In[48]:


def process_corresp_cedida_pre(item):
    if item['CD_CONTA_CONTABIL'][0:4] == '3117':
        if item['CD_CONTA_CONTABIL'][5:6] == '1':
            return item['VL_SALDO_FINAL']
    return 0


# In[49]:


def process_corresp_cedida_pos(item):
    if item['CD_CONTA_CONTABIL'][0:4] == '3117':
        if item['CD_CONTA_CONTABIL'][5:6] == '2':
            return item['VL_SALDO_FINAL']
    return 0


# In[50]:


def process_despesa(item):
    if item['CD_CONTA_CONTABIL'].strip() == '41':
          return item['VL_SALDO_FINAL']
    return 0


# In[51]:


def process_eventos_indenizaveis_pre(item):
    if item['CD_CONTA_CONTABIL'][0:3] == '411':
        if item['CD_CONTA_CONTABIL'][5:6] == '1':
            return item['VL_SALDO_FINAL']
    return 0


# In[52]:


def process_eventos_indenizaveis_pos(item):
    if item['CD_CONTA_CONTABIL'][0:3] == '411':
        if item['CD_CONTA_CONTABIL'][5:6] == '2':
            return item['VL_SALDO_FINAL']
    return 0


# In[53]:


def process_variacao_peona(item):
    if item['CD_CONTA_CONTABIL'] == '414':
          return item['VL_SALDO_FINAL']
    return 0


# In[54]:


def process_despesa_com(item):
    if item['CD_CONTA_CONTABIL'].strip() == '43':
          return item['VL_SALDO_FINAL']
    return 0


# In[55]:


def process_despesa_adm(item):
    if item['CD_CONTA_CONTABIL'].strip() == '46':
          return item['VL_SALDO_FINAL']
    return 0


# In[56]:


def recuperar_trimestre_anterior(item):
    try: 
        chave_anterior = item.name[:item.name.rfind("_")+1]
        semestre_anterior = int(item['SEMESTRE']) - 1
        if (semestre_anterior == 0):
            return None
        chave_anterior = chave_anterior+str(semestre_anterior)
        item_anterior =  data.loc[[chave_anterior]]
        if(len(item_anterior) > 0):
            item_anterior = item_anterior.squeeze()
            return item_anterior
    except:
        return None


# In[57]:


def remove_acumulado(func_calculo,item,item_anterior):
    valor_atual = func_calculo(item)
    try:
        valor_anterior = func_calculo(item_anterior)
    except:
        valor_anterior = 0
    valor_trimestre = float("{0:.2f}".format((valor_atual-valor_anterior)))
    return valor_trimestre


# In[58]:


def process(item):
    if (item['pos']% 1000 == 0):
        print("Processado",item['pos'],"de",len(data))
    item_anterior = recuperar_trimestre_anterior(item)
    if (int(item['SEMESTRE']) == 1):
        item['ATIVO'] = process_ativo(item)
        item['ATIVO_CIRCULANTE'] = process_ativo_circulante(item)
        item['CREDITO_OPER_PS'] = process_credito_oper_ps(item)
        item['PASSIVO'] = process_passivo(item)
        item['PASSIVO_CIRCULANTE'] = process_passivo_circulante(item)
        item['PASSIVO_NAO_CIRCULANTE'] = process_passivo_nao_circulante(item)
        item['PL'] = process_pl(item)
        item['RECEITA'] = process_receita(item)
        item['CONTRAPRESTACAO_PRE'] = process_contraprestacao_pre(item)
        item['CONTRAPRESTACAO_POS'] = process_contraprestacao_pos(item)
        item['CORRESP_CEDIDA_POS'] = process_corresp_cedida_pos(item)
        item['DESPESA'] = process_despesa(item)
        item['EVENTOS_INDENIZAVEIS_PRE'] = process_eventos_indenizaveis_pre(item)
        item['EVENTOS_INDENIZAVEIS_POS'] = process_eventos_indenizaveis_pos(item)
        item['VARIACAO_PEONA'] = process_variacao_peona(item)
        item['DESPESA_COM'] = process_despesa_com(item)
        item['DESPESA_ADM'] = process_despesa_adm(item)
    else:
        """SEMESTRE MAIOR QUE UM REMOVER ACUMULADO"""
        item['ATIVO'] =  remove_acumulado(process_ativo,item,item_anterior)
        item['ATIVO_CIRCULANTE'] = remove_acumulado(process_ativo_circulante,item,item_anterior)
        item['CREDITO_OPER_PS'] = remove_acumulado(process_credito_oper_ps,item,item_anterior)
        item['PASSIVO'] = remove_acumulado(process_passivo,item,item_anterior)
        item['PASSIVO_CIRCULANTE'] = remove_acumulado(process_passivo_circulante,item,item_anterior)
        item['PASSIVO_NAO_CIRCULANTE'] = remove_acumulado(process_passivo_nao_circulante,item,item_anterior)
        item['PL'] = remove_acumulado(process_pl,item,item_anterior)
        item['RECEITA'] = remove_acumulado(process_receita,item,item_anterior)
        item['CONTRAPRESTACAO_PRE'] = remove_acumulado(process_contraprestacao_pre,item,item_anterior)
        item['CONTRAPRESTACAO_POS'] = remove_acumulado(process_contraprestacao_pos,item,item_anterior)
        item['CORRESP_CEDIDA_POS'] = remove_acumulado(process_corresp_cedida_pos,item,item_anterior)
        item['DESPESA'] = remove_acumulado(process_despesa,item,item_anterior)
        item['EVENTOS_INDENIZAVEIS_PRE'] = remove_acumulado(process_eventos_indenizaveis_pre,item,item_anterior)
        item['EVENTOS_INDENIZAVEIS_POS'] = remove_acumulado(process_eventos_indenizaveis_pos,item,item_anterior)
        item['VARIACAO_PEONA'] = remove_acumulado(process_variacao_peona,item,item_anterior)
        item['DESPESA_COM'] = remove_acumulado(process_despesa_com,item,item_anterior)
        item['DESPESA_ADM'] = remove_acumulado(process_despesa_adm,item,item_anterior)
    return item
   


# In[73]:


lista_arquivos = [i for i in glob.glob(PASTA_DEMONSTRACOES_POR_ANO+"/*")]


# In[74]:


lista_arquivos


# In[84]:


def gerar_arquivos_por_ano(nome_arquivo,data,nome_arquivo_gerado):
    print("EXecutando para",nome_arquivo)
    data.insert(loc=6, column='ATIVO', value=0.0)
    data.insert(loc=7, column='ATIVO_CIRCULANTE', value=0.0)
    data.insert(loc=8, column='PPSC', value=0.0)
    data.insert(loc=9, column='CREDITO_OPER_PS', value=0.0)
    data.insert(loc=10, column='PASSIVO', value=0.0)
    data.insert(loc=11, column='PASSIVO_CIRCULANTE', value=0.0)
    data.insert(loc=12, column='PASSIVO_NAO_CIRCULANTE', value=0.0)
    data.insert(loc=13, column='PESL', value=0.0)
    data.insert(loc=14, column='PL', value=0.0)
    data.insert(loc=15, column='RECEITA', value=0.0)
    data.insert(loc=16, column='CONTRAPRESTACAO_PRE', value=0.0)
    data.insert(loc=17, column='CONTRAPRESTACAO_POS', value=0.0)
    data.insert(loc=18, column='CORRESP_CEDIDA_PRE', value=0.0)
    data.insert(loc=19, column='CORRESP_CEDIDA_POS', value=0.0)
    data.insert(loc=20, column='DESPESA', value=0.0)
    data.insert(loc=21, column='EVENTOS_INDENIZAVEIS_PRE', value=0.0)
    data.insert(loc=22, column='EVENTOS_INDENIZAVEIS_POS', value=0.0)
    data.insert(loc=23, column='VARIACAO_PEONA', value=0.0)
    data.insert(loc=24, column='DESPESA_COM', value=0.0)
    data.insert(loc=25, column='DESPESA_ADM', value=0.0)
    data['CD_CONTA_CONTABIL'] = data['CD_CONTA_CONTABIL'].str.ljust(width=13, fillchar=' ')
    data['VL_SALDO_FINAL'] = data['VL_SALDO_FINAL'].str.replace(pat=',', repl='.').astype(float)
    data = data.set_index("CHAVE")
    data = data.sort_values(by=["REG_ANS","ANO","SEMESTRE","CD_CONTA_CONTABIL"])
    data.insert(loc=0, column='pos', value=np.arange(len(data)))
    data_test = data.apply(process,axis=1)
    data_test.drop(columns=['pos'],inplace=True)
    data_test.to_csv(nome_arquivo_gerado, dtype=str)


# In[ ]:


for _arquivo in lista_arquivos[:1]:
    nome_arquivo_gerado = "ok."+_arquivo[_arquivo.rfind('/')+1:]
    data = pd.read_csv(_arquivo,dtype=str)
    gerar_arquivos_por_ano(_arquivo,data,nome_arquivo_gerado)


# #### qgrid.show_grid(data)

# In[207]:


# data.to_feather(fname='data_processed.feather')


# In[208]:


# data


# In[ ]:




