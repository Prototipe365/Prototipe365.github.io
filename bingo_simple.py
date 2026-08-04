#!/usr/bin/env python3
"""
Bingo Simple - Un juego de bingo básico en la terminal
"""

import random
import time

def generar_carton():
    """Genera un cartón de bingo aleatorio (5x5)"""
    carton = []
    
    # Columnas B, I, N, G, O con sus respectivos rangos
    rangos = [
        (1, 15),   # B
        (16, 30),  # I
        (31, 45),  # N
        (46, 60),  # G
        (61, 75)   # O
    ]
    
    for rango in rangos:
        numeros = random.sample(range(rango[0], rango[1] + 1), 5)
        carton.append(numeros)
    
    # Transponer para tener filas en lugar de columnas
    carton_transpuesto = []
    for i in range(5):
        fila = [carton[j][i] for j in range(5)]
        carton_transpuesto.append(fila)
    
    # El centro es espacio libre (marcado como 'X')
    carton_transpuesto[2][2] = 'X'
    
    return carton_transpuesto

def mostrar_carton(carton, marcados=None):
    """Muestra el cartón de bingo"""
    if marcados is None:
        marcados = set()
    
    print("\n" + "=" * 35)
    print("  B     I     N     G     O")
    print("=" * 35)
    
    for fila in carton:
        linea = ""
        for num in fila:
            if num == 'X':
                linea += f"  X  "
            elif (fila.index(num), carton.index(fila)) in marcados or num in marcados:
                linea += f"[{num:2}] "
            else:
                linea += f" {num:2}  "
        print(linea)
    
    print("=" * 35)

def sacar_bola(numeros_sacados):
    """Saca una bola aleatoria del bombo"""
    numeros_posibles = list(range(1, 76))
    numeros_disponibles = [n for n in numeros_posibles if n not in numeros_sacados]
    
    if not numeros_disponibles:
        return None
    
    bola = random.choice(numeros_disponibles)
    return bola

def obtener_letra(numero):
    """Obtiene la letra correspondiente al número"""
    if 1 <= numero <= 15:
        return 'B'
    elif 16 <= numero <= 30:
        return 'I'
    elif 31 <= numero <= 45:
        return 'N'
    elif 46 <= numero <= 60:
        return 'G'
    else:
        return 'O'

def verificar_bingo(carton, marcados):
    """Verifica si hay bingo"""
    # Verificar filas
    for i, fila in enumerate(carton):
        completada = True
        for j, num in enumerate(fila):
            if num != 'X' and (i, j) not in marcados and num not in marcados:
                completada = False
                break
        if completada:
            return True
    
    # Verificar columnas
    for j in range(5):
        completada = True
        for i in range(5):
            num = carton[i][j]
            if num != 'X' and (i, j) not in marcados and num not in marcados:
                completada = False
                break
        if completada:
            return True
    
    # Verificar diagonales
    diagonal1 = True
    diagonal2 = True
    
    for i in range(5):
        num1 = carton[i][i]
        num2 = carton[i][4-i]
        
        if num1 != 'X' and (i, i) not in marcados and num1 not in marcados:
            diagonal1 = False
        
        if num2 != 'X' and (i, 4-i) not in marcados and num2 not in marcados:
            diagonal2 = False
    
    if diagonal1 or diagonal2:
        return True
    
    return False

def main():
    print("\n" + "🎰" * 15)
    print("       ¡BIENVENIDO AL BINGO SIMPLE!")
    print("🎰" * 15)
    
    # Generar cartón del jugador
    carton_jugador = generar_carton()
    marcados = set()
    
    # El centro ya está marcado
    marcados.add((2, 2))
    
    numeros_sacados = set()
    
    print("\nTu cartón:")
    mostrar_carton(carton_jugador, marcados)
    
    print("\nInstrucciones:")
    print("- Escribe 's' para sacar una bola")
    print("- Escribe 'm <numero>' para marcar un número en tu cartón")
    print("- Escribe 'v' para verificar si tienes bingo")
    print("- Escribe 'q' para salir")
    
    while True:
        comando = input("\n¿Qué quieres hacer? ").strip().lower()
        
        if comando == 'q':
            print("\n¡Gracias por jugar! Hasta la próxima.")
            break
        
        elif comando == 's':
            bola = sacar_bola(numeros_sacados)
            if bola is None:
                print("\n¡Se han sacado todas las bolas!")
            else:
                numeros_sacados.add(bola)
                letra = obtener_letra(bola)
                print(f"\n🎱 ¡Bola número {bola} ({letra})!")
                print(f"Bolas sacadas: {len(numeros_sacados)}")
                
                # Verificar automáticamente si el número está en el cartón
                encontrado = False
                for i, fila in enumerate(carton_jugador):
                    for j, num in enumerate(fila):
                        if num == bola:
                            encontrado = True
                            print(f"✨ ¡El {bola} está en tu cartón!")
                            break
                    if encontrado:
                        break
                
                if not encontrado:
                    print("El número no está en tu cartón.")
        
        elif comando.startswith('m '):
            try:
                numero = int(comando.split()[1])
                if numero in numeros_sacados:
                    # Buscar el número en el cartón y marcarlo
                    encontrado = False
                    for i, fila in enumerate(carton_jugador):
                        for j, num in enumerate(fila):
                            if num == numero:
                                marcados.add((i, j))
                                encontrado = True
                                print(f"✅ ¡Número {numero} marcado!")
                                break
                        if encontrado:
                            break
                    
                    if not encontrado:
                        print("❌ Ese número no está en tu cartón.")
                else:
                    print("❌ Ese número aún no ha sido sorteado.")
            except (IndexError, ValueError):
                print("❌ Formato inválido. Usa: m <numero>")
        
        elif comando == 'v':
            mostrar_carton(carton_jugador, marcados)
            if verificar_bingo(carton_jugador, marcados):
                print("\n🎉🎉🎉 ¡BINGO! ¡Felicidades, has ganado! 🎉🎉🎉")
                print(f"Números sacados: {len(numeros_sacados)}")
                jugar_otra = input("\n¿Quieres jugar otra vez? (s/n): ").strip().lower()
                if jugar_otra == 's':
                    # Reiniciar juego
                    carton_jugador = generar_carton()
                    marcados = {(2, 2)}
                    numeros_sacados = set()
                    print("\n" + "="*50)
                    print("¡Nuevo juego comenzado!")
                    mostrar_carton(carton_jugador, marcados)
                else:
                    break
            else:
                print("\nAún no tienes bingo. ¡Sigue jugando!")
        
        elif comando == 'c':
            mostrar_carton(carton_jugador, marcados)
        
        else:
            print("Comandos disponibles: s (sacar), m <num> (marcar), v (verificar), c (ver cartón), q (salir)")

if __name__ == "__main__":
    main()
