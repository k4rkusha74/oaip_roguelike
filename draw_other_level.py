import curses

def end_game(stdscr, player, enemy):
    # Получаем размеры экрана
    height, width = stdscr.getmaxyx()
    
    # Очищаем экран
    stdscr.clear()
    
    # Рисуем соответствующее сообщение
    if enemy == None:
        title = "ПОБЕДА!"
        color = curses.color_pair(2)
        message = [
            "Вы победили!",
            f"Вы смогли выбраться из подземелья",
            "",
            "Нажмите любую клавишу для выхода"
        ]
    else:
        title = "ПОРАЖЕНИЕ"
        color = curses.color_pair(1)
        message = [
            "Вы пали в бою...",
            f"{enemy.name} надсмехнулся над вашим телом",
            "",
            "Нажмите любую клавишу для выхода"
        ]
    
    # Рисуем рамку
    border_color = curses.color_pair(3)
    stdscr.attron(border_color)
    stdscr.border()
    stdscr.attroff(border_color)
    
    # Рисуем заголовок
    stdscr.attron(color | curses.A_BOLD)
    stdscr.addstr(height//2 - 4, width//2 - len(title)//2, title)
    stdscr.attroff(color | curses.A_BOLD)
    
    # Рисуем сообщение
    stdscr.attron(curses.color_pair(3))
    for i, line in enumerate(message):
        stdscr.addstr(height//2 - 2 + i, width//2 - len(line)//2, line)
    stdscr.attroff(curses.color_pair(3))
    
    # Рисуем ASCII-арт
    if enemy == None:
        art = [
            "   \\O/",
            "    | ",
            "   / \\",
            "ПОБЕДИТЕЛЬ!"
        ]
    else:
        art = [
            "   (+)",
            "   /|\\",
            "   / \\",
            "  R.I.P."
        ]
    
    for i, line in enumerate(art):
        stdscr.addstr(height//2 + 2 + i, width//2 - len(line)//2, line, color)
    
    # Обновляем экран
    stdscr.refresh()
    
    # Ждем нажатия любой клавиши
    stdscr.getch()
