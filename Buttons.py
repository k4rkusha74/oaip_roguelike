class Buttons():
    def __init__(self, x_on_screem, y_on_screen):
        self.x = x_on_screem
        self.y = y_on_screen

    def drop_weapon(self, weapon, character):
        weapon.drop(character)

    def pick_up_weapon(self, weapon, character):
        weapon.pick_up(character)
    
    def replace_weapon(self, weapon, character):
        weapon.replace(character)