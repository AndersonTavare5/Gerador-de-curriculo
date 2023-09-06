from pylatex.base_classes import CommandBase, Arguments
from pylatex import Document, NoEscape, Command, UnsafeCommand
from pylatex.package import Package

# Opções do Documento
document_options = [r'paper=a4',
                    r'fontsize=11pt']

# Macros


class NewCommand_MyName(CommandBase):
    _latex_name = 'MyName'


class NewCommand_MySlogan(CommandBase):
    _latex_name = 'MySlogan'


class NewCommand_NewPart(CommandBase):
    _latex_name = 'NewPart'


class NewCommand_PersonalEntry(CommandBase):
    _latex_name = 'PersonalEntry'


class NewCommand_EducationEntry(CommandBase):
    _latex_name = 'EducationEntry'


MyName = UnsafeCommand('newcommand', r'\MyName', options=1,
                       extra_arguments=r'''
                       \huge \usefont{OT1}{phv}{b}{n} \hfill \textit{#1}
                       \par \normalsize \normalfont''')

MySlogan = UnsafeCommand('newcommand', r'\MySlogan', options=1,
                         extra_arguments=r'''
                         \large \usefont{OT1}{phv}{m}{n}\hfill \textit{#1}
                         \par \normalsize \normalfont ''')

Personal_Entry = UnsafeCommand('newcommand', r'\PersonalEntry', options=2,
                               extra_arguments=r'''
                               \noindent\hangindent=2em\hangafter=0
                               \parbox{\spacebox}{\textit{#1}} \hspace{1.5em} #2 \par''')

EducationEntry = UnsafeCommand('newcommand', r'\EducationEntry', options=4,
                               extra_arguments=r'''
                               \noindent \textbf{#1} \hfill
                               \colorbox{Black}{
                               \parbox{6em}{
                               \hfill\color{White}#2}} \par
                               \noindent \textit{#3} \par
                               \noindent\hangindent=2em\hangafter=0 \small #4
                               \normalsize \par''')

NewPart = UnsafeCommand('newcommand', r'\NewPart', options=1,
                        extra_arguments=r'\section*{\uppercase{#1}}')

# Main class


class Curriculum:
    def __init__(self, name, slogan=None):
        self.doc = Document(name + ' - Curriculum', documentclass='scrartcl',
                            document_options=document_options)
        self._load_package()
        self._set_parameters()
        self._load_macros()

        self.doc.append(NewCommand_MyName(arguments=Arguments(name)))
        if slogan != None:
            self.doc.append(NewCommand_MySlogan(arguments=Arguments(slogan)))

    def _load_package(self):
        packages = [Package('babel', 'brazil'),
                    Package('inputenc', 'utf8'),
                    Package('microtype', ['protrusion=true', 'expansion=true']),
                    Package('amsmath,amsfonts,amsthm'),
                    Package('graphicx'),
                    Package('xcolor', 'svgnames'),
                    Package('geometry'),
                    Package('sectsty'),
                    Package('url')]
        self.doc.packages = packages

    def _set_parameters(self):
        self.doc.preamble.append(NoEscape(r'\textheight=700px'))
        self.doc.preamble.append(NoEscape(r'\frenchspacing'))
        prompt = r'\usefont{OT1}{phv}{b}{n} \sectionrule{0pt}{0pt}{-5pt}{3pt}'
        self.doc.preamble.append(Command('sectionfont', NoEscape(prompt)))
        self.doc.preamble.append(Command('pagestyle', 'empty'))
        self.doc.preamble.append(Command('newlength', NoEscape(r'\spacebox')))
        self.doc.preamble.append(UnsafeCommand('settowidth', r'\spacebox',
                                               extra_arguments='8888888888'))
        self.doc.preamble.append(UnsafeCommand('newcommand', r'\sepspace',
                                               extra_arguments=r'\vspace*{1em}'))

    def _load_macros(self):
        self.doc.preamble.append(MyName)
        self.doc.preamble.append(MySlogan)
        self.doc.preamble.append(NewPart)
        self.doc.preamble.append(Personal_Entry)
        self.doc.preamble.append(EducationEntry)

    def create_part(self, part_name):
        self.doc.append(NewCommand_NewPart(arguments=Arguments(part_name)))

    def add_information_PersonalEntry(self, part_name, file_name, newcommand=None):
        self.create_part(part_name)
        file = open(file=file_name, encoding='utf8')
        while True:
            line = file.readline()
            if not line:
                break
            line = list(map(NoEscape, line.strip('\n').split(sep='\t')))
            if line[0] == 'link':
                self.doc.append(newcommand(arguments=Arguments(line[1], Command('url', line[2]))))
            else:
                self.doc.append(newcommand(arguments=Arguments(*line[1:])))
        file.close()

    def add_information(self, part_name, file_name, newcommand=None):
        self.create_part(part_name)
        file = open(file=file_name, encoding='utf8')
        while True:
            line = file.readline()
            if not line:
                break
            line = list(map(NoEscape, line.strip('\n').split(sep='\t')))
            self.doc.append(newcommand(arguments=Arguments(*line)))
            self.doc.append(NoEscape(r'\sepspace'))
        file.close()

    def create_pdf(self, compiler):
        self.doc.generate_pdf(compiler=compiler)

    def create_tex(self):
        self.doc.generate_tex()
