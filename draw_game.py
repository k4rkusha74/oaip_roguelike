import curses
from curses import ascii
import random

class Cube:
    def __init__(self, height, width, start_point_x, start_point_y):
        
        self.height = height
        self.width = width
        self.start_point_x = start_point_x
        self.start_point_y = start_point_y

class Door:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Corridor:
    def __init__(self, bend_x, bend_y):
        self.bend_x = bend_x
        self.bend_y = bend_y
        self.doors = []

    def add_door(self, door):
        self.doors.append((door))
        

class Room(Cube):
    def __init__(self, height, width, start_point_x, start_point_y):
        super().__init__(height, width, start_point_x, start_point_y)
        self.doors = []
    
    def add_door(self, door):
        self.doors.append((door))

    def key_func(obj):
            if isinstance(obj, Room):
                return obj.start_point_x
            else:
                raise TypeError('Unknown object!!!')
    

def draw_cube(stdscr, start_x, start_y, end_x, end_y, index_cube):#
    
    if index_cube == 1:
        vertical_line = "║"
        horizontal_line = "═"
        LU_corner = "╔"
        LD_corner = "╚"
        RU_corner = "╗"
        RD_corner = "╝"
    elif index_cube == 2:
        vertical_line = curses.ACS_VLINE
        horizontal_line = curses.ACS_HLINE
        LU_corner = curses.ACS_ULCORNER
        LD_corner = curses.ACS_LLCORNER
        RU_corner = curses.ACS_URCORNER
        RD_corner = curses.ACS_LRCORNER

    #углы
    try:
        stdscr.addch(start_y, start_x, LU_corner)
        stdscr.addch(start_y, end_x, RU_corner)
        stdscr.addch(end_y, start_x, LD_corner)
        stdscr.addch(end_y, end_x, RD_corner)
    except:
        pass
        
    #горизонтальные линии
    for x in range(1, end_x - start_x):
        try:
            stdscr.addch(start_y, start_x + x, horizontal_line)
            stdscr.addch(end_y, start_x + x, horizontal_line)
        except:
            continue
        
    #вертикальные линии 
    for y in range(1,  end_y - start_y):
        try:
            stdscr.addch(start_y + y, start_x, vertical_line)
            stdscr.addch(start_y + y, end_x, vertical_line)
        except:
            continue
    
    
def calculate_rooms(stdscr, max_y, max_x, list_rooms): 
    h = random.randint(int(max_y / 6), int(max_y / 4))
    w = random.randint(int(max_x / 6), int(max_x / 4))
    
    min_size = 3
    padding = 3
    max_attempts = 100 
    
    for _ in range(max_attempts):
        
        start_point_x = random.randint(min_size, max_x - w - min_size)
        start_point_y = random.randint(min_size, max_y - h - min_size)
        end_point_x = start_point_x + w
        end_point_y = start_point_y + h
        
        flag = False
        for room in list_rooms:
            if not (end_point_x + padding < room.start_point_x  or 
                    start_point_x > room.start_point_x + room.width + padding or
                    end_point_y + padding < room.start_point_y or
                    start_point_y > room.start_point_y + room.height + padding):
                flag = True
                break
        
        if not flag:
            room = Room(h, w, start_point_x, start_point_y)
            list_rooms.append(room)
            draw_cube(stdscr, start_point_x, start_point_y, end_point_x, end_point_y, 1)
            return 1
    
    return -1

#добавление двери к комнате
def add_door_in_room(y, x, list_rooms):
    for room in list_rooms:
        if (x == room.start_point_x and (room.start_point_y < y < room.start_point_y + room.height) or
        x == room.start_point_x + room.width and (room.start_point_y < y < room.start_point_y + room.height) or
        y == room.start_point_y and (room.start_point_x < x < room.start_point_x + room.width) or
        y == room.start_point_y + room.height and (room.start_point_x < x < room.start_point_x + room.width)):
            door = Door(x, y)
            room.add_door(door)

def needs_redraw(y1, x2, list_rooms):
    for room in list_rooms:
        if (((y1 == room.start_point_y or 
            y1 == room.start_point_y + room.height) and x2 > room.start_point_x) or 
            x2 == room.start_point_x or 
            x2 == room.start_point_x + room.width):
            return True
    return False

def handle_redraw(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Перегенирация карты...")
    stdscr.refresh()
    curses.napms(1000)  # Пауза 1 секунда
    curses.endwin()
    draw_game(stdscr)

def draw_corridor(stdscr, room1, room2, list_rooms):

    # Центры комнат
    x1 = room1.start_point_x + room1.width // 2
    y1 = room1.start_point_y + room1.height // 2
    x2 = room2.start_point_x + room2.width // 2
    y2 = room2.start_point_y + room2.height // 2
    
    is_corner = needs_redraw(y1, x2, list_rooms)
    if is_corner == True:
        handle_redraw(stdscr)
    
    # Горизонтальная часть
    if x2 > x1:
        step_x = 1
    else:
        step_x = -1
    for x in range(x1, x2 + step_x, step_x):
        flag = False
        for room in list_rooms:
            if (room.start_point_x < x < room.start_point_x + room.width and
                room.start_point_y < y1 < room.start_point_y + room.height):
                flag = True
        if flag == False:
            char = stdscr.inch(y1, x) & 0xFF
            if char == ord(ascii.unctrl("║")[0]):
                stdscr.addch(y1, x, "|")
                add_door_in_room(y1, x, list_rooms)
            else:
                stdscr.addch(y1, x, curses.ACS_HLINE)

        stdscr.refresh()
    
    # Вертикальная часть
    if y2 > y1:
        step_y = 1 
    else:
        step_y = -1
    for y in range(y1, y2 + step_y, step_y):
        flag = False
        for room in list_rooms:
            if (room.start_point_x < x2 < room.start_point_x + room.width and
                room.start_point_y < y < room.start_point_y + room.height):
                flag = True
        if flag == False:
            char = stdscr.inch(y, x2) & 0xFF
            if char == ord(ascii.unctrl("═")[0]):
                stdscr.addch(y, x2, "-")
                add_door_in_room(y, x2, list_rooms)
            else:
                stdscr.addch(y, x2, curses.ACS_VLINE)
        stdscr.refresh()
    
def draw_game(stdscr):

    curses.curs_set(0)#скрываем курсор
    list_rooms = list()
    list_doors = list()
    height, width = stdscr.getmaxyx()
    max_y, max_x = height - 1, width - 1 #запас
    
    draw_cube(stdscr, 0, 0, max_x, max_y, 1)#рисуем окно

    count_room = random.randint(4, 5)
    for _ in range(count_room):            #рисуем комнаты
        answear = calculate_rooms(stdscr, max_y, max_x, list_rooms)
        if answear == -1:
            break
   
    # Сортируем комнаты по X координате
    list_rooms = sorted(list_rooms, key=lambda room: room.start_point_x)

    for i in range(len(list_rooms) - 1):
        flag = False
        if list_rooms[i+1].doors:
            flag = True
        if flag == False:
            draw_corridor(stdscr, list_rooms[i], list_rooms[i+1], list_rooms)

    if len(list_rooms) <= 2:
        handle_redraw(stdscr)
    
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(draw_game)