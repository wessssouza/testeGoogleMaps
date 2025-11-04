# main.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import json
from utils import configurar_logger, salvar_json, gerar_excel, esperar
from config import BASE_URL, TIPOS_ESTABELECIMENTOS, RESULTADOS_JSON, RESULTADOS_EXCEL, LOG_FILE, WAIT_TIME

def iniciar_driver():
    """Inicializa o driver do Chrome."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    try:
        driver = webdriver.Chrome(options=options)
        logging.info("Driver do Chrome iniciado com sucesso.")
        return driver
    except Exception as e:
        logging.critical(f"Falha ao iniciar o driver: {e}")
        raise

def buscar_estabelecimentos(driver, tipo):
    """Realiza a busca no Google Maps e extrai os dados."""
    resultados = []
    try:
        driver.get(BASE_URL)
        esperar(WAIT_TIME)

        busca = driver.find_element(By.ID, "searchboxinput")
        busca.clear()
        busca.send_keys(tipo)
        busca.send_keys(Keys.ENTER)

        esperar(WAIT_TIME * 2)

        # Localiza os elementos dos resultados
        
        elementos = driver.find_elements(By.CLASS_NAME, "Nv2PK")	

        for el in elementos[:10]:  # Limite de 10 por tipo
            try:
                nome = el.find_element(By.CLASS_NAME, "qBF1Pd").text
                nota = el.find_element(By.CLASS_NAME, "MW4etd").text if el.find_elements(By.CLASS_NAME, "MW4etd") else "N/A"
                avaliacoes = el.find_element(By.CLASS_NAME, "UY7F9").text if el.find_elements(By.CLASS_NAME, "UY7F9") else "N/A"
                #endereco = el.find_element(By.XPATH, "//span[contains(text(), 'Avenida')]").text if el.find_elements(By.XPATH, "//span[contains(text(), 'Avenida')]") else "N/A" 
                #endereco =  el.find_element(By.CLASS_NAME, "W4Efsd.W4Efsd").text if el.find_elements(By.CLASS_NAME, "W4Efsd.W4Efsd") else "N/A"
                endereco = 'não disponível'
                
                resultados.append({
                    "nome": nome,
                    "tipo": tipo,
                    "nota": nota,
                    "avaliacoes": avaliacoes,
                    "endereco": endereco
                })
            except Exception as e:
                logging.warning(f"Erro ao extrair dados de um item: {e}")

    except Exception as e:
        logging.error(f"Erro durante busca de '{tipo}': {e}")
    return resultados

def main():
    configurar_logger(LOG_FILE)
    logging.info("Iniciando automação RPA Google Maps...")

    driver = iniciar_driver()
    todos_dados = []

    for tipo in TIPOS_ESTABELECIMENTOS:
        logging.info(f"Iniciando busca para: {tipo}")
        dados = buscar_estabelecimentos(driver, tipo)
        todos_dados.extend(dados)

    driver.quit()
    salvar_json(todos_dados, RESULTADOS_JSON)
    gerar_excel(todos_dados, RESULTADOS_EXCEL)

    logging.info("Automação concluída com sucesso!")

if __name__ == "__main__":
    main()
