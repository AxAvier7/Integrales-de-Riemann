import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle

#función a integrar
def f(x):
    return x**2

#límites de integración
a = 0
b = 2

#número de rectángulos inicial
n = 50

#la figura y el eje creados
fig, ax = plt.subplots()

#el rango de la x
x = np.linspace(a, b, 1000)
y = f(x)

#dibujar la función
ax.plot(x, y, 'r', linewidth=2)

#la lista donde se almacenan los rectángulos
rectangles = []

#inicialización de la animación
def init():
    ax.set_xlim(a, b)
    ax.set_ylim(0, f(b))
    return []

#actualización de la animación
def update(frame):
    global n
    n = frame
    dx = (b - a) / n
    x_rect = np.linspace(a, b, n, endpoint=False)
    y_rect = f(x_rect)
    
    #se limpian los rectángulos anteriores
    for rect in rectangles:
        rect.remove()
    rectangles.clear()
    
    #se dibujan los nuevos rectángulos
    for xi, yi in zip(x_rect, y_rect):
        rect = Rectangle((xi, 0), dx, yi, alpha=0.5, color='b')
        ax.add_patch(rect)
        rectangles.append(rect)
    
    ax.set_title(f'Suma de Riemann')
    return rectangles

#la animación en sí
ani = FuncAnimation(fig, update, frames=np.arange(50, 1, -1), init_func=init, blit=True, interval=200)

#para mostrar la animación
plt.show()