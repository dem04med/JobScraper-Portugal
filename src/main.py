from core import JobScraper, JobParser, save_to_csv

def main():
    print("Iniciando o JobScraper-Portugal...")

    # Inicializa o scraper
    scraper = JobScraper(base_url="https://www.itjobs.pt/ofertas")

    # Faz o download do HTML das páginas de ofertas
    pages = scraper.get_job_pages(num_pages=3)

    # Extrai dados completos visitando páginas individuais para melhor precisão
    print("Modo completo ativado - visitando páginas individuais para melhor precisão...")
    raw_jobs = scraper.extract_raw_jobs(pages)

    # Analisa e organiza os dados
    parser = JobParser()
    parsed_jobs = parser.parse_jobs(raw_jobs)

    # Guarda num CSV
    save_to_csv(parsed_jobs, "data/jobs_itjobs.csv")

    print(f"   • {len(parsed_jobs)} ofertas extraídas")
    
    # Estatísticas detalhadas
    fields_with_data = {}
    for field in ["Título", "Empresa", "Localização", "Tipo de contrato", "Seniority", "Tecnologias", "Modo de trabalho", "Categoria", "Data de publicação", "Descrição"]:
        count = sum(1 for job in parsed_jobs if job.get(field, "N/A") != "N/A")
        fields_with_data[field] = count
        percentage = count/len(parsed_jobs)*100
        print(f"   • {field}: {count}/{len(parsed_jobs)} ({percentage:.1f}%)")
    
if __name__ == "__main__":
    main()
