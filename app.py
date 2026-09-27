import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/') #←←←←←←Primeiro se cria as rotas, depois as funções que serão executadas quando a rota for acessada.
# Cada rota abre uma pagina do site, e cada função retorna o que será exibido na pagina. No final juntara tudo.
# os artigos sao armazenados em arquivos json, e cada arquivo tem o nome do id do artigo.
# # O id do artigo é passado na rota, e a função abre o arquivo correspondente e retorna os dados para a pagina.
def home(): 
    with open('articles/1.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
    return render_template('index.html', articles=dados)

@app.route('/article/<int:article_id>')
def article(article_id):
    with open(f'articles/{article_id}.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
    return render_template('article.html', id=article_id, titulo=dados['titulo'], conteudo=dados['conteudo'], data=dados['data'])

@app.route('/login')         #←←←←←← No momento atual estou criando a rota de login, para que o usuario possa acessar a pagina de admin, e criar artigos
def login():                 #←←←←←←No momento a pagina de login é apenas uma pagina de teste autenticação e autorização.
    return render_template('login.html')

app.run(debug=True)

