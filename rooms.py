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
        self.data = {
            "color": self.base_style["colors"]["light"],
            "coords": [self.coords[0], self.coords[1], self.size[0], self.size[1]],  # 50, 70
            "coord_rect": 20,
            "type_render": 1
        }
        self.data["sprite"] = pygame.image.load(self.img).convert_alpha()
        self.data["rect"] = self.data["sprite"].get_rect()
        self.set_sprite()

    def set_sprite(self):
        self.data["sprite"] = pygame.transform.scale(self.data["sprite"],(self.data["coords"][2], self.data["coords"][3]))
        self.data["rect"].x = self.data["coords"][0]
        self.data["rect"].y = self.data["coords"][1] + self.data["coords"][3] - self.data["coord_rect"]
        self.data["rect"].w = self.data["coords"][2]
        self.data["rect"].h = self.data["coord_rect"]  # self.character["coords"][3]

    def draw(self):
        self.parent.display.blit(self.data["sprite"], self.data["coords"])



class Reception:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game
        wall_up, wal_left, wal_right = self.game.draw_walls(colors=['black', 'black', 'black'], thinkess=30, height=200)
        avtomat_1 = Object(self.parent, self.game, self.base_style,
                               [300, 400],
                         (100, 150),
                               'sprites/avtomat/avtomat_2.png')
        avtomat_2 = Object(self.parent, self.game, self.base_style,
                         [300, 300],
                         (100, 150),
                         'sprites/avtomat/avtomat_2.png')
        self.objects = [wall_up, avtomat_1, wal_left, wal_right, avtomat_2]
        self.texture_floor = pygame.image.load('sprites/floor.png')

    def enter_rooms(self):
        # self.game.floor.fill((255, 255, 255))
        self.game.floor.blit(self.texture_floor, (0, 0))
    def delete_all(self):
        pass

    def draw(self):
        self.game.render_objects(self.objects)
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
        wall_up, wal_left, wal_right = self.game.draw_walls(colors=['black', 'black', 'black'], thinkess=30, height=200)
        self.objects = [avtomat, wall_up, wal_left, wal_right]

    def enter_rooms(self):
        self.game.character.respawn([None, 600])
        self.game.floor.fill((100, 120, 150))

    def delete_all(self):
        pass

    def draw(self):
        self.game.render_objects(self.objects)
        for obj in list(filter(lambda obj: obj.data["type_render"] == 0, self.objects)):
            obj.draw()

        if self.game.character.character["coords"][1] == 800 - self.game.character.character["coords"][3] and 300 < self.game.character.character["coords"][0] < 700:
            self.game.character.respawn([None, 150])
            self.game.room_change("reception")



class PS_room:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game

        avtomat = Object(self.parent, self.game, self.base_style, [300, self.parent.display_h // 2], (100, 150), 'sprites/avtomat/avtomat_1.png')
        wall_up, wal_left, wal_right = self.game.draw_walls(colors=['blue', 'black', 'black'], thinkess=30, height=200)
        self.objects = [avtomat, wall_up, wal_left, wal_right]

    def enter_rooms(self):
        self.game.character.respawn([750, None])
        self.game.floor.fill((200, 20, 150))

    def delete_all(self):
        pass

    def draw(self):
        self.game.render_objects(self.objects)
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
        wall_up, wal_left, wal_right = self.game.draw_walls(colors=['black', 'black', 'black'], thinkess=30, height=200)
        self.objects = [avtomat, wall_up, wal_left, wal_right]

    def enter_rooms(self):
        self.game.character.respawn([50, None])
        self.game.floor.fill((200, 100, 150))

    def delete_all(self):
        pass

    def draw(self):
        self.game.render_objects(self.objects)
        if self.game.character.character["coords"][0] == 0 and 200 < self.game.character.character["coords"][1] < 500:
            self.game.character.respawn([800, 300])
            self.game.room_change("reception")