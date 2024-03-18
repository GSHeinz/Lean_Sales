import requests
import sqlite3

# NOME PARA PESQUISA DO VENDEDOR: gustavo

def buscar_dados_cnpj(cnpj):
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro na solicitação: {response.status_code}")
        return None

def criar_tabela():
    conn = sqlite3.connect('empresas.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS empresas (
                    cnpj TEXT PRIMARY KEY,
                    situacao TEXT,
                    tipo TEXT,
                    nome TEXT,
                    natureza_juridica TEXT,
                    porte TEXT,
                    atividade_principal TEXT,
                    logradouro TEXT,
                    numero TEXT,
                    bairro TEXT,
                    municipio TEXT,
                    uf TEXT,
                    cep TEXT,
                    telefone TEXT,
                    numero_funcionarios TEXT,
                    faturamento_anual TEXT,
                    vendedor_responsavel TEXT
                    )''')
    conn.commit()
    conn.close()

def inserir_empresa(cnpj, dados_empresa):
    conn = sqlite3.connect('empresas.db')
    cursor = conn.cursor()

    atividades_principais = ', '.join([atividade['text'] for atividade in dados_empresa['atividade_principal']])

    cursor.execute('''INSERT OR REPLACE INTO empresas (cnpj, situacao, tipo, nome, natureza_juridica, porte, atividade_principal, logradouro, numero, bairro, municipio, uf, cep, telefone)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (cnpj, dados_empresa['situacao'], dados_empresa['tipo'], dados_empresa['nome'],dados_empresa['natureza_juridica'], 
                    dados_empresa['porte'], atividades_principais, dados_empresa['logradouro'],dados_empresa['numero'],
                    dados_empresa['bairro'], dados_empresa['municipio'], dados_empresa['uf'], dados_empresa['cep'], dados_empresa['telefone']))
    conn.commit()
    conn.close()
    

def consultar_empresas(vendedor_responsavel):
    conn = sqlite3.connect('empresas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM empresas WHERE vendedor_responsavel=?', (vendedor_responsavel,))
    empresas = cursor.fetchall()
    conn.close()
    return empresas

def listar_cnpjs():
    conn = sqlite3.connect('empresas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT cnpj FROM empresas')
    cnpjs = cursor.fetchall()
    conn.close()
    return cnpjs

def alterar_dados_empresa(cnpj, campo, novo_valor):
    conn = sqlite3.connect('empresas.db')
    cursor = conn.cursor()
    cursor.execute(f'UPDATE empresas SET {campo}=? WHERE cnpj=?', (novo_valor, cnpj))
    conn.commit()
    conn.close()

def main():
    criar_tabela()

    while True:
        print("\nMenu:")
        print("1. Inserir dados de empresa")
        print("2. Consultar empresa pelo vendedor")
        print("3. Alterar dados de empresa")
        print("4. Listar todos os CNPJs cadastrados")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cnpj = input("Digite o CNPJ da empresa: ")
            dados_empresa = buscar_dados_cnpj(cnpj)
            if dados_empresa:
                inserir_empresa(cnpj, dados_empresa)
                print("Dados da empresa inseridos com sucesso!")
            else:
                print("CNPJ não encontrado ou inválido.")
        
        elif opcao == '2':
            vendedor_responsavel = input("Digite o vendedor responsável da empresa: ")
            empresas = consultar_empresas(vendedor_responsavel)
            if empresas:
                print("Dados das empresas:")
                for empresa in empresas:
                    print("-----------")
                    print(f"CNPJ: {empresa[0]}")
                    print(f"Situação: {empresa[1]}")
                    print(f"Tipo: {empresa[2]}")
                    print(f"Nome: {empresa[3]}")
                    print(f"Natureza Jurídica: {empresa[4]}")
                    print(f"Porte: {empresa[5]}")
                    print(f"Atividade Principal: {empresa[6]}")
                    print(f"Logradouro: {empresa[7]}")
                    print(f"Número: {empresa[8]}")
                    print(f"Bairro: {empresa[9]}")
                    print(f"Município: {empresa[10]}")
                    print(f"UF: {empresa[11]}")
                    print(f"CEP: {empresa[12]}")
                    print(f"Telefone: {empresa[13]}")
                    print(f"Número de Funcionários: {empresa[14]}")
                    print(f"Faturamento Anual: {empresa[15]}")
                    print(f"Vendedor Responsável: {empresa[16]}")
                    print("-----------")
            else:
                print("Nenhuma empresa encontrada para o vendedor responsável informado.")

        elif opcao == '3':
            cnpj = input("Digite o CNPJ da empresa: ")
            campo = input("Digite o campo que deseja alterar: ")
            novo_valor = input("Digite o novo valor: ")
            alterar_dados_empresa(cnpj, campo, novo_valor)
            print("Dados da empresa atualizados com sucesso!")

        elif opcao == '4':
            cnpjs = listar_cnpjs()
            if cnpjs:
                print("CNPJs cadastrados:")
                for cnpj in cnpjs:
                    print(cnpj[0])
            else:
                print("Nenhuma empresa cadastrada.")

        elif opcao == '5':
            print("Saindo...")
            break
        
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()
