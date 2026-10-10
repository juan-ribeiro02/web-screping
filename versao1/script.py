import requests
import pandas as pd
from urllib.parse import urljoin
from bs4 import BeautifulSoup

url_atual = "https://quotes.toscrape.com/"
dados = []

while url_atual:
    resposta = requests.get(url_atual, timeout=10)
    soup = BeautifulSoup(resposta.content, "html.parser")

    for caixa in soup.select(".quote"):
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

    botao_next = soup.select_one("li.next a")

    if botao_next:
        # 'botao_next["href"]' retorna um caminho relativo (ex: "/page/2/")
        # 'urljoin' junta a URL base com o caminho relativo de forma segura
        caminho_relativo = botao_next["href"]
        url_atual = urljoin(url_atual, caminho_relativo)
    else:
        # Quando chegar na última página, o elemento não existirá (None)
        url_atual = None

df = pd.DataFrame(dados) #cria um dataframe
df.to_csv("versao1/arquivo.csv", index=False)

df_autores = df["autor"].value_counts().reset_index() #conta quanto cada um aparece e reseta seu indice
df_autores.columns = ["autor", "aparicoes"] #renomeia as colunas
df_autores.to_csv("versao1/autores.csv", index=False)
