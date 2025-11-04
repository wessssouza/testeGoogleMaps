# utils.py
import json
import logging
import time
from openpyxl import Workbook

def configurar_logger(log_file):
    """Configura o sistema de logs da automação."""
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def salvar_json(dados, caminho):
    """Salva dados em formato JSON."""
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        logging.info(f"Arquivo JSON salvo com sucesso: {caminho}")
    except Exception as e:
        logging.error(f"Erro ao salvar JSON: {e}")

def gerar_excel(dados, caminho):
    """Gera um arquivo Excel (.xlsx) a partir do JSON."""
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Resultados"

        headers = ["Nome", "Tipo", "Nota", "Avaliações", "Endereço"]
        ws.append(headers)

        for item in dados:
            ws.append([
                item.get("nome"),
                item.get("tipo"),
                item.get("nota"),
                item.get("avaliacoes"),
                item.get("endereco")
            ])

        # Ajustar largura das colunas
        for coluna in ws.columns:
            max_length = 0
            coluna_letra = coluna[0].column_letter
            for cell in coluna:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            ws.column_dimensions[coluna_letra].width = max_length + 2

        wb.save(caminho)
        logging.info(f"Planilha Excel gerada com sucesso: {caminho}")
    except Exception as e:
        logging.error(f"Erro ao gerar Excel: {e}")

def esperar(segundos):
    """Pausa a execução por um determinado tempo."""
    time.sleep(segundos)
