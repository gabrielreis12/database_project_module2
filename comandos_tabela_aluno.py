import sqlite3
import criacao_do_banco

def UpdateAttribute(): 

    TableName = input('Digite o nome da tabela: ')
    ID_AttributteName = input('Qual o nome do atributo de ID? ')
    AttributeName = input('Digite o atributo da tabela {TableName} escolhido: ')
    NewAttributeValue = input("Digite qual o valor do atributo que você quer atualizar: ")
    Row_ID = input('Qual o ID do usuário que você quer mudar? ')
    
    con = sqlite3.connect("escola.db",timeout=10)
    cur = con.cursor()
    # Ativamos a checagem de Chave Estrangeira (obrigatório no SQLite)
    cur.execute("PRAGMA foreign_keys = ON;")

    cur.execute(f"UPDATE {TableName} SET {AttributeName} = ? WHERE {ID_AttributteName} = ?", (NewAttributeValue, Row_ID))
    if cur.rowcount == 0:
        print(f"Erro: Nenhum/Nenhuma {TableName} encontrado com o ID num.: {Row_ID} informado.")
    else:
        con.commit()
        print("Dado atualizado com sucesso!")
        
def SelectAttribute():

    TableName = input('Qual o nome da tabela? ')
    ColumnName = input('Digite o nome da coluna que deseja visualizar: ') 
    IdColumnName = input(f'Qual o nome da coluna de ID da tabela {TableName}? ')
    Row_ID = input(f'Qual o valor do {IdColumnName} que você quer buscar? ')

    con = sqlite3.connect("escola.db",timeout=10)
    cur = con.cursor()
    # Ativamos a checagem de Chave Estrangeira (obrigatório no SQLite)
    cur.execute("PRAGMA foreign_keys = ON;")

    cur.execute(f"SELECT {ColumnName} FROM {TableName} WHERE {IdColumnName} = ?", (Row_ID,))
    
    resultado = cur.fetchone()

    if resultado is None:
        print(f"Aviso: Nenhum registro encontrado na tabela {TableName} com {IdColumnName} = {Row_ID}.")
    else:
        # O fetchone() sempre retorna uma tupla, ex: ('Matemática',). 
        # Usamos [0] para pegar apenas a string limpa dentro da tupla.
        valor_encontrado = resultado[0]
        print(f"\n--- Resultado da Busca ---")
        print(f"O valor de {ColumnName} é: {valor_encontrado}")
        print("--------------------------\n")

def FillingDictOfColumnsAndValues(TableName):

    CollectedDataDict = {}
    print("\n=== Sistema de Coleta de Dados ===")
    print("Dica: Digite 'sair' no nome do atributo para finalizar a coleta.\n")

    LimitOfInputs = GetColumnsLimit(TableName)

    while True:

        if len(CollectedDataDict) >= LimitOfInputs:
            print("Limite de Atributos para a tabela {TableName} atingido")
            break

        EntityAttribute = input('Qual o atributo? (coluna)').strip()
        
        if EntityAttribute.lower() == 'sair':
            print("Encerrando a coleta de dados...\n")
            break
        if EntityAttribute not in criacao_do_banco.possiveis_valores_atributos:
            print(f"[!] Erro: O atributo '{EntityAttribute}' não existe no banco de dados.")
            print("Verifique a grafia ou consulte os atributos permitidos.\n")
            continue # Volta para o início do loop

        Value = input(f"Qual o valor para '{EntityAttribute}'? ").strip()
        
        if Value.isdigit():
            Value = int(Value) # convertendo em inteiro caso seja numero

        CollectedDataDict[EntityAttribute] = Value
        print(f" -> OK! {EntityAttribute}: {Value} adicionado ao pacote.\n")

    return CollectedDataDict

def InsertEntity(TableName,**kwargs):

    if not kwargs:
        raise ValueError('Nenhum dado inserido para o comando INSERT')

    ColumnsJoinForSQLQuery = ", ".join(kwargs.keys())
    PlaceHolderString = ", ".join(["?"] * len(kwargs))
    ValuesOfKwargsDict = tuple(kwargs.values())

    query = f"INSERT INTO {TableName} ({ColumnsJoinForSQLQuery}) VALUES ({PlaceHolderString})"

    con = sqlite3.connect("escola.db",timeout=10)
    cur = con.cursor()

    cur.execute("PRAGMA foreign_keys = ON;")

    try:
        cur.execute(query, ValuesOfKwargsDict)
        con.commit()
        print(f"Sucesso! Dados inseridos na tabela {TableName} (ID gerado: {cur.lastrowid})")
    except sqlite3.IntegrityError as e:
        print(f"Erro de integridade no banco de dados: {e}")
    finally:
        con.close()

def ExecuteCLI_insert():

    print("\n--- Novo Cadastro ---")
    TableName = input("Digite o nome da Tabela para inserção: (Opções: 'Aluno', 'Contrato_de_Trabalho', 'Curso', 'Leciona', 'Professor', 'Prontuario_Academico': ").strip()

    # essa função retorna o dicionário pronto
    CollectedData = FillingDictOfColumnsAndValues(TableName)

    # checandos se está preenchido. 
    if CollectedData:
        # o uso do operador ** desempacota os dados da variavel CollectedData em dados estruturados
        # Ex: {'nome': 'Gabriel', 'idade': 20} vira -> nome='Gabriel', idade=20 que quando processados pela função 
        # InsertEntity REESTRUTURA eles como string de maneira que consigam ser passados para uma Query de SQLite3 
        # de maneira mais dinâmica
        InsertEntity(TableName, **CollectedData)
    else:
        print("Operação cancelada. Nenhum dado foi inserido.")

def GetColumnsLimit(TableName):

    con = sqlite3.connect("escola.db", timeout=10)
    cur = con.cursor()

    # Retorna uma lista de tuplas, onde cada tupla representa uma coluna
    cur.execute(f"PRAGMA table_info({TableName})")
    colunas = cur.fetchall() 
    
    con.close()

    # O número de colunas é o tamanho da lista.
    # Subtraímos 1 se a Chave Primária (ex: matricula_ID) for autoincremental e não precisar ser digitada.
    return len(colunas) - 1

import sqlite3

def DeleteRow():
    print("\n--- Deletar Registro ---")
    TableName = input('Qual o nome da tabela de onde deseja deletar? ')
    
    IdColumnName = input(f'Qual o nome da coluna de ID da tabela {TableName}? ')
    Row_ID = input(f'Qual o valor do {IdColumnName} que você quer deletar? ')
    
    con = sqlite3.connect("escola.db", timeout=10)
    cur = con.cursor()
    
    cur.execute("PRAGMA foreign_keys = ON;")

    cur.execute(f"DELETE FROM {TableName} WHERE {IdColumnName} = ?", (Row_ID,))
    
    # Verifica se alguma linha foi realmente afetada
    if cur.rowcount == 0:
        print(f"Aviso: Nenhum registro encontrado na tabela {TableName} com {IdColumnName} = {Row_ID}.")
        con.close()
    else:
        # Se deletou, confirmamos a alteração no banco
        con.commit()
        print(f"Sucesso: Registro com {IdColumnName} = {Row_ID} foi deletado da tabela {TableName}.")
        con.close()
