#!/usr/bin/env python
# coding: utf-8

# Exploração dos dados

import pandas as pd
import numpy as np
from rich import print


df = pd.read_csv('data/routes_base.csv')

print (df.head(1))


#Colunas com valores faltantes
print("[bold]Colunas com valores Faltantes: [red]\n {0} \n".format(
    df.columns[df.isnull().any()].values))

#linhas duplicadas
print("[bold]Duplicadas: [red]{0} ".format(
        df.duplicated().sum()))


# Transfomando os dados

# Convertendo para o formato data
df['schedule_date'] = pd.to_datetime(df['schedule_date'])
df['planning_routes'] = np.where(df['schedule_date'].dt.hour <= 10, 'primeira saída', 'segunda saída')

print(df.head(1))

df['km_pedido'] = df['route_distance_km']/df['total_orders']
df['min_pedido'] = df['route_minutes']/df['total_orders']

df['km_pedido'] = df['km_pedido'].astype(float).round(2)
df['min_pedido'] = df['min_pedido'].astype(float).round(2)

print(df.head(1))


# Dicionário variáveis criadas
#  - planning_routes {Indica o planejamento das rotas primeira saída (quando horário agendado da rota é menor que 10am) e **segunda saída** (quando horário agendado da rota é maior que 10am)}
#  - km_pedido {Indicador total de quilômetros percorridos necessários para entregar um número X de Pedidos}
#  - min_pedido {Indicado total de minutos necessários para entregar um número X de Pedidos}

# Qual o planejamento que possui maior concentração de pedidos?

df_plan = df[['planning_routes', 'total_orders']].groupby('planning_routes').sum().reset_index()
print (df_plan.shape)

# Classificação dos indicadores de km/pedido e Min/pedido por tipo de veículo 

df_indic = df[['car_type', 'km_pedido', 'min_pedido']].groupby('car_type').mean().round(2).reset_index()
print (df_indic.shape)

# Escrevendo os Dataframes

with pd.ExcelWriter('data/case_kpi.xlsx') as writer:
    df.to_excel(writer, sheet_name='dados_transformados', index=False)
    df_plan.to_excel(writer, sheet_name='analise_planejamento', index=False)
    df_indic.to_excel(writer, sheet_name='analise_indicadores', index=False)

print ("Executado com sucesso :tada: :tada:")

