# Tech Challenge

Projeto criado com o objetivo de entregar o desafio proposto pelo Curso de Software Architecture FIAP + Alura.

Este projeto tem como objetivo implementar as melhores práticas de desenvolvimento e arquitetura de código. Nesta etapa do projeto estamos utilizando a Arquitetura Limpa, com base nos requisitos levantados pelas práticas de Domain Driven Design aplicadas no módulo 1 [Event Storming](https://miro.com/app/board/uXjVM44WnuU=/?share_link_id=199664765180). (Este quadro é privado, para obter acesso basta entrar em contato com um dos membros da equipe).


## Arquitetura

<p>
    <img  src=content/arquitetura_tech_challenge.jpg>
</p>

O app está integrado com a API de QR Code Dinâmico do MercadoPago para realização do pagamento dos pedidos.

<p>
    <img  src=content/MercadoPago.jpeg>
</p>

Junto a este serviço foi criado um sistema de notificações via SMS para confirmação do pagamento e produção do pedido.

<p>
    <img  src=content/notification.png>
</p>


## Autores
- Rafael Perin - RM349501
- Lucas Gabriel - RM349527

## Stack
- Python 3.8.16
- FastAPI
- PostgreSQL 
- Docker
- Compose
- Kubernetes

## Pré-requisitos
Para executar o projeto, é necessário ter instalado:

- [Docker version >= 20.10.7](https://www.docker.com/get-started)
- [Docker-compose version >= 1.29.2](https://docs.docker.com/compose/install/)

## Rodando com docker-compose

1. Clonar o repositório e executar o comando abaixo na raiz do projeto:

```bash
$ docker compose up -d
```

Algumas variáveis de ambiente foram deixadas hardcoded no arquivo docker-compose.yml para simplicidade de execução, dado o fim apenas educacional do projeto. Outras como chaves de acesso da AWS precisam ser preenchidas para que o projeto funcione normalmente.

IMPORTANTE: Para funcionamento da integração com mercado pago localmente é necessário configurar um serviço como o NGROK para expôr o endpoint localhost de nossa API. 
 
## Rodando FastAPI

Após rodar o docker-compose, abrir os seguintes endereços no navegador:

```
http://localhost:8000/docs
```


```
http://localhost:8001/docs
```


```
http://localhost:8002/docs
```


```
http://localhost:8003/docs
```


```
http://localhost:8004/docs
```

Caso tenha o desejo de executar a aplicação via Insomnia ou Postman, é possível capturar os dados em http://localhost:8000/openapi.json e transformar em arquivo .json para ser importado.

## SAGA

Para este projeto decidimos utilizar o padrão de SAGA coreografada, podendo assim tirar proveito dos benefícios de baixo acomplamento, facilidade de manutenção e assincronia. Dado o tamanho e simplicidade do projeto, algumas desvantagens desse padrão como a complexidade de evolução e visibilidade geral do sistema não terão um impacto tão grande.

Utilizamos uma combinação dos serviços SNS e SQS da cloud AWS como solução de mensageria. O SNS fica responsável pelo disparo dos eventos, e com ele fica mais simples a integração de um novo serviço consumidor, sendo apenas necessário apontar uma nova fila SQS para este serviço, sem precisar fazer alterações no serviço de onde originou o evento.

O SQS é responsável por enfileirar os eventos disparados que serão consumidos pelos serviços correspondentes. Já é nativo do serviço um sistema de retry em caso de falha ao processar um evento, e um possível redirecionamento para uma fila DLQ quando um limite de tentativas é atingido, retirando assim um pouco da complexidade por parte da aplicação.

<p>
    <img  src=content/saga.jpg>
</p>

## OWASP ZAP

Foi utilizada a ferramenta ZAP Scanning para buscar por vulnerabilidades na aplicação, não sendo encontrada nenhuma vulnerabilidade alta ou crítica, segundo o relatório:

https://1drv.ms/u/s!AiVX_MlZ4H9_ibsIxvn0E9b6X4f97A?e=crAcI0

## RIPD 

Pensando na privacidade dos nossos usuários, e garantindo aderência à lei geral de proteção de dados, foi criado um relatório RIPD explicação como funciona toda a manipulação dos dados dos usuários. Segue abaixo o documentação com vídeo para explicação:

https://www.youtube.com/watch?v=lGvdJJlxWPY

https://1drv.ms/w/s!AiVX_MlZ4H9_ibsJrhM1_OcWz7RxCQ?e=biCMj4

## DEMO

Por fim, segue abaixo vídeo demo e detalhamento de arquitetura e padrão SAGA:

https://www.youtube.com/watch?v=HcFb-Mpxox0


