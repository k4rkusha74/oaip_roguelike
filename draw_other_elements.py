import curses
import draw_map

class View_characteristics:
    def __init__(self, name, x, y, content):
        self.name = name
        self.x = x
        self.y = y
        self.content = content

def draw_characteristics(stdscr, curren_level, view_health, view_event):
    stdscr.move(0, 0)# Перемещаем курсор в начало строки
    stdscr.clrtoeol() 
    stdscr.addstr(0,0, "Уровень:")
    stdscr.addstr(0,14, "Здоровье:")
    stdscr.addstr(0,29, "События:")

    if view_health.content > 70:
        stdscr.addstr(view_health.y, view_health.x, str(view_health.content), curses.color_pair(2))
    elif view_health.content > 30:
        stdscr.addstr(view_health.y, view_health.x, str(view_health.content), curses.color_pair(3))
    else:
        stdscr.addstr(view_health.y, view_health.x, str(view_health.content), curses.color_pair(1))

    stdscr.addstr(curren_level.y, curren_level.x, str(curren_level.content))
    stdscr.addstr(view_event.y, view_event.x, str(view_event.content))
    stdscr.refresh()

def draw_info_grid(stdscr, list_section):
    stdscr.clear()
    start_section = list(filter(lambda x: x.ID == 2, list_section))
    end_section = list(filter(lambda x: x.ID == 5, list_section))
    start_x = start_section[0].start_point_x
    start_y = start_section[0].start_point_y
    end_x = end_section[0].end_point_x
    end_y = end_section[0].end_point_y

    draw_map.draw_rectangle(stdscr, start_x, start_y, end_x, end_y, None, True)
    stdscr.addstr(start_y + 1, start_x + 1, "W - вперёд / S - назад", curses.color_pair(3))
    stdscr.addstr(start_y + 2, start_x+ 1, "D - влево / A - вправо", curses.color_pair(3))
    stdscr.addstr(start_y + 3, start_x+ 1, "E - открыть сундук", curses.color_pair(3))
    stdscr.addstr(start_y + 4, start_x+ 1, "X - закрыть сундук/окно команд", curses.color_pair(3))
    stdscr.addstr(start_y + 5, start_x+ 1, "F - атаковать", curses.color_pair(3))
    stdscr.addstr(start_y + 6, start_x+ 1, "I - показать окно команд", curses.color_pair(3))

    while True:
            key = stdscr.getch()
            key = chr(key)

            if key == 'ч' or key == 'x' or key == 'Ч' or key == 'X':
                stdscr.clear()
                return 0

