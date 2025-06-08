# 🗺️ Mapa Interativo de Indicadores Econômicos do Brasil

Este projeto é uma aplicação web que apresenta uma visualização interativa dos principais indicadores econômicos, como **inflação** e **taxa de desemprego**, para cada estado do Brasil. O objetivo é oferecer uma interface clara e dinâmica para que o usuário possa explorar e entender as nuances econômicas regionais do país de forma simples e direta.

Originalmente concebido como um trabalho acadêmico para a manipulação de dados via API, o projeto evoluiu para uma aplicação web completa, utilizando o Django para gerenciar o backend e fornecer os dados a um frontend moderno e responsivo.

## ✨ Funcionalidades

* **Mapa Interativo do Brasil:** Um mapa vetorial (SVG) onde cada estado é um elemento clicável.
* **Visualização de Dados por Estado:** Ao clicar em um estado, um painel exibe os dados atualizados de desemprego e inflação para aquela localidade.
* **Painel Informativo:** Uma seção de texto que explica a importância dos indicadores econômicos abordados no projeto.

## 🛠️ Tecnologias Utilizadas

### **Backend**
* **Python:** Linguagem principal para a lógica do servidor.
* **Django:** Framework utilizado para criar o servidor web e a API interna que fornece os dados ao frontend.

### **Frontend**
* **HTML5:** Estrutura semântica da página.
* **CSS3:** Estilização da interface, utilizando Flexbox para layouts e design responsivo.
* **JavaScript (Vanilla):** Manipulação dinâmica do DOM e consumo dos dados da API com `fetch`.

### **Automação**
* **Script Batch (.bat):** Um script foi criado para automatizar todo o processo de configuração em ambiente Windows: criação do ambiente virtual, instalação de dependências e inicialização do servidor.

## 🚀 Como Executar

1.  Clone este repositório para a sua máquina local.
2.  Navegue até a pasta raiz do projeto.
3.  Execute o arquivo de script `start_site.bat`
4.  O script irá:
    * Criar um ambiente virtual (`venv`).
    * Ativar o ambiente.
    * Instalar todas as dependências listadas no `requirements.txt`.
    * Iniciar o servidor Django.
5.  Após alguns segundos, o seu navegador padrão será aberto automaticamente na página do projeto: `http://127.0.0.1:8000/`.

## 📊 Fonte dos Dados

Todos os indicadores econômicos são obtidos em tempo real através da **API de Agregados do SIDRA**, fornecida e mantida pelo **IBGE** (Instituto Brasileiro de Geografia e Estatística).
