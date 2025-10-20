# JobScraper-Portugal

Sistema avançado de **Web Scraping** para extração automatizada de ofertas de emprego na área de **Tecnologias de Informação** em Portugal. O projeto utiliza técnicas inteligentes de scraping e análise para processar dados do [ITJobs.pt](https://www.itjobs.pt/) com alta precisão.

## Características Principais

- **Extração Inteligente**: Análise detalhada de páginas individuais para máxima precisão
- **Detecção Automática**: Identifica automaticamente o número total de páginas disponíveis
- **Análise Avançada**: Reconhecimento de 100+ tecnologias e classificação por seniority/categoria
- **Relatórios Profissionais**: Geração automática de PDFs com estatísticas e visualizações
- **Arquitetura Modular**: Design limpo com separação de responsabilidades

## Dados Extraídos

| Campo | Descrição | Método de Extração |
|-------|-----------|-------------------|
| **Título** | Nome da posição | Seletores CSS específicos |
| **Empresa** | Nome da empresa contratante | Análise estrutural HTML |
| **Localização** | Cidade/região da vaga | Extração e normalização |
| **Tecnologias** | Lista de tecnologias identificadas | Padrões regex inteligentes |
| **Seniority** | Nível profissional (Junior/Senior/etc.) | Análise semântica de conteúdo |
| **Categoria** | Área profissional (Frontend/Backend/etc.) | Classificação automatizada |
| **Tipo de Contrato** | Modalidade contratual | Análise de metadados |
| **Modo de Trabalho** | Presencial/Remoto/Híbrido | Detecção por palavras-chave |
| **Data de Publicação** | Quando foi publicada | Extração temporal |
| **Descrição** | Resumo da oferta | Limpeza e formatação |

## Tecnologias Utilizadas

**Linguagem**: Python 3.7+

**Web Scraping & Automação**:
- `Selenium` - Navegação automatizada e execução de JavaScript
- `BeautifulSoup4` - Parsing avançado de HTML
- `WebDriver-Manager` - Gestão automática do ChromeDriver

**Análise & Processamento**:
- `pandas` - Manipulação e estruturação de dados
- `numpy` - Computação numérica
- `re` (regex) - Reconhecimento de padrões

**Visualização & Relatórios**:
- `matplotlib` - Gráficos e visualizações
- `seaborn` - Visualizações estatísticas avançadas
- `PdfPages` - Geração de relatórios PDF

## Estrutura do Projeto

```
JobScraper-Portugal/
├── src/
│   ├── core/                    # Módulo principal
│   │   ├── __init__.py         # Exportações do módulo
│   │   ├── scraper.py          # Extração inteligente (JobScraper)
│   │   ├── parser.py           # Padronização (JobParser)
│   │   └── utils.py            # Persistência CSV
│   │
│   ├── data/                   # Dados extraídos
│   │   └── *.csv              # Arquivos CSV gerados
│   │
│   ├── main.py                 # Execução padrão (3 páginas)
│   ├── max_main.py            # Execução completa (detecção automática)
│   └── generate_report.py     # Gerador de relatórios PDF
│
├── requirements.txt           # Dependências Python principais
├── requirements_analysis.txt  # Dependências para análise e relatórios
└── README.md                 # Documentação
```

## Instalação e Configuração

### Pré-requisitos
- **Python 3.7+** instalado
- **Google Chrome** atualizado
- **Conexão à internet** ativa

### Instalação
1. **Clonar** o projeto
2. **Navegar** para a pasta do projeto:
   ```bash
   cd JobScraper-Portugal
   ```
3. **Instalar dependências**:
   ```bash
   # Dependências principais (scraping)
   pip install -r requirements.txt
   
   # Dependências para análise e relatórios (opcional)
   pip install -r requirements_analysis.txt
   ```

##  Como Executar

### Scraping de Dados

**Teste Rápido (3 páginas)**:
```bash
cd src
python main.py
```
-  **Tempo**: ~3-5 minutos
-  **Output**: `data/jobs_itjobs.csv`

**Extração Completa (todas as páginas)**:
```bash
cd src
python max_main.py
```
-  **Tempo**: 30+ minutos (depende do número de páginas)
-  **Output**: `data/jobs_itjobs_max_{N}pages.csv`
-  **Funcionalidade**: Detecção automática do número de páginas

### Geração de Relatórios

```bash
cd src
python generate_report.py
```
-  **Output**: `relatorio_jobs_YYYYMMDD_HHMMSS.pdf`
-  **Conteúdo**: 4 páginas com análises estatísticas completas

## Arquitectura Técnica

### Fluxo de Dados
```
ITJobs.pt → Selenium → BeautifulSoup → JobScraper → JobParser → CSV → JobAnalyzer → PDF
```

### Componentes Principais

#### **JobScraper** (`core/scraper.py`)
- **Navegação**: Selenium WebDriver em modo headless
- **Extração**: BeautifulSoup com seletores CSS específicos
- **Inteligência**: 
  - 100+ padrões regex para tecnologias
  - 7 níveis de seniority
  - 15+ categorias profissionais
  - Detecção de modo de trabalho

#### **JobParser** (`core/parser.py`)
- **Padronização**: Converte chaves técnicas para rótulos legíveis
- **Robustez**: Tratamento de valores em falta com fallback "N/A"
- **Mapeamento**: Estrutura consistente para exportação CSV

#### **Utils** (`core/utils.py`)
- **Persistência**: Exportação CSV com encoding UTF-8
- **Flexibilidade**: Descoberta dinâmica de colunas
- **Automação**: Criação automática de diretórios

#### **JobAnalyzer** (`generate_report.py`)
- **Processamento**: Limpeza e estruturação de dados
- **Visualização**: Gráficos profissionais com matplotlib/seaborn
- **Relatório**: PDF multi-página com:
  - Resumo executivo
  - Distribuições por seniority/empresa/categoria
  - Análise geográfica
  - Ranking de tecnologias

##  Estratégias de Extração

### Detecção de Páginas (`max_main.py`)
1. **Análise de Paginação**: Busca elementos de navegação
2. **Informação de Resultados**: Extrai padrões "X de Y páginas"
3. **Teste Incremental**: Failsafe com visitação sequencial

### Extração Inteligente
- **Duas Passadas**: Listagens → Páginas individuais
- **Seletores Específicos**: Descobertos via análise automatizada
- **Padrões Regex**: Desenvolvidos com base em análise estatística

##  Solução de Problemas

| Problema | Causa Provável | Solução |
|----------|---------------|---------|
| `ModuleNotFoundError` | Dependências não instaladas | `pip install -r requirements.txt` |
| `ChromeDriver error` | Chrome desatualizado | Atualizar Google Chrome |
| `TimeoutException` | Conexão lenta | Verificar internet/aguardar |
| `No CSV found` | Execução sem scraping | Executar `main.py` primeiro |

##  Outputs Gerados

### Ficheiros CSV
- **Localização**: `src/data/`
- **Encoding**: UTF-8 (suporte completo a acentos)
- **Formato**: Headers em português, dados estruturados
- **Colunas**: 11 campos padronizados

### Relatórios PDF
- **Localização**: `src/`
- **Páginas**: 4 páginas estruturadas
- **Gráficos**: Visualizações coloridas e profissionais
- **Estatísticas**: Análises quantitativas e distribuições

---

*Desenvolvido para análise de mercado de trabalho em TI, pesquisa académica e relatórios executivos.*
