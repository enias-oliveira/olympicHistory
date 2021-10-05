# Sobre
Ester README tem por objetivo fornecer as informaÃ§Ãµes necessÃ¡rias para instalaÃ§Ã£o e execuÃ§Ã£o de uma API REST, feita com Django e o Django Rest framework, que usa um [Dataset de 120 anos de historia das Olimpíadas](https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results#athlete_events.csv).

#  InstalaÃ§Ã£o

## DependÃªncias

Esse projeto foi desenvolvido com [Poetry](https://python-poetry.org/), uma alternativa ao Pip para gestÃ£o de dependencias. 
 
Dito isso, o arquivo "requirements.txt" dÃ¡ suporte para o uso do Pip.

### Instalação com Docker

Está disponivel uma configuração para para rodar a aplicação com o docker / docker-compose. Basta ter as duas ferramentas devidamente configuradas e rodar `docker-compose up --build`

Nota se que os comandos seeds vão popular toda vez que subir os containers, recomendo criar um volume e deletar caso for rodar novamente. (O ideial seria colocar uma condição, vou colocar no futuro)

Acessando o `localhost:8000` você terá acesso a API.

### Passo-a-passo para instalaÃ§Ã£o Manual com Pip
*Na linha de comando, usando Bash:*
- 1. Criar um ambiente virtual usando venv : `python -m venv venv`
- 2. Entrar no ambiente virtual: `source venv/bin/activate`
- 3 . Instalar todas as dependencias: `pip install -r requirements.txt`
- 4. Rodar migrations `python manage.py migrate`
- 5. Rodar commando seeds `python manage.py seed_countries data/noc_regions.csv; python manage.py seed_athletes data/athlete_events.csv'`
- 6. Iniciar servidor `python manage.py runserver 0.0.0.0:8000`

### Passo-a-passo para instalaÃ§Ã£o com Poetry

*Na linha de comando, usando Bash:*
- 1. Entrar no ambiente virtual: `poetry shell`
- 2. Instalar todas dependencias: `poetry install`
- Igual ao Pip


## Banco de Dados

Se for rodar localmente, será necessÃ¡rio criar um Banco de dados local sem nenhuma configuraÃ§Ã£o ou tabela e depois rodar as migrations.

A API salva os dados em um banco de dados PostgreSQL para fácil deploy no Heroku.

Também é possivel usar uma versão "Teste", que usa o SQLite, basta adicionar uma variável de ambiente TEST=True


## Variaveis de ambiente

O arquivo "dev.env" é onde se espera colocar as variáveis de ambiente relacionadas ao Banco PostgreSQL local

## Endpoints

### Games
Games são os jogos Olimpícos. Podem ser lidos individualmente, listados, criados, atualizados e deletados. 


Exemplos:
`api/games/`
`api/games/1`
`api/games?year=2012`

![List Games]( ./readme_images/list_games.png )

Tambem podem ser filtrados por Ano e/ou Cidade atráves dos parametros name e city na url.
