from lxml import etree
import os
import sys

def validate_xml_with_xsd(xml_file, xsd_file):
    try:
        # Carrega o Schema XSD
        print(f" Carregando Schema: {xsd_file}")
        with open(xsd_file, 'rb') as schema_file:
            schema_doc = etree.parse(schema_file)
            schema = etree.XMLSchema(schema_doc)
        
        # Carrega o arquivo XML
        print(f" Carregando XML: {xml_file}")
        with open(xml_file, 'rb') as xml_file_handle:
            xml_doc = etree.parse(xml_file_handle)
        
        # Valida XML contra Schema
        print(" Validando XML contra Schema...")
        is_valid = schema.validate(xml_doc)
        
        # Coleta erros se existirem
        errors = []
        if not is_valid:
            for error in schema.error_log:
                errors.append(f"Linha {error.line}: {error.message}")
        
        return is_valid, errors
        
    except etree.XMLSyntaxError as e:
        return False, [f"Erro de sintaxe XML: {e}"]
    except etree.XMLSchemaError as e:
        return False, [f"Erro no Schema XSD: {e}"]
    except FileNotFoundError as e:
        return False, [f"Arquivo não encontrado: {e}"]
    except Exception as e:
        return False, [f"Erro inesperado: {e}"]

def validate_xml_syntax(xml_file):    
    try:
        print(f" Verificando sintaxe XML: {xml_file}")
        with open(xml_file, 'r', encoding='utf-8') as f:
            etree.parse(f)
        return True, []
    except etree.XMLSyntaxError as e:
        return False, [f"Erro de sintaxe: {e}"]
    except Exception as e:
        return False, [f"Erro: {e}"]

def display_xml_info(xml_file): 
    try:
        with open(xml_file, 'r', encoding='utf-8') as f:
            tree = etree.parse(f)
            root = tree.getroot()
        
        print(f"\n Informações do XML:")
        print(f"    Elemento raiz: {root.tag}")
        print(f"    Atributos: {dict(root.attrib)}")
        print(f"    Elementos filhos: {len(list(root))}")
        
        # Conta ofertas se existir
        ofertas = root.findall('.//oferta')
        if ofertas:
            print(f"    Total de ofertas: {len(ofertas)}")
            
    except Exception as e:
        print(f" Erro ao ler XML: {e}")

def main():
    xml_file = "jobs_sample.xml"
    xsd_file = "jobs_schema.xsd"
    
    print(" JobScraper-Portugal: XML Validator")
    print("=" * 50)
    
    # Verifica se arquivos existem
    if not os.path.exists(xml_file):
        print(f" Arquivo XML não encontrado: {xml_file}")
        return
    
    if not os.path.exists(xsd_file):
        print(f" Arquivo XSD não encontrado: {xsd_file}")
        return
    
    # Exibe informações do XML
    display_xml_info(xml_file)
    
    # Etapa 1: Validação de sintaxe
    print(f"\n Etapa 1: Validação de Sintaxe XML")
    print("-" * 40)
    syntax_valid, syntax_errors = validate_xml_syntax(xml_file)
    
    if syntax_valid:
        print(" XML bem formado (sintaxe válida)")
    else:
        print(" XML mal formado:")
        for error in syntax_errors:
            print(f"   • {error}")
        return
    
    # Etapa 2: Validação contra Schema
    print(f"\n Etapa 2: Validação contra Schema XSD")
    print("-" * 40)
    schema_valid, schema_errors = validate_xml_with_xsd(xml_file, xsd_file)
    
    if schema_valid:
        print(" XML válido contra o Schema!")
        print(" Todos os elementos e tipos estão corretos")
    else:
        print(" XML inválido contra o Schema:")
        for error in schema_errors:
            print(f"   • {error}")
    
    # Resumo final
    print(f"\n Resumo da Validação:")
    print(f"    Arquivo XML: {xml_file}")
    print(f"    Schema XSD: {xsd_file}")
    print(f"    Sintaxe válida: {'Sim' if syntax_valid else 'Não'}")
    print(f"    Schema válido: {'Sim' if schema_valid else 'Não'}")
    
    if syntax_valid and schema_valid:
        print(f"\n VALIDAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"   O XML está completamente válido e em conformidade com o Schema")
    else:
        print(f"\n  VALIDAÇÃO FALHOU")
        print(f"   Corrija os erros antes de prosseguir")

if __name__ == "__main__":
    main()