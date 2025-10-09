from scraper import JobScraper
from parser import JobParser
from utils import save_to_csv

def main():
    print("🚀 Iniciando o JobScraper-Portugal...")

    # Inicializa o scraper
    scraper = JobScraper(base_url="https://www.itjobs.pt/ofertas")

    # Faz o download do HTML das páginas de ofertas
    pages = scraper.get_job_pages(num_pages=3)  # número inicial de páginas a recolher

    # Extrai dados brutos das ofertas
    raw_jobs = scraper.extract_raw_jobs(pages)

    # Analisa e organiza os dados
    parser = JobParser()
    parsed_jobs = parser.parse_jobs(raw_jobs)

    # Guarda num CSV
    save_to_csv(parsed_jobs, "data/jobs_itjobs.csv")

    print("✅ Concluído! Dados guardados em 'data/jobs_itjobs.csv'")

if __name__ == "__main__":
    main()
