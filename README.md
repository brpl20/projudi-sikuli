# Como usar

1. Instale Python e todas as dependências necessárias no projeto; 
2. Instale o navegador automatizado de Firefox: `gechodriver` nos meus testes eu utilizei a versão `geckodriver-v0.34.0-linux64.tar.gz`; 
3. Entre no Projudi e faça sua autenticação normalmente; 
4. Ache seu Token de autenticação e feche o Projudi; 
5. Abra o arquivo `firstTry.py` e edite conforme a sua necessidadade: 
    - Insira o token na variável token; 
    - Crie uma lista de processos na variável `processos`; 
6. Deixe rodar, ele irá baixar todos os processos da lista; 

## Parte 2

Se você quiser avançar você pode utilizar o `popler.sh` para extrair apenas algumas folhas do PDF e o `gpt.py` para extrair informações por IA. 

## Atualização 20/08/2024 

Parece que o Projudi alterou a forma de funcionamento e agora a cada sessão temos um novo `token` assim foi preciso adicionar alguns passos a mais: 

1. Autenticar normalmente com um browser normal (usando o firefox);
2. Fechar o navegador e iniciar com o código;
3. Procurar o elemento <Advogado> para clicar como se fosse um usuário;
4. Identificar iFrames;
5. Identificar todas as tokens como uma lista;
6. Filtrar a buscar para apenas a buscar_processos;
7. Extrair a chave e fazer a primeira requisição;
8. Iniciar o looping com os processos pendentes;

_Extra:_ Adicionei também ao GPT um criador de cards no Trello para cada processo; 
