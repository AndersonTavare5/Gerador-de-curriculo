from module_curriculum import Curriculum
from module_curriculum import NewCommand_EducationEntry
from module_curriculum import NewCommand_PersonalEntry
import subprocess

text_error = 'Opção inválida: Digite corretamente o número da opção.\n\n'


def menu_apresentacao():
    text = '''
    Verifique que a pasta 'Informacoes curriculo' está na mesma pasta que
    esse executável e que dentro dele esteja os seguintes arquivos .txt:
    [EducationaEntry, PersonalEntry, Skills, WorkEntry]

    Caso esses arquivos estiverem com os nomes errados, o programa não
    executará com sucesso.

    Verifique também se as informações dentro dos aquivos estão corretas
    e formatadas corretamente. Deve haver um 'TAB' separando cada uma das
    informações em cada linha.

    EducationalEntry e WorkEntry possuem 4 informações por linha
    PersonalEntry e Skills possuem 3 informações por linha (sendo a primeira
        uma referência se a para o programa saber se o que será adicionado
        é ou não um link)

    Informe o seu nome completo e em seguida escolha se deseja ou não
    adicionar um slogan para o seu currículo.

    '''
    print(text)


def menu_compiler():
    text = '''
    Escolha o compilador. Digite o número da opção que representa o
    compilador que está instalado no seu computador. Tenha certeza de
    ter instalado o Miktex na sua máquina.

    1 - pdflatex (recomendado)
    2 - latexmk
    3 - gerar apenas arquivo .tex
    4 - cancelar ação

    '''
    print(text)
    while True:
        try:
            escolha = int(input("Digite sua escolha: "))
            lista = ['pdflatex', 'latexmk', 'tex', 'quit']
            return lista[escolha-1]
        except ValueError:
            print(text_error)
        except IndexError:
            print(text_error)


menu_apresentacao()
nome = str(input('Seu nome completo: '))
while True:
    value = input('Deseja adicionar um slogan? (s/n): ').lower().strip()
    if value == 's':
        slogan = str(input('Seu slogan: '))
        break
    else:
        slogan = None
        break

cur = Curriculum(nome, slogan=slogan)

while True:
    try:
        file = r'Informacoes curriculo\PersonalEntry.txt'
        cur.add_information_PersonalEntry(part_name='Informações Pessoais', file_name=file, newcommand=NewCommand_PersonalEntry)

        file = r'Informacoes curriculo\EducationalEntry.txt'
        cur.add_information(part_name='Educação',  file_name=file, newcommand=NewCommand_EducationEntry)

        file = r'Informacoes curriculo\WorkEntry.txt'
        cur.add_information(part_name='Educação',  file_name=file, newcommand=NewCommand_EducationEntry)

        file = r'Informacoes curriculo\Skills.txt'
        cur.add_information_PersonalEntry(part_name='Educação',  file_name=file, newcommand=NewCommand_PersonalEntry)

        esc = menu_compiler()
        if esc in ['pdflatex', 'latexmk']:
            cur.create_pdf(esc)
        elif esc == 'tex':
            cur.create_tex()
        break

    except subprocess.CalledProcessError:
        print("Compilador não encontrado ou com erro.")
        esc = input('Deseja tentar de novo? (s/n): ').lower().strip()
        if esc == 's':
            continue
        else:
            break

    except FileNotFoundError:
        text = '''
    Arquivo não encontrado.

    Confira se baixou a pasta com os arquivos txt e que não alterou o nome
    dos arquivos nem da pasta e tente novamente'''
        print(text)
        input('Pressione ENTER para fechar o programa')
        break