
import comandos_tabela_aluno


print('Olá! Qual comando deseja realizar?')
InitialInput = input(' 1. INSERT\n 2. UPDATE\n 3. DELETE\n 4. SELECT\n').strip()

match InitialInput:
    case '1':
        ReceivedInput = 'INSERT'
        print(f'COMANDO SELECIONADO: \n {ReceivedInput}')
        comandos_tabela_aluno.ExecuteCLI_insert()

    case '2':
        ReceivedInput = 'UPDATE'
        print(f'COMANDO SELECIONADO: \n {ReceivedInput}')
        comandos_tabela_aluno.UpdateAttribute()

    case '3':
        ReceivedInput = 'DELETE'
        print(f'COMANDO SELECIONADO: \n {ReceivedInput}')
        comandos_tabela_aluno.DeleteRow()

    case '4':
        ReceivedInput = 'SELECT'
        print(f'COMANDO SELECIONADO: \n {ReceivedInput}')
        comandos_tabela_aluno.SelectAttribute()
    case _:
        print("No COMMANDS match")