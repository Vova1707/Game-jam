import pygame

class Object:
    def __init__(self, parent, game, base_style, coords):
        self.base_style = base_style
        self.parent = parent
        self.game = game

        self.coords = coords
        self.init_data()

    def init_data(self):
        part_file_path = r"sprites\character\base_choice" + '\\'
        self.data_obj = {
            "color": self.base_style["colors"]["light"],
            "coords": [self.coords[0], self.coords[1], 100, 140]  # 50, 70
        }
        self.data_obj["sprite"] = pygame.image.load(part_file_path+"walk\\"+f"walk_front_0.png").convert_alpha()
        self.data_obj["rect"] = self.data_obj["sprite"].get_rect()
        self.set_sprite()

    def set_sprite(self):
        self.data_obj["sprite"] = pygame.transform.scale(self.data_obj["sprite"],(self.data_obj["coords"][2], self.data_obj["coords"][3]))
        self.data_obj["rect"].x, self.data_obj["rect"].y, self.data_obj["rect"].w, self.data_obj["rect"].h = self.data_obj["coords"]

    def draw(self):
        self.parent.display.blit(self.data_obj["sprite"], self.data_obj["coords"])



class Reception:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game
        self.test_obj = Object(self.parent, self.game, self.base_style, [self.parent.display_w // 2, self.parent.display_h - 300])
        self.texture_floor = pygame.image.load('sprites/floor/floor_on_main.png')

        self.rect_objs = [self.test_obj.data_obj["rect"]] # Объекты в комнате (их прямоугольные зоны для отслеживания коллизии)

    def draw(self):
        self.game.floor.fill((255, 255, 255))
        self.game.floor.blit(self.texture_floor, (0, 0))

    def delete_all(self):
        pass

    def enter_rooms(self):
        self.test_obj.draw()
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

        self.test_obj = Object(self.parent, self.game, self.base_style, [self.parent.display_w // 2, 300])
        self.rect_objs = [self.test_obj.data_obj["rect"]]  # Объекты в комнате (их прямоугольные зоны для отслеживания коллизии)

    def draw(self):
        self.game.character.respawn([None, 600])
        self.game.floor.fill((100, 120, 150))

    def delete_all(self):
        pass

    def enter_rooms(self):
        self.test_obj.draw()
        if self.game.character.character["coords"][1] == 800 - self.game.character.character["coords"][3] and 300 < self.game.character.character["coords"][0] < 700:
            self.game.character.respawn([None, 150])
            self.game.room_change("reception")



class PS_room:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game

        self.test_obj = Object(self.parent, self.game, self.base_style, [300, self.parent.display_h // 2])
        self.rect_objs = [self.test_obj.data_obj["rect"]]  # Объекты в комнате (их прямоугольные зоны для отслеживания коллизии)

    def draw(self):
        self.game.character.respawn([750, None])
        self.game.floor.fill((200, 20, 150))

    def delete_all(self):
        pass

    def enter_rooms(self):
        self.test_obj.draw()
        if self.game.character.character["coords"][0] == 1000 - self.game.character.character["coords"][2] and 200 < self.game.character.character["coords"][1] < 500:
            self.game.character.respawn([100, 330])
            self.game.room_change("reception")



class VR_room:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game

        self.test_obj = Object(self.parent, self.game, self.base_style, [self.parent.display_w-300, self.parent.display_h // 2])
        self.rect_objs = [self.test_obj.data_obj["rect"]]  # Объекты в комнате (их прямоугольные зоны для отслеживания коллизии)

    def draw(self):
        self.game.character.respawn([50, None])
        self.game.floor.fill((200, 100, 150))

    def delete_all(self):
        pass

    def enter_rooms(self):
        self.test_obj.draw()
        if self.game.character.character["coords"][0] == 0 and 200 < self.game.character.character["coords"][1] < 500:
            self.game.character.respawn([800, 300])
            self.game.room_change("reception")