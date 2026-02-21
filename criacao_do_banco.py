import sqlite3

def criar_tabelas():
    con = sqlite3.connect("escola.db") # criação do banco de dados
    cur = con.cursor() # leva os comandos do SQL do python para dentro do banco de dados

    cur.executescript("""
        -- 1º Passo: Tabelas Independentes
        CREATE TABLE IF NOT EXISTS Curso (
            ID_curso INT PRIMARY KEY,
            nome_curso VARCHAR(100),
            turno VARCHAR(20)
        );

        CREATE TABLE IF NOT EXISTS Professor (
            ID_matricula INT PRIMARY KEY,
            nome VARCHAR(100),
            departamento VARCHAR(50),
            nivel_de_formacao VARCHAR(50)
        );

        -- 2º Passo: Tabelas Dependentes Diretas
        CREATE TABLE IF NOT EXISTS Aluno (
            matricula_ID INT PRIMARY KEY,
            Nome VARCHAR(100),
            CPF VARCHAR(14),
            DoB DATE,
            nomePai VARCHAR(100),
            nomeMae VARCHAR(100),
            ID_curso INT,
            FOREIGN KEY(ID_curso) REFERENCES Curso(ID_curso)
        );

        CREATE TABLE IF NOT EXISTS Contrato_de_Trabalho (
            ID_contrato INT PRIMARY KEY,
            tipo_de_vinculo VARCHAR(50),
            carga_horaria_semanal INT,
            ID_matricula_professor INT UNIQUE,
            FOREIGN KEY(ID_matricula_professor) REFERENCES Professor(ID_matricula)
        );

        -- 3º Passo: Tabelas Dependentes de 2º Nível
        CREATE TABLE IF NOT EXISTS Prontuario_Academico (
            ID_prontuario INT PRIMARY KEY,
            data_de_matricula DATE,
            Situacao VARCHAR(20),
            matricula_ID_aluno INT UNIQUE,
            FOREIGN KEY(matricula_ID_aluno) REFERENCES Aluno(matricula_ID)
        );

        -- 4º Passo: Tabela Associativa (N:M)
        CREATE TABLE IF NOT EXISTS Leciona (
            ID_curso INT,
            ID_matricula INT,
            semestre VARCHAR(10),
            PRIMARY KEY (ID_curso, ID_matricula, semestre),
            FOREIGN KEY(ID_curso) REFERENCES Curso(ID_curso),
            FOREIGN KEY(ID_matricula) REFERENCES Professor(ID_matricula)
        );
    """)
    
    con.commit()
    con.close()

# Executando a função para gerar o arquivo
criar_tabelas()