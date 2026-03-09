import sqlite3

possiveis_valores_atributos = [
    'ID_curso', 
    'nomeCurso', 
    'turno',
    'ID_matriculaProfessor', 
    'nome', 
    'departamento', 
    'nivel_de_formacao',
    'ID_AlunoMatricula', 
    'alunoCPF', 
    'AlunoDOB', 
    'nomePai', 
    'nomeMae', 
    'ID_cursoFK',
    'ID_contrato', 
    'tipo_de_vinculo', 
    'carga_horaria_semanal',
    'ID_AlunoMatriculaProntuario', 
    'data_de_matricula', 
    'situacao',
    'semestre'
]
def criar_tabelas():
    # criação do banco de dados
    con = sqlite3.connect("escola.db") 
    cur = con.cursor() 

    cur.execute("PRAGMA foreign_keys = ON;")

    # Script do MySQL adaptado para o SQLite3 com IA
    cur.executescript("""
    -- 1. Tabelas Pai (Sem chaves estrangeiras)
    
    CREATE TABLE IF NOT EXISTS Curso (
        ID_curso INTEGER NOT NULL PRIMARY KEY,
        nomeCurso VARCHAR(100),
        turno VARCHAR(20)
    );

    CREATE TABLE IF NOT EXISTS Professor (
        ID_matriculaProfessor INTEGER NOT NULL PRIMARY KEY,
        nome VARCHAR(100),
        departamento VARCHAR(50),
        nivel_de_formacao VARCHAR(50)
    );

    -- 2. Tabelas Filhas (Com chaves estrangeiras)

    CREATE TABLE IF NOT EXISTS Aluno (
        ID_AlunoMatricula INTEGER NOT NULL PRIMARY KEY,
        nome VARCHAR(100),
        alunoCPF VARCHAR(14),
        AlunoDOB DATE,
        nomePai VARCHAR(100),
        nomeMae VARCHAR(100),
        ID_cursoFK INT NOT NULL,
        FOREIGN KEY (ID_cursoFK) REFERENCES Curso (ID_curso)
    );

    CREATE TABLE IF NOT EXISTS Contrato_de_Trabalho (
        ID_contrato INTEGER NOT NULL PRIMARY KEY,
        tipo_de_vinculo VARCHAR(50),
        carga_horaria_semanal INT,
        FOREIGN KEY (ID_contrato) REFERENCES Professor (ID_matriculaProfessor)
    );

    -- 3. Tabelas Netas e Associativas

    CREATE TABLE IF NOT EXISTS Prontuario_Academico (
        ID_AlunoMatriculaProntuario INTEGER PRIMARY KEY,
        data_de_matricula DATE,
        situacao VARCHAR(20),
        FOREIGN KEY (ID_AlunoMatriculaProntuario) REFERENCES Aluno (ID_AlunoMatricula)
    );

    CREATE TABLE IF NOT EXISTS Leciona (
        ID_curso INT NOT NULL,
        ID_matriculaProfessor INT NOT NULL,
        semestre VARCHAR(10) NOT NULL,
        PRIMARY KEY (ID_curso, ID_matriculaProfessor, semestre),
        FOREIGN KEY (ID_curso) REFERENCES Curso (ID_curso),
        FOREIGN KEY (ID_matriculaProfessor) REFERENCES Professor (ID_matriculaProfessor)
    );
    """)
    
    con.commit()
    con.close()
    print("Banco de dados 'escola.db' e tabelas criados com sucesso usando SQLite!")

# Executando a função para gerar o arquivo
criar_tabelas()