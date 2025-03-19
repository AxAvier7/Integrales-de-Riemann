import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from scipy.integrate import quad

import matplotlib
matplotlib.use('TkAgg')

#funciones disponibles
def f1(x):
    return np.exp(-x) * np.sin(2 * np.pi * x)  #f(x) = e^(-x) * sin(2πx)

def f2(x):
    return np.sin(x)  #f(x) = sin(x)

def f3(x):
    return x**2  #f(x) = x^2

def f4(x):
    return np.sqrt(x)  #f(x) = √x

def f5(x):
    return np.exp(-x**2) * np.cos(3 * np.pi * x)  #f(x) = e^(-x^2) * cos(3πx)

def f6(x):
    try:
        return np.log(x + 1) * np.sin(x**2)  #f(x) = log(x + 1) * sin(x^2)
    except:
        return np.nan  #control de error numérico

#funciones disponibles con sus dominios
functions = {
    '1': {'name': 'e^(-x) * sin(2πx)', 'func': f1, 'domain': (-np.inf, np.inf)},
    '2': {'name': 'sin(x)', 'func': f2, 'domain': (-np.inf, np.inf)},
    '3': {'name': 'x^2', 'func': f3, 'domain': (-np.inf, np.inf)},
    '4': {'name': '√x', 'func': f4, 'domain': (0, np.inf)},
    '5': {'name': 'e^(-x^2) * cos(3πx)', 'func': f5, 'domain': (-np.inf, np.inf)},
    '6': {'name': 'log(x + 1) * sin(x^2)', 'func': f6, 'domain': (-1, np.inf)},
}

#mostrar el menú
def show_menu():
    print("\nSelecciona una función para animar:")
    for key, value in functions.items():
        print(f"{key}: {value['name']}")
    print("0: Salir")

#validar límites de integración
def get_valid_limits(function_info):
    while True:
        try:
            a = float(input("Ingresa el límite inferior de integración (a): "))
            b = float(input("Ingresa el límite superior de integración (b): "))
            
            #verificar que a < b
            if a >= b:
                print("Error: El límite inferior debe ser menor que el límite superior. Inténtalo de nuevo.")
                continue
            
            #verificar que los límites estén dentro del dominio
            domain = function_info['domain']
            if a < domain[0] or b > domain[1]:
                print(f"Error: Los límites deben estar dentro del dominio de la función ({domain[0]}, {domain[1]}).")
                continue
            
            #caso excepcional de la función 6 por un tema de complejidad
            if function_info['name'] == 'log(x + 1) * sin(x^2)' and b > 20:
                print(f"Advertencia: Para esta función, el límite superior no puede ser mayor que 20.")
                b = 20
            
            return a, b
        except ValueError:
            print("Error: Ingresa un número válido. Inténtalo de nuevo.")

def main():
    while True:
        
        show_menu()

        choice = input("Ingresa el número de la función (o 0 para salir): ")

        if choice == '0':
            print("Fin del programa.")
            break

        if choice not in functions:
            print("Selección no válida. Inténtalo de nuevo.")
            continue

        #función seleccionada
        selected_function = functions[choice]['func']
        function_name = functions[choice]['name']
        function_domain = functions[choice]['domain']

        print(f"\nFunción seleccionada: {function_name}")
        print(f"Dominio válido: ({function_domain[0]}, {function_domain[1]})")
        a, b = get_valid_limits(functions[choice])

        #valor real de la integral
        try:
            integral_value, _ = quad(selected_function, a, b)
        except Exception as e:
            print(f"Error al calcular la integral: {e}")
            continue

        #se inicia con un rectángulo
        n = 1

        #la figura y el eje
        fig, ax = plt.subplots()

        #rango de x
        x = np.linspace(a, b, 5000)  # Más puntos para una curva más suave
        y = selected_function(x)
        y = np.nan_to_num(y, nan=0.0, posinf=0.0, neginf=0.0)  # Filtrar valores no válidos

        #dibujo de la función
        ax.plot(x, y, 'r', linewidth=2, label=f'f(x) = {function_name}')
        ax.legend(loc='upper right')
        ax.grid(True)

        #lista de rectángulos
        rectangles = []

        #la animación
        def init():
            ax.set_xlim(a, b)
            y_min, y_max = np.min(y), np.max(y)
            ax.set_ylim(y_min - 0.2, y_max + 0.2) 
            return []

        def update(frame):
            global n
            n = frame
            dx = (b - a) / n
            x_rect = np.linspace(a, b, n, endpoint=False)
            y_rect = selected_function(x_rect)
            y_rect = np.nan_to_num(y_rect, nan=0.0, posinf=0.0, neginf=0.0) 
            
            #suma de Riemann
            riemann_sum = np.sum(y_rect) * dx
            
            #actualizar cantidad de rectángulos
            while len(rectangles) < n:
                rect = Rectangle((0, 0), 0, 0, alpha=0.5, color='b')
                ax.add_patch(rect)
                rectangles.append(rect)
            
            for i, (xi, yi) in enumerate(zip(x_rect, y_rect)):
                rectangles[i].set_width(dx)
                rectangles[i].set_height(yi)
                rectangles[i].set_xy((xi, 0))
            
            for i in range(n, len(rectangles)):
                rectangles[i].set_width(0)
                rectangles[i].set_height(0)
            
            ax.set_title(f'Suma de Riemann con {n} rectángulos\nSuma = {riemann_sum:.4f}\nValor real = {integral_value:.4f}')
            
            return rectangles

        ani = FuncAnimation(fig, update, frames=np.arange(1, 201), init_func=init, blit=False, interval=100)

        plt.show()

#ejecución real del programa
if __name__ == "__main__":
    main()