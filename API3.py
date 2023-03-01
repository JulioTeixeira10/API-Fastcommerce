#Bibliotecas para requests, horarios, codificações, arquivo .cfg e permissões de arquivos
import requests
import datetime
import os
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
import urllib.parse
from configparser import ConfigParser

#Funções
def tratamento(): #Função para tratamento de erros
    global errodesc
    errodesc = []
    index1 = checkresponse.find("<ErrCod>1</ErrCod>")
    index2 = checkresponse.find("<ErrCod>2</ErrCod>")
    index3 = checkresponse.find("<ErrCod>3</ErrCod>")
    index4 = checkresponse.find("<ErrCod>4</ErrCod>")
    index5 = checkresponse.find("<ErrCod>5</ErrCod>")
    index6 = checkresponse.find("<ErrCod>6</ErrCod>")
    index7 = checkresponse.find("<ErrCod>7</ErrCod>")
    index8 = checkresponse.find("<ErrCod>8</ErrCod>")
    index9 = checkresponse.find("<ErrCod>9</ErrCod>")
    index10 = checkresponse.find("<ErrCod>10</ErrCod>")
    index11 = checkresponse.find("<ErrCod>11</ErrCod>")
    index12 = checkresponse.find("<ErrCod>12</ErrCod>")
    index13 = checkresponse.find("<ErrCod>13</ErrCod>")
    index14 = checkresponse.find("<ErrCod>14</ErrCod>")
    index15 = checkresponse.find("<ErrCod>15</ErrCod>")
    index16 = checkresponse.find("<ErrCod>16</ErrCod>")
    index17 = checkresponse.find("<ErrCod>17</ErrCod>")
    index18 = checkresponse.find("<ErrCod>18</ErrCod>")
    if index1 > 1:
        errodesc = "Loja não encontrada"
    elif index2 > 1:
        errodesc = "Usuario Inválido"
    elif index3 > 1:
        errodesc = "Sem Senha"
    elif index4 > 1:
        errodesc = "Erro de Login"
    elif index5 > 1:
        errodesc = "Endereço IP Bloqueado"
    elif index6 > 1:
        errodesc = "Muitas Tentativas. Usuario suspenso por 3 minutos"
    elif index7 > 1:
        errodesc = "Erro de Login. Proximo login invalido suspenderá o usuario por 3 minutos"
    elif index8 > 1:
        errodesc = "Método 19 inválido. Ordens inválidas nos registros XML"
    elif index9 > 1:
        errodesc = "Report/Utility não encontrado ou acesso negado. Limite de 20 acessos por hora atingido"
    elif index10 > 1:
        errodesc = "Accesso à API negado"
    elif index11 > 1:
        errodesc = "Erro de Report/Utility"
    elif index12 > 1:
        errodesc = "StoreID inválido para este login"
    elif index13 > 1:
        errodesc = "StoreID não informado"
    elif index14 > 1:
        errodesc = "Loja suspensa"
    elif index15 > 1:
        errodesc = "Periodo de demostração finalizado"
    elif index16 > 1:
        errodesc = "XMLRecords não informado"
    elif index17 > 1:
        errodesc = "Acesso negado"
    elif index18 > 1:
        errodesc = "Produto(s) inválido(s) no XMLRecords"
def arquivo(): #Função para criação dos arquivos de erro ERRO18.TXT e ERROGERAL.TXT
    tratamento() #função chamada para obter o campo errodesc
    if errodesc == "Produto(s) inválido(s) no XMLRecords":
        file = open(f"{dirErros}\\ERRO18-{timeLOG}.TXT","w+")
        file.write(time)
        file.write("\n \n")
        file.write(errodesc)
        file.close()
    else:
        file = open(f"{dirErros}\\ERROGERAL-{timeLOG}.TXT","w+")
        file.write(time)
        if checkresponse == "The page cannot be displayed because an internal server error has occurred.":
            file.write("\n \nHouve um erro interno no servidor do Fastcommerce.")
            file.close()
        else:
            file = open(f"{dirErros}\\ERROGERAL-{timeLOG}.TXT","a")
            file.write("\n \n")
            file.write(errodesc)
            file.close()
def UnlockLogFile(): #Função desbloquear o arquivo de log
    try:
        os.chmod(f"{dirLog}\\LOG-{timeLOG}.log", S_IWUSR|S_IREAD)
    except FileNotFoundError:
        pass
def LockLogFile(): #Função bloquear o arquivo de log
    try:
        os.chmod(f"{dirLog}\\LOG-{timeLOG}.log", S_IREAD|S_IRGRP|S_IROTH)
    except FileNotFoundError:
        pass

#Diretorios
dirLog = "C:\\Bancamais\\Fastcommerce\\Log" #Diretorio do arquivo de LOG
dirXML = "C:\\Bancamais\\Fastcommerce\\XML" #Diretorio do arquivo XML
dirErros = "C:\\Bancamais\\Fastcommerce\\Erros" #Diretorio dos arquivos de erro
dirDados = "C:\\Bancamais\\Fastcommerce\\DadosLoja" #Diretorio do arquivo de dados da loja

#Administração do arquivo .cfg
config_object = ConfigParser()
config_object.read(f"{dirDados}\\StoreData.cfg")
STOREINFO = config_object["STOREINFO"]
StoreName = STOREINFO["StoreName"]
StoreID = STOREINFO["StoreID"]
Username = STOREINFO["Username"]
password = STOREINFO["password"]
timeLOG = STOREINFO["ultdata"]

#Script para adicionar o horario nos arquivos de erro e no arquivo de LOG
today_datetime = datetime.datetime.today()
time = today_datetime.strftime('%d/%m/%Y %H:%M:%S')

#Script para trazer e codificar o XML para a URL
try:
    textoxml = open(f'{dirXML}\\xml.txt','r')
except FileNotFoundError: #tratamento de erro se o XML não for encontrado
    UnlockLogFile()
    file = open(f"{dirLog}\\LOG-{timeLOG}.log","a")
    file.write(time)
    file.write(" - [ERRO XML] - XML NÃO encontrado. \n")
    LockLogFile()
    file = open(f"{dirErros}\\ERROGERAL-{timeLOG}.TXT","w+")
    file.write(time)
    file.write(" - XML NÃO encontrado.")
    file.close()
    exit()
str = textoxml.read()
new = urllib.parse.quote(str)
xmlrecord = new

#Script para enviar a request
url = "https://www.rumo.com.br/sistema/adm/APILogon.asp"
payload= (f"""StoreName={StoreName}&StoreID={StoreID}&Username={Username}&
          method=ProductManagement&password={password}&XMLRecords={xmlrecord}""")
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'}
try:
    response = requests.request("POST", url, headers=headers, data=payload)
except: #Tratamento de erro em caso de que o usuario não tenha internet ou a data esteja muito adiantada
    UnlockLogFile()
    file = open(f"{dirLog}\\LOG-{timeLOG}.log","a")
    file.write(time)
    file.write(" - [ERRO XML] - ERRO de CONEXÃO ou de CERTIFICADO SSL.\n")
    LockLogFile()
    file = open(f"{dirErros}\\ERROGERAL-{timeLOG}.TXT","w+")
    file.write(time)
    file.write("\n \nERRO de CONEXÃO ou de CERTIFICADO SSL. Se asegure de que seu PC está conectado à internet e que a data não esteja muito adiantada. ")
    file.close()
    exit()

#Script para checar erros na request
checkresponse = response.text
index = checkresponse.find("<ErrDescr>OK</ErrDescr>")
if index != (-1):
    pass
else:
    arquivo()

#Info sobre a quantidade de registros
COMANDO = xmlrecord.count('Comando')
ccc = checkresponse.find(f'Valid="{COMANDO}"')
if COMANDO == 0: #tratamento de erro se não existir nenhum registro no XML
    file = open(f"{dirErros}\\ERROGERAL-{timeLOG}.TXT","w+")
    file.write(time)
    file.write("\n \nO XML recebido NÃO contém nenhum registro. Verifique o XML, emita um novo e tente novamente.")
    file.close()
    UnlockLogFile()
    file = open(f"{dirLog}\\LOG-{timeLOG}.log","a")
    file.write(time)
    file.write(" - [ERRO XML] - O XML recebido NÃO contém nenhum registro. \n")
    LockLogFile()
    exit()

#Função para calcular quantos registros foram válidos e quantos não
Validvalueindex = checkresponse.find('Valid="')
v1 = Validvalueindex + 7
v2 = Validvalueindex + 8
v3 = Validvalueindex + 9
v4 = Validvalueindex + 10               
v5 = Validvalueindex + 11

try:                                           
    if checkresponse[v2] == '"':
        Valuestr = checkresponse[v1]
        Value =int(Valuestr)
    elif checkresponse[v3] == '"':
        Valuestr = checkresponse[v1] + checkresponse[v2]
        Value =int(Valuestr)
    elif checkresponse[v4] == '"':
        Valuestr = checkresponse[v1] + checkresponse[v2] + checkresponse[v3]
        Value =int(Valuestr)
    elif checkresponse[v5] == '"':
        Valuestr = checkresponse[v1] + checkresponse[v2] + checkresponse[v3] + checkresponse[v4]
        Value =int(Valuestr)
except:
    pass

if ccc != (-1): #Detalhes arquivo ERRO18
    pass
else:
    if errodesc == "Produto(s) inválido(s) no XMLRecords":
        file = open(f"{dirErros}\\ERRO18-{timeLOG}.TXT","a")
        if Value == 1:
            file.write(f"\nO XML recebido contém {COMANDO} registro(s), mas apenas 1 foi enviado porque houve um erro no registro número {Value + 1}.")
        elif Value > 1:
            file.write(f" - O XML recebido contém {COMANDO} registros, mas apenas os {Value} primeiros foram enviados porque houve um erro no registro número {Value + 1}.")
        elif Value == 0:
            file.write(f" - O XML recebido contém {COMANDO} registro(s), mas nenhum foi enviado porque houve um erro no primeiro registro do XML.")
        file.write(f"\n[ Registros ENVIADOS: {Value} ]")
        file.write(f"\n[ Registros FALTANDO: {COMANDO - Value} ]")
        file.close()

#Log de XMLs enviados
UnlockLogFile()
file = open(f"{dirLog}\\LOG-{timeLOG}.log","a")
file.write(time)
if checkresponse == "The page cannot be displayed because an internal server error has occurred.":
    file.write(" - [ERRO XML] - Houve um erro interno no servidor do Fastcommerce.")
try:
    erroc = errodesc.count(" ")
    if erroc > 0:
        file.write(" - [ERRO XML] - ")
except NameError:
    pass
try:
    file.write(errodesc)
except NameError:
    file.write(" - [XML Enviado] - TUDO CERTO")
except TypeError:
    pass
file.write("\n")
file.close()
LockLogFile()

exit()