from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pandas as pd
from config import BREVO_API_KEY, BREVO_ENDPOINT
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route("/biografia")
def biografia():
  return render_template("biografia.html")

@app.route("/raspagem")
def raspagem():
  return render_template("raspagem.html")

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route('/enviar', methods=['POST'])
def enviar():
    try:
        if request.method == 'POST':
            nome = request.form['nome']
            email = request.form['email']
            mensagem = request.form['mensagem']

            # Monta o payload da mensagem
            email_data = {
                "from": email,
                "to": "melissa.mmod@gmail.com",
                "subject": "Nova Mensagem de Contato",
                "text": f"De: {nome}\nE-mail: {email}\nMensagem: {mensagem}",
            }

            # Envia o e-mail usando a API do Brevo
            response = requests.post(
                BREVO_ENDPOINT,
                json=email_data,
                headers={"Authorization": f"Bearer {BREVO_API_KEY}"}
            )

            # Verifica se a solicitação foi bem-sucedida (código de status 2xx)
            if response.status_code // 100 != 2:
                return f"Erro ao enviar a mensagem: {response.text}", 500

            return "E-mail enviado com sucesso!"
    except requests.RequestException as e:
        return f"Erro de rede ao enviar a mensagem: {str(e)}", 500
    except Exception as e:
        return f"Erro interno do servidor: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/")
def home():
   return render_template("layout.html")

@app.route("/teste")
def teste():
   return render_template("teste.html")


# Raspa as noticias da BBC
def bbc():
    url = 'https://www.bbc.com/portuguese/topics/c5qvpqj1dy4t'
    response = requests.get(url)
    noticias_bbc = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links_titulos = soup.find_all('div', class_='bbc-bjn8wh e1v051r10')
        for link_titulo in links_titulos:
            titulo = link_titulo.find('a').text
            link = link_titulo.find('a')['href']
            noticias = {"titulo": titulo, "link": link} 
            noticias_bbc.append(noticias)
    return noticias_bbc

@app.route("/bbcresultado")
def bbcresultado():
    noticias_bbc = bbc()
    return render_template('resultadoraspagem.html', noticias_bbc=noticias_bbc)

if __name__ == '__main__':
    app.run(debug=True)