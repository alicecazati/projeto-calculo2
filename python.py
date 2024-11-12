import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad  


# Função para simplificar o polinômio somando termos de mesmo grau
def simplificar_polinomio(coef, graus):
    termos_simplificados = {}
    for c, g in zip(coef, graus):
        if g in termos_simplificados:
            termos_simplificados[g] += c
        else:
            termos_simplificados[g] = c
    # Ordenar em ordem decrescente de grau
        graus_simplificados, coef_simplificados = zip(*sorted(termos_simplificados.items(), key=lambda x: x[0], reverse=True))
    return coef_simplificados, graus_simplificados

# Função para calcular o polinômio e sua integral
def calcular_polinomio_e_integral(coef, graus, intervalo_min, intervalo_max, passo):
    x_values = np.arange(intervalo_min, intervalo_max + passo, passo)
    y_polinomio = np.zeros_like(x_values)
    y_integral = np.zeros_like(x_values)

    for c, g in zip(coef, graus):
        y_polinomio += c * x_values ** g
        y_integral += c / (g + 1) * x_values ** (g + 1)

    return x_values, y_polinomio, y_integral

# Função para reconstruir a equação do polinômio e a integral
def construir_equacao_polinomio_e_integral(coeficientes, graus):
    termos = []
    termos_integral = []
    
    termos_polinomio = list(zip(coeficientes, graus))
    termos_polinomio.sort(key=lambda x: x[1], reverse=True)

    for coef, grau in termos_polinomio:
        if coef == 0:
            continue  

        # Formatar o termo do polinômio
        if grau == 0:
            termo = f"{coef}"
        elif grau == 1:
            termo = f"{coef}x" if coef != 1 else "x"
        else:
            termo = f"{coef}x^{grau}" if coef != 1 else f"x^{grau}"

        termos.append(termo)

        # Calcular e formatar o termo da integral
        coef_integral = coef / (grau + 1)
        grau_integral = grau + 1

        if grau_integral == 0:
            termo_integral = f"{coef_integral}"  # Constante
        elif grau_integral == 1:
            termo_integral = f"{coef_integral}x" if coef_integral != 1 else "x"
        else:
            termo_integral = f"{coef_integral}x^{grau_integral}" if coef_integral != 1 else f"x^{grau_integral}"

        termos_integral.append(termo_integral)

    if not termos:
        return "f(x) = 0", "Integral = 0"

    equacao = termos[0]
    for termo in termos[1:]:
        if termo.startswith('-'):
            equacao += " - " + termo[1:]
        else:
            equacao += " + " + termo

    integral = termos_integral[0]
    for termo in termos_integral[1:]:
        if termo.startswith('-'):
            integral += " - " + termo[1:]
        else:
            integral += " + " + termo

    return f"f(x) = {equacao}", f"Integral = {integral} + C"

# Função para calcular a integral definida
def calcular_integral_definida(coef, graus, a, b):
    def polinomio(x):
        return sum(c * x**g for c, g in zip(coef, graus))
    
    resultado, _ = quad(polinomio, a, b)
    return resultado

# Função para preencher a área usando a soma de Riemann
def preencher_area_soma_riemann(x_values, y_values, a, b, n=1000):
    dx = (b - a) / n
    area = 0
    for i in range(n):
        x = a + i * dx
        area += np.interp(x, x_values, y_values) * dx
    return area

def plotar_grafico(valores_x, valores_y_polinomio, valores_y_integral, a, b, equacao_polinomio, integral_polinomio, area_soma_riemann):
    plt.figure(figsize=(10, 6))

    # Plot do polinômio
    plt.plot(valores_x, valores_y_polinomio, label="Polinômio", color="blue", linewidth=2)

    # Plot da integral indefinida do polinômio
    plt.plot(valores_x, valores_y_integral, label="Integral Indefinida do Polinômio", color="green", linestyle="--", linewidth=2)

    # Preencher a área sob o polinômio entre a e b usando a soma de Riemann com barrinhas
    dx = (b - a) / 50 # Divida o intervalo em 50 retângulos
    x_mid = np.arange(a, b, dx) + dx / 2  # Calcula os pontos médios para a soma de Riemann
    y_mid = np.interp(x_mid, valores_x, valores_y_polinomio)  # Avalia a função nesses pontos

    # Adiciona as barrinhas para a soma de Riemann
    plt.bar(x_mid, y_mid, width=dx, align='center', color='skyblue', edgecolor='blue', alpha=0.6, label="Barrinhas da Soma de Riemann")

    # Desenhar linhas verticais para delimitar a área
    plt.axvline(x=a, color='red', linestyle='--', label=f'Limite Inferior: x={a}')
    plt.axvline(x=b, color='orange', linestyle='--', label=f'Limite Superior: x={b}')

    # Adicionar a equação do polinômio e a integral no gráfico
    plt.text(0.05, 0.95, equacao_polinomio, transform=plt.gca().transAxes, fontsize=12,
             verticalalignment='top', bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
    plt.text(0.05, 0.90, integral_polinomio, transform=plt.gca().transAxes, fontsize=12,
             verticalalignment='top', bbox=dict(boxstyle="round", facecolor="lightgreen", alpha=0.5))

    plt.title("Polinômio e sua Integral Indefinida")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.xlim(-6, 6)  
    plt.ylim(-6, 6)  
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
    plt.legend()
    plt.grid(True)
    plt.show()

def calcular_valor_funcional(coef, graus, a):
    valor = sum(c * a**g for c, g in zip(coef, graus))
    return valor
# Função para plotar os valores funcionais no gráfico
def plotar_valores_funcionais(valores_x, valores_y):
    plt.figure(figsize=(8, 8))
    
    # Plotar os pontos como marcadores vermelhos
    plt.scatter(valores_x, valores_y, color='red', label='Valores Funcionais', zorder=5)
    
    # Adicionar as coordenadas de cada ponto diretamente no gráfico
    for x, y in zip(valores_x, valores_y):
        plt.text(x, y, f"({x}, {y:.2f})", fontsize=12, ha='right')
    
    # Definir limites para os eixos x e y
    plt.xlim(-9,9)
    plt.ylim(-100,100)
    
    # Adicionar linhas horizontais e verticais para o eixo x e y
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    
    
    
    # Ativar a grade do gráfico
    plt.grid(True)
    # Labels e título
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Valores Funcionais em um Plano Cartesiano")
    
    # Exibir a legenda
    plt.legend()
    
    # Exibir o gráfico
    plt.show()

# Função principal para coordenar a leitura dos dados e a plotagem
def main():
    while True:
        num_termos = input("Digite o número de termos do polinômio (ou 'sair' para encerrar): ")
        if num_termos.lower() == 'sair':
            break

        num_termos = int(num_termos)
        
        coef = []
        graus = []

        for i in range(num_termos):
            c, g = map(float, input(f"Digite o coeficiente e o grau do termo {i + 1} (ex: 3 2): ").split())
            coef.append(c)
            graus.append(int(g))

        # Ordenar polinômio
         
        coef, graus = simplificar_polinomio(coef, graus)  # Chamada para simplificar

        # Definir os limites do intervalo e o passo
        intervalo_min = -10.0
        intervalo_max = 10.0
        passo = 0.1

        # Calcular polinômio e integral
        x_values, y_polinomio, y_integral = calcular_polinomio_e_integral(coef, graus, intervalo_min, intervalo_max, passo)

        # Reconstruir a equação do polinômio e sua integral
        equacao_polinomio, integral_polinomio = construir_equacao_polinomio_e_integral(coef, graus)
        print(f"\nEquação do Polinômio: {equacao_polinomio}")
        print(f"Integral: {integral_polinomio}")

        # Perguntar se deseja calcular a integral definida
        calcular_integral = input("Deseja calcular a integral definida (S/N)? ").strip().lower()
        if calcular_integral == 's':
            a = float(input("Digite o limite inferior (a): "))
            b = float(input("Digite o limite superior (b): "))
            resultado_integral = calcular_integral_definida(coef, graus, a, b)
            print(f"Integral definida de {a} a {b}: {resultado_integral}")

           # Perguntar o número de retângulos para a soma de Riemann
            num_retangulos = int(input("Digite o número de retângulos para a soma de Riemann: "))

            # Calcular a área usando soma de Riemann
            area_soma_riemann = preencher_area_soma_riemann(x_values, y_polinomio, a, b, num_retangulos)
            print(f"Área sob o polinômio entre {a} e {b} (Soma de Riemann): {area_soma_riemann:.2f}")


            # Plotar o gráfico
            plotar_grafico(x_values, y_polinomio, y_integral, a, b, equacao_polinomio, integral_polinomio, area_soma_riemann)
          # Perguntar se deseja calcular os valores funcionais
            calcular_valores_funcionais = input("Deseja calcular os valores funcionais (S/N)? ").strip().lower()
            if calcular_valores_funcionais == 's':
                valores_funcionais_x = []  # Certifique-se de que as listas estejam fora do loop
                valores_funcionais_y = []
                
                # Obter os valores funcionais
                while True:
                    entrada = input("Digite o ponto para o valor funcional (ou 'sair' para encerrar): ")
                    if entrada.lower() == 'sair':
                        break
                    try:
                        a = float(entrada)
                        valor_funcional = calcular_valor_funcional(coef, graus, a)
                        valores_funcionais_x.append(a)  # Adicionar o valor de x na lista
                        valores_funcionais_y.append(valor_funcional)  # Adicionar o valor de f(x) na lista
                        print(f"f({a}) = {valor_funcional}")
                    except ValueError:
                        print("Entrada inválida! Por favor, insira um número válido.")
                
                # Verificar a quantidade de pontos coletados
                print(f"Valores coletados: {len(valores_funcionais_x)} pontos.")
                
                # Plotar o gráfico dos valores funcionais após o gráfico da integral
                if valores_funcionais_x:  # Verificar se a lista não está vazia
                     plotar_valores_funcionais(valores_funcionais_x, valores_funcionais_y)

if __name__ == "__main__":
    main()
