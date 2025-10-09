from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

class JobScraper:
    def __init__(self, base_url="https://www.itjobs.pt/ofertas", max_pages=3):
        self.base_url = base_url
        self.max_pages = max_pages
        self.driver = None

    def init_driver(self):
        """Inicializa o Chrome em modo headless."""
        options = Options()
        options.add_argument("--headless") 
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=options)

    def get_job_pages(self, num_pages=3):
        """
        Percorre várias páginas de ofertas e recolhe o HTML de cada uma.
        Retorna uma lista com o conteúdo de todas as páginas.
        """
        self.init_driver()
        pages_html = []

        for page in range(1, num_pages + 1):
            url = f"{self.base_url}?page={page}"
            print(f"📄 A carregar página {page}: {url}")
            self.driver.get(url)
            time.sleep(3)  
            pages_html.append(self.driver.page_source)

        self.driver.quit()
        return pages_html

    def extract_raw_jobs(self, pages_html):
        """
        Extrai dados brutos (não processados) das páginas obtidas.
        Retorna uma lista de dicionários com os campos base.
        """
        all_offers = []

        for page_html in pages_html:
            soup = BeautifulSoup(page_html, "html.parser")
            offers = soup.select("ul.listing > li")

            for offer in offers:
                # Extrai título e link
                title_tag = offer.select_one(".list-title a.title")
                title = title_tag.get_text(strip=True) if title_tag else "N/A"

                # Corrige link para sempre ser completo
                link = "N/A"
                if title_tag and title_tag.get("href"):
                    href = title_tag["href"]
                    if href.startswith("/oferta/"):
                        link = "https://www.itjobs.pt" + href
                    elif href.startswith("http"):
                        link = href

                # Extrai empresa
                company_tag = offer.select_one(".list-name a")
                company = company_tag.get_text(strip=True) if company_tag else "N/A"

                # Extrai localização e salário
                location = "N/A"
                salary = "N/A"
                details_tag = offer.select_one(".list-details")
                if details_tag:
                    details_text = details_tag.get_text(" ", strip=True)
                    # Salário
                    if "€" in details_text:
                        salary = details_text.split("€")[-1].strip()
                    # Localização
                    for city in ["Lisboa", "Porto", "Coimbra", "Braga", "Aveiro", "Remoto", "Remote"]:
                        if city.lower() in details_text.lower():
                            location = city
                            break

                all_offers.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "salary": salary,
                    "link": link
                })

        print(f"🔍 Foram extraídas {len(all_offers)} ofertas brutas.")
        return all_offers
