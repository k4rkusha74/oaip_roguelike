import curses
import random
from Item import Weapon, Armor, UseItem, WeaponNothing, ArmorNothing
from Storage import Inventory, Arming, ArmorStorage, Chest
from EnemyAnimations import EnemyAnimations

class BattleWindow:
    def __init__(self, stdscr, player, enemy):  
        self.stdscr = stdscr
        self.player = player
        self.current_enemy = enemy  
        self.in_battle = True
        self.in_inventory = False
        self.selected_action = 0
        self.selected_item = 0
        
        self.key_bindings = {
            'up': ord('w'),
            'down': ord('s'),
            'left': ord('a'),
            'right': ord('d'),
            'confirm': ord(' '),
            'escape': 27,
            'retreat': ord('f')
        }
        

    def start_battle(self, enemy):
        self.current_enemy = enemy
        self.in_battle = True
        self.selected_action = 0

    def draw(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        
        # Рамка вокруг экрана
        self.stdscr.border()
        
        if self.in_battle:
            self.draw_enemy_window(h, w)
            
            # Кнопка отступления
            self.stdscr.addstr(1, 2, "[F] Отступить", 
                curses.A_BOLD if self.selected_action == 4 else curses.A_NORMAL)
            
            # Информация о враге
            enemy_info = f"{self.current_enemy.name}: {self.current_enemy.current_health}/{self.current_enemy.health} HP"
            self.stdscr.addstr(1, w - len(enemy_info) - 2, enemy_info, curses.A_BOLD)
            
            # Действия игрока
            self.draw_player_actions(h, w)
            
            # Статус игрока
            self.draw_player_status(h, w)
        
        elif self.in_inventory:
            self.draw_inventory(h, w)
        
        self.stdscr.refresh()

    def draw_enemy_window(self, h, w):
        win_h = h // 3
        win_w = w // 2
        win_y = 1
        win_x = (w - win_w) // 2
        
        win = curses.newwin(win_h, win_w, win_y, win_x)
        win.border()
        
        enemy_art = EnemyAnimations.get_enemy_art(self.current_enemy.name)
        for i, line in enumerate(enemy_art):
            if i < win_h - 2:
                try:
                    win.addstr(i + 1, (win_w - len(line)) // 2, line)
                except curses.error:
                    pass
        
        win.refresh()

    def draw_player_actions(self, h, w):
        action_y = h - 6
        action_x = 2
        
        if action_y < 0 or action_x < 0:
            return
            
        weapon1 = self.player.hand.items[0]
        weapon2 = self.player.hand.items[1]
        
        actions = [
            f"[1] Атака: {weapon1.name} ({weapon1.damage} урона)",
            f"[2] Атака: {weapon2.name} ({weapon2.damage} урона)",
            "[3] Уклон (33% шанс)",
            "[4] Расходники",
        ]
        
        for i, action in enumerate(actions):
            if action_y + i >= h - 1:
                break
            try:
                attr = curses.A_REVERSE if i == self.selected_action else curses.A_NORMAL
                self.stdscr.addstr(action_y + i, action_x, action, attr)
            except curses.error:
                pass

    def draw_player_status(self, h, w):
        status_y = h - 5
        status_x = w - 30
        
        total_block = self.player.get_armor()
        
        status = [
            f"Игрок: {self.player.name}",
            f"HP: {self.player.current_health}/{self.player.health}",
            f"Защита: {total_block*100:.0f}%",
            f"Оружие: {self.player.hand.items[0].name}"
        ]
        
        for i, line in enumerate(status):
            self.stdscr.addstr(status_y + i, status_x, line)

    def draw_inventory(self, h, w):
        self.stdscr.addstr(2, 2, "ИНВЕНТАРЬ:", curses.A_BOLD)
        self.stdscr.addstr(3, 2, "Используйте W/S для выбора, Enter для использования, Esc для выхода")
        
        items = self.player.inventory.get_items()
        for i, item in enumerate(items):
            attr = curses.A_REVERSE if i == self.selected_item else curses.A_NORMAL
            counter = f" x{item.counter}" if hasattr(item, 'counter') else ""
            self.stdscr.addstr(5 + i, 2, f"[{i+1}] {item.name}{counter}", attr)

    def handle_input(self, key):
        if self.in_inventory:
            self.handle_inventory_input(key)
        else:
            self.handle_battle_input(key)

    def handle_inventory_input(self, key):
        items = self.player.inventory.get_items()
        
        if key == self.key_bindings['up'] and self.selected_item > 0:
            self.selected_item -= 1
        elif key == self.key_bindings['down'] and self.selected_item < len(items) - 1:
            self.selected_item += 1
        elif key == self.key_bindings['confirm'] and items:
            self.use_item(self.selected_item)
            self.in_inventory = False
        elif key == self.key_bindings['escape']:
            self.in_inventory = False

    def handle_battle_input(self, key):
        if key == self.key_bindings['up'] and self.selected_action > 0:
            self.selected_action -= 1
        elif key == self.key_bindings['down'] and self.selected_action < 3:
            self.selected_action += 1
        elif key == self.key_bindings['confirm']:
            self.execute_action(self.selected_action)
        elif key == ord('1'):
            self.execute_action(0)
        elif key == ord('2'):
            self.execute_action(1)
        elif key == ord('3'):
            self.execute_action(2)
        elif key == ord('4'):
            self.execute_action(3)
        elif key == self.key_bindings['retreat']:
            self.retreat()

    def execute_action(self, action_index):
        if action_index in [0, 1]:
            self.player.attack(self.current_enemy)
            if self.current_enemy.current_health <= 0:
                self.show_result_message(f"Вы победили {self.current_enemy.name}!")
                self.in_battle = False
                return True  
            else:
                self.enemy_counter_attack()
        elif action_index == 2:
            self.dodge()
        elif action_index == 3:
            if any(isinstance(item, UseItem) for item in self.player.inventory.get_items()):
                self.in_inventory = True
                self.selected_item = 0
        return False  

    def enemy_counter_attack(self):
        if self.current_enemy.current_health > 0:
            self.current_enemy.attack(self.player)
            if self.player.current_health <= 0:
                self.player.current_health = 0

    def dodge(self):
        if random.random() < 0.33:
            pass
        else:
            self.enemy_counter_attack()

    def use_item(self, item_index):
        items = self.player.inventory.get_items()
        if 0 <= item_index < len(items):
            item = items[item_index]
            if isinstance(item, UseItem):
                item.use(self.player)
                if hasattr(item, 'counter') and item.counter <= 0:
                    self.player.inventory.remove(item)

    def retreat(self):
        if random.random() < 0.7:
            self.in_battle = False
        else:
            self.enemy_counter_attack()

    def show_result_message(self, message):
        h, w = self.stdscr.getmaxyx()
        # Очищаем область сообщения
        for i in range(h//2 - 1, h//2 + 2):
            self.stdscr.addstr(i, 0, " " * w)
        # Выводим сообщение
        self.stdscr.addstr(h//2, (w - len(message))//2, message, curses.A_BOLD)
        self.stdscr.refresh()
        curses.napms(2000)  # Пауза 2 секунды
        # Полностью очищаем экран
        self.stdscr.clear()
        self.in_battle = False
