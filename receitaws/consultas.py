# AUTOGENERATED! DO NOT EDIT! File to edit: ..\consultas.ipynb.

# %% auto 0
__all__ = ['BASEURL', 'AMBIENTE', 'TYPE', 'CPF_SIMPLES', 'SEXO', 'SIZE', 'Request', 'save_request', 'request_from_file']

# %% ..\consultas.ipynb 2
import re
from typing import Union, Iterable

import requests
import pandas as pd

from fastcore.basics import store_attr
from fastcore.foundation import L
from fastcore.parallel import parallel
from fastcore.xtras import Path
from fastcore.script import call_parse, Param

BASEURL = "http://webservicesintranet{}.anatel.gov.br/receita/rest/"
AMBIENTE = {'ds', 'hm', 'su', 'pd'}
TYPE = {'cpf': "obterPessoaFisica", 'cnpj': "obterPessoaJuridica"}
CPF_SIMPLES = ('cpf', 'nome', 'nomeMae', 'dataNascimento', 'estrangeiro',
               'tituloEleitor', 'dataAtualizacao', 'dataRegistroAnatel', 
               'resultado', 'unidadeAdministrativaCodigo', 'anoObito', 'erro')
SEXO =  {1: 'Masculino', 2: 'Feminino', 9 : 'Não encontrado'}
SIZE = {11: 'cpf', 14: 'cnpj'}

# %% ..\consultas.ipynb 5
class Request:
    def __init__(self, 
                 cpf_usr: Union[str, int], # CPF do usuário requisitante
                 ambiente: str = 'ds', # Ambiente onde realizar a requisição: ds: desenvolvimento, hm: homologação, su: sustentação, pd: produção
                 origem: str = None, # Texto com identificação da requisição: e.g. "Teste"
                 cache: int = 36, # Tempo de expiração do cache em meses (Produção)
    ):
        """Classe para fazer requisições ao Web Service Infoconv da Receita Federal"""
        store_attr()
        assert isinstance(self.origem, str), "origem não pode ficar vazio e deve ser uma string de até 30 caracteres"
        self.origem = self.origem[:30]
        assert (ambiente := self.ambiente.lower()) in AMBIENTE, f"Ambiente inválido, escolha uma das opções {AMBIENTE}"
        if ambiente == 'pd':
            self.ambiente = ''

    def format_url(self, query)-> str: 
        if (tipo := len(query)) not in SIZE:
            raise ValueError("Query inválida, CPF possui 11 caracteres e CNPJ possui 14 caracteres")
        tipo = SIZE[tipo] 
        req_type = TYPE[tipo]
        suffix = ''
        if self.cache is not None:
            try:
                cache = int(self.cache)
                assert cache >= 0, "Tempo de expiração do cache inválido, escolha um número inteiro maior que zero"
            except ValueError as e:
                raise ValueError("Valor inválido de expira_cache, escolha um número inteiro maior que zero") from e
            req_type += 'IgnoraCacheAntigo'
            suffix = f'&mesesExpiraCache={cache}'

        return f'{BASEURL.format(self.ambiente)}{req_type}?{tipo}={query}&cpfUsuario={self.cpf_usr}{suffix}&origem={self.origem}'

    @staticmethod
    def parse_json(cnpj_dict)-> dict:
        d = {}
        for k,v in cnpj_dict.items():
            if isinstance(v, list): 
                v = '|'.join(v)
            if isinstance(v, dict):
                d.update({f'{k}_{sk}': sv for sk, sv in v.items()})
                continue
            d[k] = v
        return {k:v.lstrip().rstrip() if isinstance(v, str) else v for k, v in d.items()}

    def get_request(self, url)-> dict:
        """Make a request to the url and return the json response"""
        r = requests.get(url)
        if r.status_code == 200 and r.headers['content-type'] == 'application/json':
            return Request.parse_json(r.json())
        return {}

    def query_ws(self, 
                 query: Union[str, int], # Identificador da requisição: CPF ou CNPJ de acordo com o tipo

                ):
        query = ''.join(re.findall("\d", query))
        return self.get_request(self.format_url(query))
    
    def batch_request(self, queries: Iterable[Union[str, int]]):                        
        return L(queries).map(self.query_ws)
        

# %% ..\consultas.ipynb 21
def save_request(results: Iterable, # Lista com o retorno das requisições
                 saida: str, # Nome do Arquivo de Saída
):
    """Salva a lista de requisições `results` no arquivo `saida`"""
    df = pd.DataFrame(results)
    try:
        saida = Path(saida)
    except TypeError:
        saida = Path.cwd()
    match suffix := saida.suffix:
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
            df.to_clipboard(sep=',', index=False)

@call_parse
def request_from_file(filename: Param("Arquivo texto de entrada: 1 CPF | CNPJ por linha", str),
                      cpf_usuario: Param("CPF do usuário requisitante", str),
                      ambiente: Param("Ambiente onde realizar a requisição: ds | hm | su | pd", str) = 'ds', 
                      origem: Param("Texto com identificação da requisição: e.g. 'Teste'", str) = None, 
                      cache: Param("Tempo de expiração do cache em meses (Produção)",  int) = 36, 
                      saida: Param("Arquivo de saída da requisição", str) = None, 
):
    """Lê o arquivo `filename` com um CPF | CPNJ por linha. Faz a requisição no `ambiente` do receita-ws e salva os resultados em `saida`"""
    contents = Path(filename).readlines()
    req = Request(cpf_usuario, ambiente, origem, cache)
    results = req.batch_request(contents)
    save_request(results, saida)
