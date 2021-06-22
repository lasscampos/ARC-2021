#!/usr/bin/python3
import random
# Função de entrada dos dados
def entrada():
    dados_txt = input("Por favor, informe a quantidade de dados: ")
    dados_int = int(dados_txt)

    faces_txt = input("Agora, informe a quantidade maxima de faces: ")
    faces_int = int(faces_txt)

    return dados_int, faces_int

# Programa principal
dados, faces = entrada()

# Saída de dados: valor de cada dao inividual e soma ao final
somatorio = 0
for rodada in range(1, dados + 1):
    aleatorio = random.randint(1, faces) 
    somatorio = somatorio + aleatorio
print("--#--")
