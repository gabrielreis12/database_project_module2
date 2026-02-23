import sqlite3
import criacao_do_banco

# pensei em utilizar o kwargs** para deixar o código mais flexível na mudança de informações do banco

def atualizar_curso_aluno(matricula_id, novo_id_curso):
    con = sqlite3.connect("escola.db")
    cur = con.cursor()
    
    # Ativamos a checagem de Chave Estrangeira (obrigatório no SQLite)
    cur.execute("PRAGMA foreign_keys = ON;")
    
    # o bloco try/except existe para previnir a procura de um ID inexistente nesse caso
    try:
        cur.execute("""
            UPDATE Aluno
            SET ID_curso = ?
            WHERE matricula_ID = ?
        """, (novo_id_curso, matricula_id))
        
        # O rowcount nos diz quantas linhas o UPDATE afetou
        if cur.rowcount == 0:
            print(f"Erro: Nenhum aluno encontrado com a matrícula {matricula_id}.")
        else:
            con.commit()
            print("Curso do aluno atualizado com sucesso!")
            
    except sqlite3.IntegrityError:
        # Se tentar colocar um ID_curso que não existe na tabela Curso, cai aqui!
        print(f"Erro: O curso de ID {novo_id_curso} não existe no sistema.")
        
    finally:
        con.close()

def atualizar_nome_aluno(matricula_id, novo_nome_aluno):
    con = sqlite3.connect("escola.db")
    cur = con.cursor()
    
    # Ativamos a checagem de Chave Estrangeira (obrigatório no SQLite)
    cur.execute("PRAGMA foreign_keys = ON;")
    
    cur.execute("""
    UPDATE Aluno
    SET Nome = ? 
    WHERE matricula_ID = ?
    """, (novo_nome_aluno, matricula_id))  
    # # notar ordem dos parâmetros nome_nome_aluno vem antes de matricula. a ordem importa já que a primeira interrogação se refere ao atributo Nome da tabela Aluno, enquanto a segunda interrogação é acerca do matricula_ID e é PK    
        # O rowcount nos diz quantas linhas o UPDATE afetou
    if cur.rowcount == 0:
        print(f"Erro: Nenhum aluno encontrado com a matrícula {matricula_id}.")
    else:
        con.commit()
        print("Nome do aluno atualizado com sucesso!")
            
    con.close()

def atualizar_CPF_aluno(matricula_id, novo_CPF_aluno):

    confirmando_se_quer_mudar_o_CPF = input('Você tem certeza que o atributo que deseja mudar é o CPF?').capitalize()
    print('PRESSIONE a tecla A) para SIM, PRESSIONE a tecla B) para NÃO')
    print('A) Sim        B) Não')
    # aqui, quis adicionar uma camada de segurança para o BD, no sentido de que normalmente não se muda o dado CPF, mas, definitivamente é uma função que precisa existir
    if confirmando_se_quer_mudar_o_CPF == 'A':

        con = sqlite3.connect("escola.db")
        cur = con.cursor()
        
        # Ativamos a checagem de Chave Estrangeira (obrigatório no SQLite)
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute("""
        UPDATE Aluno
        SET CPF = ? 
        WHERE matricula_ID = ?
        """, (novo_CPF_aluno, matricula_id))  
        # # notar ordem dos parâmetros nome_nome_aluno vem antes de matricula. a ordem importa já que a primeira interrogação se refere ao atributo Nome da tabela Aluno, enquanto a segunda interrogação é acerca do matricula_ID e é PK    
            # O rowcount nos diz quantas linhas o UPDATE afetou
        if cur.rowcount == 0:
            print(f"Erro: Nenhum aluno encontrado com a matrícula {matricula_id}.")
        else:
            con.commit()
            print("CPF do aluno atualizado com sucesso!")
                
        con.close()
    else:
        print('Obrigado por confirmar!')

def inserir_aluno(matricula_id, Nome, CPF, DOB, nome_pai, nome_mae, id_curso):
    con = sqlite3.connect("escola.db")
    cur = con.cursor()
        
    # Ativamos a checagem de Chave Estrangeira (obrigatório no SQLite)
    cur.execute("PRAGMA foreign_keys = ON;")
    try:

        cur.execute("""
            INSERT INTO Aluno 
            VALUES (?,?,?,?,?,?,?) 
            WHERE matricula_ID = ?
            """, (matricula_id, Nome, CPF, DOB, nome_pai, nome_mae, id_curso))

    except sqlite3.IntegrityError as erro:
    # Se cair aqui, ou a matrícula já existe, ou o ID do curso é inválido!
        print("Erro ao inserir aluno!")
        print(f"Detalhe: Verifique se a matrícula {matricula_id} já existe ou se o curso {id_curso} é válido.")
        print(f"Aviso do banco de dados: {erro}")