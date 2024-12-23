import pygame
from pygame_widgets.button import Button

THIKNESS_WALL = 30
HEIGHT_WALL = 200
TYPE_BUTTONS = {
    "comp_cord": (87, 5), "comp_size": (63, 28),
    "color": {
            "inactive": (0, 0, 0),
            "hover": (0, 32, 214),
            "pressed": (200, 208, 200),
            "text": (200, 208, 200)
    }
}

class Object:
    def __init__(self, parent, game, base_style, coords, size, image, coord_rect=20):
        self.base_style = base_style
        self.parent = parent
        self.game = game
        self.img = image
        self.size = size

        self.coords = coords
        self.coord_rect = coord_rect
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
        if self.coord_rect == 0:
            self.data["coord_rect"] = self.size[1]
        elif self.coord_rect < 0:
            self.data["coord_rect"] = self.size[1] - abs(self.coord_rect)
        else:
            self.data["coord_rect"] = self.coord_rect
        self.set_sprite()

    def set_sprite(self):
        self.data["sprite"] = pygame.transform.scale(self.data["sprite"],(self.data["coords"][2], self.data["coords"][3]))
        self.data["rect"].x = self.data["coords"][0]
        self.data["rect"].y = self.data["coords"][1] + self.data["coords"][3] - self.data["coord_rect"]
        self.data["rect"].w = self.data["coords"][2]
        self.data["rect"].h = self.data["coord_rect"]  # self.character["coords"][3]

    def draw(self):
        self.parent.display.blit(self.data["sprite"], self.data["coords"])



class Buttons:
    def __init__(self, parent, game, object, layer, func, coords, size, colors):
        self.parent = parent
        self.game = game
        self.object = object
        self.layer = layer
        self.func = func
        self.size = size
        self.coords = coords
        self.colors = colors
        if "hover" not in self.colors.keys(): self.colors["hover"] = self.colors["inactive"]
        elif "pressed" not in self.colors.keys(): self.colors["pressed"] = self.colors["inactive"]
        self.data = {
            "coords": (self.object.data["coords"][0]+self.coords[0], self.object.data["coords"][1]+self.coords[1], self.size[0], self.size[1]),
            "color": {
                "inactive": self.colors["inactive"],
                "hover":  self.colors["hover"],
                "pressed": self.colors["pressed"],
                "text": self.colors["inactive"]
            },
            "func": self.func,
            # "type_render": 1
        }
        self.create(layer)

    def create(self, layer):
        self.layer = layer
        self.data["button"] = self.parent.button(coords=self.data["coords"],
                                             text="",
                                             color=self.data["color"],
                                             font=pygame.font.SysFont(None, 30),
                                             func=self.data["func"],
                                            layer=layer
                                            )
    def delete(self):
        del self.data["button"]

class Reception:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game
        walls = self.game.draw_walls(color_left=["black", "blue"], color_up=["blue", "black"],  color_right=["black", "black"],
                                                            thinkess=THIKNESS_WALL, height=HEIGHT_WALL, width_door=150)
        avtomat_1 = Object(self.parent, self.game, self.base_style,
                               [790, 80],
                         (100, 150),
                               'sprites/avtomat/avtomat_2.png')
        avtomat_2 = Object(self.parent, self.game, self.base_style,
                         [870, 80],
                         (100, 150),
                         'sprites/avtomat/avtomat_3.png')
        title_reseption_room = Object(self.parent, self.game, self.base_style, [600, 20],
                                     (200, 150), 'sprites/titles/ultimate_reseption_logo.png')

        reseption_room_table = Object(self.parent, self.game, self.base_style, [400, 350],
                                      (200, 140), 'sprites/_other/reseption_table.png')
        plant_1 = Object(self.parent, self.game, self.base_style, [300, 130],
                                      (100, 100), 'sprites/plant/plant_1.png')

        divan_1 = Object(self.parent, self.game, self.base_style, [23, 700],
                                      (200, 100), 'sprites/sofas/black_sofa.png', coord_rect=-40)
        divan_2 = Object(self.parent, self.game, self.base_style, [211, 700],
                         (200, 100), 'sprites/sofas/green_sofa.png', coord_rect=-40)

        divan_3 = Object(self.parent, self.game, self.base_style, [592, 700],
                         (200, 100), 'sprites/sofas/black_sofa.png', coord_rect=-40)
        divan_4 = Object(self.parent, self.game, self.base_style, [780, 700],
                         (200, 100), 'sprites/sofas/green_sofa.png', coord_rect=-40)
        self.objects = [*walls, avtomat_1, avtomat_2, title_reseption_room, reseption_room_table,
                        divan_1, divan_2, divan_3, divan_4, plant_1]
        self.texture_floor = pygame.image.load('sprites/floor.png')

    def enter_rooms(self):
        self.game.floor.blit(self.texture_floor, (0, 0))

    def delete_all(self):
        pass

    def draw(self):
        self.game.render_objects(self.objects)
        # for obj in self.objects:
        #     pygame.draw.rect(self.parent.display, (255, 255, 255), obj.data["rect"])
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
        #avtomat_1 = Object(self.parent, self.game, self.base_style, [790, 75],
                         #(100, 150), 'sprites/avtomat/avtomat_2.png')

        #avtomat_2 = Object(self.parent, self.game, self.base_style, [870, 75],
                         #(100, 150), 'sprites/avtomat/avtomat_3.png')

        title_computer_room = Object(self.parent, self.game, self.base_style, [100, 20],
                         (200, 125), 'sprites/titles/computer_room_logo.png')

        computer_1 = Object(self.parent, self.game, self.base_style, [30, 110],
                                     (200, 125), 'sprites/comp/comp_1.png')
        button_computer_1 = Buttons(parent=self.parent, game=self.game, object=computer_1, layer=self.parent.display,
                                    # self.game.layer_buttons_1
                                    func=lambda: self.game.change_game('ps'), coords=TYPE_BUTTONS["comp_cord"],
                                    size=TYPE_BUTTONS["comp_size"],
                                    colors=TYPE_BUTTONS["color"])
        computer_2 = Object(self.parent, self.game, self.base_style, [250, 110],
                          (200, 125), 'sprites/comp/comp_1.png')
        computer_3 = Object(self.parent, self.game, self.base_style, [480, 110],
                            (200, 125), 'sprites/comp/comp_1.png')
        computer_4 = Object(self.parent, self.game, self.base_style, [710, 110],
                            (200, 125), 'sprites/comp/comp_1.png')

        divan_1 = Object(self.parent, self.game, self.base_style, [23, 700],
                         (200, 100), 'sprites/sofas/black_sofa.png', coord_rect=-40)
        divan_2 = Object(self.parent, self.game, self.base_style, [211, 700],
                         (200, 100), 'sprites/sofas/black_sofa.png', coord_rect=-40)

        divan_3 = Object(self.parent, self.game, self.base_style, [592, 700],
                         (200, 100), 'sprites/sofas/black_sofa.png', coord_rect=-40)
        divan_4 = Object(self.parent, self.game, self.base_style, [780, 700],
                         (200, 100), 'sprites/sofas/green_sofa.png', coord_rect=-40)
        computer_4 = Object(self.parent, self.game, self.base_style, [30, 330],
                            (200, 125), 'sprites/comp/comp_1.png')
        # def __init__(self, parent, game, object, layer, func, coords, size, colors):
        button_computer_4 = Buttons(parent=self.parent, game=self.game, object=computer_4, layer=self.parent.display, # self.game.layer_buttons_1
                                    func=lambda: self.game.change_game('circle'), coords=TYPE_BUTTONS["comp_cord"], size=TYPE_BUTTONS["comp_size"],
                                    colors=TYPE_BUTTONS["color"])

        self.buttons = [button_computer_1, button_computer_4]

        self.objects = [*walls, title_computer_room, computer_1, computer_2, computer_3, computer_4, divan_1, divan_2]

        self.texture_floor = pygame.image.load('sprites/floor.png')
        # self.buttons = []
        # self.init_button_menu()

    def init_button_menu(self):
        w, h = 60, 40
        button_ps = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": (111 - 260 + 480, 111, 75, 37),
            "text": "",
            "color": {
                "inactive": self.base_style["colors"]["black"],
                "hover": self.base_style["colors"]["base1"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            },
            "func": lambda: self.game.change_game('ps')
        }
        button_ps["button"] = self.parent.button(coords=button_ps["coords"],
                                                              text=button_ps["text"],
                                                              color=button_ps["color"],
                                                              font=button_ps["font"],
                                                              func=button_ps["func"])

        button_Comp = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": (111, 111, 75, 37),
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

        self.buttons.append(button_ps)
        self.buttons.append(button_Comp)

    def enter_rooms(self):
        self.game.character.respawn([self.parent.display_w // 2, self.parent.display_h-self.game.character.character["coords"][3]-THIKNESS_WALL-20])
        self.game.floor.blit(self.texture_floor, (0, 0))

    def delete_all(self):
        for j in range(len(self.buttons) - 1, -1, -1):
            del self.buttons[j]

    def draw(self):
        self.game.render_objects(self.objects, self.buttons)
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