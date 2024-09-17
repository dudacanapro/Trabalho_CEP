# Trabalho CEP Aplicativo 
import streamlit as st
from scipy.stats import binom

def calcular_prob_aceitacao(tam_amostra, itens_aceitos, tx_defeitos):
    # Cálculo da probabilidade de aceitação usando a distribuição binomial
    prob_aceitacao = binom.cdf(itens_aceitos, tam_amostra, tx_defeitos)
    return prob_aceitacao

def calcular_risco_fornecedor(tam_amostra, itens_aceitos, tx_defeitos_aceitaveis):
    # Cálculo do risco do fornecedor (probabilidade de rejeitar injustamente um lote aceitável)
    risco_fornecedor = 1 - binom.cdf(itens_aceitos, tam_amostra, tx_defeitos_aceitaveis)
    return risco_fornecedor

def calcular_risco_consumidor(tam_amostra, itens_aceitos, tx_defeitos_inaceitaveis):
    # Cálculo do risco do consumidor (probabilidade de aceitar injustamente um lote inaceitável)
    risco_consumidor = binom.cdf(itens_aceitos, tam_amostra, tx_defeitos_inaceitaveis)
    return risco_consumidor

def calcular_ITM(tam_lote, tam_amostra, tx_aceitacao):
    # Cálculo ITM
    ITM = (1 - tx_aceitacao) * (tam_lote - tam_amostra) + tam_amostra
    return ITM

def main():
    # Digitação dos dados 
    tam_lote = st.number_input("Digite o tamanho do lote (N): ")
    tam_amostra = st.number_input("Digite o tamanho da amostra (n): ")
    numero_lotes = st.number_input("Digite o número de lotes: ")
    itens_aceitos = st.number_input("Digite o número de itens aceitáveis (a): ")
    custo_unitario = st.number_input("Digite o custo unitário de inspeção: R$ ")
    custo_lote_rejeitado = st.number_input("Digite o custo de deslocamento por lote reprovado: R$ ")
    tx_defeitos = st.number_input("Digite o histórico da taxa de defeituosos do fornecedor (número entre 0 a 1 separado por '.'): ")
    tx_defeitos_aceitaveis = st.number_input("Digite a taxa de defeitos aceitável (NQA) (número entre 0 a 1 separado por '.' ): ")
    taxa_defeitos_inaceitaveis = st.number_input("Digite a taxa de defeitos inaceitável (PTDL) (número entre 0 a 1 separado por '.' ): ")

    # Cálculo probabilidade de aceitação (NQA e Real do Fornecedor)
    tx_aceitacao = calcular_prob_aceitacao(tam_amostra, itens_aceitos, tx_defeitos)
    tx_aceitacao_NQA = calcular_prob_aceitacao(tam_amostra, itens_aceitos,tx_defeitos_aceitaveis)

    # Cálculo probabilidade do fornecedor ter um lote injustamente reprovado
    tx_injustamente_rejeitada = (1 - tx_aceitacao)
    tx_injustamente_rejeitada_NQA = (1- tx_aceitacao_NQA)

    # Cálculo ITM
    ITM = calcular_ITM (tam_lote, tam_amostra, tx_aceitacao)

    # Cálculo custo de inspeção
    custo_inspecao = numero_lotes * ITM * custo_unitario

    # Cálculo custo de deslocamento
    custo_deslocamento = numero_lotes * custo_lote_rejeitado * (1 - tx_aceitacao)

    # Cálculo risco do fornecedor
    risco_fornecedor = calcular_risco_fornecedor(tam_amostra, itens_aceitos, tx_defeitos_aceitaveis)

    # Cálculo risco do consumidor
    risco_consumidor = calcular_risco_consumidor(tam_amostra,itens_aceitos, tx_defeitos_inaceitaveis)


    # Resultados 
    st.write(f"Probabilidade de aceitação real (fornecedor) do lote: {tx_aceitacao:.4f}")
    st.write(f"Probabilidade de rejeição injusta do lote do fornecedor: {tx_injustamente_rejeitada:.4f}")
    st.write(f"Probabilidade de aceitação desejado do lote: {tx_aceitacao_NQA:.4f}")
    st.write(f"Probabilidade de rejeição injusta do lote do fornecedor: {tx_injustamente_rejeitada_NQA:.4f}")
    st.write(f"Custo de inspeção: R$ {custo_inspecao:.2f}")
    st.write(f"Custo de deslocamento: R$ {custo_deslocamento:.2f}")
    st.write(f"Risco do consumidor (aceitação injusta) com um lote (PTML: {taxa_defeitos_inaceitaveis}) é: {risco_consumidor:.4f}")
    



if __name__ == "__main__":
    main()
