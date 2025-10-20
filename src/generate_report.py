import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from datetime import datetime
import os
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Configuração para suporte de caracteres portugueses
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial', 'sans-serif']
sns.set_palette("husl")

class JobAnalyzer:

    def __init__(self, csv_file):
        """Inicializa o analisador com o ficheiro CSV"""
        self.csv_file = csv_file
        self.df = None
        self.report_name = f"relatorio_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
    def load_data(self):
        """Carrega e prepara os dados do CSV"""
        print("A carregar dados do CSV...")
        try:
            self.df = pd.read_csv(self.csv_file)
            print(f"Dados carregados: {len(self.df)} ofertas de emprego")
            return True
        except Exception as e:
            print(f"Erro ao carregar CSV: {e}")
            return False
    
    def preprocess_data(self):
        """Pré-processa os dados para análise"""
        print("A processar dados...")
        
        # Remove valores N/A e limpa dados
        self.df = self.df.replace('N/A', pd.NA)
        
        # Processa tecnologias (separa por vírgula)
        self.df['Tecnologias_Lista'] = self.df['Tecnologias'].apply(
            lambda x: [tech.strip() for tech in str(x).split(',') if tech.strip() != 'nan'] if pd.notna(x) else []
        )
        
        # Processa localização (primeira cidade mencionada)
        self.df['Cidade_Principal'] = self.df['Localização'].apply(
            lambda x: str(x).split(',')[0].strip() if pd.notna(x) else 'Não especificado'
        )
        
        modo_col = None
        if 'Modo de trabalho' in self.df.columns:
            modo_col = 'Modo de trabalho'
        elif 'Modo' in self.df.columns:
            modo_col = 'Modo'
        
        if modo_col:
            self.df['Modo_Principal'] = self.df[modo_col].apply(
                lambda x: str(x).split(',')[0].strip() if pd.notna(x) else 'Não especificado'
            )
        else:
            self.df['Modo_Principal'] = 'Não especificado'
            print("Coluna 'Modo' não encontrada - usando valor padrão")
        
        print("Dados processados com sucesso")
    
    def create_overview_stats(self, pdf):
        """Cria página de estatísticas gerais"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Visão Geral das Ofertas de Emprego', fontsize=20, fontweight='bold')
        
        # 1. Distribuição por Seniority
        seniority_counts = self.df['Seniority'].value_counts()
        ax1.pie(seniority_counts.values, labels=seniority_counts.index, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Distribuição por Nível de Seniority', fontweight='bold')
        
        # 2. Top 10 Empresas
        top_companies = self.df['Empresa'].value_counts().head(10)
        ax2.barh(top_companies.index[::-1], top_companies.values[::-1], color='skyblue')
        ax2.set_title('Top 10 Empresas com Mais Ofertas', fontweight='bold')
        ax2.set_xlabel('Número de Ofertas')
        
        # 3. Distribuição por Categoria
        category_counts = self.df['Categoria'].value_counts()
        ax3.bar(range(len(category_counts)), category_counts.values, color='lightcoral')
        ax3.set_title('Distribuição por Categoria Profissional', fontweight='bold')
        ax3.set_xticks(range(len(category_counts)))
        ax3.set_xticklabels(category_counts.index, rotation=45, ha='right')
        ax3.set_ylabel('Número de Ofertas')
        
        # 4. Modo de Trabalho
        mode_counts = self.df['Modo_Principal'].value_counts()
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
        ax4.pie(mode_counts.values, labels=mode_counts.index, autopct='%1.1f%%', 
                startangle=90, colors=colors[:len(mode_counts)])
        ax4.set_title('Modo de Trabalho', fontweight='bold')
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def create_location_analysis(self, pdf):
        """Análise por localização"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('  Análise por Localização', fontsize=20, fontweight='bold')
        
        # 1. Top 15 Cidades
        top_cities = self.df['Cidade_Principal'].value_counts().head(15)
        ax1.barh(top_cities.index[::-1], top_cities.values[::-1], color='lightgreen')
        ax1.set_title('Top 15 Cidades com Mais Ofertas', fontweight='bold')
        ax1.set_xlabel('Número de Ofertas')
        
        # 2. Distribuição Lisboa vs Porto vs Outras
        lisboa_count = self.df[self.df['Cidade_Principal'].str.contains('Lisboa', case=False, na=False)].shape[0]
        porto_count = self.df[self.df['Cidade_Principal'].str.contains('Porto', case=False, na=False)].shape[0]
        outras_count = len(self.df) - lisboa_count - porto_count
        
        ax2.pie([lisboa_count, porto_count, outras_count], 
                labels=['Lisboa', 'Porto', 'Outras'], 
                autopct='%1.1f%%', startangle=90)
        ax2.set_title('Lisboa vs Porto vs Outras Cidades', fontweight='bold')
        
        # 3. Modo de trabalho por cidade (top 10 cidades)
        top_10_cities = self.df['Cidade_Principal'].value_counts().head(10).index
        city_mode_data = []
        for city in top_10_cities:
            city_data = self.df[self.df['Cidade_Principal'] == city]
            remote_pct = (city_data['Modo_Principal'] == 'Remoto').sum() / len(city_data) * 100
            city_mode_data.append((city, remote_pct))
        
        cities, remote_percentages = zip(*city_mode_data)
        ax3.bar(range(len(cities)), remote_percentages, color='orange')
        ax3.set_title('% de Trabalho Remoto por Cidade (Top 10)', fontweight='bold')
        ax3.set_xticks(range(len(cities)))
        ax3.set_xticklabels(cities, rotation=45, ha='right')
        ax3.set_ylabel('% Trabalho Remoto')
        
        # 4. Heatmap de categorias por cidade (top 5 cidades e categorias)
        top_5_cities = self.df['Cidade_Principal'].value_counts().head(5).index
        top_5_categories = self.df['Categoria'].value_counts().head(5).index
        
        heatmap_data = []
        for city in top_5_cities:
            city_row = []
            for category in top_5_categories:
                count = len(self.df[(self.df['Cidade_Principal'] == city) & 
                                  (self.df['Categoria'] == category)])
                city_row.append(count)
            heatmap_data.append(city_row)
        
        sns.heatmap(heatmap_data, annot=True, fmt='d', 
                   xticklabels=[cat[:15] + '...' if len(cat) > 15 else cat for cat in top_5_categories],
                   yticklabels=top_5_cities, ax=ax4, cmap='YlOrRd')
        ax4.set_title('Ofertas por Cidade vs Categoria', fontweight='bold')
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def create_technology_analysis(self, pdf):
        """Análise de tecnologias"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('   Análise de Tecnologias', fontsize=20, fontweight='bold')
        
        # Extrai todas as tecnologias
        all_technologies = []
        for tech_list in self.df['Tecnologias_Lista']:
            all_technologies.extend(tech_list)
        
        tech_counter = Counter(all_technologies)
        
        # 1. Top 20 Tecnologias Mais Procuradas
        top_20_techs = dict(tech_counter.most_common(20))
        ax1.barh(list(top_20_techs.keys())[::-1], list(top_20_techs.values())[::-1], color='mediumpurple')
        ax1.set_title('Top 20 Tecnologias Mais Procuradas', fontweight='bold')
        ax1.set_xlabel('Número de Ofertas')
        
        # 2. Linguagens de Programação vs Frameworks vs Ferramentas
        programming_langs = ['Python', 'JavaScript', 'Java', 'C#', 'PHP', 'TypeScript', 'Go', 'Ruby', 'Swift', 'Kotlin']
        frameworks = ['React', 'Angular', 'Vue', 'Django', 'Flask', 'Spring', 'Laravel', '.NET', 'Node.js']
        tools = ['Docker', 'Kubernetes', 'Git', 'Jenkins', 'AWS', 'Azure', 'Google Cloud']
        
        lang_count = sum(tech_counter[lang] for lang in programming_langs if lang in tech_counter)
        framework_count = sum(tech_counter[fw] for fw in frameworks if fw in tech_counter)
        tools_count = sum(tech_counter[tool] for tool in tools if tool in tech_counter)
        
        ax2.pie([lang_count, framework_count, tools_count], 
                labels=['Linguagens', 'Frameworks', 'Ferramentas'],
                autopct='%1.1f%%', startangle=90)
        ax2.set_title('Distribuição: Linguagens vs Frameworks vs Ferramentas', fontweight='bold')
        
        # 3. Tecnologias por Seniority Level
        seniority_levels = ['Junior', 'Mid-level', 'Senior', 'Lead']
        tech_by_seniority = {level: [] for level in seniority_levels}
        
        for level in seniority_levels:
            level_data = self.df[self.df['Seniority'] == level]
            level_techs = []
            for tech_list in level_data['Tecnologias_Lista']:
                level_techs.extend(tech_list)
            tech_by_seniority[level] = len(set(level_techs))  # Tecnologias únicas
        
        ax3.bar(tech_by_seniority.keys(), tech_by_seniority.values(), color='lightblue')
        ax3.set_title('Diversidade de Tecnologias por Nível', fontweight='bold')
        ax3.set_ylabel('Número de Tecnologias Únicas')
        
        # 4. Cloud Technologies
        cloud_techs = ['AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'Terraform']
        cloud_counts = [tech_counter.get(tech, 0) for tech in cloud_techs]
        
        ax4.bar(cloud_techs, cloud_counts, color='lightcyan')
        ax4.set_title('Tecnologias Cloud/DevOps', fontweight='bold')
        ax4.set_ylabel('Número de Ofertas')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def create_summary_statistics(self, pdf):
        """Página de estatísticas resumo"""
        fig, ax = plt.subplots(figsize=(16, 12))
        ax.axis('off')
        
        # Estatísticas gerais
        total_jobs = len(self.df)
        unique_companies = self.df['Empresa'].nunique()
        unique_cities = self.df['Cidade_Principal'].nunique()
        
        # Tecnologias
        all_techs = []
        for tech_list in self.df['Tecnologias_Lista']:
            all_techs.extend(tech_list)
        unique_technologies = len(set(all_techs))
        
        # Percentagens
        remote_pct = (self.df['Modo_Principal'] == 'Remoto').sum() / total_jobs * 100
        senior_pct = (self.df['Seniority'] == 'Senior').sum() / total_jobs * 100
        
        # Cria texto do resumo
        summary_text = f"""
   RELATÓRIO ESTATÍSTICO - OFERTAS DE EMPREGO IT EM PORTUGAL
═══════════════════════════════════════════════════════════════

   ESTATÍSTICAS GERAIS
────────────────────────────
• Total de Ofertas Analisadas: {total_jobs:,}
• Empresas Únicas: {unique_companies:,}
• Cidades/Localizações: {unique_cities:,}
• Tecnologias Identificadas: {unique_technologies:,}

   TOP 5 EMPRESAS
────────────────────────────
"""
        
        # Add top 5 companies
        top_companies = self.df['Empresa'].value_counts().head(5)
        for i, (company, count) in enumerate(top_companies.items(), 1):
            summary_text += f"  {i}. {company}: {count} ofertas\n"
        
        summary_text += f"""
   TOP 5 CIDADES
────────────────────────────
"""
        
        # Add top 5 cities
        top_cities = self.df['Cidade_Principal'].value_counts().head(5)
        for i, (city, count) in enumerate(top_cities.items(), 1):
            summary_text += f"  {i}. {city}: {count} ofertas\n"
        
        summary_text += f"""
   TOP 10 TECNOLOGIAS
────────────────────────────
"""
        
        # Add top 10 technologies
        all_technologies = []
        for tech_list in self.df['Tecnologias_Lista']:
            all_technologies.extend(tech_list)
        tech_counter = Counter(all_technologies)
        
        for i, (tech, count) in enumerate(tech_counter.most_common(10), 1):
            summary_text += f"  {i}. {tech}: {count} ofertas\n"
        
        # Adiciona o texto à página
        ax.text(0.05, 0.95, summary_text, transform=ax.transAxes, fontsize=12,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=1", facecolor="lightgray", alpha=0.8))
        
        plt.title('RESUMO EXECUTIVO', fontsize=24, fontweight='bold', pad=20)
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def generate_report(self):
        """Gera o relatório PDF completo"""
        if not self.load_data():
            return False
        
        self.preprocess_data()
        
        print(f"   A gerar relatório PDF: {self.report_name}")
        
        with PdfPages(self.report_name) as pdf:
            # Página 1: Resumo Executivo
            self.create_summary_statistics(pdf)
            
            # Página 2: Visão Geral
            self.create_overview_stats(pdf)
            
            # Página 3: Análise por Localização
            self.create_location_analysis(pdf)
            
            # Página 4: Análise de Tecnologias
            self.create_technology_analysis(pdf)
        
        print(f"  Relatório gerado com sucesso: {self.report_name}")
        print(f"   Localização: {os.path.abspath(self.report_name)}")
        return True

def main():
    """Função principal"""
    print("Gerador de Relatório Estatístico - JobScraper Portugal")
    print("=" * 60)
    
    # Procura por ficheiros CSV na pasta data
    data_folder = "data"
    csv_files = []
    
    if os.path.exists(data_folder):
        csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
    
    # Também procura na pasta atual
    current_csv = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    all_csv_files = []
    if csv_files:
        all_csv_files.extend([os.path.join(data_folder, f) for f in csv_files])
    if current_csv:
        all_csv_files.extend(current_csv)
    
    if not all_csv_files:
        print("Nenhum ficheiro CSV encontrado!")
        print("Certifique-se de que existe um ficheiro .csv na pasta 'data' ou na pasta atual")
        return
    
    print(f"Ficheiros CSV encontrados:")
    for i, file in enumerate(all_csv_files, 1):
        print(f"  {i}. {file}")
    
    if len(all_csv_files) == 1:
        csv_file = all_csv_files[0]
        print(f"A usar: {csv_file}")
    else:
        try:
            choice = int(input(f"\nEscolha o ficheiro (1-{len(all_csv_files)}): ")) - 1
            csv_file = all_csv_files[choice]
        except (ValueError, IndexError):
            print("Escolha inválida!")
            return
    
    # Gera o relatório
    analyzer = JobAnalyzer(csv_file)
    success = analyzer.generate_report()
    
    if success:
        print("\nRelatório PDF gerado com sucesso!")
        print("O relatório inclui:")
        print("   • Resumo executivo com estatísticas principais")
        print("   • Análise de distribuição por seniority, empresa e categoria")
        print("   • Análise detalhada por localização")
        print("   • Análise completa de tecnologias e ferramentas")
        print("   • Gráficos e visualizações profissionais")

if __name__ == "__main__":
    main()