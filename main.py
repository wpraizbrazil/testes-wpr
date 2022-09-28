from typing import Union
from fastapi import FastAPI
from random import randint
from pydantic import BaseModel
import requests
 
alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z', ' ']
fraseConvertidaArray2 = []
 
 
class decriptografaFrase(BaseModel):
    fraseCripto: str
    chave: int
 
 
# ---------------------------- API -------------------------------
app = FastAPI()
 
 
@app.get("/getCifra")
def getCifra():
    # Faz a requisição da dogAPI e o tratamento da frase recebida
    link = "http://dog-api.kinduff.com/api/facts"
    requisicao = requests.get(link)
    dicionario = requisicao.json()
    fraseConvertidaArray = []
    frase = str(dicionario['facts'])  # Define que nossa frase será a chave para facts
    # Faz o tratamento da frase que recebemos e remove os caracteres especiais para evitar erros de cripstografia
    caracteres = ",!?[]'-.:;$%0123456789()*/#@&¨"
    caracteres2 = ',!?[]-.:;$%0"123456789()+*/#@&¨'
    frase = ''.join(l for l in frase if l not in caracteres and caracteres2)
    fraseFormatadaArray = list(frase.upper())
    chave = randint(1, 25)
 
    # Função responsável pela criptografia da frase recebida da dogAPI
    def criptografa(fraseFormatadaArray, chave, alfabeto, fraseConvertidaArray):
        for i in fraseFormatadaArray:
            posicao = alfabeto.index(i)
            if i == ' ':
                nova_Posicao = posicao
            else:
                nova_Posicao = posicao + (chave)
            caractere_criptografado = alfabeto[nova_Posicao % len(alfabeto)]
            fraseConvertidaArray.append(caractere_criptografado)
            fraseConvertidaString = ''.join(fraseConvertidaArray)
            fraseImpressaUsuario = fraseConvertidaString.lower()
        return fraseImpressaUsuario
 
    # Chamada da função de criptografia
    fraseCriptografada = criptografa(fraseFormatadaArray, chave, alfabeto, fraseConvertidaArray)
    # Retorno do JSON
    return {'Frase': fraseCriptografada, 'chave': chave}
 
 
@app.post("/resolveCifra")
def resolveCifra(fraseDecripto: decriptografaFrase):
    def decriptografa(fraseFormatadaArray, chave, alfabeto, fraseConvertidaArray):
        print("cheguei aqui?")
        for i in fraseFormatadaArray:
            posicao = alfabeto.index(i)
            if i == ' ':
                nova_Posicao = posicao
            else:
                nova_Posicao = posicao - (chave)
            caractere_criptografado = alfabeto[nova_Posicao % len(alfabeto)]
            fraseConvertidaArray.append(caractere_criptografado)
            fraseConvertidaString = ''.join(fraseConvertidaArray)
            fraseImpressaUsuario = fraseConvertidaString.lower()
 
        return fraseImpressaUsuario
 
    criptografadaArray = list((fraseDecripto.fraseCripto).upper())
    fraseDecriptografada = decriptografa(criptografadaArray, fraseDecripto.chave, alfabeto, fraseConvertidaArray2)
    return {'Frase': fraseDecriptografada, 'chave': fraseDecripto.chave}
