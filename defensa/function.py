def agregar_parentesis(self, lista_nombres):
        resultado_final = []
    
        for cadena in lista_nombres:
            longitud = len(cadena)
            resultado = []

            mitad = longitud // 2

            for i, char in enumerate(cadena):
                if i < mitad:
                    if i > 0:
                        resultado.append('(')
                    resultado.append(char)
                elif longitud % 2 == 0 and i == mitad:
                    resultado.append(char)
                    resultado.append(')')
                elif longitud % 2 == 0 and i == mitad + 1:
                    resultado.append(char)
                else:
                    resultado.append(char)
                    if i < longitud - 1:
                        resultado.append(')')

            resultado_final.append(''.join(resultado))

        return resultado_final
