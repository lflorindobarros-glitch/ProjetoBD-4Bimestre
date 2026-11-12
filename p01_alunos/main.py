"""Projeto 01: CRUD de alunos por matricula (com desafios extras)."""
import re
from pymongo.errors import DuplicateKeyError
from conexao import banco

alunos = banco['alunos_p01']
alunos.create_index('matricula', unique=True)  # impede matricula duplicada

# Desafio 1: formato da matricula = apenas numeros, de 4 a 12 digitos.
PADRAO_MATRICULA = re.compile(r'\d{4,12}')


def ler_matricula():
    matricula = input('Matrícula (4 a 12 números): ').strip()
    if not PADRAO_MATRICULA.fullmatch(matricula):
        print('Matrícula inválida: use apenas números (4 a 12 dígitos).')
        return None
    return matricula


while True:
    print('\n[1] Cadastrar [2] Listar [3] Alterar [4] Excluir '
          '[5] Buscar por curso [0] Sair')
    opcao = input('Opção: ').strip()
    if opcao == '1':
        matricula = ler_matricula()
        if matricula is None:
            continue
        nome = input('Nome: ').strip()
        curso = input('Curso: ').strip()
        if not all([nome, curso]):
            print('Preencha todos os campos.')
            continue
        try:
            alunos.insert_one({'matricula': matricula, 'nome': nome, 'curso': curso})
            print('Aluno cadastrado!')
        except DuplicateKeyError:
            print('Matrícula já cadastrada.')
    elif opcao == '2':
        for aluno in alunos.find({}, {'_id': 0}).sort('nome', 1):
            print(aluno)
    elif opcao == '3':
        matricula = ler_matricula()
        if matricula is None:
            continue
        novo_curso = input('Novo curso: ').strip()
        if novo_curso:
            r = alunos.update_one({'matricula': matricula}, {'$set': {'curso': novo_curso}})
            print('Atualizado!' if r.matched_count else 'Aluno não encontrado.')
    elif opcao == '4':
        matricula = ler_matricula()
        if matricula is None:
            continue
        r = alunos.delete_one({'matricula': matricula})
        print('Excluído!' if r.deleted_count else 'Aluno não encontrado.')
    elif opcao == '5':
        # Desafio 2: busca por curso (ignora maiusculas/minusculas).
        trecho = input('Curso (ou parte do nome): ').strip()
        if not trecho:
            print('Informe um termo.')
            continue
        filtro = {'curso': {'$regex': re.escape(trecho), '$options': 'i'}}
        encontrados = list(alunos.find(filtro, {'_id': 0}).sort('nome', 1))
        if not encontrados:
            print('Nenhum aluno encontrado nesse curso.')
        for aluno in encontrados:
            print(aluno)
    elif opcao == '0':
        break
    else:
        print('Opção inválida.')
