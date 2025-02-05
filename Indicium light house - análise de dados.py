#!/usr/bin/env python
# coding: utf-8

# In[37]:


# Indicium LIgh House- desafio Análise de Dados
## Procederemos a análise de dados, utilizando os arquivos CSV disponibilizados
### Faremos de modo didático e gradual, utilizando o notebook que ficará disponível posteriormente no github
## Buscaremos abordar os dados de modo a responder as perguntas e endereçar os KPIs


# In[38]:


### Iniciamos importando as libs necessárias para o desafio
import pandas as pd  # manipulação de dados
import numpy as np  # operações numéricas
import matplotlib.pyplot as plt  # crias algumas visualizações
import seaborn as sns  # gerar gráficos mais complexos
from datetime import datetime  # manipulação de datas


# In[39]:


## próximo passo é carregar os dados que serão utilizados, após feito o upload para o jupyter
# Carregamento dos datasets
caminho_dados = "Indicium_light_house/"

# Carregar cada dataset em um DataFrame
df_agencias = pd.read_csv(caminho_dados + "agencias.csv")
df_clientes = pd.read_csv(caminho_dados + "clientes.csv")
df_colab_agencia = pd.read_csv(caminho_dados + "colaborador_agencia.csv")
df_colaboradores = pd.read_csv(caminho_dados + "colaboradores.csv")
df_contas = pd.read_csv(caminho_dados + "contas.csv")
df_propostas = pd.read_csv(caminho_dados + "propostas_credito.csv")
df_transacoes = pd.read_csv(caminho_dados + "transacoes.csv")


# In[40]:


# agora precismos realizar a primeir análise dos dados, visual e também quanto a dimensão dos dados
# Verificando as primeiras 15 linhas de cada dataset

print(df_transacoes.head(15))

print(df_propostas.head(15))

print(df_contas.head(15))

print(df_clientes.head(15))

print(df_agencias.head(15))

print(df_colab_agencia.head(15))

print(df_colaboradores.head(15))


# In[41]:


### Ficou claro que observar todos os datasets em ambiente python demonstra ser contraproducente
## Melhor criar uma funcao simples que utiliza um dicionario em que as chaves sao categorias e os valores sao os datasets
# Assim fica mais simples e rapido de codar para exibir informações básicas sobre os datasets

print("\nInformações sobre os datasets carregados:")
dfs = {
    "Agências": df_agencias,
    "Clientes": df_clientes,
    "Colaboradores Agência": df_colab_agencia,
    "Colaboradores": df_colaboradores,
    "Contas": df_contas,
    "Propostas Crédito": df_propostas,
    "Transações": df_transacoes,
}
# Exibir as primeiras informacoes descritivas de cada dataset
for nome, df in dfs.items():
    print(f"\n{nome} - Linhas: {df.shape[0]}, Colunas: {df.shape[1]}")
    print(df.head())  # Exibir as primeiras linhas do dataset
    print(f"\nInfo descritivas:")
    print(df.info())
   


# In[42]:


# Vamos a primeira pergunta: 

## Qual trimestre tem, em média, mais transacoes aprovadas e qual tem, também em média, maior volume movimentado?

### Para responder a essa pergunta, precisamos seguir os seguintes passos:
### Transformar os dados daas colunas de data em formato datetime para melhor manipular
### Criar uma coluna de trimestre na tabela de transações
### Agrupar as transações por trimestre


# In[43]:


# Convertendo a coluna de data para o tipo datetime
df_transacoes['data_transacao'] = pd.to_datetime(df_transacoes['data_transacao'])

# Criando a coluna de trimestre
df_transacoes['trimestre'] = df_transacoes['data_transacao'].dt.quarter


# In[44]:


# Agrupando as transacoes por trimestre e calculando a média usando o metodo groupby e .agg()
transacoes_por_trimestre = df_transacoes.groupby('trimestre').agg(
    media_transacoes=('cod_transacao', 'count'),
    volume_medio=('valor_transacao', 'sum')
).reset_index()

# Encontrando os trimestres com os maiores valores
trimestre_mais_transacoes = transacoes_por_trimestre.loc[transacoes_por_trimestre['media_transacoes'].idxmax(), 'trimestre']
trimestre_maior_volume = transacoes_por_trimestre.loc[transacoes_por_trimestre['volume_medio'].idxmax(), 'trimestre']

print(f"O trimestre com mais transações em média é o {trimestre_mais_transacoes}º trimestre.")
print(f"O trimestre com maior volume movimentado em média é o {trimestre_maior_volume}º trimestre.")


# In[45]:


# o quatro trimestre apresenta maior volume e mais transcoes, o que implica nao so que sao realizados mais negocios
# como tambem que os negocios tendem a ser mais substaciais, ou seja, as pessoas precisam de mais dinheiro no final do ano


# In[46]:


# Visualizando os resultados
fig, ax = plt.subplots(1, 2, figsize=(12, 4))

sns.barplot(x='trimestre', y='media_transacoes', data=transacoes_por_trimestre, ax=ax[0])
ax[0].set_title('Média de Transações por Trimestre')
ax[0].set_xlabel('Trimestre')
ax[0].set_ylabel('Média de Transações')

sns.barplot(x='trimestre', y='volume_medio', data=transacoes_por_trimestre, ax=ax[1])
ax[1].set_title('Volume Médio Movimentado por Trimestre')
ax[1].set_xlabel('Trimestre')
ax[1].set_ylabel('Volume Médio')

plt.tight_layout()
plt.show()


# In[ ]:





# In[50]:


# Sabendo que o 4 trimestre tende a ser mais movimentado e volumoso, podemos responder sobre a taxa de aprovacao
# podemos chegar ao seguinte, numero absoluto de propostas que se realizaram em forma de negocio / valor total de propostas
# podemos usar funcao lambda para encontrar os valores de Aprovada e somar estes valores inserindo o resultado em uma variavel
# na tabela de propostas existe o status da proposta que apresenta valores como: em analise, aprovada..
# Contar o total de propostas e aprovações por trimestre

# Converter a coluna de data para o tipo datetime no DataFrame df_propostas
df_propostas['data_entrada_proposta'] = pd.to_datetime(df_propostas['data_entrada_proposta'])

# Criar a coluna de trimestre no DataFrame df_propostas
df_propostas['trimestre'] = df_propostas['data_entrada_proposta'].dt.quarter

# Contar o total de propostas e as aprovacoes por trimestre
propostas_por_trimestre = df_propostas.groupby('trimestre').agg(
    total_propostas=('cod_proposta', 'count'),
    propostas_aprovadas=('status_proposta', lambda x: (x == 'Aprovada').sum())
).reset_index()

# Calcular a taxa de aprovacao por trimestre
propostas_por_trimestre['taxa_aprovacao'] = (propostas_por_trimestre['propostas_aprovadas'] / propostas_por_trimestre['total_propostas']) * 100

# Combinar com as transações para analisar a relação entre aprovações e transações
df_trimestre = transacoes_por_trimestre.merge(propostas_por_trimestre, on='trimestre', how='left')

# Mostrar o trimestre com a maior taxa de aprovação
df_trimestre_sorted = df_trimestre.sort_values(by='taxa_aprovacao', ascending=False)
trimestre_maior_aprovacao = df_trimestre_sorted.iloc[0]

print("\nTrimestre com maior taxa de aprovação:")
print(f"Trimestre: {int(trimestre_maior_aprovacao['trimestre'])}")
print(f"Média de transações: {trimestre_maior_aprovacao['media_transacoes']:.0f}")
print(f"Volume médio movimentado: R$ {trimestre_maior_aprovacao['volume_medio']:,.2f}")
print(f"Total de propostas: {int(trimestre_maior_aprovacao['total_propostas'])}")
print(f"Propostas aprovadas: {int(trimestre_maior_aprovacao['propostas_aprovadas'])}")
print(f"Taxa de aprovação: {trimestre_maior_aprovacao['taxa_aprovacao']:.2f}%")


# In[51]:


# Visualizar taxa de aprovação por trimestre
plt.figure(figsize=(10,5))
sns.barplot(x=df_trimestre['trimestre'].astype(str), y=df_trimestre['taxa_aprovacao'], palette="Blues_r")
plt.title("Taxa de Aprovação de Propostas por Trimestre")
plt.xlabel("Trimestre")
plt.ylabel("Taxa de Aprovação (%)")
plt.xticks(rotation=45)
plt.show()


# In[ ]:


#Pergunta do analista  meses que contém R no seu nome  e volume de transacoes
# A despeito de parecer uma hipotese absurda, podemos responder aos nobre colega usando de 
# referencial estatistico de correlacao, ou seja, o quanto um fator influencia em outro, no caso em especifico
# quanto o fato de um mes ter a letra R ou nao afeta no numero de negocios.
# como apontam os dados o 4 trimestre segue como o top em termos de volume de transacao, todos os meses deste trimestre
#possuem a letra R em seu nome, o que aparenta falsa relacao de causalidade.
# o primeiro trimestre tambem possue R em todos os nomes dos meses, contudo, como apontam os dados, fica no botton da analise
# Portanto, sem perder o tempo com formulas ou dados ou graficos complicados, basta informar ao colega que nao passa de uma
#coicidencia comica.


# In[ ]:


#Pergunta 4: André Tech solicitou  dados públicas para enriquecer a base de dados do BanVic 
# ampliar as possibilidades de análise, considerando principalmente a necessidade atual apresentada.
# em que pese o IPCA ser um bom termometro da inflacao e economia, ele reflete uma realidade menos acurada do que o INPC
# O IPCA indice de precos ao consumidor amplo, leva em conta mais itens supefluos, logo, dialoga com populacao mais abastada
# O INPC por seu turno trata de itens mais necessarios e de uso comum, ele mede mais fidedignamente os impactos da inflacao
# O IPCA , por ser mais amplo, acaba diluindo mais as implicacoes de dinamicas de preco na economia
#ja que o interesse seria eriquecer o banco de dados, melhor usar o INPC disponivel por API no site do IBGE 
# disponibilizo o arquivo das series historicas do INPC no mesmo link do projeto que esta no github


# In[ ]:


#vamos demonstrar alguns KPIs - Key Performance Indicators que podem ser uteis ao tomador de decisoes 
# Taxa de aprovacao de credito - o coracao do negocio-  pode indicar melhores oportunidades de vender o produto
#Volume de transacoes por agencia, possivel integrar os dados de agencias e de negocios realizados, encontrando qual
# unidade vende mais e a partir dai tentar replicar os procedimentos as demais agencias aumentando o aproveitamento
# no mesmo sentido, quais os funcionarios vendem mais, ou seja, quais profissionais podem ser os diretores ou gerentes
# no proposito de que liderem times e campanhas para melhorar os indices e treinar mais colaboradores.


# In[56]:


# 1. Taxa de Aprovação de Crédito
df_propostas['aprovada'] = df_propostas['status_proposta'].apply(lambda x: 1 if x == 'Aprovada' else 0)
taxa_aprovacao = df_propostas['aprovada'].mean() * 100
print(f"Taxa de Aprovação de Crédito: {taxa_aprovacao:.2f}%")


# In[59]:


# 2. Volume de Transações por Agência
transacoes_por_agencia = df_transacoes.groupby('num_conta').agg(
    total_transacoes=('valor_transacao', 'count'),
    volume_total=('valor_transacao', 'sum')
).reset_index()

df_contas_agencias = df_contas[['num_conta', 'cod_agencia']].merge(transacoes_por_agencia, on='num_conta', how='left')
df_agencias_transacoes = df_contas_agencias.merge(df_agencias[['cod_agencia', 'nome', 'cidade']], on='cod_agencia', how='left')
agencias_transacoes = df_agencias_transacoes.groupby(['nome', 'cidade']).agg(
    total_transacoes=('total_transacoes', 'sum'),
    volume_total=('volume_total', 'sum')
).reset_index()

print("Top 10 Agências com Maior Volume de Transações:")
print(agencias_transacoes.sort_values(by='volume_total', ascending=False).head(10))


# In[ ]:





# In[64]:


# 3. Funcionários que Mais Realizam Vendas
vendas_por_funcionario = df_propostas.groupby('cod_colaborador').agg(
    propostas_realizadas=('cod_proposta', 'count'),
    propostas_aprovadas=('aprovada', 'sum')
).reset_index()
vendas_por_funcionario['taxa_aprovacao'] = (vendas_por_funcionario['propostas_aprovadas'] / vendas_por_funcionario['propostas_realizadas']) * 100

# Mesclar com os nomes dos colaboradores e suas respectivas agências
df_vendas_funcionarios = vendas_por_funcionario.merge(df_colaboradores[['cod_colaborador', 'primeiro_nome', 'ultimo_nome']], on='cod_colaborador', how='left')
df_vendas_funcionarios = df_vendas_funcionarios.merge(df_colab_agencia[['cod_colaborador', 'cod_agencia']], on='cod_colaborador', how='left')
df_vendas_funcionarios = df_vendas_funcionarios.merge(df_agencias[['cod_agencia', 'nome']], on='cod_agencia', how='left')

# Selecionar apenas as colunas necessárias
df_vendas_funcionarios = df_vendas_funcionarios[['primeiro_nome', 'ultimo_nome', 'nome', 'taxa_aprovacao']]

print("Top 10 Funcionários com Maior Taxa de Aprovação:")
print(df_vendas_funcionarios.sort_values(by='taxa_aprovacao', ascending=False).head(10))


# In[ ]:





# In[ ]:


###podemos ir avante com as primeiras analises - verificar quais os clientes mais ativos, agencias que mais fecham negocios
###qual tipo de emprestimo mais ralizado, ou seja, a media dos valores, para segmentar ofertas


# In[ ]:




