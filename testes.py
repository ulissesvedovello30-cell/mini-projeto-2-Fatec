frutas = [("maçã", "vermelha"), ("banana", "amarela"), ("morango", "vermelha")]

por_cor = {}
for fruta, cor in frutas:
    if cor not in por_cor:
        por_cor[cor] = []
    por_cor[cor].append(fruta)

print(por_cor)