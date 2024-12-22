import pygame

class Reception:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game
        self.texture_floor = pygame.image.load('sprites/floor/floor_on_main.png')
        self.start_coords = [self.parent.display_w // 2, self.parent.display_h // 2]

    def draw(self):
        self.game.floor.fill((255, 255, 255))
        self.game.character.character["coords"][0] = self.start_coords[0]
        self.game.character.character["coords"][1] = self.start_coords[1]
        self.game.floor.blit(self.texture_floor, (0, 0))

    def delete_all(self):
        pass

    def enter_rooms(self):
        if self.game.character.character["coords"][0] == 1000 - self.game.character.character["coords"][2] and 200 < self.game.character.character["coords"][1] < 500:
            self.start_coords = [450, 300]
            self.game.room_change("vr_room")
        if self.game.character.character["coords"][0] == 0 and 200 < self.game.character.character["coords"][1] < 500:
            self.start_coords = [100, 330]
            self.game.room_change("ps_room")
        if self.game.character.character["coords"][1] == 0 and 200 < self.game.character.character["coords"][0] < 500:
            self.start_coords[1] = 150
            self.game.room_change("comp_room")



class Computer_room:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game

    def draw(self):
        self.game.character.character["coords"][1] = 600
        self.game.floor.fill((100, 120, 150))

    def delete_all(self):
        pass

    def enter_rooms(self):
        if self.game.character.character["coords"][1] == 800 - self.game.character.character["coords"][3] and 300 < self.game.character.character["coords"][0] < 700:
            self.game.room_change("reception")



class PS_room:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game

    def draw(self):
        self.game.character.character["coords"][0] = 750
        self.game.floor.fill((200, 20, 150))

    def delete_all(self):
        pass

    def enter_rooms(self):
        if self.game.character.character["coords"][0] == 1000 - self.game.character.character["coords"][2] and 200 < self.game.character.character["coords"][1] < 500:
            self.game.room_change("reception")



class VR_room:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game

    def draw(self):
        self.game.character.character["coords"][0] = 50
        self.game.floor.fill((200, 100, 150))

    def delete_all(self):
        pass

    def enter_rooms(self):
        if self.game.character.character["coords"][0] == 0 and 200 < self.game.character.character["coords"][1] < 500:
            self.game.room_change("reception")