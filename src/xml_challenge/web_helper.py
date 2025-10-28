import os

def display_file_contents():
    xml_file = "jobs_sample.xml"
    xsd_file = "jobs_schema.xsd"
    
    print(" JobScraper-Portugal: Web Validation Helper")
    print("=" * 60)
    
    # Verifica arquivos
    if not os.path.exists(xml_file):
        print(f" {xml_file} não encontrado!")
        return
    
    if not os.path.exists(xsd_file):
        print(f" {xsd_file} não encontrado!")  
        return
    
    # Informações dos arquivos
    xml_size = os.path.getsize(xml_file)
    xsd_size = os.path.getsize(xsd_file)
    
    print(f" {xml_file}: {xml_size:,} bytes")
    print(f" {xsd_file}: {xsd_size:,} bytes")
    print()
    
    # Opções
    print(" Opções disponíveis:")
    print("1. Mostrar início do XML (para preview)")
    print("2. Mostrar XSD completo (para copy/paste)")
    print("3. Informações para upload direto")
    print("4. Verificar encoding dos arquivos")
    
    choice = input("\nEscolha uma opção (1-4): ").strip()
    
    if choice == "1":
        show_xml_preview(xml_file)
    elif choice == "2": 
        show_xsd_content(xsd_file)
    elif choice == "3":
        show_upload_info(xml_file, xsd_file)
    elif choice == "4":
        check_encoding(xml_file, xsd_file)
    else:
        print(" Opção inválida!")

def show_xml_preview(xml_file):
    """Mostra preview do XML"""
    print(f"\n Preview do {xml_file} (primeiras 20 linhas):")
    print("-" * 50)
    
    with open(xml_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines[:20], 1):
            print(f"{i:2d}: {line.rstrip()}")
    
    if len(lines) > 20:
        print(f"... (mais {len(lines)-20} linhas)")
    
    print(f"\n Total de linhas: {len(lines)}")

def show_xsd_content(xsd_file):
    """Mostra XSD completo para copy/paste"""
    print(f"\n Conteúdo completo do {xsd_file}:")
    print("=" * 50)
    print(" Copie todo o texto abaixo para validadores web:")
    print("-" * 50)
    
    with open(xsd_file, 'r', encoding='utf-8') as f:
        print(f.read())
    
    print("-" * 50)
    print(" Fim do XSD - pronto para copy/paste!")

def show_upload_info(xml_file, xsd_file):
    """Mostra informações para upload direto"""
    print(f"\n Informações para Upload Direto:")
    print("-" * 30)
    
    xml_path = os.path.abspath(xml_file)
    xsd_path = os.path.abspath(xsd_file)
    
    print(f" XML File:")
    print(f"   Caminho: {xml_path}")
    print(f"   Tamanho: {os.path.getsize(xml_file):,} bytes")
    print()
    print(f" XSD File:")  
    print(f"   Caminho: {xsd_path}")
    print(f"   Tamanho: {os.path.getsize(xsd_file):,} bytes")
    print()
    print(" Use estes caminhos para upload direto em validadores que suportam!")

def check_encoding(xml_file, xsd_file):
    """Verifica encoding dos arquivos"""
    print(f"\n Verificação de Encoding:")
    print("-" * 25)
    
    files = [xml_file, xsd_file]
    
    for file in files:
        try:
            # Tenta ler como UTF-8
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verifica BOM
            with open(file, 'rb') as f:
                first_bytes = f.read(3)
                has_bom = first_bytes == b'\xef\xbb\xbf'
            
            print(f" {file}:")
            print(f"   UTF-8 válido")
            print(f"   BOM: {'Sim' if has_bom else 'Não'}")
            print(f"   Linhas: {content.count(chr(10)) + 1}")
            print()
            
        except UnicodeDecodeError:
            print(f" {file}:")
            print(f"    Não é UTF-8 válido")
            print()

if __name__ == "__main__":
    display_file_contents()