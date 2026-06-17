import streamlit as st
import pandas as pd
import numpy as np
import locale

# Define a localização para o português do Brasil
 locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

#valor = 1550.456
#valor_formatado = locale.currency(valor, grouping=True)

# CALX Configuração da página do Streamlit
st.set_page_config(page_title="Valor de Diagnósticos TIC-BNCC", layout="wide")



# 1. Cria duas colunas: uma menor para o logo e uma maior para o texto
# O parâmetro vertical_alignment="center" garante que fiquem bem alinhados

col1, col2 = st.columns([1, 4])

with col1:
    # Insira o nome exato do arquivo de imagem do logo que está na sua pasta Downloads
    st.image("CUBO COLOR TRANSP.png", width=150) 
with col2:

    # O título agora sem o emoji de gráfico antigo, já que tem o logo!
    st.title("Calculadora de Orçamento Simplificado")

#st.title("📊 Calculadora de Orçamento Simplificado")

st.subheader("Diagnóstico TIC / BNCC Escolas PE")
st.markdown("---")


# --- PARAMETROS FIXOS (Conforme Calculadora Orcamento... Parametros.csv) ---
GASOLINA_PRECO = 7.1
KM_POR_LITRO = 8.0
DIARIA_HOTEL = 250.0
ALIMENTACAO = 60.0
DIARIA_SERVICO = 200.0
LOCACAO_CARRO = 200.0
VALOR_RELATORIO_ESCOLA = 200.0

PESSOAS_EQUIPE = 2
EQUIPES = 1
ESCOLAS_DIA_EQUIPE = 2  
# Capacidade teórica, mas o cálculo usa Escolas/dia real de campo

COMISSAO_EDUM =  0.2
#COMISSAO_PARTNER =  0.3
ISS = 0.05
PC = 0.0925  # PIS/COFINS
IR_CSLL = 0.35
PLAN_MARGIN =  0.263
MULTIPLICADOR = 1/((1- COMISSAO_EDUM - ISS - PC) - PLAN_MARGIN/(1-IR_CSLL))
DISTANCIA_HOTEL = 5.0
D_ENTRE_ESCOLAS = 3.0

print(MULTIPLICADOR)

# --- PAINEL LATERAL DE ENTRADAS (INPUTS) ---
#st.sidebar.header("🔧 Variáveis do Projeto")

st.sidebar.image("EDUMETRICA COLOR.png", width=500)

# Entradas que o usuário deseja testar

n_escolas = st.sidebar.number_input("Número de Escolas", min_value=1, max_value=1000, value=100, step=10)
distancia_cidade = st.sidebar.number_input("Distância da Cidade (km)", min_value=0, max_value=2000, value=250, step=50)

#st.sidebar.markdown("---")
#st.sidebar.markdown("Regras de Logística Aplicadas:")
# Conforme aba de cálculos padrão para 100 escolas / 34 dias
# --- CÁLCULOS LOGÍSTICOS E OPERACIONAIS ---
# Dias necessários (Arredondado para cima)

dias_necessarios = int(np.ceil(n_escolas / ESCOLAS_DIA_EQUIPE))

# Cálculo da Distância Total baseada na estrutura da planilha
# Ida e volta para a cidade + deslocamentos diários hotel/escolas
distancia_total = (distancia_cidade * 2) + (dias_necessarios * DISTANCIA_HOTEL * 2) + (n_escolas * D_ENTRE_ESCOLAS)

# Custos Diretos
custo_hotel = dias_necessarios * DIARIA_HOTEL * PESSOAS_EQUIPE
custo_alimentacao = dias_necessarios * ALIMENTACAO * PESSOAS_EQUIPE
custo_combustivel = (distancia_total / KM_POR_LITRO) * GASOLINA_PRECO
custo_carro = dias_necessarios * LOCACAO_CARRO
custo_relatorio = n_escolas * VALOR_RELATORIO_ESCOLA
custo_mao_de_obra = dias_necessarios * DIARIA_SERVICO * PESSOAS_EQUIPE
custo_base = custo_hotel + custo_alimentacao + custo_combustivel + custo_carro + custo_relatorio + custo_mao_de_obra

# --- FATURAMENTO E IMPOSTOS ---
# Faturamento estimado baseado no multiplicador comercial sobre o custo base
receita_total = custo_base * MULTIPLICADOR
receita_por_escola = receita_total / n_escolas

comissao_EDUM = receita_total * COMISSAO_EDUM

# Impostos e Deduções
total_impostos_sobre_faturamento = receita_total * (ISS + PC)
lucro_antes_ir = receita_total - total_impostos_sobre_faturamento - comissao_EDUM - custo_base 
imposto_renda_csll = max(0.0, lucro_antes_ir * IR_CSLL)

# Margem e Rentabilidade Líquida
resultado_liquido_total = lucro_antes_ir - imposto_renda_csll
resultado_liquido_por_escola = resultado_liquido_total / n_escolas
margem_liquida_percentual = (resultado_liquido_total / receita_total) * 100 if receita_total > 0 else 0

# --- APRESENTAÇÃO DOS RESULTADOS ---

# Cards de Métricas Principais
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Receita por Escola", value=f"R$ {receita_por_escola:,.2f}")
with col2:
    st.metric(label="Receita Total Estimada", value=f"R$ {receita_total:,.2f}")
with col3:
   st.metric(label="Margem Líquida Real", value=f"{margem_liquida_percentual:.2f}%")

#st.markdown("### 📋 Detalhamento Financeiro e Operacional")


# --- MATRIZ DE SENSIBILIDADE (Simulador baseado no arquivo Variaveis.csv) ---
st.markdown("---")

st.markdown("### 🔍 Matriz de Sensibilidade de Valor a Ser Cobrado por Escola")
st.markdown("Veja como o preço por escola varia de acordo com o Número de Escolas (linhas) e a Distância (colunas):")

# Simulação da tabela dinâmica
distancias_teste = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]
escolas_teste = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

matriz_dados = []
for esc in escolas_teste:
    linha = []
    for dist in distancias_teste:
        # Replicação simplificada da variação da matriz
        dias_sim = int(np.ceil(esc / ESCOLAS_DIA_EQUIPE))
        dist_total_sim = (dist * 2) + (dias_sim * DISTANCIA_HOTEL* 2) + (esc * D_ENTRE_ESCOLAS)
        c_base_sim = (dias_sim * DIARIA_HOTEL * PESSOAS_EQUIPE) + (dias_sim * ALIMENTACAO * PESSOAS_EQUIPE) + \
                     ((dist_total_sim / KM_POR_LITRO) * GASOLINA_PRECO) + (dias_sim * LOCACAO_CARRO) + \
                     (esc * VALOR_RELATORIO_ESCOLA) + (dias_sim * DIARIA_SERVICO * PESSOAS_EQUIPE)
        
        rec_tot_sim = c_base_sim * MULTIPLICADOR
        rec_tot = rec_tot_sim / esc
        #print(locale.currency(rec_tot, grouping=True))
        imp_sim = rec_tot_sim * (ISS + PC)
        comissao_EDUM = rec_tot_sim * COMISSAO_EDUM 
        lair_sim = rec_tot_sim - c_base_sim - imp_sim - comissao_EDUM 
        liq_sim = lair_sim * (1 - IR_CSLL)
        
        # Margem unitária líquida aproximada conforme comportamento do seu arquivo original

        margem_un = liq_sim / esc
        linha.append(locale.currency(rec_tot, grouping=True))
    matriz_dados.append(linha)

df_matriz = pd.DataFrame(matriz_dados, index=escolas_teste, columns=[f"{d} km" for d in distancias_teste])
df_matriz.index.name = "Nº Escolas"

st.dataframe(df_matriz.style.background_gradient(cmap="viridis", axis=None))

