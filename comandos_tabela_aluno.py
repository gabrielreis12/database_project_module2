import sqlite3
import criacao_do_banco

# d    IterableOfTablesNames = ", ".join(args)


# pensei em utilizar o kwargs** para deixar o código mais flexível na mudança de informações do banco

def UpdateAttribute(TableName, AttributeType, NewAttributeValue, EntityID):

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
    PlaceholderString = ", ".join(["?"] * len(kwargs))
    ValuesOfKwargsDict = tuple(kwargs.values())

    query = query = f"INSERT INTO {TableName} ({ColumnsJoinForSQLQuery}) VALUES ({PlaceholderString})"

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
    TableName = input("Digite o nome da Tabela para inserção:\n Opções: 'Aluno', 'Contrato_de_Trabalho', 'Curso', 'Leciona', 'Professor', 'Prontuario_Academico'").strip()

    if TableName not in criacao_do_banco.possiveis_valores_tabelas:
        raise ValueError('[!] Erro: A tabela "{TableName}" é inválida. Nenhum dado inserido para o comando INSERT')

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