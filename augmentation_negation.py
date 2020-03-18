import re
import pandas as pd
import json

def augmentation_negation(list_negation, re_fetch, match_negation, line):
    lista = [(line[0], line[1])]
    if re.search(re_fetch, line[0]) != None and re.search(re_fetch, line[1]) != None:
        for index, word_neg in enumerate(list_negation):
            if index == 20:
                break

            print(f'Frase: {line[0]} --- frase(gi): {line[1]}')
            word_neg_split = word_neg[0].split('_')[1]
            fetch_word = match_negation["\\b(" + word_neg_split + ")\\b"]
            print(f'fetch_word = {word_neg_split} --- match_negation[fetch_word] = {fetch_word}')
            lista.append((re.sub(re_fetch, fetch_word, line[0]), re.sub(re_fetch, fetch_word, line[1])))

    return lista

df_negation = pd.read_csv('negacao.csv')

list_negation = df_negation.values.tolist()

fetching_expression = ""
match_negation = {}

for neg in list_negation:
    word = neg[0].split('_')[1]
    fetching_expression += "\\b(" + word.upper() + ")\\b|"
    match_negation[r'\b(' + word.upper() + r')\b'] = "(" + neg[0].upper() + ")"

#print(json.dumps(match_negation, indent=4))

fetching_expression[:-1]
re_fetch = r"" + fetching_expression

#print(re_fetch)

teste_frases = [('WEINTRAUB CONVERSAR JAIR BOLSONARO', 'WEINTRAUB&FAMOSO CONVERSAR JAIR_BOLSONARO&FAMOSO'), ('WEINTRAUB SAIR', 'WEINTRAUB&FAMOSO SAIR'),
                ('JOHN LENNON IR CASA', 'JOHN_LENNON&FAMOSO IR CASA'), ('HARRY POTTER CONVERSAR HITLER', 'HARRY_POTTER&FAMOSO CONVERSAR HITLER&FAMOSO'),
                ('OPA', 'OPA')]
                

for i in teste_frases:
    print(augmentation_negation(list_negation, re_fetch, match_negation, i))

