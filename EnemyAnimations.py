class EnemyAnimations:
    @staticmethod
    def get_slime_animation():
        return [
            "   #####   ",
            "  #######  ",
            " ######### ",
            " ######### ",
            "  #######  ",
            "   #####   "
        ]

    @staticmethod
    def get_rat_animation():
        return [
            "   /\\_/\\   ",
            "  ( o.o )  ",
            "   > ^ <   ",
            "  /     \\  "
        ]

    @staticmethod
    def get_goblin_animation():
        return [
            "    /\\     ",
            "   /  \\    ",
            "  |    |   ",
            "  |o  o|   ",
            "  |  ^ |   ",
            "  | \\_/ |  "
        ]

    @staticmethod
    def get_lich_animation():
        return [
            "    _()_    ",
            "   / || \\   ",
            "  |  ||  |  ",
            "  |  ||  |  ",
            "  |  ||  |  ",
            "  | \\__/ |  ",
            "  \\______/  "
        ]

    @staticmethod
    def get_dwarf_animation():
        return [
            "   .---.   ",
            "  /o   o\\  ",
            " |   ^   | ",
            " |  \\_/  | ",
            "  \\_____/  ",
            "  /     \\  "
        ]

    @staticmethod
    def get_orc_animation():
        return [
            "   .---.   ",
            "  / O O \\  ",
            " |   ^   | ",
            " |  [-]  | ",
            "  \\_____/  ",
            "   |   |   "
        ]

    @staticmethod
    def get_enemy_art(enemy_name):
        enemy_animations = {
            "Слизень": EnemyAnimations.get_slime_animation,
            "Крыса": EnemyAnimations.get_rat_animation,
            "Гоблин": EnemyAnimations.get_goblin_animation,
            "Лич": EnemyAnimations.get_lich_animation,
            "Гном": EnemyAnimations.get_dwarf_animation,
            "Орк": EnemyAnimations.get_orc_animation
        }
        
        for name, animation in enemy_animations.items():
            if name in enemy_name:
                return animation()
        
        return EnemyAnimations.get_goblin_animation()
