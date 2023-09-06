from module_curriculum import Curriculum
from module_curriculum import NewCommand_EducationEntry
from module_curriculum import NewCommand_PersonalEntry
import subprocess

nome = str(input('Seu nome completo: '))
while True:
    value = input('Deseja adicionar um slogan? (s/n): ')
    if value == 's':
        slogan = str(input('Seu slogan: '))
        break
    else:
        slogan = None
        break

cur = Curriculum(nome, slogan=slogan)

file = r'curriculum information\Personal_Entry.txt'
cur.add_information_PersonalEntry(part_name='Informações Pessoais', file_name=file, newcommand=NewCommand_PersonalEntry)

file = r'curriculum information\EducationalEntry.txt'
cur.add_information(part_name='Educação',  file_name=file, newcommand=NewCommand_EducationEntry)

file = r'curriculum information\WorkEntry.txt'
cur.add_information(part_name='Educação',  file_name=file, newcommand=NewCommand_EducationEntry)

file = r'curriculum information\Skills.txt'
cur.add_information_PersonalEntry(part_name='Educação',  file_name=file, newcommand=NewCommand_PersonalEntry)

try:
    cur.create_pdf('pdflatex')
except subprocess.CalledProcessError:
    pass
