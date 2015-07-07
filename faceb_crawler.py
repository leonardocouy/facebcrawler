# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from getpass import getpass
from bs4 import BeautifulSoup
from mechanize import Browser
import re

'''
    English
    --------------------------
    The goal of this script is get data of FACEB Academic Zone (My College)
    using BeautifulSoup(http://www.crummy.com/software/BeautifulSoup/) and Mechanize(https://github.com/jjlee/mechanize)
    I'm using BeautifulSoup to Collect/Extract data that are about of HTML tags and
    Mechanize to authenticate and obtaining the source code of the page.

    HOW TO RUN?
        It's recommended to have Python 2.x!!!
        If you prefer to use Python 3.x, you will need install the lib Mechanize Unofficial Version
        Mechanize Unofficial Version: http://web.cecs.pdx.edu/~adevore/mechanize/ and install BeautifulSoup manually.
        1 - Install the requirements in your virtual environment(if you prefer)
            1.1 - Activate your virtualenv
            1.2 - pip install -r requirements.txt
        2 - Run the python script or open the terminal and run manually.
        3 - Follow the instructions and finish!

    Remembering that this script was made for studies and personal use. non-profit.
    This script was made by Leonardo Flores Couy (https://github.com/leonardocouy)
    Study, use and contribute!

    Thanks!

    Brazilian Portuguese
    --------------------------
    O objetivo deste script é extrair informacoes de um portal academico da minha faculdade(FACEB), utilizando
    BeautifulSoup(http://www.crummy.com/software/BeautifulSoup/) e Mechanize(https://github.com/jjlee/mechanize)
    Papel do BeautifulSoup é: Coletar/Extrair dados que estão sobre atributos de tags HTML
    Para autenticação e a obtenção do codigo-fonte da pagina se utiliza a lib
    Mechanize(https://github.com/jjlee/mechanize).

    COMO RODAR?
        É recomendado ter Python 2.x!!!
        Se você preferir usar Python 3.x, você vai precisar instalar a biblioteca Mechanize Versão Não-Oficial
        Mechanize Versão Não-Oficial: http://web.cecs.pdx.edu/~adevore/mechanize/ e instale o BeautifulSoup Manualmente.
        1 - Instale os requirementos no seu ambiente virtual(se você preferir)
            1.1 - Ative seu ambiente virtual
            1.2 - pip install -r requirements.txt
        2 - Rode o script ou abra o terminal e rode manualmente
        3 - Siga as instruções e fim!

    Lembrando que este script foi feito para estudos e para uso pessoal, sem fins lucrativos.
    Este script foi feito por Leonardo Flores Couy (https://github.com/leonardocouy)
    Estude, use e contribua!

    Obrigado!

'''

enrollment = raw_input("Enter the code of your enrollment(E.G: 0011111): ")
password = getpass("Enter your password: ")

url = "http://portal.unipacbomdespacho.com.br/Corpore.Net/Main.aspx?ActionID=" \
      "EduNotaAvaliacaoActionWeb&SelectedMenuIDKey=mnNotasAval"

browser = Browser()
browser.open(url)

''' Perform authentication in Academic Zone '''

browser.select_form(name="Form1")
browser["txtUser"] = enrollment
browser["txtPass"] = password
response = browser.submit()

''' Choose the educational context '''

context_url = "http://portal.unipacbomdespacho.com.br/Corpore.Net/Source/Edu-Educacional/RM.EDU.CONTEXTO/"\
              "EduSelecionarContextoModalWebForm.aspx?Qs=ActionID%3dEduNotaAvaliacaoActionWeb%26SelectedMenuIDKey%3dmn"\
              "NotasAvalCorpore.Net/Main.aspx?ActionID=EduNotaAvaliacaoActionWeb&SelectedMenuIDKey=mnNotasAval"

browser.open(context_url)
bs = BeautifulSoup(browser.response().read())
raw_years = bs.find_all("input", id="rdContexto")
years = [(year.next.text, year.attrs['value']) for year in raw_years]

print("\n----- Contexts -----\n")
for num, context in enumerate(years):
    print("{0}: {1} ".format(num, context[0]))

option = int(input("\nSelect the context year that you like to access: "))
browser.select_form(name="form1")
browser["rdContexto"] = [years[option][1]]
browser.submit()

''' Extracting all grades '''
browser.open(url)
bs = BeautifulSoup(browser.response().read())
raw_stages = bs.find_all('div', attrs={'id': re.compile('ctl23_PanelEtapa\d')})
raw_name_stages = bs.find_all('td', attrs={'class': 'EduCollapsiblePanelCabecalho', 'align': None})
name_stages = [name_stage.string for name_stage in raw_name_stages]

''' Extracting classes of the selected context '''
raw_classes = raw_stages[0].find_all("span", attrs={'class': 'EduLabel'})
classes = [klass.contents[0].string for klass in raw_classes]

''' Showing the stages and grades '''
for name_stage, raw_stage in zip(name_stages, raw_stages):  # (Name Stage, HTML div id="ctl23_PanelEtapa")
                                                            # E.G: 1st Stage, DIV containing all grades.
    raw_stage_grades = raw_stage.find_all("table", attrs={'class': 'EduGridMain'})
    raw_grades = [raw_stage_grade.find_all("tr", attrs={'class': None}) for raw_stage_grade in raw_stage_grades]

    print("{0}\n".format(name_stage.encode('utf-8')))
    for raw_grade, klass in zip(raw_grades, classes):  # (HTML Table, Class) E.G: Table containing the grades, Math
        print(klass + "\n")
        for grade in raw_grade[:-1]:  # Containing evaluations of this klass (Ignoring last item)
            print("Type of Evaluation: {0}".format(grade.contents[1].string.encode('utf-8')))
            print("Date: {0}".format(grade.contents[2].string.encode('utf-8')))
            print("Value of Evaluation: {0}".format(grade.contents[3].string))
            print("Your Value: {0}\n".format(grade.contents[4].string))
        print("Total: {0}".format(raw_grade[-1].contents[4].contents[1]))
        print("------------------")

