# JobScraper-Portugal

Este projeto, desenvolvido no âmbito do estudo e prática de **Web Scraping e Web Crawling**, visa a recolha automática de **ofertas de emprego na área de Tecnologias de Informação (TI)** em **Portugal**, extraindo dados relevantes sobre:
- Título da vaga
- Empresa contratante
- Localização
- Salário (quando disponível)
- Tecnologias ou requisitos mencionados
- Link direto para a oferta

A recolha desta informação será extraída do ITJobs (https://www.itjobs.pt/) através de técnicas de **Web Crawling em Python**.

## Tecnologias e Bibliotecas Utilizadas  Linguagem Principal - Python

Web Scraping - `requests`, `beautifulSoup4`<br>
Automação - `Selenium`<br>
Estruturação e Análise de Dados - `pandas`<br>
Armazenamento/Exportação - `csv`, `json`<br>
Tratamento de Exceções e Logs - `logging`<br>

## Estrutura de Diretórios

JobScraper-Portugal/<br>
│<br>
├── data/ # Dados recolhidos (CSV/JSON)<br>
├── src/ # Código-fonte<br>
│ ├── main.py # Ponto de entrada do programa<br>
│ ├── scraper.py # Funções de scraping<br>
│ ├── parser.py # Extração e limpeza dos dados<br>
│ └── utils.py # Funções auxiliares<br>
│<br>
├── requirements.txt # Dependências do projeto<br>
└── README.md # Documentação<br>
