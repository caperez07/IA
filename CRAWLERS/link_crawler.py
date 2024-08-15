from langchain_community.document_loaders import WebBaseLoader
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

# Função para extrair todos os links de uma página
def get_links(url, domain):
    links = set()
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            # Converter links relativos em absolutos
            full_link = urljoin(url, link)
            # Verifica se o link pertence ao mesmo domínio e não é o que queremos bloquear
            if urlparse(full_link).netloc == domain and not full_link.startswith("https://rollingstone.com.br/edicoes/"):
                links.add(full_link)
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
    return links

# Função para extrair e salvar o texto de uma página
def save_page_text(url, filename):
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()

        with open(filename, 'a', encoding='utf-8') as file:
            for doc in docs:
                file.write(f"URL: {url}\n{doc.page_content}\n\n")  # Supondo que 'page_content' seja um atributo
            
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")

# Função principal do crawler
def crawl_website(start_url, filename):
    visited = set()
    domain = urlparse(start_url).netloc
    to_visit = {start_url}

    while to_visit:
        current_url = to_visit.pop()
        if current_url not in visited:
            print(f"Visitando: {current_url}")
            save_page_text(current_url, filename)
            visited.add(current_url)
            new_links = get_links(current_url, domain)
            to_visit.update(new_links - visited)
            # Pequena pausa para evitar sobrecarregar o servidor
            time.sleep(1)

if __name__ == "__main__":
    start_url = "https://rollingstone.com.br"  # Substitua pelo site alvo
    output_file = "rs.txt"
    crawl_website(start_url, output_file)
    print(f"Texto extraído do site inteiro foi salvo em {output_file}")
