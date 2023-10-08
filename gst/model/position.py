class Position:
    def __init__(self,
                 pos_player: list,
                 pos_enemy: list,
                 bomb_player: bool,
                 bomb_enemy: bool,
                 bombs=None
                 ):
        if bombs is None:
            bombs = []
        self.bombs = bombs  # list bom mới
        self.bomb_enemy = bomb_enemy
        self.bomb_player = bomb_player
        self.pos_player = pos_player
        self.pos_enemy = pos_enemy

    def __str__(self):
        return f"{self.pos_player} {self.bomb_player} {self.pos_enemy} {self.bomb_enemy} {self.bombs}"
