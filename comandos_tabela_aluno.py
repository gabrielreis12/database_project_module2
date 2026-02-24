import sqlite3
import criacao_do_banco

# d

# pensei em utilizar o kwargs** para deixar o código mais flexível na mudança de informações do banco

def atualizar_atributo(TableName, AttributeType, NewAttributeValue, EntityID):

    con = sqlite3.connect("escola.db",timeout=10)
    cur = con.cursor()
    
    # Ativamos a checagem de Chave Estrangeira (obrigatório no SQLite)
    cur.execute("PRAGMA foreign_keys = ON;")

    # utilizando duas variaveis como condicional para que os valores dos parâmetros da funcao atualizar_atributo sejam apenas os reais nomes dos atributos e das tabelas e não um comando em SQL que consulte dados, ou exclua os dados do BD
    VariableForCondition1 = AttributeType in criacao_do_banco.possiveis_valores_atributos
    VariableForCondition2 = TableName in criacao_do_banco.possiveis_valores_tabelas
    
    if VariableForCondition1 and VariableForCondition2:

        # o bloco try/except existe para previnir a procura de um ID inexistente nesse caso
        try:
            cur.execute(f"UPDATE {TableName} SET {AttributeType} = ? WHERE matricula_ID = ?", (NewAttributeValue, EntityID))
            
            # O rowcount nos diz quantas linhas o UPDATE afetou
            if cur.rowcount == 0:
                print(f"Erro: Nenhum/Nenhuma {TableName} encontrado com o ID num.: {EntityID} informado.")
            else:
                con.commit()
                print("Dado atualizado com sucesso!")
                
        except sqlite3.IntegrityError:
            # Se tentar colocar um ID_curso que não existe na tabela Curso, cai aqui!
            print(f"Erro: A entidade {TableName} com {EntityID} não existe no sistema.")
            
        finally:
            con.close()
    
    else:
        print('Perigo! Risco de vulnerabilidade!')
    

def inserir_aluno(matricula_id, nome_curso, cpf_curso, dob_curso, nome_pai_curso, nome_mae_curso, id_curso):
    con = sqlite3.connect("escola.db",timeout=10)
    cur = con.cursor()
        
    # Ativamos a checagem de Chave Estrangeira (obrigatório no SQLite)
    cur.execute("PRAGMA foreign_keys = ON;")
    try:

        cur.execute("""
            INSERT INTO Aluno 
            VALUES (?,?,?,?,?,?,?) 
            """, (matricula_id, nome_curso, cpf_curso, dob_curso, nome_pai_curso, nome_mae_curso, id_curso))
        con.commit()
        print('Salvo com sucesso!')
        
    except sqlite3.IntegrityError as erro:
    # Se cair aqui, ou a matrícula já existe, ou o ID do curso é inválido!
        print("Erro ao inserir aluno! (funcao inserir aluno)")
        print(f"Detalhe: Verifique se a matrícula {matricula_id} já existe ou se o curso {id_curso} é válido.")
        print(f"Aviso do banco de dados: {erro}")
    finally:
        cur.close()
        con.close()

def delete_aluno(matricula_id):

    con = sqlite3.connect("escola.db",timeout=10)
    cur = con.cursor()
        
    # Ativamos a checagem de Chave Estrangeira (obrigatório no SQLite)
    cur.execute("PRAGMA foreign_keys = ON;")
    try:

        cur.execute("""
            DELETE FROM Aluno 
            WHERE matricula_ID = ?
            """, (matricula_id,))
        con.commit()
        print('Salvo com sucesso!')
        
    except sqlite3.IntegrityError as erro:
    # Se cair aqui, ou a matrícula já existe, ou o ID do curso é inválido!
        print("Erro ao inserir aluno! (funcao inserir aluno)")
        print(f"Detalhe: Verifique se a matrícula {matricula_id} já existe ou se o curso {id_curso} é válido.")
        print(f"Aviso do banco de dados: {erro}")
    finally:
        cur.close()
        con.close()