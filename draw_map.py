import curses
import random


class Rectangle:
    def __init__(self, height, width, start_point_x, start_point_y):
        self.height = height
        self.width = width
        self.start_point_x = start_point_x
        self.start_point_y = start_point_y

class Section(Rectangle):
    def __init__(self, ID, height, width, start_point_x, start_point_y, end_point_x, end_point_y, room_in_section):
        super().__init__(height, width, start_point_x, start_point_y)
        self.ID = ID
        self.end_point_x = end_point_x
        self.end_point_y = end_point_y
        self.room_in_section = room_in_section
        self.connections = set()
        
class Door:
    def __init__(self, x, y, orientation, symbol):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.symbol = symbol
        
    def symbol_door(self):
        if self.orientation == "horizontal":
            self.symbol = "|"
        else:
            self.symbol = "-"

        return self.symbol

class Corridor:
    def __init__(self):
        self.doors = []

    def add_door(self, door):
        self.doors.append((door))
        
class Room(Rectangle):
    def __init__(self, height, width, start_point_x, start_point_y):
        super().__init__(height, width, start_point_x, start_point_y)
        self.doors = []
    
    def add_door(self, door):
        self.doors.append((door))

    def key_func(obj):
            if isinstance(obj, Room):
                return obj.start_point_x
            
#рисуем комнаты
def draw_rectangle(stdscr, start_x, start_y, end_x, end_y):#
    
    vertical_line = "║"
    horizontal_line = "═"
    LU_corner = "╔"
    LD_corner = "╚"
    RU_corner = "╗"
    RD_corner = "╝"
    
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

#рисуем коридоры и двери
def draw_corridor(stdscr, corridor):

    door1, door2 = corridor.doors[0], corridor.doors[1]
    x1, y1 = door1.x + 1, door1.y
    x2, y2 = door2.x, door2.y

    for door in corridor.doors: #рисуем двери
        symbol = door.symbol_door()
        stdscr.addch(door.y, door.x, symbol)

    if corridor.doors[0].y < corridor.doors[1].y:
        sign = 1
    else:
        sign = -1
    if y1 == y2:
        while x1 != x2:
            stdscr.addch(y1 + 1, x1, "─")
            stdscr.addch(y1 - 1, x1, "─")
            x1 += 1
    else:
        y1 += 1
        while y1 != y2:
            stdscr.addch(y1, x2 - 1, "│")
            stdscr.addch(y1, x2 + 1, "│")
            y1 += sign
            stdscr.refresh()
                          

#рассчет комнат              
def calculate_rooms(stdscr, list_rooms, list_section, count_rooms):
    rooms_to_place = random.sample(list_section, count_rooms)
   
    for section in rooms_to_place:
        flag = False
        while flag != True:
            # генерируем размеры комнаты
            h = random.randint(max(3, int(section.height / 2)), section.height - 2)
            w = random.randint(max(3, int(section.width / 2)), section.width - 2)
            
            # вычисляем центр секции
            centre_section_x = section.start_point_x + section.width // 2
            centre_section_y = section.start_point_y + section.height // 2
            
            max_start_x = section.end_point_x - w 
            max_start_y = section.end_point_y - h 

            # генерируем позицию с учетом размера комнаты
            start_point_x = random.randint(section.start_point_x, max_start_x)
            start_point_y = random.randint(section.start_point_y, max_start_y)
            
            if (start_point_x < centre_section_x < start_point_x + w and
                start_point_y < centre_section_y < start_point_y + h):
                if not (start_point_x - section.start_point_x < 2 or start_point_y - section.start_point_y < 2):
                    flag = True

                    stdscr.addch(centre_section_y, centre_section_x, "♥")

        room = Room(h, w, start_point_x, start_point_y)
        section.room_in_section = True
        list_rooms.append(room)

    return list_rooms
  


#добавление двери к комнате и проверка что точка на перимитре комнаты
def point_on_perimeter(y, x, list_rooms, orientation, list_doors):
    for room in list_rooms:
        if (x == room.start_point_x and (room.start_point_y <= y <= room.start_point_y + room.height) or
        x == room.start_point_x + room.width and (room.start_point_y <= y <= room.start_point_y + room.height) or
        y == room.start_point_y and (room.start_point_x <= x <= room.start_point_x + room.width) or
        y == room.start_point_y + room.height and (room.start_point_x <= x <= room.start_point_x + room.width)):
            for door in list_doors:
                if door.x == x and door.y == y:
                    return door
            door = Door(x, y, orientation, " ")
            room.add_door(door)
            return door
    return None
            
#точка в комнате
def point_in_room(x, y, list_rooms):
    flag = False
    for room in list_rooms:
            if (room.start_point_x < x < room.start_point_x + room.width and
                room.start_point_y < y < room.start_point_y + room.height):
                flag = True
    return flag

#рассчет сетки окна
def calculate_grid(stdscr, max_y, max_x):
    def calculate_section(start_point_x, start_point_y, witdh_section, height_section, id):
        for i in range(3):
            end_point_x = start_point_x + witdh_section
            end_point_y = start_point_y + height_section
            section = Section(id, height_section, witdh_section, start_point_x, start_point_y, end_point_x, end_point_y, False)
            list_section.append(section)
            start_point_x = start_point_x + witdh_section
            id += 1
            
    witdh_section = int(max_x / 3)
    height_section = int(max_y / 2)

    list_section = list()
    id = 1
    for i in range(2):
        if i == 1:
            start_point_y = height_section + 1
            id = 4
        else:
            start_point_y = 1
            
        start_point_x = 0
        calculate_section(start_point_x, start_point_y, witdh_section, height_section, id)

    for point in list_section:#для отображения секций
        stdscr.addch(point.start_point_y, point.start_point_x, "+")
        stdscr.addch(point.end_point_y, point.end_point_x, "+")
    return list_section

#рассчет соединений секций
def calculate_section_connections(list_section):
    list_true_section = [s for s in list_section if s.room_in_section]

    # Таблица связей для каждого ID секции
    adjacency_map = {
        1: [2, 4, 3],
        2: [1, 3, 5],
        3: [2, 6, 1],
        4: [1, 5, 6],
        5: [2, 4, 6],
        6: [3, 5, 4]
    }

    # Соединим все секции, указанные в таблице смежности
    for section in list_true_section:
        if section.room_in_section:
            available_ids = adjacency_map.get(section.ID, [])
            for target_id in available_ids:
                target_section = next((sec for sec in list_true_section if sec.ID == target_id), None)
                if target_section:
                    section.connections.add(target_section)
                    target_section.connections.add(section)

    return list_true_section

#рассчет коридоров и дверей
def calculate_corridors_and_doors(list_section, list_rooms, list_corridor, list_doors):
    list_doors.clear()
    list_corridor.clear()

    # Словарь для отслеживания созданных коридоров
    created_corridors = set()

    # Обходим все секции
    for section in list_section:
        if not section.room_in_section:
            continue

        # Проходим по всем связанным секциям
        for connection in section.connections:
            if not connection.room_in_section:
                continue

            # Создаем уникальный ключ для соединения
            connection_key = frozenset({section.ID, connection.ID})

            # Пропускаем обработанные ранее соединения
            if connection_key in created_corridors:
                continue

            # Координаты центральных точек секций
            x1, y1 = section.start_point_x + section.width // 2, section.start_point_y + section.height // 2
            x2, y2 = connection.start_point_x + connection.width // 2, connection.start_point_y + connection.height // 2

            # Определяем направление движения
            step_x = 1 if x2 > x1 else -1 if x2 < x1 else 0
            step_y = 1 if y2 > y1 else -1 if y2 < y1 else 0

            # Начало движения
            current_x, current_y = x1, y1

            # Списки найденных дверей
            doors_found = []

            # Поиск дверей на маршруте
            while True:
                # Двигаемся к следующей точке
                if current_x != x2:
                    current_x += step_x
                if current_y != y2:
                    current_y += step_y

                # Определяем ориентацию двери
                orientation = "horizontal" if step_y == 0 else "vertical"

                # Проверяем, находится ли точка вне комнаты
                if not point_in_room(current_x, current_y, list_rooms):
                    door = point_on_perimeter(current_y, current_x, list_rooms, orientation, list_doors)
                    if door:
                        doors_found.append(door)

                # Останавливаемся, если достигли цели
                if current_x == x2 and current_y == y2:
                    break

            # Создаем коридор, если нашли две двери
            if len(doors_found) >= 2:
                corridor = Corridor()
                corridor.add_door(doors_found[0])
                corridor.add_door(doors_found[1])
                list_corridor.append(corridor)
                created_corridors.add(connection_key)
                list_doors.extend(doors_found[:2])
            
#высчитываем все объекты на карте
def calculate_all_objects_in_map(stdscr, max_y, max_x, list_rooms, list_corridor, list_doors):

    list_section = calculate_grid(stdscr, max_y, max_x)

    count_room = random.randint(4,6)
    list_rooms = calculate_rooms(stdscr, list_rooms, list_section, count_room)

    list_section = calculate_section_connections(list_section)
    
    calculate_corridors_and_doors(list_section, list_rooms, list_corridor, list_doors)
    
#рисуем все объекты на карте
def draw_map(stdscr, max_y, max_x, list_rooms, list_corridor):
    curses.curs_set(0)#скрываем курсор
    
    for room in list_rooms: #рисуем комнаты
        draw_rectangle(stdscr, room.start_point_x, room.start_point_y, room.start_point_x + room.width, room.start_point_y + room.height)
        stdscr.refresh()
    
    for corridor in list_corridor:#рисуем коридоры
        draw_corridor(stdscr, corridor)
        stdscr.refresh()

    stdscr.addstr(0,0, "Здоровье:")
    stdscr.addstr(0,15, "ещё что-то:")
    stdscr.addstr(0,35, "События:")

def main(stdscr):
    height, width = stdscr.getmaxyx()
    max_y, max_x = height - 1, width - 1 #запас

    list_rooms = list()
    list_corridor = list()
    list_doors = list()
    

    calculate_all_objects_in_map(stdscr, max_y, max_x, list_rooms, list_corridor, list_doors)
    draw_map(stdscr, max_y, max_x, list_rooms, list_corridor)
    
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)