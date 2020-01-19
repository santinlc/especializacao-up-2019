import math

class CalculoIndicadores:

	def __init__(self):
		pass

	def calcular_resultado_liquido(self,x):
		resultado_liquido = x['RECEITA']-x['DESPESA']-x['IMPOSTO SOBRE LUCRO']
		return resultado_liquido

	def calcular_corresponsabilidade_cedida(self,x):
		corresp_cedida = math.fabs(x['CORRESP_CEDIDA_PRE']) + math.fabs(x['CORRESP_CEDIDA_POS'])
		return corresp_cedida

	def calcular_contraprestacoes_efetivas(self,x):
		contraprest_efetiva = x['RECEITA_COM_ASSISTENCIA_A_SAUDE'] + x['TRIBUTOS DIRETOS'] + self.calcular_corresponsabilidade_cedida(x)
		return contraprest_efetiva

	def calcular_mll(self,x):
		result_liquido = self.calcular_resultado_liquido(x)
		contraprestacoes = self.calcular_contraprestacoes_efetivas(x)
		if(contraprestacoes == 0 ):
			return 0
		return result_liquido/contraprestacoes
	
	def calcular_roe(self,x):
		return self.calcular_resultado_liquido(x)/x['PL']

	def calcular_roa(self,x):
		return self.calcular_resultado_liquido(x)/x['ATIVO']


	def calcular_eventos_indenizaveis_liquido(self,x):
		return x['DESPESA'] + self.calcular_corresponsabilidade_cedida(x)

	def calcular_dm(self,x):
		contraprestacoes = self.calcular_contraprestacoes_efetivas(x)
		if(contraprestacoes == 0 ):
			return 0
		return self.calcular_eventos_indenizaveis_liquido(x)/contraprestacoes

	def calcular_da(self,x):
		contraprestacoes = self.calcular_contraprestacoes_efetivas(x)
		if(contraprestacoes == 0 ):
			return 0
		return x['DESPESA_ADM']/contraprestacoes

	def calcular_dc(self,x):
		contraprestacoes = self.calcular_contraprestacoes_efetivas(x)
		if(contraprestacoes == 0 ):
			return 0
		return x['DESPESA_COM']/contraprestacoes

	def calcular_dop(self,x):
		y = self.calcular_eventos_indenizaveis_liquido(x)+x['DESPESA_ADM']+x['DESPESA_COM']+x['OUTRAS DESPESAS OPERACIONAIS']
		z = self.calcular_contraprestacoes_efetivas(x)+x['OUTRAS DESPESAS OPERACIONAIS']
		if (z ==0):
			return 0
		return y/z			

	def calcular_resultado_financeiro_liquido(self,x):
		return x['RECEITAS FINANCEIRAS'] - x['DESPESAS FINANCEIRAS']	

	def calcular_irf(self,x):
		contraprestracoes_efetivas = self.calcular_contraprestacoes_efetivas(x)
		if (contraprestracoes_efetivas == 0):
			return 0
		return self.calcular_resultado_financeiro_liquido(x)/contraprestracoes_efetivas

	def calcular_liquidez_corrente(self,x):
		return x['ATIVO_CIRCULANTE']/x['PASSIVO_CIRCULANTE']

	def calcular_ct_cp(self,x):
		return (x['PASSIVO_CIRCULANTE']+x['PASSIVO_NAO_CIRCULANTE'])/x['PL']

	def calcular_pmrc(self,x):
		contraprestacao_efetiva = self.calcular_contraprestacoes_efetivas(x)
		if (contraprestacao_efetiva == 0):
			return 0
		return ((x['CREDITO_OPER_PS'] + math.fabs(x['PPSC']))/contraprestacao_efetiva)*360

	def calcular_provisao_eventos_a_liquidar(self,x):
		return x['PESL_OUTROS'] + x['PESL_SUS']

	def calcular_pmpe(self,x):
		return (self.calcular_provisao_eventos_a_liquidar(x)/self.calcular_eventos_indenizaveis_liquido(x))*360

	def calcular_provisoes_tecnicas_exigidas(self,x):
		return x['REMISSAO'] + x['PESL_SUS']+ x['PESL_OUTROS'] + x['PEONA_OUTROS']

	def calcular_latro_pt(self,x):
		provisoes_tecnicas = self.calcular_provisoes_tecnicas_exigidas(x)
		if (provisoes_tecnicas == 0):
			return 0
		return x['APLICAÇÕES GARANTIDORAS']/provisoes_tecnicas