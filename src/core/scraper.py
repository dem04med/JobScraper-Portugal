import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

class JobScraper:
    def __init__(self, base_url="https://www.itjobs.pt/ofertas", max_pages=3):
        self.base_url = base_url
        self.max_pages = max_pages
        self.driver = None

    def extract_seniority(self, title, description=""):
        """
        Extrai o nível de seniority usando título e descrição.
        Retorna: "Senior", "Junior", "Lead", "Manager", "Mid-level", "N/A"
        """
        full_text = (title + " " + description).lower()
        
        # Padrões de seniority ordenados por prioridade (mais específicos primeiro)
        seniority_patterns = [
            # Director específico (deve vir antes de C-Level)
            ("Director", ["director of", "diretor de", "head of engineering", "head of technology"]),
            
            # C-Level e Executive
            ("C-Level", ["cto", "ceo", "cfo", "chief technology officer", "chief executive officer"]),
            
            # Management
            ("Manager", [
                "manager", "engineering manager", "project manager", "product manager",
                "scrum master", "coordenador", "coordinator"
            ]),
            
            # Lead positions
            ("Lead", [
                "lead developer", "lead engineer", "principal", "architect",
                "technical architect", "solution architect", "software architect",
                "tech lead", "technical lead", "team lead"  # Movido para cima
            ]),
            
            # Senior levels
            ("Senior", [
                "senior", "sénior", "sr.", "expert", "specialist",
                "5+ years", "mais de 5 anos", "+5 anos", "5 anos de experiência",
                "experiência superior a 5", "mínimo 5 anos"
            ]),
            
            # Junior levels
            ("Junior", [
                "junior", "júnior", "jr.", "trainee", "intern", "estagiário",
                "entry level", "graduate", "recém formado", "menos de 2 anos",
                "até 2 anos", "0-2 anos", "sem experiência"
            ]),
            
            # Mid-level
            ("Mid-level", [
                "mid-level", "médio", "pleno", "2-5 anos", "2 a 5 anos",
                "entre 2 e 5", "3+ years", "4+ years", "alguns anos de experiência"
            ])
        ]
        
        # Procura por padrões específicos
        for seniority_level, patterns in seniority_patterns:
            for pattern in patterns:
                if pattern in full_text:
                    return seniority_level
        
        # Análise de contexto adicional
        if description:
            desc_lower = description.lower()
            
            # Procura por indicadores de experiência
            experience_indicators = {
                "Senior": [
                    "experiência sólida", "vasta experiência", "ampla experiência",
                    "conhecimento avançado", "expertise", "mentoring", "liderar equipa"
                ],
                "Junior": [
                    "início de carreira", "primeira oportunidade", "desenvolver competências",
                    "aprender", "crescimento profissional", "orientação"
                ],
                "Manager": [
                    "gerir equipa", "gestão de pessoas", "liderança", "coordenar projeto",
                    "responsabilidades de gestão"
                ]
            }
            
            for level, indicators in experience_indicators.items():
                if any(indicator in desc_lower for indicator in indicators):
                    return level
        
        return "N/A"

    def extract_category(self, title, description="", technologies=""):
        """
        Extrai categoria profissional usando título, descrição e tecnologias.
        Retorna categoria mais específica possível.
        """
        full_text = (title + " " + description + " " + technologies).lower()
        
        # Categorias ordenadas por especificidade (mais específicas primeiro)
        category_patterns = [
            # QA específico (deve vir antes de DevOps para "automation")
            ("QA", [
                "qa", "quality assurance", "tester", "test automation",
                "qa engineer", "qa automation", "test engineer",
                "selenium", "testing", "qualidade", "controlo de qualidade"
            ]),
            
            # Desenvolvimento específico
            ("Frontend", [
                "frontend", "front-end", "front end", "ui developer", "interface",
                "react", "angular", "vue", "html", "css", "javascript frontend",
                "desenvolvimento web frontend", "cliente side"
            ]),
            
            ("Backend", [
                "backend", "back-end", "back end", "server side", "api development",
                "microservices", "web services", "rest api", "servidor",
                "desenvolvimento backend", "server"
            ]),
            
            ("Fullstack", [
                "fullstack", "full-stack", "full stack", "frontend e backend",
                "desenvolvimento completo", "end to end"
            ]),
            
            # Mobile
            ("Mobile", [
                "mobile", "android", "ios", "swift", "kotlin", "react native",
                "flutter", "xamarin", "desenvolvimento mobile", "app development"
            ]),
            
            # Data & Analytics
            ("Data Science", [
                "data scientist", "cientista de dados", "machine learning", "ai",
                "artificial intelligence", "deep learning", "analytics",
                "big data", "data mining"
            ]),
            
            ("Data Engineering", [
                "data engineer", "engenheiro de dados", "etl", "data pipeline",
                "data warehouse", "data lake", "spark", "hadoop"
            ]),
            
            ("Data Analytics", [
                "data analyst", "analista de dados", "business intelligence",
                "power bi", "tableau", "qlik", "reporting", "dashboards"
            ]),
            
            # DevOps & Infrastructure
            ("DevOps", [
                "devops", "dev ops", "site reliability", "sre", "platform engineer",
                "ci/cd", "continuous integration", "deployment", "automation"
            ]),
            
            ("Infrastructure", [
                "infrastructure", "infraestrutura", "system administrator",
                "network", "linux", "windows server", "system engineer"
            ]),
            
            # ERP/CRM (específico)
            ("ERP/CRM", [
                "sap", "sap consultant", "dynamics", "dynamics 365", "salesforce",
                "erp", "crm", "oracle", "peoplesoft", "workday"
            ]),
            
            # Cloud (específico)
            ("Cloud", [
                "cloud engineer", "cloud architect", "cloud developer",
                "aws engineer", "azure engineer", "gcp engineer",
                "cloud specialist", "cloud consultant"
            ]),
            
            # Security (específico)
            ("Security", [
                "security engineer", "cybersecurity", "information security",
                "security analyst", "security architect", "security specialist",
                "penetration testing", "ethical hacking", "segurança"
            ]),
            
            # Management & Leadership
            ("Technical Management", [
                "engineering manager", "tech lead", "technical lead",
                "head of engineering", "cto", "team lead"
            ]),
            
            ("Product Management", [
                "product manager", "product owner", "scrum master",
                "project manager", "agile coach"
            ]),
            
            # Business & Analysis
            ("Business Analysis", [
                "business analyst", "analista de negócio", "functional analyst",
                "requirements", "process analyst", "consultant"
            ]),
            
            # Design
            ("UX/UI Design", [
                "ux", "ui", "designer", "user experience", "user interface",
                "figma", "sketch", "adobe", "design"
            ]),
            
            # Specialized
            ("Security", [
                "security", "cybersecurity", "information security",
                "penetration testing", "ethical hacking", "segurança"
            ]),
            
            ("ERP/CRM", [
                "sap", "dynamics", "salesforce", "erp", "crm",
                "oracle", "peoplesoft", "workday"
            ]),
            
            # General categories (less specific)
            ("Software Development", [
                "developer", "programmer", "software engineer", "desenvolvedor",
                "programador", "engenheiro de software"
            ])
        ]
        
        # Procura por padrões específicos
        for category, patterns in category_patterns:
            for pattern in patterns:
                if pattern in full_text:
                    return category
        
        # Análise baseada em tecnologias se categoria ainda não foi encontrada
        if technologies and technologies != "N/A":
            tech_lower = technologies.lower()
            
            tech_categories = {
                "Frontend": ["react", "angular", "vue", "html", "css", "javascript"],
                "Backend": ["node.js", "python", "java", "spring", ".net", "php"],
                "Data Science": ["python", "r", "machine learning", "tensorflow"],
                "Mobile": ["swift", "kotlin", "react native", "flutter"],
                "Cloud": ["aws", "azure", "docker", "kubernetes"],
                "DevOps": ["jenkins", "git", "terraform", "ansible"]
            }
            
            for category, tech_patterns in tech_categories.items():
                if any(tech in tech_lower for tech in tech_patterns):
                    return category
        
        return "N/A"

    def extract_technologies(self, text):
        """
        Extrai tecnologias de um texto usando múltiplas estratégias.
        Retorna uma lista de tecnologias encontradas.
        """
        if not text:
            return []
        
        text_lower = text.lower()
        found_techs = set()  # Usar set para evitar duplicados
        
        # 1. Lista expandida de tecnologias com variações
        tech_patterns = {
            # Linguagens de programação
            "JavaScript": ["javascript", "js", "ecmascript"],
            "TypeScript": ["typescript", "ts"],
            "Python": ["python", "py"],
            "Java": [r"\bjava\b"],  # usar regex para evitar javascript
            "C#": ["c#", "csharp", "c sharp"],
            "C++": ["c++", "cpp", "c plus plus"],
            "PHP": ["php"],
            "Ruby": ["ruby"],
            "Go": [r"\bgo\b", "golang"],
            "Rust": ["rust"],
            "Swift": ["swift"],
            "Kotlin": ["kotlin"],
            "Scala": ["scala"],
            "R": [r"\br\b"],
            
            # Frameworks Frontend
            "React": ["react", "reactjs", "react.js"],
            "Angular": ["angular", "angularjs"],
            "Vue": ["vue", "vuejs", "vue.js"],
            "Svelte": ["svelte"],
            "Next.js": ["next.js", "nextjs", "next js"],
            "Nuxt.js": ["nuxt.js", "nuxtjs", "nuxt js"],
            
            # Frameworks Backend
            "Node.js": ["node.js", "nodejs", "node js"],
            ".NET": [".net", "dotnet", "asp.net", "net framework"],
            "Spring": ["spring boot", "spring framework", "spring"],
            "Django": ["django"],
            "Flask": ["flask"],
            "Laravel": ["laravel"],
            "Express": ["express.js", "expressjs", "express"],
            "FastAPI": ["fastapi", "fast api"],
            
            # Bases de dados
            "SQL": ["sql"],
            "MySQL": ["mysql"],
            "PostgreSQL": ["postgresql", "postgres"],
            "MongoDB": ["mongodb", "mongo"],
            "Redis": ["redis"],
            "Oracle": ["oracle db", "oracle database", "oracle"],
            "SQL Server": ["sql server", "sqlserver"],
            "SQLite": ["sqlite"],
            "Elasticsearch": ["elasticsearch", "elastic search"],
            
            # Cloud & DevOps
            "AWS": ["aws", "amazon web services"],
            "Azure": ["azure", "microsoft azure"],
            "Google Cloud": ["google cloud", "gcp", "google cloud platform"],
            "Docker": ["docker"],
            "Kubernetes": ["kubernetes", "k8s"],
            "Jenkins": ["jenkins"],
            "GitLab": ["gitlab", "gitlab ci"],
            "GitHub": ["github", "github actions"],
            "Terraform": ["terraform"],
            "Ansible": ["ansible"],
            "Puppet": ["puppet"],
            "Chef": ["chef"],
            
            # Ferramentas & Outras
            "Git": ["git"],
            "SVN": ["svn", "subversion"],
            "JIRA": ["jira"],
            "Confluence": ["confluence"],
            "Figma": ["figma"],
            "Adobe": ["adobe", "photoshop", "illustrator"],
            
            # Business & Microsoft
            "Power Platform": ["power platform"],
            "Power Apps": ["power apps", "powerapps"],
            "Power Automate": ["power automate", "power flow"],
            "Power BI": ["power bi", "powerbi"],
            "Dynamics 365": ["dynamics 365", "dynamics365"],
            "SharePoint": ["sharepoint"],
            "Office 365": ["office 365", "o365"],
            
            # Metodologias (também interessantes)
            "Agile": ["agile", "scrum", "kanban"],
            "DevOps": ["devops", "dev ops"],
            "Microservices": ["microservices", "micro services"],
            "API REST": ["rest api", "restful", "rest"],
            "GraphQL": ["graphql", "graph ql"],
            "Blockchain": ["blockchain", "web3"],
            "Machine Learning": ["machine learning", "ml", "ai", "artificial intelligence"],
            "Data Science": ["data science", "data analytics"],
        }
        
        # 2. Procurar por cada tecnologia e suas variações
        for tech_name, patterns in tech_patterns.items():
            for pattern in patterns:
                if pattern.startswith(r"\b") and pattern.endswith(r"\b"):
                    # Usar regex para padrões com word boundaries
                    if re.search(pattern, text_lower):
                        found_techs.add(tech_name)
                        break
                else:
                    # Procura simples por substring
                    if pattern in text_lower:
                        found_techs.add(tech_name)
                        break
        
        # 3. Procurar por padrões específicos de versões
        version_patterns = [
            (r"python\s*[23]\.\d+", "Python"),
            (r"java\s*\d+", "Java"),
            (r"php\s*[5-8]\.\d+", "PHP"),
            (r"angular\s*\d+", "Angular"),
            (r"vue\s*[23]", "Vue"),
            (r"react\s*\d+", "React"),
        ]
        
        for pattern, tech_name in version_patterns:
            if re.search(pattern, text_lower):
                found_techs.add(tech_name)
        
        # 4. Converter para lista ordenada
        return sorted(list(found_techs))

    def extract_work_mode(self, text, description=""):
        """
        Extrai modo(s) de trabalho, suportando múltiplos modos.
        Retorna string com modos separados por vírgula ou modo único.
        """
        if not text:
            text = ""
        
        full_text = (text + " " + description).lower()
        found_modes = set()
        
        # Padrões de deteção mais específicos para evitar falsos positivos
        work_mode_patterns = [
            # Remoto (mais específico primeiro)
            ("Remoto", [
                "100% remoto", "totalmente remoto", "completamente remoto",
                "trabalho remoto", "permite trabalho remoto", "full remote",
                "trabalhar remotamente", "home office", "à distância"
            ]),
            # Híbrido (padrões específicos)
            ("Híbrido", [
                "híbrido", "hibrido", "modalidade híbrida", "trabalho híbrido",
                "parcialmente remoto", "alguns dias remoto", "dias no escritório",
                "flexível", "flexible working", "misto"
            ]),
            # Presencial (específico)
            ("Presencial", [
                "100% presencial", "totalmente presencial", "no escritório",
                "presencial", "on-site", "no local"
            ]),
            # Palavras genéricas de remoto (só se não encontrou híbrido específico)
            ("Remoto_Generic", [
                "remoto", "remote"
            ])
        ]
        
        # Primeira passagem - procurar padrões específicos
        for mode_name, patterns in work_mode_patterns:
            if mode_name == "Remoto_Generic":
                continue  # Skip na primeira passagem
            
            for pattern in patterns:
                if pattern in full_text:
                    # Para híbrido, verifica se não há contradição
                    if mode_name == "Híbrido":
                        # Se já tem "100% remoto", não adiciona híbrido
                        if any(p in full_text for p in ["100% remoto", "totalmente remoto"]):
                            continue
                    found_modes.add(mode_name)
                    break
        
        # Segunda passagem - só se não encontrou modos específicos
        if not found_modes:
            for pattern in work_mode_patterns[3][1]:  # Remoto_Generic
                if pattern in full_text:
                    found_modes.add("Remoto")
                    break
        
        # Se mencionou múltiplas modalidades explicitamente
        explicit_multi = [
            "remoto e presencial", "presencial e remoto",
            "híbrido e remoto", "remoto e híbrido"
        ]
        
        for multi_pattern in explicit_multi:
            if multi_pattern in full_text:
                if "remoto" in multi_pattern and "presencial" in multi_pattern:
                    found_modes.update(["Remoto", "Presencial"])
                elif "híbrido" in multi_pattern and "remoto" in multi_pattern:
                    found_modes.update(["Híbrido", "Remoto"])
                break
        
        # Se não encontrou nenhum modo específico, assume presencial
        if not found_modes:
            return "Presencial"
        
        # Remove conflitos: se tem híbrido, remove presencial genérico
        if "Híbrido" in found_modes and "Presencial" in found_modes:
            # Só mantém presencial se foi explicitamente mencionado
            if not any(p in full_text for p in ["no escritório", "presencial", "on-site"]):
                found_modes.discard("Presencial")
        
        # Ordena por prioridade
        mode_priority = ["Remoto", "Híbrido", "Presencial"]
        sorted_modes = sorted(found_modes, key=lambda x: mode_priority.index(x) if x in mode_priority else 999)
        
        # Retorna modos separados por vírgula se múltiplos
        return ", ".join(sorted_modes)

    def init_driver(self):
        """Inicializa o Chrome em modo headless."""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=options)

    def get_job_pages(self, num_pages=3):
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
        Extrai dados completos das ofertas visitando páginas individuais para máxima precisão.
        """
        all_offers = []

        # Inicializa o driver para visitar páginas individuais
        self.init_driver()

        for page_html in pages_html:
            soup = BeautifulSoup(page_html, "html.parser")
            offers = soup.select("ul.listing > li")

            for offer in offers:
                # Título e link
                title_tag = offer.select_one(".list-title a.title")
                title = title_tag.get_text(strip=True) if title_tag else "N/A"
                link = "N/A"
                if title_tag and title_tag.get("href"):
                    href = title_tag["href"]
                    if href.startswith("/oferta/"):
                        link = "https://www.itjobs.pt" + href
                    elif href.startswith("http"):
                        link = href

                # Empresa
                company_tag = offer.select_one(".list-name a")
                company = company_tag.get_text(strip=True) if company_tag else "N/A"

                # Localização e outros detalhes da lista
                location = "N/A"
                contract_type = "N/A"
                mode = "N/A"
                
                details_tag = offer.select_one(".list-details")
                if details_tag:
                    details_text = details_tag.get_text(" ", strip=True)
                    
                    # Extrair localização (primeiro conjunto de cidades antes de outros detalhes)
                    # As cidades aparecem no início: "Lisboa, Porto Full-time Remoto"
                    cities = ["Lisboa", "Porto", "Coimbra", "Braga", "Aveiro", "Faro", "Viseu", "Setúbal"]
                    found_cities = []
                    
                    # Procura por cidades no texto
                    for city in cities:
                        if city in details_text:
                            found_cities.append(city)
                    
                    if found_cities:
                        location = ", ".join(found_cities)
                    
                    # Extrair tipo de contrato
                    if "Full-time" in details_text:
                        contract_type = "Full-time"
                    elif "Part-time" in details_text:
                        contract_type = "Part-time"
                    elif "Freelance" in details_text:
                        contract_type = "Freelance"
                    
                    # Extrair modo de trabalho (suporte para múltiplos modos)
                    mode = self.extract_work_mode(details_text)

                # Inicializa campos que serão preenchidos na página individual
                description = "N/A"
                pub_date = "N/A"
                seniority = "N/A"
                category = "N/A"
                technologies = "N/A"

                # Visita a página individual para obter detalhes completos
                if link != "N/A":
                    try:
                        print(f"     Analisando: {title[:50]}...")
                        self.driver.get(link)
                        time.sleep(2)
                        job_soup = BeautifulSoup(self.driver.page_source, "html.parser")

                        # Data de publicação (na classe over-title)
                        date_tag = job_soup.select_one(".over-title small")
                        if date_tag:
                            pub_date = date_tag.get_text(strip=True)

                        # Tipo de contrato (melhorado - procura por "Contrato" na lista de detalhes)
                        contract_items = job_soup.select(".item-details .list-inline li")
                        for item in contract_items:
                            title_span = item.select_one(".title")
                            field_span = item.select_one(".field")
                            if title_span and field_span and "contrato" in title_span.get_text(strip=True).lower():
                                contract_type = field_span.get_text(strip=True)
                                break

                        # Remoto/Modo de trabalho (melhorado - procura na lista de detalhes + descrição)
                        remote_details = []
                        for item in contract_items:
                            title_span = item.select_one(".title")
                            field_span = item.select_one(".field")
                            if title_span and field_span and "remoto" in title_span.get_text(strip=True).lower():
                                remote_details.append(field_span.get_text(strip=True))
                        
                        # Extrair modo de trabalho considerando detalhes + descrição
                        remote_text = " ".join(remote_details)
                        mode = self.extract_work_mode(remote_text, description)

                        # Descrição (da classe content-block)
                        desc_tag = job_soup.select_one(".content-block")
                        if desc_tag:
                            # Remove scripts e outros elementos desnecessários
                            for script in desc_tag(["script", "style"]):
                                script.decompose()
                            description = desc_tag.get_text(" ", strip=True)
                            # Limita o tamanho da descrição
                            if len(description) > 800:
                                description = description[:800] + "..."

                        # Tecnologias extraídas da descrição e título (se ainda não foram encontradas ou para melhorar)
                        full_text = title + " " + description
                        found_techs_complete = self.extract_technologies(full_text)
                        
                        if found_techs_complete:
                            technologies = ", ".join(found_techs_complete)

                        # Melhora seniority e categoria com dados completos
                        seniority = self.extract_seniority(title, description)
                        category = self.extract_category(title, description, technologies)

                        # Modo de trabalho já foi extraído acima com detecção melhorada

                    except Exception as e:
                        print(f"   ⚠️ Erro ao processar {link}: {e}")

                all_offers.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "contract_type": contract_type,
                    "seniority": seniority,
                    "technologies": technologies,
                    "description": description,
                    "link": link,
                    "pub_date": pub_date,
                    "mode": mode,
                    "category": category
                })

        # Fecha o driver
        if self.driver:
            self.driver.quit()

        print(f"Foram extraídas {len(all_offers)} ofertas completas.")
        return all_offers