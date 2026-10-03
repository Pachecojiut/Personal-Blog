import json
from flask import Flask, render_template, request, session, redirect,url_for
import os

app = Flask(__name__)
app.secret_key = 'uma-chave-secreta-qualquer'
@app.route('/') #←←←←←←Primeiro se cria as rotas, depois as funções que serão executadas quando a rota for acessada.
# Cada rota abre uma pagina do site, e cada função retorna o que será exibido na pagina. No final juntara tudo.
# os artigos sao armazenados em arquivos json, e cada arquivo tem o nome do id do artigo.
# # O id do artigo é passado na rota, e a função abre o arquivo correspondente e retorna os dados para a pagina.

# Rota para a pagina inicial. Que exibe o primeiro artigo.
def home():
    arquivos = os.listdir('articles')  #←←←←←←Lista todos os arquivos na pasta articles.
    dados = []                          #←←←←←←Armazena os dados dos artigos em uma lista.
    for arquivo in arquivos:            #←←←←←←Percorre todos os arquivos na pasta articles.
        if arquivo.endswith('.json'):#←←←←←←Se for .json, abre o arquivo e carrega os dados.
            id_artigo = int(arquivo.split('.')[0])
            with open(f'articles/{arquivo}', 'r', encoding='utf-8') as f:   
                dados_artigo=(json.load(f))    #←←←←←←Finalmente abre o arquivo e carrega os dados/artigos.
            dados_artigo['id'] = id_artigo
            dados.append(dados_artigo)
    return render_template('index.html', articles=dados)

# Rota para exibir um artigo específico, o id do artigo é passado na rota e a função abre o arquivo.
@app.route('/article/<int:article_id>')
def article(article_id):
    with open(f'articles/{article_id}.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
    return render_template('article.html', id=article_id, titulo=dados['titulo'], conteudo=dados['conteudo'], data=dados['data'])

# Rota de Login.
@app.route('/login', methods=['GET', 'POST'])         #←←←←←← A pagina de login usa metodos GET e POST, GET para exibir. POST para envio de dados.
def login():                 
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['senha']
        print(usuario)
        print(senha)
        if usuario == 'admin' and senha == '123':       #←←←←←←Acesso para pagina administrativa, caso o usuario e senha estejam corretos.
            session['logado']=True                      #←←←←←←←Se o usuario e senha estiverem corretos, a variavel de sessao 'logado' é criada e recebe o valor True.
            print('Usuario logado')
            return redirect('/admin')                             #←←←←←←←Redireciona para a pagina administrativa.
        else:
            return render_template('login.html', error='Usuario ou senha incorretos')
    return render_template('login.html')
# Rota de Admin.
@app.route('/admin')
def admin():
    arquivos = os.listdir('articles')
    dados = []
    for arquivo in arquivos:
        if arquivo.endswith('.json'):#←←←←←←Se for .json, abre o arquivo e carrega os dados.
            id_artigo = int(arquivo.split('.')[0])
            with open(f'articles/{arquivo}', 'r', encoding='utf-8') as f:   
                dados_artigo=(json.load(f))    #←←←←←←Finalmente abre o arquivo e carrega os dados/artigos.
            dados_artigo['id'] = id_artigo
            dados.append(dados_artigo)
    if session.get('logado')==True:  #←←←←←←←Se a variavel de sessao 'logado' existir e for True, o usuario tem acesso a pagina administrativa.
        return render_template('admin.html', articles=dados)
    else:
        return render_template('login.html', error='Acesso negado. Faça login primeiro')

# Rota para criar um novo artigo.
@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        novo_artigo = {'titulo': request.form['titulo'], 'conteudo': request.form['conteudo'], 'data': request.form['data']}

        # Resolvendo a questão dos IDs dos artigos. Dentro da função new(), antes de criar o novo artigo, vamos listar todos os arquivos na pasta articles e pegar o maior ID para criar o próximo artigo com o ID correto.
        arquivos = os.listdir('articles')  #←←←←←←Lista todos os arquivos na pasta articles.
        ids = []
        for arquivo in arquivos:
            if arquivo.endswith('.json'):  #←←←←←← '.endswith' Verifica se o arquivo termina com .json, para garantir que só pegue os arquivos de artigos.
                id_artigo = int(arquivo.split('.')[0])  #←←←←←←Pega o nome do arquivo (que é o id do artigo) e converte para inteiro.
                ids.append(id_artigo)  #←←←←←←Adiciona o id do artigo na lista de ids.
        novo_id = max(ids)+1  #←←←←←←Pega o maior id da lista e adiciona 1 para criar o próximo id.
        
        with open(f'articles/{novo_id}.json', 'w', encoding='utf-8') as arquivo:
            json.dump(novo_artigo, arquivo, ensure_ascii=False, indent=4)
            return redirect(url_for('admin'))
    return render_template('new.html')


@app.route('/admin/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    with open(f'articles/{article_id}.json', 'r', encoding='utf-8') as arquivo:
        artigo = json.load(arquivo)
    if request.method == 'POST':
        artigo = {'titulo': request.form['titulo'], 'conteudo': request.form['conteudo'], 'data': request.form['data']}
        with open(f'articles/{article_id}.json', 'w', encoding='utf-8') as arquivo:
            json.dump(artigo, arquivo, ensure_ascii=False, indent=4)
        return redirect(f'/admin')
    return render_template('edit.html', artigo=artigo)


@app.route('/admin/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    os.remove(f'articles/{article_id}.json')
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)



