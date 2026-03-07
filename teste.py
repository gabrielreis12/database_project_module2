import criacao_do_banco
import comandos_tabela_aluno
import sqlite3

con = sqlite3.connect("escola.db") # criação do banco de dados
cur = con.cursor()

comandos_tabela_aluno.ExecuteCLI_insert()

# coisas feitas ate entao
# implementei limite de entradas na função de INSERT atributtes
# configurei autoincrement na tabela Aluno (checar se o ID das outras tabelas possui AUTOINCREMENT)
# configurei a função de INSERT e de UPDATE
