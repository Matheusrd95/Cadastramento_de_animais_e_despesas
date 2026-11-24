# -*- coding: utf-8 -*-
"""Sistema de Gestão de Fauna e Bem-Estar com resumo simples via IA."""

import json
import os
from datetime import datetime
from google import genai
from google.genai import types

# ==========================================
# 1. MANIPULAÇÃO DE ARQUIVO (PERSISTÊNCIA)
# ==========================================
ARQUIVO_DADOS = 'dados_fauna.json'

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    return {"animais": [], "fornecedores": [], "despesas": []}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

# ==========================================
# 2. FUNÇÕES BÁSICAS (REGRAS DE NEGÓCIO E CRUD)
# ==========================================
def registrar_novo_animal(nome, status_geral, especie, status_castracao, localizacao):
    dados = carregar_dados()
    novo_id = len(dados['animais']) + 1
    data_atual = datetime.now().strftime("%Y-%m-%d")

    novo_animal = {
        "id": novo_id,
        "nome": nome,
        "status_geral": status_geral,
        "especie": especie,
        "status_castracao": status_castracao,
        "localizacao_campus": localizacao,
        "data_registro": data_atual
    }

    dados['animais'].append(novo_animal)
    salvar_dados(dados)
    print(f"\n✅ Sucesso! Animal '{nome}' cadastrado com o ID: {novo_id}")

def editar_animal(animal_id):
    dados = carregar_dados()
    encontrou = False

    for animal in dados['animais']:
        if animal['id'] == int(animal_id):
            encontrou = True
            print(f"\n--- EDITANDO ANIMAL: {animal['nome']} ---")
            print("Dica: Deixe em branco e aperte ENTER para manter a informação atual.")

            # O .get() previne erros caso leia um dado antigo que não tinha essa chave
            status_atual = animal.get('status_geral', 'Ativo')

            novo_nome = input(f"Nome atual ({animal['nome']}): ")
            if novo_nome.strip() != "": animal['nome'] = novo_nome

            novo_status = input(f"Status atual ({status_atual}): ")
            if novo_status.strip() != "": animal['status_geral'] = novo_status

            nova_esp = input(f"Espécie atual ({animal['especie']}): ")
            if nova_esp.strip() != "": animal['especie'] = nova_esp

            novo_cast = input(f"Status Castração atual ({animal['status_castracao']}): ")
            if novo_cast.strip() != "": animal['status_castracao'] = novo_cast

            novo_loc = input(f"Localização atual ({animal['localizacao_campus']}): ")
            if novo_loc.strip() != "": animal['localizacao_campus'] = novo_loc

            break

    if encontrou:
        salvar_dados(dados)
        print(f"\n✅ Sucesso! Cadastro atualizado.")
    else:
        print("\n❌ Erro: ID do animal não encontrado.")

def registrar_novo_fornecedor(nome, servico, telefone):
    dados = carregar_dados()
    novo_id = len(dados['fornecedores']) + 1

    novo_fornecedor = {
        "id": novo_id,
        "nome_empresa": nome,
        "servico_oferecido": servico,
        "telefone": telefone
    }

    dados['fornecedores'].append(novo_fornecedor)
    salvar_dados(dados)
    print(f"\n✅ Sucesso! Fornecedor '{nome}' homologado com o ID: {novo_id}")

def registrar_nova_despesa(animal_id, fornecedor_id, descricao, valor):
    dados = carregar_dados()
    novo_id = len(dados['despesas']) + 1
    data_atual = datetime.now().strftime("%Y-%m-%d")

    nova_despesa = {
        "id": novo_id,
        "animal_id": int(animal_id),
        "fornecedor_id": int(fornecedor_id),
        "descricao": descricao,
        "valor": float(valor),
        "data_despesa": data_atual
    }

    dados['despesas'].append(nova_despesa)
    salvar_dados(dados)
    print(f"\n✅ Sucesso! Despesa de R$ {float(valor):.2f} registrada no sistema.")

# ==========================================
# 3. MÓDULOS DE RELATÓRIO E VISUALIZAÇÃO
# ==========================================
def gerar_relatorio_animais():
    print("\n" + "="*85)
    print("📋 RELATÓRIO OPERACIONAL: ANIMAIS CADASTRADOS")
    print("="*85)

    dados = carregar_dados()
    animais = dados['animais']

    if not animais:
        print("Nenhum animal cadastrado no sistema ainda.")
        print("="*85)
        return

    # Cabeçalho atualizado com a nova ordem: ID, NOME, STATUS GERAL...
    print(f"{'ID':<4} | {'NOME':<12} | {'STATUS GERAL':<12} | {'ESPÉCIE':<8} | {'CASTRAÇÃO':<12} | {'LOCALIZAÇÃO':<18}")
    print("-" * 85)

    for a in animais:
        # Usa .get() para não dar erro em cadastros antigos que não tinham o status_geral
        status = a.get('status_geral', 'Ativo')
        print(f"{a['id']:<4} | {a['nome']:<12} | {status:<12} | {a['especie']:<8} | {a['status_castracao']:<12} | {a['localizacao_campus']:<18}")

    print("="*85 + "\n")

def gerar_relatorio_governanca():
    print("\n" + "="*85)
    print("📊 RELATÓRIO EXECUTIVO DE GOVERNANÇA E CUSTOS")
    print("="*85)

    dados = carregar_dados()

    if not dados['despesas']:
        print("Nenhuma despesa registrada ainda.")
        print("="*85 + "\n")
        return

    mapa_fornecedores = {f['id']: f['nome_empresa'] for f in dados['fornecedores']}
    resumo_gastos = {}

    for despesa in dados['despesas']:
        id_forn = despesa['fornecedor_id']
        valor = despesa['valor']

        if id_forn not in resumo_gastos:
            resumo_gastos[id_forn] = {
                "nome": mapa_fornecedores.get(id_forn, "Fornecedor Desconhecido"),
                "qtd_servicos": 0,
                "custo_total": 0.0
            }

        resumo_gastos[id_forn]["qtd_servicos"] += 1
        resumo_gastos[id_forn]["custo_total"] += valor

    gastos_ordenados = sorted(resumo_gastos.values(), key=lambda x: x['custo_total'], reverse=True)

    print("CUSTOS CONSOLIDADOS POR FORNECEDOR:")
    for item in gastos_ordenados:
        print(f" - {item['nome']:<20} | Serviços: {item['qtd_servicos']:<3} | Custo Total: R$ {item['custo_total']:.2f}")

    print("="*85 + "\n")

# ==========================================
# 4. RESUMO SIMPLES COM IA (LLM)
# ==========================================
def gerar_resumo_ia():
    chave = os.environ.get("GEMINI_API_KEY")
    if not chave:
        print("\n⚠️ Configure a variável GEMINI_API_KEY antes de usar o resumo com IA.")
        return

    dados = carregar_dados()
    if not dados["animais"] and not dados["despesas"]:
        print("\n⚠️ Não há dados cadastrados ainda para gerar um resumo.")
        return

    prompt = f"""
    Leia os dados abaixo em JSON e faça um resumo curto e direto em português com:
    1. Quantidade de animais e pendências de castração.
    2. Resumo das despesas e fornecedores.
    3. Uma recomendação prática do que priorizar agora.
    Use apenas as informações presentes nos dados.

    DADOS:
    {json.dumps(dados, ensure_ascii=False, indent=2)}
    """

    try:
        client = genai.Client(api_key=chave)
        resposta = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.2),
        )
        print("\n" + "="*85)
        print("🤖 RESUMO GERADO COM IA")
        print("="*85)
        print(resposta.text)
        print("="*85 + "\n")
    except Exception as e:
        print(f"\n❌ Erro ao chamar a IA: {e}")

# ==========================================
# 5. INTERFACE DE USUÁRIO (MENU INTERATIVO)
# ==========================================
def exibir_menu():
    while True:
        print("\n" + "="*45)
        print("🐾 SISTEMA DE GESTÃO DE FAUNA E BEM-ESTAR")
        print("="*45)
        print("1. Cadastrar Novo Animal")
        print("2. Editar Cadastro de Animal")
        print("3. Cadastrar Novo Fornecedor")
        print("4. Registrar Nova Despesa")
        print("5. Ver Tabela de Animais Cadastrados")
        print("6. Ver Relatório Executivo de Custos")
        print("7. Gerar Resumo Simples com IA")
        print("0. Sair do Sistema")
        print("="*45)

        opcao = input("Escolha uma opção (0-7): ").strip()

        if opcao == '1':
            print("\n--- CADASTRO DE ANIMAL ---")
            nome = input("Nome do animal: ")
            status_geral = input("Status do Animal (Ativo, Inativo, Adotado): ")
            especie = input("Espécie (ex: Cão, Gato, Ave): ")
            status_cast = input("Status Castração (Castrado, Pendente): ")
            local = input("Localização: ")
            registrar_novo_animal(nome, status_geral, especie, status_cast, local)

        elif opcao == '2':
            print("\n--- ATUALIZAÇÃO DE CADASTRO ---")
            gerar_relatorio_animais()
            animal_id = input("\nDigite o ID do animal que deseja editar: ")
            try:
                editar_animal(animal_id)
            except ValueError:
                print("❌ Erro: O ID precisa ser um número.")

        elif opcao == '3':
            print("\n--- HOMOLOGAÇÃO DE FORNECEDOR ---")
            nome = input("Nome da Empresa/Clínica: ")
            servico = input("Serviço Oferecido (ex: Ração, Veterinário): ")
            telefone = input("Telefone de Contato: ")
            registrar_novo_fornecedor(nome, servico, telefone)

        elif opcao == '4':
            print("\n--- REGISTRO DE DESPESA ---")
            animal_id = input("ID do Animal atendido: ")
            forn_id = input("ID do Fornecedor acionado: ")
            desc = input("Descrição do Serviço/Produto: ")
            valor = input("Valor Total (use ponto para centavos, ex: 150.50): ")
            try:
                registrar_nova_despesa(animal_id, forn_id, desc, valor)
            except ValueError:
                print("❌ Erro: Certifique-se de digitar números válidos para IDs e Valor.")

        elif opcao == '5':
            gerar_relatorio_animais()

        elif opcao == '6':
            gerar_relatorio_governanca()

        elif opcao == '7':
            gerar_resumo_ia()

        elif opcao == '0':
            print("\nEncerrando o sistema. Até logo!\n")
            break

        else:
            print("\n❌ Opção inválida. Tente novamente.")

# ==========================================
# 5. INICIALIZAÇÃO
# ==========================================
if __name__ == "__main__":
    exibir_menu()
