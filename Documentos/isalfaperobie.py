def analizar_texto(texto):
    tiene_numeros = False
    tiene_signos = False

    for caracter in texto:
        if caracter.isdigit():
            tiene_numeros = True
        elif not caracter.isalnum() and not caracter.isspace():
            tiene_signos = True

    return tiene_numeros, tiene_signos
