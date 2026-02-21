import sqlite3
import criacao_do_banco

# pensei em utilizar o kwargs** para deixar o código mais flexível na mudança de informações do banco

def atualizar_registro(tabela, coluna_id, valor_id, **kwargs):
    con = sqlite3.connect("escola.db")
    cur = con.cursor()

    

