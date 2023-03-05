Este script interage com a API da Fastcommerce para a troca de dados entre um site de e-commerce e um sistema ERP. Está escrito em Python e requer as seguintes bibliotecas para funcionar corretamente:
requests
datetime
os
stat
urllib.parse
configparser

Funções
tratamento()
Esta função é responsável por lidar com os códigos de erro retornados pela API da Fastcommerce. Ela procura por tags XML específicas na resposta e define a variável errodesc para uma descrição legível do erro, se houver. 

Os possíveis erros são:
Loja não encontrada
Usuário Inválido
Sem Senha
Erro de Login
Endereço IP Bloqueado
Muitas Tentativas. Usuário suspenso por 3 minutos
Erro de Login. Próximo login inválido suspenderá o usuário por 3 minutos
Método 19 inválido. Ordens inválidas nos registros XML
Report/Utility não encontrado ou acesso negado. Limite de 20 acessos por hora atingido
Acesso à API negado
Erro de Report/Utility
StoreID inválido para este login
StoreID não informado
Loja suspensa
Período de demonstração finalizado
XMLRecords não informado
Acesso negado
Produto(s) inválido(s) no XMLRecords

arquivo()
Esta função cria dois tipos de arquivos de erro, dependendo do código de erro retornado pela API. Se o código de erro for Produto(s) inválido(s) no XMLRecords, ele cria um arquivo chamado ERRO18-{timeLOG}.TXT no diretório dirErros, contendo o carimbo de data/hora e a variável errodesc. Caso contrário, ele cria um arquivo chamado ERROGERAL-{timeLOG}.TXT no mesmo diretório, contendo o carimbo de data/hora e uma mensagem de erro genérica ou a variável errodesc. Se a API retornar um erro interno do servidor, a mensagem de erro será diferente.

UnlockLogFile()
Esta função desbloqueia o arquivo de log removendo as permissões de gravação. É chamada antes do script começar a escrever no arquivo de log.

LockLogFile()
Esta função bloqueia o arquivo de log removendo as permissões de gravação. É chamada após o script terminar de escrever no arquivo de log.

Diretórios
O script usa os seguintes diretórios:

dirLog: diretório onde o arquivo de log está localizado
dirXML: diretório onde os arquivos XML estão localizados
dirErros: diretório onde os arquivos de erro estão localizados
Observe que esses diretórios devem existir e ser acessíveis pelo script.
