class JobParser:
    def parse_jobs(self, raw_jobs):
        """
        Organiza os dados extraídos pelo scraper e garante consistência
        nas chaves para o CSV final.
        """
        parsed = []

        for job in raw_jobs:
            try:
                parsed.append({
                    "Título": job.get("title", "N/A"),
                    "Empresa": job.get("company", "N/A"),
                    "Localização": job.get("location", "N/A"),
                    "Tipo de contrato": job.get("contract_type", "N/A"),
                    "Seniority": job.get("seniority", "N/A"),
                    "Tecnologias": job.get("technologies", "N/A"),
                    "Descrição": job.get("description", "N/A"),
                    "Link": job.get("link", "N/A"),
                    "Data de publicação": job.get("pub_date", "N/A"),
                    "Modo de trabalho": job.get("mode", "N/A"),
                    "Categoria": job.get("category", "N/A")
                })
            except Exception as e:
                print(f"Erro ao analisar oferta: {e}")

        return parsed
