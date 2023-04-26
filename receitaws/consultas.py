# AUTOGENERATED! DO NOT EDIT! File to edit: ..\notebooks\consultas.ipynb.

# %% auto 0
__all__ = ['salvar_requisicao', 'requisitar_em_lote']

# %% ..\notebooks\consultas.ipynb 2
import re
import os
from typing import Union, Iterable
from time import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
import pandas as pd

from fastcore.basics import store_attr, listify
from fastcore.foundation import L
from fastcore.parallel import parallel
from fastcore.xtras import Path, partialler

from validate_docbr import CPF, CNPJ
from .requisicoes import Requisicao

# %% ..\notebooks\consultas.ipynb 3
def salvar_requisicao(results: Iterable, # Lista com o retorno das requisições
                 saida: str, # Nome do Arquivo de Saída
)->None:
    """Salva a lista de requisições `results` no arquivo `saida`"""
    df = pd.DataFrame(results)
    if saida is None:
        saida = Path.cwd() / 'resultados.csv'
    try:
        saida = Path(saida)
    except TypeError as e:
        raise TypeError("Verifique o caminho do arquivo de saída digitado!") from e

    match saida.suffix:
        case '.csv' | '.txt':
            df.to_csv(saida, index=False)
        case '.xlsx':
            df.to_excel(saida, index=False, engine='openpyxl')
        case '.json':
            df.to_json(saida)
        case '.md':
            df.to_markdown(saida, index=False)
        case '.html':
            df.to_html(saida, index=False)
        case _:
            df.to_csv(saida, index=False)
            
    return df

def requisitar_em_lote(entrada: str, # Arquivo texto de entrada: 1 CPF | CNPJ por linha ou objeto python iterável
                       cpf_usuario: str, # CPF do usuário requisitante
                       tipo: str, # Tipo de Requisição CPF | CNPJ
                       origem: str, # Texto com identificação da requisição: e.g. 'Teste'
                       ambiente: str = 'hm', # Ambiente onde realizar a requisição: hm | pd 
                       cache: int = 36, # Tempo de expiração do cache em meses 
                       saida: str = None, # Arquivo de saída da requisição
                       n_workers: int = 2, # Número de requisições a serem efetuadas em paralelo
)->pd.DataFrame:
    """Lê o arquivo `entrada` com um CPF | CPNJ por linha ou o objeto python iterável.
    Faz a requisição no `ambiente` do receita-ws e salva os resultados em `saida`
    """
    try:
        conteudo = Path(entrada).readlines()
    except TypeError:
        conteudo = listify(entrada)
    req = Requisicao(cpf_usuario, tipo, ambiente, origem, cache)
    resultado = req.consultar_em_lote(conteudo, n_workers)
    return salvar_requisicao(resultado, saida)
