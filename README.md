# JobScraper-Portugal

Sistema de **Web Scraping** para extração automatizada de ofertas de emprego na área de **Tecnologias de Informação** em Portugal. Extrai dados do [ITJobs.pt](https://www.itjobs.pt/) com análise inteligente de tecnologias e geração de relatórios profissionais.

## Características Principais

- **Extração Inteligente**: Análise detalhada de páginas individuais para máxima precisão
- **Detecção Automática**: Identifica automaticamente o número total de páginas disponíveis  
- **Análise Avançada**: Reconhecimento de 100+ tecnologias e classificação por seniority
- **Relatórios PDF**: Geração automática de relatórios com estatísticas e visualizações
- **XML Challenge**: Sistema completo de transformação CSV → XML → Schema → Validação
- **Arquitetura Modular**: Design limpo com separação de responsabilidades

## Dados Extraídos

| Campo | Descrição | 
|-------|-----------|
| **Título** | Nome da posição |
| **Empresa** | Nome da empresa contratante |
| **Localização** | Cidade/região da vaga |
| **Tecnologias** | Lista de tecnologias identificadas |
| **Seniority** | Nível profissional (Junior/Senior/etc.) |
| **Categoria** | Área profissional (Frontend/Backend/etc.) |
| **Tipo de Contrato** | Modalidade contratual |
| **Modo de Trabalho** | Presencial/Remoto/Híbrido |
| **Data de Publicação** | Quando foi publicada |
| **URL** | Link direto para a oferta |
| **Descrição** | Resumo da oferta |

## Tecnologias Utilizadas

**Linguagem**: Python 3.7+

**Web Scraping**:
- Selenium WebDriver - Navegação automatizada
- BeautifulSoup4 - Parsing avançado de HTML  
- WebDriver-Manager - Gestão automática do ChromeDriver

**Processamento de Dados**:
- pandas - Manipulação de dados
- numpy - Computação numérica
- lxml - Processamento XML e validação Schema

**Visualização**:
- matplotlib - Gráficos e visualizações
- seaborn - Visualizações estatísticas
- PdfPages - Geração de relatórios PDF

## Estrutura do Projeto

```
JobScraper-Portugal/
├── src/
│   ├── core/                    # Módulos principais
│   │   ├── scraper.py          # Extração de dados (JobScraper)
│   │   ├── parser.py           # Normalização (JobParser) 
│   │   └── utils.py            # Persistência CSV
│   │
│   ├── xml_challenge/          # Sistema XML
│   │   ├── csv_to_xml.py       # Conversor CSV → XML
│   │   ├── jobs_schema.xsd     # Schema XSD
│   │   ├── xml_validator.py    # Validador Python
│   │   └── jobs_sample.xml     # XML gerado
│   │
│   ├── data/                   # Datasets CSV
│   │
│   ├── main.py                 # Execução padrão (3 páginas)
│   ├── max_main.py             # Execução completa (auto-detecção)
│   └── generate_report.py      # Gerador de relatórios PDF
│
├── requirements.txt            # Dependências principais
└── README.md                   # Documentação
```

## Instalação

### Pré-requisitos
- Python 3.7+
- Google Chrome atualizado
- Conexão à internet

### Setup
```bash
# Clonar repositório
git clone https://github.com/dem04med/JobScraper-Portugal.git
cd JobScraper-Portugal

# Instalar dependências
pip install -r requirements.txt

# Opcional: dependências para relatórios
pip install -r requirements_analysis.txt
```

## Como Executar

### 1. Extração de Dados (Web Scraping)

**Teste Rápido (3 páginas)**:
```bash
cd src
python main.py
```
- Tempo: 3-5 minutos
- Output: `data/jobs_itjobs.csv`
- Uso: Testes e demonstrações

**Extração Completa (auto-detecção)**:
```bash
cd src
python max_main.py  
```
- Tempo: 30-60 minutos
- Output: `data/jobs_itjobs_max_{N}pages.csv`
- Uso: Análise completa de mercado

### 2. Geração de Relatórios

```bash
cd src
python generate_report.py
```
- Output: `relatorio_jobs_YYYYMMDD_HHMMSS.pdf`
- Conteúdo: 4 páginas com análises estatísticas

### 3. XML Challenge

**Conversão CSV → XML**:
```bash
cd src/xml_challenge
python csv_to_xml.py
```

**Validação XML/XSD**:
```bash
cd src/xml_challenge
python xml_validator.py
```

## Solução de Problemas

| Problema | Solução |
|----------|---------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `ChromeDriver error` | Atualizar Google Chrome |
| `TimeoutException` | Verificar conexão internet |
| Nenhum dado extraído | Verificar se site não mudou estrutura |

## Outputs Gerados

### Ficheiros CSV
- **Localização**: `src/data/`
- **Encoding**: UTF-8 
- **Campos**: 11 colunas com dados estruturados

### Relatórios PDF  
- **Localização**: `src/`
- **Páginas**: 4 páginas com gráficos profissionais
- **Análises**: Tecnologias, seniority, geografia, empresas

### XML Challenge
- **jobs_sample.xml**: Dataset convertido para XML
- **jobs_schema.xsd**: Schema de validação  
- **Validação**: Sintaxe e conformidade XSD

