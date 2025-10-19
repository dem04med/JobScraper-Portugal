import csv
import os

def save_to_csv(data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    if not data:
        print("Nenhum dado para guardar.")
        return

    # Cria lista de chaves consistente para todas as linhas
    all_keys = set()
    for row in data:
        all_keys.update(row.keys())
    keys = list(all_keys)

    # Escreve o CSV
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"Dados guardados em {filepath}")
