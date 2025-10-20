from core import JobScraper, JobParser, save_to_csv
import re
from bs4 import BeautifulSoup

def detect_max_pages(scraper):
    
    print("A detectar número máximo de páginas...")
    
    try:
        scraper.init_driver()
        
        # Vai para a primeira página
        scraper.driver.get(scraper.base_url + "?page=1")
        
        # Parse do HTML
        soup = BeautifulSoup(scraper.driver.page_source, "html.parser")
        
        max_pages = 1
        
        # Estratégia 1: Procurar por paginação
        pagination_selectors = [
            ".pagination a",           # Links de paginação comuns
            ".page-link",             # Bootstrap pagination
            ".pagination-list a",     # Outro padrão comum
            "a[href*='page=']"        # Qualquer link com page=
        ]
        
        for selector in pagination_selectors:
            page_links = soup.select(selector)
            if page_links:
                print(f"Encontrados {len(page_links)} links de paginação com seletor: {selector}")
                
                # Extrai números de página dos links
                page_numbers = []
                for link in page_links:
                    href = link.get('href', '')
                    text = link.get_text(strip=True)
                    
                    # Procura por page= no href
                    page_match = re.search(r'page=(\d+)', href)
                    if page_match:
                        page_numbers.append(int(page_match.group(1)))
                    
                    # Procura por número no texto do link
                    if text.isdigit():
                        page_numbers.append(int(text))
                
                if page_numbers:
                    max_from_links = max(page_numbers)
                    max_pages = max(max_pages, max_from_links)
                    print(f"    Maior número de página encontrado nos links: {max_from_links}")
                break
        
        # Estratégia 2: Procurar por informação de resultados
        result_info_selectors = [
            ".results-info",
            ".search-results-info", 
            ".pagination-info",
            ".total-results"
        ]
        
        for selector in result_info_selectors:
            info_element = soup.select_one(selector)
            if info_element:
                info_text = info_element.get_text()
                print(f"Informação de resultados: {info_text}")
                
                # Procura por padrões como "Página 1 de 15" ou "1-20 de 300 resultados"
                page_pattern = re.search(r'(\d+)\s*de\s*(\d+)', info_text)
                if page_pattern:
                    total_pages = int(page_pattern.group(2))
                    max_pages = max(max_pages, total_pages)
                    print(f"Páginas totais encontradas na informação: {total_pages}")
                break
        
        # Estratégia 3: Testar páginas incrementalmente
        if max_pages <= 3: 
            print("A testar páginas incrementalmente...")
            test_page = 2
            
            while True:  # Sem limite - testa até não encontrar mais páginas
                test_url = f"{scraper.base_url}?page={test_page}"
                scraper.driver.get(test_url)
                
                test_soup = BeautifulSoup(scraper.driver.page_source, "html.parser")
                
                # Verifica se há ofertas na página
                job_selectors = [
                    ".job-item",
                    ".offer-item", 
                    ".job-listing",
                    "article",
                    ".search-result"
                ]
                
                has_jobs = False
                for job_selector in job_selectors:
                    if test_soup.select(job_selector):
                        has_jobs = True
                        break
                
                if not has_jobs:
                    # Se não há ofertas, a página anterior era a última
                    max_pages = test_page - 1
                    print(f"Página {test_page} está vazia. Total de páginas: {max_pages}")
                    break
                
                test_page += 1
                
                # Mostra progresso a cada 10 páginas
                if test_page % 10 == 0:
                    print(f"Testada página {test_page-1}... continuando")
                
                # Segurança extrema - parar se chegar a 1000 páginas (improvável)
                if test_page > 1000:
                    max_pages = 1000
                    print(f"Limite extremo de segurança atingido: {max_pages} páginas")
                    break
        
        scraper.driver.quit()
        
        print(f"Detecção concluída! Total de páginas encontradas: {max_pages}")
        return max_pages
        
    except Exception as e:
        print(f"Erro na detecção de páginas: {e}")
        if scraper.driver:
            scraper.driver.quit()
        return 10

def main():
    print("Iniciando o JobScraper-Portugal...")

    # Inicializa o scraper
    scraper = JobScraper(base_url="https://www.itjobs.pt/ofertas")

    # Detecta automaticamente o número máximo de páginas
    max_pages = detect_max_pages(scraper)
    
    print(f"\nA processar {max_pages} páginas...")
    
    # Faz o download do HTML das páginas de ofertas
    pages = scraper.get_job_pages(num_pages=max_pages)

    # Extrai dados completos visitando páginas individuais para melhor precisão
    print("Modo completo ativado - visitando páginas individuais para melhor precisão...")
    if max_pages > 50:
        print("AVISO: Com muitas páginas, este processo pode demorar várias horas!")
    
    raw_jobs = scraper.extract_raw_jobs(pages)

    # Analisa e organiza os dados
    parser = JobParser()
    parsed_jobs = parser.parse_jobs(raw_jobs)

    # Guarda num CSV com nome que inclui o número de páginas
    filename = f"data/jobs_itjobs_max_{max_pages}pages.csv"
    save_to_csv(parsed_jobs, filename)

    print("Concluído! Dados guardados em '{}'".format(filename))
    print(f"Estatísticas:")
    print(f"   • {max_pages} páginas processadas")
    print(f"   • {len(parsed_jobs)} ofertas extraídas")
    print(f"   • Média de {len(parsed_jobs)/max_pages:.1f} ofertas por página")
    
    # Estatísticas detalhadas
    fields_with_data = {}
    for field in ["Título", "Empresa", "Localização", "Tipo de contrato", "Seniority", "Tecnologias", "Modo de trabalho", "Categoria", "Data de publicação", "Descrição"]:
        count = sum(1 for job in parsed_jobs if job.get(field, "N/A") != "N/A")
        fields_with_data[field] = count
        percentage = count/len(parsed_jobs)*100 if len(parsed_jobs) > 0 else 0
        print(f"   • {field}: {count}/{len(parsed_jobs)} ({percentage:.1f}%)")

if __name__ == "__main__":
    main()