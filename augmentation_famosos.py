import re
import random
import pandas as pd
import json

def augmentation_famosos(line, re_gr, re_gi, famososExamples_gr, famososExamples_gi, dict_gr, dict_gi):
    lista = list()
    
    line_gr = line[0]
    line_gi = line[1]
    
    occurences_gr = re.findall(re_gr, line_gr)
    occurences_gi = re.findall(re_gi, line_gi)
    
    lista.append((line_gr, line_gi))
    if occurences_gr != [] and occurences_gi != [] and len(occurences_gr) == len(occurences_gi):
        print('Entrei')
        for index, (famoso_gr, famoso_gi) in enumerate(list(zip(famososExamples_gr, famososExamples_gi))):
            if index == 50:
                break 
            
            if re.search(dict_gr[famoso_gr], line_gr) == None and re.search(dict_gi[famoso_gi], line_gi) == None:
                lista.append((re.sub(re_gr, famoso_gr, line_gr, 1), re.sub(re_gi, famoso_gi, line_gi, 1)))
        
        return lista
    
    return lista          

df_famosos = pd.read_csv('data/famosos_teste.csv')

famosos_gr, famosos_gi = df_famosos['gr'].values.tolist(), df_famosos['gi'].values.tolist()
combined_gr = ""
combined_gi = ""
match_famoso_gr = {}
match_famoso_gi = {}

for (famoso_gr, famoso_gi) in list(zip(famosos_gr, famosos_gi)):
    lista_gr = famoso_gr.split(' ')
    lista_gi = famoso_gi.split('_')
    match_famoso_gr[famoso_gr] = ""
    match_famoso_gi[famoso_gi] = ""
    combined_gr += "("
    combined_gi += "("
    
    for i in range(0, len(lista_gr) - 1):
        combined_gr += "(\\b" + (lista_gr[i]) + "\\b)(\s|_)"
        match_famoso_gr[famoso_gr] += "(\\b" + (lista_gr[i]) + "\\b)?(\s|_)?"
    for j in range(0, len(lista_gi) - 1):
        combined_gi += "(" + (lista_gi[j]) + "_)"
        match_famoso_gi[famoso_gi] += "(" + (lista_gi[j]) + "_)?"
    
    combined_gr += "(\\b" + (''.join(lista_gr[-1:])) + "\\b))|"
    match_famoso_gr[famoso_gr] += "(\\b" + (''.join(lista_gr[-1:])) + "\\b)"
    match_famoso_gr[famoso_gr] = r"" + match_famoso_gr[famoso_gr]

    combined_gi += "" + (''.join(lista_gi[-1:])) + ")|"
    match_famoso_gi[famoso_gi] += "((" + (''.join(lista_gi[-1:])) + "))"
    match_famoso_gi[famoso_gi] = r"" + match_famoso_gi[famoso_gi]
    
combined_gr = combined_gr[:-1]
re_gr = r"" + combined_gr
combined_gi = combined_gi[:-1]
re_gi = r"" + combined_gi

teste_frases = [('WEINTRAUB CONVERSAR BOLSONARO', 'WEINTRAUB&FAMOSO CONVERSAR BOLSONARO&FAMOSO'), ('ABRAHAM WEINTRAUB SAIR', 'ABRAHAM_WEINTRAUB&FAMOSO SAIR'),
                ('JOHN LENNON IR CASA', 'JOHN_LENNON&FAMOSO IR CASA'), ('HARRY POTTER CONVERSAR HITLER', 'HARRY_POTTER&FAMOSO CONVERSAR HITLER&FAMOSO'),
                ('OPA', 'OPA'), ('MICHELLE BOLSONARO CONVERSAR EDUARDO BOLSONARO', 'MICHELLE_BOLSONARO&FAMOSO CONVERSAR EDUARDO_BOLSONARO&FAMOSO'), ('ELE SER GRANDE SER ALEXANDRE GRANDE', 'ELE SER GRANDE SER ALEXANDRE_GRANDE&FAMOSO')]

for i in teste_frases:
    print(*augmentation_famosos(i, re_gr, re_gi, famosos_gr, famosos_gi, match_famoso_gr, match_famoso_gi), sep='\n')
    print()
