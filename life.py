__author__ = 'ipetrash'


## Conway's Game of Life (1970).
# Место действия этой игры — «вселенная» — это размеченная на клетки
# поверхность или плоскость — безграничная, ограниченная, или замкнутая
# (в пределе — бесконечная плоскость).
# Каждая клетка на этой поверхности может находиться в двух состояниях: быть
# «живой» или быть «мёртвой» (пустой).
# Клетка имеет восемь соседей (окружающих клеток).
# Распределение живых клеток в начале игры называется первым поколением. Каждое
# следующее поколение рассчитывается на основе предыдущего по таким правилам:
# в пустой (мёртвой) клетке, рядом с которой ровно три живые клетки, зарождается жизнь;
# если у живой клетки есть две или три живые соседки, то эта клетка продолжает жить; в
# противном случае (если соседей меньше двух или больше трёх) клетка умирает
# («от одиночества» или «от перенаселённости»).
# Игра прекращается, если на поле не останется ни одной «живой» клетки, если при
# очередном шаге ни одна из клеток не меняет своего состояния (складывается стабильная
# конфигурация) или если конфигурация на очередном шаге в точности (без сдвигов и поворотов)
# повторит себя же на одном из более ранних шагов (складывается периодическая конфигурация).
#
# Эти простые правила приводят к огромному разнообразию форм, которые могут возникнуть в игре.
#
# Игрок не принимает прямого участия в игре, а лишь расставляет или генерирует начальную
# конфигурацию «живых» клеток, которые затем взаимодействуют согласно правилам уже без его
# участия (он является наблюдателем).
#
#
# https://github.com/yangit/Life
# http://habrahabr.ru/post/151832/
# https://ru.wikipedia.org/wiki/Жизнь_(игра)
# http://habrahabr.ru/post/140581/
# http://habrahabr.ru/company/mailru/blog/228379/



from random import randrange

from OpenGL.GL import *
from OpenGL.GLUT import *


__author__ = 'ipetrash'

width, height = 400, 400  # window size
field_width, field_height = 70, 70  # internal resolution
interval = 333  # update interval in milliseconds
timer = False


field = []
for j in range(field_height):
    field.append([])

    for i in range(field_width):
        field[j].append(False)


def count_neighbors(field_arr, row, col):
    count = 0

    if col-1 >= 0 and field_arr[row][col-1]:
        count += 1

    if row-1 >= 0 and col-1 >= 0 and field_arr[row-1][col-1]:
        count += 1

    if row-1 >= 0 and field_arr[row-1][col]:
        count += 1

    if row-1 >= 0 and col+1 < field_width and field_arr[row-1][col+1]:
        count += 1

    if col+1 < field_width and field_arr[row][col+1]:
        count += 1

    if row+1 < field_height and col+1 < field_width and field_arr[row+1][col+1]:
        count += 1

    if row+1 < field_height and field_arr[row+1][col]:
        count += 1

    if row+1 < field_height and col-1 >= 0 and field_arr[row+1][col-1]:
        count += 1

    return count


def check_neighbors(field_arr, row, col):
    cell = field_arr[row][col]
    count = count_neighbors(field_arr, row, col)

    # Правила жизни клеток:
    #   * в пустой (мёртвой) клетке, рядом с которой ровно три живые клетки, зарождается жизнь;
    #   * если у живой клетки есть две или три живые соседки, то эта клетка продолжает жить;
    #   * если соседей меньше двух или больше трёх) клетка умирает («от одиночества» или
    #     «от перенаселённости»).

    # в пустой (мёртвой) клетке, рядом с которой ровно три живые клетки, зарождается жизнь;
    if not cell and count == 3:
        field_arr[row][col] = True

    # если соседей меньше двух или больше трёх) клетка умирает («от одиночества»
    # или «от перенаселённости»).
    elif cell and (count < 2 or count > 3):
        field_arr[row][col] = False


for j in range(field_height):
    for i in range(field_width):
        if randrange(5) == 0:  # 20% chance
            field[j][i] = True


# # Интересная фигура:
# #      *
# #    * *
# #  * *
# #
# field[20][20+1] = True
# field[20-1][20] = True
# field[20][20] = True
# field[20-1][20-1] = True
# field[20+1][20+1] = True
# #

# # Интересная фигура:
# #     * *
# #     * *
# #  * *
# #  * *
# #
# field[20][20] = True
# field[20][20+1] = True
# field[20+1][20] = True
# field[20+1][20+1] = True
#
# field[20+2][20+2] = True
# field[20+2][20+1+2] = True
# field[20+1+2][20+2] = True
# field[20+1+2][20+1+2] = True
# #


def refresh2d_custom(w, h, i_w, i_h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, i_w, 0.0, i_h, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def draw_rect(x, y, w, h):
    glBegin(GL_QUADS)  # start drawing a rectangle
    glVertex2f(x, y)  # bottom left point
    glVertex2f(x + w, y)  # bottom right point
    glVertex2f(x + w, y + h)  # top right point
    glVertex2f(x, y + h)  # top left point
    glEnd()  # done drawing a rectangle


def draw():  # draw is called all the time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the screen
    glLoadIdentity()  # reset position
    refresh2d_custom(width, height, field_width, field_height)

    for j in range(field_height):
        for i in range(field_width):
            if field[j][i]:
                draw_rect(i, j, 1, 1)

    glutSwapBuffers()  # important for double buffering


def update(value):
    global timer

    if timer:
        for j in range(field_height):
            for i in range(field_width):
                check_neighbors(field, j, i)

    glutTimerFunc(interval, update, 0)  # trigger next update


def keyboard(*args):
    global timer

    key = args[0]

    # Нажатие на пробел
    if key == b' ':
        timer = not timer


# TODO: проверить работу алгоритма
# TODO: расстановка на поле кликом мышки
# TODO: настройка интервала
# TODO: возможность остановки таймера и ручного перехода к следующему поколению
# TODO: инвентирование цветов: поле -- белый цвет, клетки -- черный
# TODO: клетки показывать с рамкой
# TODO: переименовать check_neighbors на что-то связанное с "новым поколением"


if __name__ == '__main__':
    # initialization
    glutInit()  # initialize glut
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(width, height)  # set window size
    glutCreateWindow(b"Life 1970")  # create window with title
    glutDisplayFunc(draw)  # set draw function callback
    glutIdleFunc(draw)  # draw all the time
    glutKeyboardFunc(keyboard)  # tell opengl that we want to check keys
    glutTimerFunc(interval, update, 0)  # trigger next update
    glutMainLoop()  # start everything