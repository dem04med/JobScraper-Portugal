import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import sys

def clean_xml_text(text):
    """Limpa texto para ser válido em XML"""
    if pd.isna(text) or text == "N/A":
        return ""
    
    # Converte para string e limita tamanho se necessário
    text = str(text).strip()
    
    # Remove caracteres problemáticos para XML
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    
    # Limita descrição se muito longa
    if len(text) > 500:
        text = text[:500] + "..."
    
    return text

def convert_csv_to_xml(csv_file_path, xml_output_path, max_records=None):    
    try:
        # Carrega CSV
        print(f" CSV carregado: {csv_file_path}")
        df = pd.read_csv(csv_file_path)
        
        # Limita número de registos se especificado
        if max_records is not None and len(df) > max_records:
            df = df.head(max_records)
            print(f" Processando primeiros {max_records} registos de {len(pd.read_csv(csv_file_path))}")
        else:
            print(f" Processando todos os {len(df)} registos disponíveis")
        
        # Cria elemento raiz
        root = ET.Element("ofertas_emprego")
        root.set("total", str(len(df)))
        root.set("fonte", "ITJobs.pt")
        root.set("gerado_por", "JobScraper-Portugal")
        
        # Processa cada linha do CSV
        for index, row in df.iterrows():
            # Elemento para cada oferta
            oferta = ET.SubElement(root, "oferta")
            oferta.set("id", str(index + 1))
            
            # Adiciona todos os campos do CSV
            campos = {
                "titulo": row.get("Título", ""),
                "empresa": row.get("Empresa", ""),
                "localizacao": row.get("Localização", ""),
                "tecnologias": row.get("Tecnologias", ""),
                "seniority": row.get("Seniority", ""),
                "categoria": row.get("Categoria", ""),
                "tipo_contrato": row.get("Tipo de contrato", ""),
                "modo_trabalho": row.get("Modo de trabalho", ""),
                "data_publicacao": row.get("Data de publicação", ""),
                "descricao": row.get("Descrição", ""),
                "link": row.get("Link", "")
            }
            
            # Adiciona cada campo como elemento XML
            for campo_nome, campo_valor in campos.items():
                elemento = ET.SubElement(oferta, campo_nome)
                elemento.text = clean_xml_text(campo_valor)
        
        # Converte para string XML bem formatada
        rough_string = ET.tostring(root, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ", encoding=None)
        
        # Remove linha em branco extra
        pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])
        
        # Salva XML
        with open(xml_output_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
        
        print(f" XML criado com sucesso: {xml_output_path}")
        print(f" Registos processados: {len(df)}")
        print(f" Campos por registo: {len(campos)}")
        
        return True
        
    except Exception as e:
        print(f" Erro ao converter CSV para XML: {e}")
        return False

def main():
    """Função principal"""
    
    # Caminhos dos arquivos
    csv_path = "../data/jobs_itjobs.csv"
    xml_path = "jobs_sample.xml"
    
    print(" JobScraper-Portugal: CSV to XML Converter")
    print("=" * 50)
    
    # Verifica se CSV existe
    if not os.path.exists(csv_path):
        print(f" Arquivo CSV não encontrado: {csv_path}")
        print(" Execute primeiro o scraper para gerar os dados")
        return
    
    # Converte CSV para XML (todos os registos)
    success = convert_csv_to_xml(csv_path, xml_path, max_records=None)
    
    if success:
        print("\n Conversão concluída!")
        print(f" Arquivo XML disponível em: {xml_path}")
    else:
        print("\n Falha na conversão!")

if __name__ == "__main__":
    main()
