import pygame

class Object:
    def __init__(self, parent, game, base_style, coords, size, image):
        self.base_style = base_style
        self.parent = parent
        self.game = game
        self.img = image
        self.size = size

        self.coords = coords
        self.init_data()

    def init_data(self):
        self.data_obj = {
            "color": self.base_style["colors"]["light"],
            "coords": [self.coords[0], self.coords[1], self.size[0], self.size[1]],  # 50, 70
            "coord_rect": 20,
            "type_render": 1
        }
        self.data_obj["sprite"] = pygame.image.load(self.img).convert_alpha()
        self.data_obj["rect"] = self.data_obj["sprite"].get_rect()
        self.set_sprite()

    def set_sprite(self):
        self.data_obj["sprite"] = pygame.transform.scale(self.data_obj["sprite"],(self.data_obj["coords"][2], self.data_obj["coords"][3]))
        self.data_obj["rect"].x = self.data_obj["coords"][0]
        self.data_obj["rect"].y = self.data_obj["coords"][1] + self.data_obj["coords"][3] - self.data_obj["coord_rect"]
        self.data_obj["rect"].w = self.data_obj["coords"][2]
        self.data_obj["rect"].h = self.data_obj["coord_rect"]  # self.character["coords"][3]

    def draw(self):
        self.parent.display.blit(self.data_obj["sprite"], self.data_obj["coords"])



class Reception:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game
        avtomat = Object(self.parent, self.game, self.base_style,
                               [800, 50],
                         (100, 150),
                               'sprites/avtomat/avtomat_2.png')
        wall = Object(self.parent, self.game, self.base_style, [0, 0],
                      (1000, 200), 'sprites/walls/front_black_wall.png')

        wal_1 = Object(self.parent, self.game, self.base_style, [0, 0],
                      (30, 800), 'sprites/walls/side_black_wall.png')

        wal_2 = Object(self.parent, self.game, self.base_style, [970, 0],
                       (30, 800), 'sprites/walls/side_blue_wall.png')

        self.texture_floor = pygame.image.load('sprites/floor.png')

        self.objects = [wall, wal_1, wal_2, avtomat]

        self.rect_objs = [avtomat.data_obj["rect"]] # Объекты в комнате (их прямоугольные зоны для отслеживания коллизии)

    def enter_rooms(self):
        # self.game.floor.fill((255, 255, 255))
        self.game.floor.blit(self.texture_floor, (0, 0))
    def delete_all(self):
        pass

    def draw(self):
        for i in self.objects: i.draw()
        if self.game.character.character["coords"][0] == 1000 - self.game.character.character["coords"][2] and 200 < self.game.character.character["coords"][1] < 500:
            # self.game.character.respawn([450, 300])
            self.game.room_change("vr_room")
        if self.game.character.character["coords"][0] == 0 and 200 < self.game.character.character["coords"][1] < 500:
            # self.game.character.respawn([100, 330])
            self.game.room_change("ps_room")
        if self.game.character.character["coords"][1] == 0 and 200 < self.game.character.character["coords"][0] < 500:
            # self.game.character.respawn([None, 150])
            self.game.room_change("comp_room")



class Computer_room:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game

        avtomat = Object(self.parent, self.game, self.base_style, [self.parent.display_w // 2, 300],
                         (100, 150), 'sprites/avtomat/avtomat_2.png')
        wall = Object(self.parent, self.game, self.base_style, [0, 0],
                      (1000, 200), 'sprites/walls/front_blue_wall.png')
        wal_1 = Object(self.parent, self.game, self.base_style, [970, 0],
                       (30, 800), 'sprites/walls/side_black_wall.png')

        wal_2 = Object(self.parent, self.game, self.base_style, [0, 0],
                       (30, 800), 'sprites/walls/side_blue_wall.png')
        self.objects = [avtomat, wall, wal_1, wal_2]
        self.rect_objs = [avtomat.data_obj["rect"]] # wall.data_obj["rect"] # Объекты в комнате (их прямоугольные зоны для отслеживания коллизии)

    def enter_rooms(self):
        self.game.character.respawn([None, 600])
        self.game.floor.fill((100, 120, 150))

    def delete_all(self):
        pass

    def draw(self):
        for i in self.objects: i.draw()
        if self.game.character.character["coords"][1] == 800 - self.game.character.character["coords"][3] and 300 < self.game.character.character["coords"][0] < 700:
            self.game.character.respawn([None, 150])
            self.game.room_change("reception")



class PS_room:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game

        avtomat = Object(self.parent, self.game, self.base_style, [300, self.parent.display_h // 2], (100, 150), 'sprites/avtomat/avtomat_1.png')
        wall = Object(self.parent, self.game, self.base_style, [0, 0],
                      (1000, 200), 'sprites/walls/front_blue_wall.png')
        wal_1 = Object(self.parent, self.game, self.base_style, [970, 0],
                       (30, 800), 'sprites/walls/side_black_wall.png')

        wal_2 = Object(self.parent, self.game, self.base_style, [0, 0],
                       (30, 800), 'sprites/walls/side_blue_wall.png')
        self.objects = [avtomat, wall, wal_1, wal_2]
        self.rect_objs = [avtomat.data_obj["rect"]] #, wall.data_obj["rect"]  # Объекты в комнате (их прямоугольные зоны для отслеживания коллизии)

    def enter_rooms(self):
        self.game.character.respawn([750, None])
        self.game.floor.fill((200, 20, 150))

    def delete_all(self):
        pass

    def draw(self):
        for i in self.objects: i.draw()
        if self.game.character.character["coords"][0] == 1000 - self.game.character.character["coords"][2] and 200 < self.game.character.character["coords"][1] < 500:
            self.game.character.respawn([100, 330])
            self.game.room_change("reception")



class VR_room:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game

        avtomat = Object(self.parent, self.game, self.base_style, [300, self.parent.display_h // 2], (100, 150),
                         'sprites/avtomat/avtomat_1.png')
        wall = Object(self.parent, self.game, self.base_style, [0, 0],
                      (1000, 200), 'sprites/walls/front_blue_wall.png')
        wal_1 = Object(self.parent, self.game, self.base_style, [970, 0],
                       (30, 800), 'sprites/walls/side_black_wall.png')

        wal_2 = Object(self.parent, self.game, self.base_style, [0, 0],
                       (30, 800), 'sprites/walls/side_blue_wall.png')
        self.objects = [avtomat, wall, wal_1, wal_2]
        self.rect_objs = [avtomat.data_obj["rect"]] # , wall.data_obj["rect"] # Объекты в комнате (их прямоугольные зоны для отслеживания коллизии)

    def enter_rooms(self):
        self.game.character.respawn([50, None])
        self.game.floor.fill((200, 100, 150))

    def delete_all(self):
        pass

    def draw(self):
        for i in self.objects: i.draw()
        if self.game.character.character["coords"][0] == 0 and 200 < self.game.character.character["coords"][1] < 500:
            self.game.character.respawn([800, 300])
            self.game.room_change("reception")