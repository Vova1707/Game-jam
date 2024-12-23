import pygame
from pygame_widgets.button import Button

THIKNESS_WALL = 30
HEIGHT_WALL = 200

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
        walls = self.game.draw_walls(color_left=["black", "blue"], color_up=["blue", "black"],  color_right=["black", "black"],
                                                            thinkess=THIKNESS_WALL, height=HEIGHT_WALL, width_door=150)
        avtomat_1 = Object(self.parent, self.game, self.base_style,
                               [300, 400],
                         (100, 150),
                               'sprites/avtomat/avtomat_2.png')
        avtomat_2 = Object(self.parent, self.game, self.base_style,
                         [300, 300],
                         (100, 150),
                         'sprites/avtomat/avtomat_2.png') #wall_up
        self.objects = [avtomat_1, *walls, avtomat_2]
        self.texture_floor = pygame.image.load('sprites/floor.png')

    def enter_rooms(self):
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

        walls = self.game.draw_walls(color_left=["black"], color_up=["blue"],
                                     color_right=["black"],
                                     thinkess=THIKNESS_WALL, height=HEIGHT_WALL, width_door=150)
        avtomat = Object(self.parent, self.game, self.base_style, [self.parent.display_w // 2, 300],
                         (100, 150), 'sprites/avtomat/avtomat_2.png')
        self.objects = [avtomat, *walls]

        self.texture_floor = pygame.image.load('sprites/floor.png')

        self.buttons = []
        self.init_button_menu()

    def init_button_menu(self):
        w, h = 80, 80
        button_ToMenu = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": (400, 400, w, h),
            "text": "",
            "color": {
                "inactive": self.base_style["colors"]["black"],
                "hover": self.base_style["colors"]["base1"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            },
            "func": lambda: self.game.change_game('ps')
        }
        button_ToMenu["button"] = self.parent.button(coords=button_ToMenu["coords"],
                                                              text=button_ToMenu["text"],
                                                              color=button_ToMenu["color"],
                                                              font=button_ToMenu["font"],
                                                              func=button_ToMenu["func"])

        button_Comp = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": (600, 600, w, h),
            "text": "",
            "color": {
                "inactive": self.base_style["colors"]["black"],
                "hover": self.base_style["colors"]["base1"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            },
            "func": lambda: self.game.change_game('circle')
        }
        button_Comp["button"] = self.parent.button(coords=button_Comp["coords"],
                                                     text=button_Comp["text"],
                                                     color=button_Comp["color"],
                                                     font=button_Comp["font"],
                                                     func=button_Comp["func"])

        self.buttons.append(button_ToMenu)
        self.buttons.append(button_Comp)

    def enter_rooms(self):
        self.game.character.respawn([self.parent.display_w // 2, self.parent.display_h-self.game.character.character["coords"][3]])
        self.game.floor.blit(self.texture_floor, (0, 0))

    def delete_all(self):
        for j in range(len(self.buttons) - 1, -1, -1):
            del self.buttons[j]

    def draw(self):
        self.game.render_objects(self.objects)
        for obj in list(filter(lambda obj: obj.data["type_render"] == 0, self.objects)):
            obj.draw()

        if self.game.character.character["coords"][1] == 800 - self.game.character.character["coords"][3] and 300 < self.game.character.character["coords"][0] < 700:
            print([self.parent.display_w // 2, self.game.character.character["coords"][3]+HEIGHT_WALL])
            self.game.character.respawn([self.parent.display_w // 2, HEIGHT_WALL])
            self.game.room_change("reception")



class PS_room:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game

        walls = self.game.draw_walls(color_left=["blue"], color_up=["black"],
                                     color_right=["black", "blue"],
                                     thinkess=THIKNESS_WALL, height=HEIGHT_WALL, width_door=150)
        avtomat = Object(self.parent, self.game, self.base_style, [300, self.parent.display_h // 2], (100, 150), 'sprites/avtomat/avtomat_1.png')
        self.objects = [avtomat, *walls]

        self.texture_floor = pygame.image.load('sprites/floor.png')

    def enter_rooms(self):
        self.game.character.respawn([self.parent.display_w-self.game.character.character["coords"][2], self.parent.display_h // 2])
        self.game.floor.blit(self.texture_floor, (0, 0))

    def delete_all(self):
        pass

    def draw(self):
        self.game.render_objects(self.objects)
        if self.game.character.character["coords"][0] == 1000 - self.game.character.character["coords"][2] and 200 < self.game.character.character["coords"][1] < 500:
            self.game.character.respawn([self.game.character.character["coords"][2], self.parent.display_h // 2])
            self.game.room_change("reception")



class VR_room:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game

        walls = self.game.draw_walls(color_left=["black", "black"], color_up=["black"],
                                     color_right=["black"],
                                     thinkess=THIKNESS_WALL, height=HEIGHT_WALL, width_door=150)
        avtomat = Object(self.parent, self.game, self.base_style, [300, self.parent.display_h // 2], (100, 150),
                         'sprites/avtomat/avtomat_1.png')
        self.objects = [avtomat, *walls]

        self.texture_floor = pygame.image.load('sprites/floor.png')

    def enter_rooms(self):
        self.game.character.respawn([self.game.character.character["coords"][2], self.parent.display_h // 2])
        self.game.floor.blit(self.texture_floor, (0, 0))

    def delete_all(self):
        pass

    def draw(self):
        self.game.render_objects(self.objects)
        if self.game.character.character["coords"][0] == 0 and 200 < self.game.character.character["coords"][1] < 500:
            self.game.character.respawn([self.parent.display_w - self.game.character.character["coords"][2], self.parent.display_h // 2])
            self.game.room_change("reception")