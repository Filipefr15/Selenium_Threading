Metas
#Criar método interativo de rodar o programa (localhost:XXXX)
#Para que seja possível inserir inputs e receber respostas em "tempo real"
#Atualmente a utilidade do docker está "limitada", tecnicamente é necessário alterar
#informações internamente para pesquisar cnpjs

#comando para realizar a build:
#docker build -t selenium-webdriver:1.0.0 .

#comando para rodar em linha de comando:
#docker run --rm -it selenium-webdriver:1.0.0 bash

#para copiar o arquivo gerado dentro do container, docker ps
#docker cp <CONTAINER ID>:/app/funds.xlsx <PATH para copiar>