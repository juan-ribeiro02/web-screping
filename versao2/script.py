from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

#abrir o chrome controlado pelo slenium
driver = webdriver.Chrome()
#navega ate o site
driver.get("https://quotes.toscrape.com/js/")

#lista para acumular os dados
dados = []
pagina = 1

while True:
    print(f"colentando os dados da pagina {pagina}...")

    #espera ate 10 seg para o JS renderizar as caixas
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".quote")))

    # Passa o HTML já renderizado para o BeautifulSoup ler de uma só vez
    soup = BeautifulSoup(driver.page_source, "html.parser")
    caixas = soup.select(".quote")

    #percorre cada bloco de citacao
    for caixa in caixas:
        #busca o primeiro elemento span com a classe text, e o get_text(strip = True) remove espacos e quebras de linha
        texto = caixa.find("span", class_="text").get_text(strip = True) 
        #busca o primeiro elemento small com a classe author
        autor = caixa.find("small", class_="author").get_text(strip = True) 
        # 'caixa.select(".tag")' busca todos os links (tags <a>) com a classe CSS 'tag' dentro desta caixa
        # A list comprehension percorre cada elemento encontrado e extrai seu texto limpo em uma lista
        tags = [tag.get_text(strip = True) for tag in caixa.select(".tag")] 

        dados.append({
            "texto": texto,
            "autor": autor,
            "tags": " ,".join(tags) #junta as tags separada por virgula
        })

    #avanca para a proxima pagina
    try:
        pagina =+ 1
        botao_next = driver.find_element(By.CSS_SELECTOR, "li.next > a")
        botao_next.click()
    except NoSuchElementException:
        #quando chega na ultima
        print("ultima pagina alcancada!!")
        break

#fecha a janela do navegador     
driver.quit()

df = pd.DataFrame(dados) #cria um dataframe
df.to_csv("versao2/arquivo.csv", index=False)

df_autores = df["autor"].value_counts().reset_index() #conta quanto cada um aparece e reseta seu indice
df_autores.columns = ["autor", "aparicoes"] #renomeia as colunas
df_autores.to_csv("versao2/autores.csv", index=False)