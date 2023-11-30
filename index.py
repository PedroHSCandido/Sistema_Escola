from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/loginAluno', methods=['GET'])
def loginAluno():
    return render_template('loginAluno.html')

@app.route('/logarAluno', methods=['POST'])
def logarAluno():
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    cpfAluno = request.form['cpf']
    senhaAluno = request.form['senha']
    
    query = 'SELECT * FROM pedro_TB_aluno WHERE cpf = %s and senha = %s'
    mycursor.execute(query, (cpfAluno, senhaAluno))

    aluno = mycursor.fetchone()

    if aluno is not None:
        return redirect(url_for('homeAluno', cpf=cpfAluno))

    return render_template('loginAluno.html')       


@app.route('/homeAluno/<cpf>', methods=['GET'])
def homeAluno(cpf):
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    queryNotas = 'SELECT pedro_TB_disciplina.nomeDisciplina, pedro_TB_notas.nota1, pedro_TB_notas.nota2, pedro_TB_notas.nota3, pedro_TB_notas.nota4 FROM pedro_TB_disciplina INNER JOIN pedro_TB_notas ON pedro_TB_disciplina.nomeDisciplina = pedro_TB_notas.notaDisciplina WHERE pedro_TB_notas.cpfAluno = %s'
    mycursor.execute(queryNotas, (cpf,))
    notas = mycursor.fetchall()

    print(notas)
    return render_template('homeAluno.html', cpf=cpf, notas=notas)


@app.route('/loginAdm', methods=['GET'])
def loginAdm():
    return render_template('loginAdm.html')

@app.route('/homeAdm', methods=['POST'])
def logarAdm():
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    loginAdm = request.form['login']
    senhaAdm = request.form['senha']
    
    # Busca na coluna cpf e senha se existe o valor passado pelo usuario
    query = 'SELECT * FROM pedro_TB_funcionario WHERE login = %s and senha = %s'
    mycursor.execute(query, (loginAdm, senhaAdm,))

    # Armazenando em uma variavel o resultado da query
    funcionario = mycursor.fetchone()

    if funcionario is not None:
        return render_template('homeAdm.html')

    return render_template('loginAdm.html')

@app.route('/cadastrarAluno', methods=['GET'])
def cadastrarAluno():
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "select  cpf,nome, senha from pedro_TB_aluno"
    mycursor.execute(query)
    resultado = mycursor.fetchall()
    return render_template('cadastrarAluno.html', alunos = resultado)

@app.route('/registrarAluno', methods=['POST'])
def registrarAluno(): 
    nome = request.form['nome'] 
    senha= request.form["senha"]
    cpf = request.form["cpf"]
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "INSERT INTO pedro_TB_aluno (nome,cpf,senha) VALUES (%s, %s,%s)"
    values = (nome,cpf,senha)
    mycursor.execute(query,values)
    db.commit()
    return redirect(url_for('cadastrarAluno'))

@app.route('/excluirAluno/<aluno>')
def excluirAluno(aluno):
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "delete from pedro_TB_aluno where cpf = '" + aluno + "'"
    print(query)
    mycursor.execute(query)
    db.commit()
    return redirect(url_for('cadastrarAluno'))

@app.route('/editarAluno/<aluno>')
def editarAluno(aluno):
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "select nome, cpf, senha from pedro_TB_aluno where cpf = '" + aluno + "'"
    mycursor.execute(query)
    resultado = mycursor.fetchall()
    db.commit()
    return render_template('editarAluno.html', alunos = resultado)

@app.route('/gravarAlteracaoAluno', methods=['POST'])
def gravarAlteracaoAluno():
    nome = request.form['nome']
    cpf = request.form['cpf']
    senha = request.form['senha']
    usuarioAnterior = request.form['usuarioAnterior']
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "Update pedro_TB_aluno set nome = '"+nome+ "', cpf = '" + cpf  +"', senha = '" + senha  + "' where cpf = '" +usuarioAnterior + "'"
    mycursor.execute(query)
    db.commit()
    return redirect(url_for('cadastrarAluno'))

@app.route('/cadastrarFuncionario', methods=['GET'])
def cadastrarFuncionario():
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "select cpf, nome, email, login, senha from pedro_TB_funcionario"
    mycursor.execute(query)
    resultado = mycursor.fetchall()
    return render_template('cadastrarFuncionario.html', funcionarios = resultado)


@app.route('/registrarFuncionario', methods=['POST'])
def registrarFuncionario(): 
    nome = request.form['nome'] 
    email = request.form['email'] 
    cpf = request.form['cpf'] 
    login= request.form["login"]
    senha = request.form["senha"]
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "INSERT INTO pedro_TB_funcionario (nome, email, cpf, login, senha) VALUES (%s, %s ,%s ,%s ,%s)"
    values = (nome,email, cpf, login, senha)
    mycursor.execute(query,values)
    db.commit()
    return redirect(url_for('cadastrarFuncionario'))

@app.route('/excluirFuncionario/<funcionario>')
def excluirFuncionario(funcionario):
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "delete from pedro_TB_funcionario where cpf = '" + funcionario + "'"
    print(query)
    mycursor.execute(query)
    db.commit()
    return redirect(url_for('cadastrarFuncionario'))

@app.route('/editarFuncionario/<funcionario>')
def editarFuncionario(funcionario):
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "select cpf, nome, email, login, senha from pedro_TB_funcionario where cpf = '" + funcionario + "'"
    mycursor.execute(query)
    resultado = mycursor.fetchall()
    db.commit()
    return render_template('editarFuncionario.html', funcionarios = resultado)

@app.route('/gravarAlteracaoFuncionario', methods=['POST'])
def gravarAlteracaoFuncionario():
    nome = request.form['nome'] 
    email = request.form['email'] 
    cpf = request.form['cpf'] 
    login= request.form["login"]
    senha = request.form["senha"]
    usuarioAnterior = request.form['usuarioAnterior']
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "Update pedro_TB_funcionario set nome = '"+nome+ "',email = '"+email+ "', cpf = '" + cpf  +"',login = '"+login+ "', senha = '" + senha  + "' where cpf = '" +usuarioAnterior + "'"
    mycursor.execute(query)
    db.commit()
    return redirect(url_for('cadastrarFuncionario'))

@app.route('/cadastrarDisciplina', methods=['GET'])
def cadastrarDisciplina():
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "select nomeDisciplina from pedro_TB_disciplina"
    mycursor.execute(query)
    resultado = mycursor.fetchall()
    return render_template('cadastrarDisciplina.html', disciplinas = resultado)


@app.route('/registrarDisciplina', methods=['POST'])
def registrarDisciplina(): 
    nomeDisciplina = request.form['nomeDisciplina'] 
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "INSERT INTO pedro_TB_disciplina (nomeDisciplina) VALUES (%s)"
    values = (nomeDisciplina,)
    mycursor.execute(query,values)
    db.commit()
    return redirect(url_for('cadastrarDisciplina'))

@app.route('/excluirDisciplina/<disciplina>')
def excluirDisciplina(disciplina):
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "delete from pedro_TB_disciplina where nomeDisciplina = '" + disciplina + "'"
    print(query)
    mycursor.execute(query)
    db.commit()
    return redirect(url_for('cadastrarDisciplina'))

@app.route('/editarDisciplina/<disciplina>')
def editarDisciplina(disciplina):
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "select nomeDisciplina from pedro_TB_disciplina where nomeDisciplina = '" + disciplina + "'"
    mycursor.execute(query)
    resultado = mycursor.fetchall()
    db.commit()
    return render_template('editarDisciplina.html', disciplinas = resultado)

@app.route('/gravarAlteracaoDisciplina', methods=['POST'])
def gravarAlteracaoDisciplina():
    nomeDisciplina = request.form['nomeDisciplina'] 
    disciplinaAnterior = request.form['disciplinaAnterior']
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "Update pedro_TB_disciplina set nomeDisciplina = '"+nomeDisciplina+ "' where nomeDisciplina = '" +disciplinaAnterior + "'"
    mycursor.execute(query)
    db.commit()
    return redirect(url_for('cadastrarDisciplina'))

@app.route('/cadastrarNotas', methods=['GET'])
def cadastrarNotas():
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    queryAluno = "select cpf,nome from pedro_TB_aluno"
    queryDisciplina = "select nomeDisciplina from pedro_TB_disciplina"
    queryNotas = "SELECT idNotas, cpfAluno, notaDisciplina, nota1, nota2, nota3, nota4 FROM pedro_TB_notas"
    mycursor.execute(queryAluno)
    alunos = mycursor.fetchall()
    mycursor.execute(queryDisciplina)
    disciplinas = mycursor.fetchall()
    mycursor.execute(queryNotas)
    notas = mycursor.fetchall()

    return render_template('cadastrarNotas.html', alunos= alunos, disciplinas=disciplinas, notas = notas)


@app.route('/registrarNotas', methods=['POST'])
def registrarNotas():
    cpfAluno = request.form['cpfAluno'] 
    notaDisciplina = request.form['notaDisciplina'] 
    nota1 = request.form['nota1']
    nota2 = request.form['nota2']
    nota3 = request.form['nota3']
    nota4 = request.form['nota4']
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "INSERT INTO pedro_TB_notas (cpfAluno, notaDisciplina,nota1,nota2,nota3,nota4) VALUES (%s,%s,%s,%s,%s,%s)"
    values = (cpfAluno,notaDisciplina,nota1,nota2,nota3,nota4)
    mycursor.execute(query,values)
    db.commit()
    return redirect(url_for("cadastrarNotas"))


@app.route('/excluirNota/<idNotas>')
def excluirNota(idNotas):
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "DELETE FROM pedro_TB_notas WHERE idNotas = %s"
    mycursor.execute(query, (idNotas,))
    db.commit()
    return redirect(url_for('cadastrarNotas'))


@app.route('/editarNota/<idNotas>', methods=['GET'])
def editarNota(idNotas):
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "SELECT * FROM pedro_TB_notas WHERE idNotas = %s"
    mycursor.execute(query, (idNotas,))
    notas = mycursor.fetchone()
    return render_template('editarNotas.html', notas=notas)

@app.route('/gravarAlteracaoNota', methods=['POST'])
def atualizarNota():
    idNota = request.form['idNota']
    nota1 = request.form['nota1']
    nota2 = request.form['nota2']
    nota3 = request.form['nota3']
    nota4 = request.form['nota4']
    
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    
    query = "UPDATE pedro_TB_notas SET nota1=%s, nota2=%s, nota3=%s, nota4=%s WHERE idNotas=%s"
    values = (nota1, nota2, nota3, nota4, idNota)
    
    mycursor.execute(query, values)
    db.commit()
    
    return redirect(url_for('cadastrarNotas'))



app.run()
