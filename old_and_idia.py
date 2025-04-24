import os
import sys
import time
from enum import Enum
import keyboard

class BattleWindow:
    class Action(Enum):
        ATTACK_LEFT = 1
        ATTACK_RIGHT = 2
        DODGE = 3
        ITEMS = 4
        RETREAT = 5
        SPELL = 6
    
    def __init__(self):
        # Данные игрока
        self.player_name = "Артас"
        self.player_hp = 120
        self.player_max_hp = 120
        self.player_mana = 80
        self.player_max_mana = 80
        self.stamina = 50
        self.max_stamina = 100
        self.left_weapon = "Ледяной Клинок"
        self.right_weapon = "Морозное Дыхание"
        
        # Данные врага
        self.enemy_name = "Лич"
        self.enemy_hp = 150
        self.enemy_max_hp = 150
        
        # Настройки клавиш
        self.key_bindings = {
            'q': self.Action.ATTACK_LEFT,
            'e': self.Action.ATTACK_RIGHT,
            's': self.Action.DODGE,
            'd': self.Action.ITEMS,
            'r': self.Action.RETREAT,
            'f': self.Action.SPELL
        }
        
        # Размеры консоли
        self.console_width = 80
        self.console_height = 19
        
        # Состояния
        self.in_battle = True
        self.in_items_menu = False
        
        # Анимация
        self.animation_frame = 0
        self.animation_delay = 0.2
        self.last_animation_time = time.time()
    
    def clear_screen(self):
        """Очистка экрана консоли"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw_border(self):
        """Отрисовка границ окна"""
        print('+' + '-' * (self.console_width - 2) + '+')
    
    def draw_empty_line(self):
        """Отрисовка пустой строки"""
        print('|' + ' ' * (self.console_width - 2) + '|')
    
    def draw_centered_text(self, text):
        """Отрисовка текста по центру"""
        spaces = (self.console_width - 2 - len(text)) // 2
        print('|' + ' ' * spaces + text + ' ' * (self.console_width - 2 - len(text) - spaces) + '|')
    
    def draw_enemy_window(self):
        """Отрисовка окна врага с анимацией"""
        self.draw_empty_line()
        enemy_title = f"{self.enemy_name} HP: {self.enemy_hp}/{self.enemy_max_hp}"
        print('|' + ' ' * (self.console_width - 2 - len(enemy_title)) + enemy_title + '|')
        self.draw_empty_line()
        
        # Анимация врага
        current_time = time.time()
        if current_time - self.last_animation_time > self.animation_delay:
            self.animation_frame = (self.animation_frame + 1) % 3
            self.last_animation_time = current_time
        
        if self.enemy_name == "Лич":
            frames = [
                [
                    "    ████████    ",
                    "  ██▒▒▒▒▒▒▒▒██  ",
                    "██▒▒▒▒▒▒▒▒▒▒▒▒██",
                    "██▒▒▒▒▒▒▒▒▒▒▒▒██",
                    "  ██▒▒▒▒▒▒▒▒██  ",
                    "    ████████    "
                ],
                [
                    "    ████████    ",
                    "  ██▒▒▒▒▒▒▒▒██  ",
                    "██▒▒▒▒▒▒▒▒▒▒▒▒██",
                    "██▒▒▒▒▒▒▒▒▒▒▒▒██",
                    "  ██▒▒▒▒▒▒▒▒██  ",
                    "    ████████    "
                ],
                [
                    "    ████████    ",
                    "  ██▒▒▒▒▒▒▒▒██  ",
                    "██▒▒▒▒▒▒▒▒▒▒▒▒██",
                    "██▒▒▒▒▒▒▒▒▒▒▒▒██",
                    "  ██▒▒▒▒▒▒▒▒██  ",
                    "    ████████    "
                ]
            ]
        else:
            frames = [
                ["⚔️ Враг ⚔️"],
                ["⚡ Враг ⚡"],
                ["💀 Враг 💀"]
            ]
        
        for line in frames[self.animation_frame]:
            self.draw_centered_text(line)
        
        for _ in range(5):
            self.draw_empty_line()
    
    def draw_player_stats(self):
        """Отрисовка статистики игрока"""
        # Статистика в правом нижнем углу
        stats = [
            f"Имя: {self.player_name}",
            f"HP: {self.player_hp}/{self.player_max_hp}",
            f"Мана: {self.player_mana}/{self.player_max_mana}",
            f"Выносливость: {self.stamina}/{self.max_stamina}"
        ]
        
        # Позиционирование
        empty_lines = self.console_height - 12 - len(stats)
        for _ in range(empty_lines):
            self.draw_empty_line()
        
        # Отрисовка статистики
        for stat in stats:
            print('|' + ' ' * (self.console_width - 2 - len(stat)) + stat + '|')
    
    def draw_buttons(self):
        """Отрисовка кнопок действий"""
        # Находим кнопки для текущих биндов
        left_key = [k for k, v in self.key_bindings.items() if v == self.Action.ATTACK_LEFT][0]
        right_key = [k for k, v in self.key_bindings.items() if v == self.Action.ATTACK_RIGHT][0]
        dodge_key = [k for k, v in self.key_bindings.items() if v == self.Action.DODGE][0]
        items_key = [k for k, v in self.key_bindings.items() if v == self.Action.ITEMS][0]
        retreat_key = [k for k, v in self.key_bindings.items() if v == self.Action.RETREAT][0]
        spell_key = [k for k, v in self.key_bindings.items() if v == self.Action.SPELL][0]
        
        # Левая нижняя часть - кнопки действий
        buttons = [
            f"[{left_key}] {self.left_weapon}",
            f"[{right_key}] {self.right_weapon}",
            f"[{spell_key}] Заклинание (10 маны)",
            f"[{dodge_key}] Уклон",
            f"[{items_key}] Расходники"
        ]
        
        # Левая верхняя часть - кнопка отступления
        retreat_button = f"[{retreat_key}] Отступить"
        print('|' + retreat_button + ' ' * (self.console_width - 2 - len(retreat_button)) + '|')
        
        # Пустые строки между верхней и нижней частью
        for _ in range(self.console_height - 8 - len(buttons)):
            self.draw_empty_line()
        
        # Отрисовка кнопок действий
        for button in buttons:
            print('|' + button + ' ' * (self.console_width - 2 - len(button)) + '|')
    
    def draw_items_menu(self):
        """Отрисовка меню расходников"""
        self.clear_screen()
        self.draw_border()
        self.draw_centered_text("МЕНЮ РАСХОДНИКОВ")
        self.draw_empty_line()
        
        items = [
            "1. Зелье здоровья (+30 HP)",
            "2. Зелье маны (+20 Mana)",
            "3. Яд (наносит 25 урона врагу)",
            "4. Эликсир выносливости (+40 Stamina)",
            "5. Назад"
        ]
        
        for item in items:
            self.draw_centered_text(item)
        
        for _ in range(self.console_height - 6 - len(items)):
            self.draw_empty_line()
        
        self.draw_border()
    
    def handle_items_menu(self):
        """Обработка меню расходников"""
        while self.in_items_menu:
            self.draw_items_menu()
            
            if keyboard.is_pressed('1'):
                self.player_hp = min(self.player_max_hp, self.player_hp + 30)
                time.sleep(0.2)
            elif keyboard.is_pressed('2'):
                self.player_mana = min(self.player_max_mana, self.player_mana + 20)
                time.sleep(0.2)
            elif keyboard.is_pressed('3'):
                self.enemy_hp = max(0, self.enemy_hp - 25)
                time.sleep(0.2)
            elif keyboard.is_pressed('4'):
                self.stamina = min(self.max_stamina, self.stamina + 40)
                time.sleep(0.2)
            elif keyboard.is_pressed('5'):
                self.in_items_menu = False
                time.sleep(0.2)
    
    def draw(self):
        """Основная отрисовка окна"""
        self.clear_screen()
        self.draw_border()
        self.draw_enemy_window()
        self.draw_player_stats()
        self.draw_buttons()
        self.draw_border()
    
    def handle_input(self):
        """Обработка ввода пользователя"""
        for key, action in self.key_bindings.items():
            if keyboard.is_pressed(key):
                if action == self.Action.ATTACK_LEFT:
                    self.attack_left()
                elif action == self.Action.ATTACK_RIGHT:
                    self.attack_right()
                elif action == self.Action.DODGE:
                    self.dodge()
                elif action == self.Action.ITEMS:
                    self.in_items_menu = True
                    self.handle_items_menu()
                elif action == self.Action.RETREAT:
                    self.retreat()
                elif action == self.Action.SPELL:
                    self.cast_spell()
                
                time.sleep(0.2)
                return
    
    def attack_left(self):
        """Атака левой рукой"""
        if self.stamina >= 10:
            damage = 15
            self.enemy_hp = max(0, self.enemy_hp - damage)
            self.stamina -= 10
            print(f"Вы атаковали {self.left_weapon.lower()} и нанесли {damage} урона!")
        else:
            print("Недостаточно выносливости!")
        time.sleep(1)
    
    def attack_right(self):
        """Атака правой рукой"""
        if self.stamina >= 8:
            damage = 10
            self.enemy_hp = max(0, self.enemy_hp - damage)
            self.stamina -= 8
            print(f"Вы атаковали {self.right_weapon.lower()} и нанесли {damage} урона!")
        else:
            print("Недостаточно выносливости!")
        time.sleep(1)
    
    def cast_spell(self):
        """Использование заклинания"""
        if self.player_mana >= 10:
            damage = 25
            self.enemy_hp = max(0, self.enemy_hp - damage)
            self.player_mana -= 10
            print(f"Вы использовали заклинание и нанесли {damage} урона!")
        else:
            print("Недостаточно маны!")
        time.sleep(1)
    
    def dodge(self):
        """Уклонение"""
        if self.stamina >= 15:
            self.stamina -= 15
            print("Вы уклонились от атаки!")
        else:
            print("Недостаточно выносливости!")
        time.sleep(1)
    
    def retreat(self):
        """Отступление"""
        print("Вы отступили от боя!")
        self.in_battle = False
        time.sleep(1)
    
    def change_key_binding(self, action, new_key):
        """Изменение привязки клавиш"""
        old_bindings = [k for k, v in self.key_bindings.items() if v == action]
        for key in old_bindings:
            self.key_bindings.pop(key)
        
        self.key_bindings[new_key] = action
    
    def run(self):
        """Основной цикл боя"""
        while self.in_battle and self.enemy_hp > 0 and self.player_hp > 0:
            self.draw()
            self.handle_input()
            
            # Восстановление характеристик
            self.stamina = min(self.max_stamina, self.stamina + 1)
            self.player_mana = min(self.player_max_mana, self.player_mana + 0.5)
            
            time.sleep(0.05)
        
        # Завершение боя
        self.clear_screen()
        if self.enemy_hp <= 0:
            print("Победа! Враг повержен!")
        elif self.player_hp <= 0:
            print("Поражение! Вы пали в бою!")
        else:
            print("Вы сбежали с поля боя.")

# Запуск боевого окна
if __name__ == "__main__":
    battle = BattleWindow()
    battle.run()
