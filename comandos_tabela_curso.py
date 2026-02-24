import sqlite3
import criacao_do_banco


def inserir_curso(id_curso, nome_curso, turno_curso):
    con = sqlite3.connect("escola.db",timeout=10)
    cur = con.cursor()
        
    # Ativamos a checagem de Chave Estrangeira (obrigatório no SQLite)
    cur.execute("PRAGMA foreign_keys = ON;")
    try:

        cur.execute("""
            INSERT INTO Curso 
            VALUES (?,?,?) 
            """, (id_curso, nome_curso, turno_curso))

        con.commit()
        print("Salvo com sucesso!")

    except sqlite3.IntegrityError as erro:
    # Se cair aqui, ou a matrícula já existe, ou o ID do curso é inválido!
        print("Erro ao inserir aluno! (funcao inserir curso)")
        print(f"Detalhe: Verifique se a matrícula {id_curso} já existe ou se o curso {id_curso} é válido.")
        print(f"Aviso do banco de dados: {erro}")
    finally:
        cur.close()
        con.close()


'''import sqlite3
import criacao_do_banco


def inserir_curso(id_curso, nome_curso, turno_curso):
    con = sqlite3.connect("escola.db")
    cur = con.cursor()
        
    # Ativamos a checagem de Chave Estrangeira (obrigatório no SQLite)
    cur.execute("PRAGMA foreign_keys = ON;")
    try:

        cur.execute("""
            INSERT INTO Curso 
            VALUES (?,?,?) 
            WHERE matricula_ID = ?
            """, (id_curso, nome_curso, turno_curso))

    except sqlite3.IntegrityError as erro:
    # Se cair aqui, ou a matrícula já existe, ou o ID do curso é inválido!
        print("Erro ao inserir aluno!")
        print(f"Detalhe: Verifique se a matrícula {matricula_id} já existe ou se o curso {id_curso} é válido.")
        print(f"Aviso do banco de dados: {erro}")'''