class JobParser:
    def parse_jobs(self, raw_jobs):
        parsed = []
        for job in raw_jobs:
            try:
                link = job.get("link", "N/A")
                
                if link != "N/A":
                    if link.startswith("/oferta/"):
                        link = "https://www.itjobs.pt" + link
                    elif link.startswith("//"):
                        link = "https:" + link
                    elif not link.startswith("http"):
                        link = "N/A"

                parsed.append({
                    "Título": job.get("title", "N/A"),
                    "Empresa": job.get("company", "N/A"),
                    "Localização": job.get("location", "N/A"),
                    "Link": link,
                    "Salário": job.get("salary", "N/A")
                })
            except Exception as e:
                print(f"⚠️ Erro ao analisar oferta: {e}")
        return parsed
