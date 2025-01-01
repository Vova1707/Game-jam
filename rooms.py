import pygame
from pygame.locals import Rect

THIKNESS_WALL = 30
HEIGHT_WALL = 200
TYPE_BUTTONS = {
    "comp_cord": (77, -5), "comp_size": (83, 47), # (63, 28)
    "avtomat_cord": (10, 23), "avtomat_size": (96, 182),
    "avtomat_green_cord": (15, 33), "avtomat_green_size": (93, 162),
    "tv_ps_cord": (-5, -5), "tv_ps_size": (310, 135),
    "tv_vr_cord": (-5, -5), "tv_vr_size": (110, 60),
    "reception_table_cord": (2, -5), "reception_table_size": (190, 150),
    "color": {
            "inactive": (0, 0, 0, 0), # (0, 0, 0)
            "hover": (200, 208, 200, 200), # (0, 32, 214)
            "pressed": (200, 208, 200),
            "text": (200, 208, 200)
    }
}
TYPE_SPRITES = {
    "comp_size": (200, 125),
    "sofa_size": (200, 100),
    "avtomat_size": (120, 200), # (100, 150)
    "avtomat_y_up": 50,
    'chair': (80, 132),
    'clock': (40, 40)
}
TYPE_ENERGY = {
    "green": {"price": 2, "val": 1},
    "yellow": {"price": 4, "val": 3},
    "blue": {"price": 6, "val": 5},
}




class Object:
    def __init__(self, parent, game, base_style, coords, size, image=None, size_rect=(0, 20), type_collide="rect"): #absolute_coords_rect=(0, 0)
        self.base_style = base_style
        self.parent = parent
        self.game = game
        self.image = image

        size_rect = list(size_rect)

        self.data = {
            "color": self.base_style["colors"]["light"],
            "coords": [coords[0], coords[1], size[0], size[1]],  # 50, 70
            "size_rect": size_rect,
            # "absolute_coords_rect": absolute_coords_rect,
            "type_render": 1, # тип слоя, на котором будет отрисовка
            # "type_collide": type_collide
            # "mask" - коллизия по маске
            # "rect" - коллизия по прямоугольнику
        }
        if self.image == None:
            self.data["rect"] = Rect(coords[0], coords[1], size[0], size[1])
        else:
            self.data["sprite"] = pygame.image.load(self.image).convert_alpha()
            self.data["sprite"] = pygame.transform.scale(self.data["sprite"],
                                                         (self.data["coords"][2], self.data["coords"][3]))
            self.data["mask"] = pygame.mask.from_surface(self.data["sprite"])
            self.data["rect"] = self.data["sprite"].get_rect()
        for i in range(len(size_rect)):
            if self.data["size_rect"][i] == 0:
                self.data["size_rect"][i] = size[i]
            elif self.data["size_rect"][i] < 0:
                self.data["size_rect"][i] = size[i] - abs(size_rect[i])
            else:
                self.data["size_rect"][i] = size_rect[i]
        # if self.data["absolute_coords_rect"][0] <= 0:
        #     self.data["absolute_coords_rect"][0] = self.data["coords"][0] + self.size[0]
        # else:
        #     self.data["absolute_coords_rect"][0] = self.data["absolute_coords_rect"][0]
        self.set_sprite()

    def set_sprite(self):
        self.data["rect"].x = self.data["coords"][0] # + self.data["absolute_coords_rect"][0]
        self.data["rect"].y = self.data["coords"][1] + self.data["coords"][3] - self.data["size_rect"][1] # - self.data["absolute_coords_rect"][1]
        self.data["rect"].w = self.data["size_rect"][0] # self.data["coords"][2]
        self.data["rect"].h = self.data["size_rect"][1] # self.character["coords"][3]

    def update_sprite(self, image):
        if self.image != None:
            self.image = image
            self.data["sprite"] = pygame.image.load(self.image).convert_alpha()
            self.data["sprite"] = pygame.transform.scale(self.data["sprite"],(self.data["coords"][2], self.data["coords"][3]))
            self.set_sprite()

    def draw(self):
        if self.image != None:
            self.parent.display.blit(self.data["sprite"], self.data["coords"])



class Hitbox_Button:
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
        avtomat_1 = Object(self.parent, self.game, self.base_style,
                               [20, TYPE_SPRITES["avtomat_y_up"]],
                         TYPE_SPRITES["avtomat_size"],
                               'sprites/avtomat/avtomat_2.png')
        avtomat_2 = Object(self.parent, self.game, self.base_style,
                         [110, TYPE_SPRITES["avtomat_y_up"]],
                         TYPE_SPRITES["avtomat_size"],
                         'sprites/avtomat/avtomat_3.png')
        title_room = Object(self.parent, self.game, self.base_style, [590, 15],
                                     (280, 190), 'sprites/titles/ultimate_reseption_logo.png')

        reception_table = Object(self.parent, self.game, self.base_style, [400, 350],
                                      (200, 140), 'sprites/_other/reseption_table.png', size_rect=(0, -70))
        plant_1 = Object(self.parent, self.game, self.base_style, [300, 130],
                                      (100, 100), 'sprites/plant/plant_1.png')

        sofa_1 = Object(self.parent, self.game, self.base_style, [23, 700],
                                      TYPE_SPRITES["sofa_size"], 'sprites/sofas/black_sofa.png', size_rect=(0, -40))
        sofa_2 = Object(self.parent, self.game, self.base_style, [211, 700],
                         TYPE_SPRITES["sofa_size"], 'sprites/sofas/green_sofa.png', size_rect=(0, -40))

        sofa_3 = Object(self.parent, self.game, self.base_style, [592, 700],
                         TYPE_SPRITES["sofa_size"], 'sprites/sofas/black_sofa.png', size_rect=(0, -40))
        sofa_4 = Object(self.parent, self.game, self.base_style, [780, 700],
                         TYPE_SPRITES["sofa_size"], 'sprites/sofas/green_sofa.png', size_rect=(0, -40))

        walls, self.passages = self.game.draw_walls(color_left=["black", "blue"], color_up=["blue", "black"],  color_right=["black", "black"],
                                     thinkess=THIKNESS_WALL, height=HEIGHT_WALL, width_door=150, down="wall, pass")
        print("reception passages", *self.passages.items())
        dop_walls = dict(list(filter(lambda x: x[0] in ["wall_up_1", "wall_up_2"], walls.items())))
        walls = dict(list(filter(lambda x: x[0] not in dop_walls.keys(), walls.items())))

        self.buttons = []
        # ------------------
        self.objects = {"avtomat_1": avtomat_1, "avtomat_2": avtomat_2, "title_room": title_room,
                        "reception_table": reception_table,
                        "plant_1": plant_1,
                        "sofa_1": sofa_1, "sofa_2": sofa_2, "sofa_3": sofa_3, "sofa_4": sofa_4
        }
        for k, v in walls.items():
            self.objects[k] = v
        self.list_objects = list(self.objects.values())
        # ------------------
        self.dop_objects = {}
        for k, v in dop_walls.items():
            self.dop_objects[k] = v
        self.list_dop_objects = list(self.dop_objects.values())

        self.texture_floor = pygame.image.load('sprites/floor.png')
        self.init_buttons()

    def enter_rooms(self):
        self.game.floor.blit(self.texture_floor, (0, 0))
        self.game.data_layers = [0] * len(self.buttons)
        self.game.old_data_layers = [0] * len(self.buttons)

    def init_buttons(self):
        button_avtomat_yellow = Hitbox_Button(parent=self.parent, game=self.game, object=self.objects["avtomat_1"], layer=self.parent.display,
                                   # self.game.layer_buttons_1
                                   func=lambda: self.game.energy_character_up(price=TYPE_ENERGY["yellow"]["price"],
                                                                              val=TYPE_ENERGY["yellow"]["val"]),
                                   coords=TYPE_BUTTONS["avtomat_cord"],
                                   size=TYPE_BUTTONS["avtomat_size"],
                                   colors=TYPE_BUTTONS["color"])
        self.buttons.append(button_avtomat_yellow)
        button_avtomat_blue = Hitbox_Button(parent=self.parent, game=self.game, object=self.objects["avtomat_2"],
                                              layer=self.parent.display,
                                              func=lambda: self.game.energy_character_up(price=TYPE_ENERGY["blue"]["price"],
                                                                                        val=TYPE_ENERGY["blue"]["val"]),
                                              coords=TYPE_BUTTONS["avtomat_cord"],
                                              size=TYPE_BUTTONS["avtomat_size"],
                                              colors=TYPE_BUTTONS["color"])
        self.buttons.append(button_avtomat_blue)
        button_reception_table = Hitbox_Button(parent=self.parent, game=self.game, object=self.objects["reception_table"],
                                             layer=self.parent.display,
                                             func=lambda: self.game.set_discount(discount=20, money=60, delay=2500),
                                             coords=TYPE_BUTTONS["reception_table_cord"],
                                             size=TYPE_BUTTONS["reception_table_size"],
                                             colors=TYPE_BUTTONS["color"])
        self.buttons.append(button_reception_table)


    def delete_buttons(self):
        for j in range(len(self.buttons) - 1, -1, -1):
            del self.buttons[j]

    def delete_all(self):
        self.delete_buttons()

    def draw(self):
        self.game.render_objects(self.list_objects, buttons=self.buttons, dop_objects=self.list_dop_objects)
        # print(self.game.character.character["absolute_coords_rect"], " | ", self.game.character.character["absolute_coords_rect"][0] <= self.passages["left"][0], self.passages["left"][1][0] < self.game.character.character["absolute_coords_rect"][1] < self.passages["left"][1][1])
        if self.game.character.character["absolute_coords_rect"][0] >= self.passages["right"][0] and self.passages["right"][1][0] < self.game.character.character["absolute_coords_rect"][1] < self.passages["right"][1][1]:
            # self.game.character.respawn([450, 300])
            self.game.room_change("vr_room")
        if self.game.character.character["absolute_coords_rect"][0] <= self.passages["left"][0] and self.passages["left"][1][0] < self.game.character.character["absolute_coords_rect"][1] < self.passages["left"][1][1]:
            # self.game.character.respawn([100, 330])
            self.game.room_change("ps_room")
        if self.passages["up"][0][0] < self.game.character.character["absolute_coords_rect"][0] < self.passages["up"][0][1] and self.game.character.character["absolute_coords_rect"][1] <= self.passages["up"][1]:
            # self.game.character.respawn([None, 150])
            self.game.room_change("comp_room")
        if self.passages["down"][0][0] < self.game.character.character["absolute_coords_rect"][0] < self.passages["down"][0][1] and self.game.character.character["absolute_coords_rect"][1] >= self.passages["down"][1]:
            # self.game.character.respawn([None, 150])
            #print("ВЫХОД")
            self.game.set_message("Выход из игры", delay=700) # set_message_exit("Выйти из игры?")
            self.parent.display_change("menu")



class Computer_room:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game

        avtomat_1 = Object(self.parent, self.game, self.base_style,
                           [770, TYPE_SPRITES["avtomat_y_up"]],
                           TYPE_SPRITES["avtomat_size"],
                           'sprites/avtomat/avtomat_3.png')
        avtomat_2 = Object(self.parent, self.game, self.base_style,
                           [860, TYPE_SPRITES["avtomat_y_up"]],
                           TYPE_SPRITES["avtomat_size"],
                           'sprites/avtomat/avtomat_1.png')
        clock = Object(self.parent, self.game, self.base_style, [650, 60],
                         TYPE_SPRITES["clock"], 'sprites/_other/clock.png')

        title_room = Object(self.parent, self.game, self.base_style, [100, 20],
                         TYPE_SPRITES["comp_size"], 'sprites/titles/computer_room_logo.png')
        chair_1 = Object(self.parent, self.game, self.base_style, [300, 110],
                         TYPE_SPRITES["chair"], 'sprites/_other/chair_1.png', size_rect=(0, -100))

        chair_2 = Object(self.parent, self.game, self.base_style, [530, 113],
                         TYPE_SPRITES["chair"], 'sprites/_other/chair_2.png', size_rect=(0, -100))

        chair_3 = Object(self.parent, self.game, self.base_style, [300, 250],
                         TYPE_SPRITES["chair"], 'sprites/_other/chair_2.png', size_rect=(0, -100))

        chair_4 = Object(self.parent, self.game, self.base_style, [520, 400],
                         TYPE_SPRITES["chair"], 'sprites/_other/chair_1.png', size_rect=(0, -100))

        chair_5 = Object(self.parent, self.game, self.base_style, [100, 400],
                         TYPE_SPRITES["chair"], 'sprites/_other/chair_1.png', size_rect=(0, -100))

        sofa_1 = Object(self.parent, self.game, self.base_style, [23, 700],
                         TYPE_SPRITES["sofa_size"], 'sprites/sofas/black_sofa.png', size_rect=(0, -40))
        sofa_2 = Object(self.parent, self.game, self.base_style, [211, 700],
                         TYPE_SPRITES["sofa_size"], 'sprites/sofas/black_sofa.png', size_rect=(0, -40))

        self.computer_sprites = ['sprites/comp/gaming_comp_1.png', 'sprites/comp/gaming_comp_2.png',
                                 'sprites/comp/gaming_comp_3.png', 'sprites/comp/gaming_comp_4.png',
                                 'sprites/comp/gaming_comp_5.png', 'sprites/comp/gaming_comp_6.png',
                                 'sprites/comp/gaming_comp_7.png', 'sprites/comp/gaming_comp_8.png',
                                 'sprites/comp/gaming_comp_9.png']

        computer_1 = Object(self.parent, self.game, self.base_style, [30, 110],
                            TYPE_SPRITES["comp_size"], self.computer_sprites[4], size_rect=(0, -100))
        computer_2 = Object(self.parent, self.game, self.base_style, [250, 110],
                            TYPE_SPRITES["comp_size"], self.computer_sprites[4], size_rect=(0, -100))
        computer_3 = Object(self.parent, self.game, self.base_style, [480, 105],
                            TYPE_SPRITES["comp_size"], self.computer_sprites[4])
        computer_4 = Object(self.parent, self.game, self.base_style, [30, 250],  # 300
                            TYPE_SPRITES["comp_size"], self.computer_sprites[4], size_rect=(0, -100))
        computer_5 = Object(self.parent, self.game, self.base_style, [250, 250],  # 300
                            TYPE_SPRITES["comp_size"], self.computer_sprites[4], size_rect=(0, -100))
        computer_6 = Object(self.parent, self.game, self.base_style, [480, 250],  # 300
                            TYPE_SPRITES["comp_size"], self.computer_sprites[4], size_rect=(0, -100))
        computer_7 = Object(self.parent, self.game, self.base_style, [30, 400],  # 300
                            TYPE_SPRITES["comp_size"], self.computer_sprites[4], size_rect=(0, -100))
        computer_8 = Object(self.parent, self.game, self.base_style, [250, 400],  # 300
                            TYPE_SPRITES["comp_size"], self.computer_sprites[4], size_rect=(0, -100))
        computer_9 = Object(self.parent, self.game, self.base_style, [480, 400],  # 300
                            TYPE_SPRITES["comp_size"], self.computer_sprites[4], size_rect=(0, -100))

        self.sprite_computer_for_1 = [1, 0.1, 8]
        self.sprite_computer_isprite_1 = self.sprite_computer_for_1[0]
        self.sprite_computer_isprite_1_OLD = self.sprite_computer_isprite_1
        self.sprite_computer_for_2 = [3, 0.1, 8]
        self.sprite_computer_isprite_2 = self.sprite_computer_for_2[0]
        self.sprite_computer_isprite_2_OLD = self.sprite_computer_isprite_2
        self.sprite_computer_for_3 = [2, 0.1, 8]
        self.sprite_computer_isprite_3 = self.sprite_computer_for_3[0]
        self.sprite_computer_isprite_3_OLD = self.sprite_computer_isprite_3
        self.sprite_computer_for_4 = [4, 0.1, 8]
        self.sprite_computer_isprite_4 = self.sprite_computer_for_4[0]
        self.sprite_computer_isprite_4_OLD = self.sprite_computer_isprite_4
        self.sprite_computer_for_5 = [9, 0.1, 8]
        self.sprite_computer_isprite_5 = self.sprite_computer_for_5[0]
        self.sprite_computer_isprite_5_OLD = self.sprite_computer_isprite_5
        self.sprite_computer_for_6 = [7, 0.1, 8]
        self.sprite_computer_isprite_6 = self.sprite_computer_for_6[0]
        self.sprite_computer_isprite_6_OLD = self.sprite_computer_isprite_6
        self.sprite_computer_for_7 = [8, 0.1, 8]
        self.sprite_computer_isprite_7 = self.sprite_computer_for_7[0]
        self.sprite_computer_isprite_7_OLD = self.sprite_computer_isprite_7
        self.sprite_computer_for_8 = [6, 0.1, 8]
        self.sprite_computer_isprite_8 = self.sprite_computer_for_8[0]
        self.sprite_computer_isprite_8_OLD = self.sprite_computer_isprite_8
        self.sprite_computer_for_9 = [5, 0.1, 8]
        self.sprite_computer_isprite_9 = self.sprite_computer_for_9[0]
        self.sprite_computer_isprite_9_OLD = self.sprite_computer_isprite_9

        walls, self.passages = self.game.draw_walls(color_left=["black"], color_up=["blue"],
                                     color_right=["black"],
                                     thinkess=THIKNESS_WALL, height=HEIGHT_WALL, width_door=150, down="wall, pass")
        print("comp passages", *self.passages.items())
        dop_walls = dict(list(filter(lambda x: x[0] in ["wall_up"], walls.items())))
        walls = dict(list(filter(lambda x: x[0] not in dop_walls.keys(), walls.items())))

        self.buttons = []
        # ------------------
        self.objects = {"title_room": title_room,
                        'chair_2': chair_2, 'chair_1': chair_1, 'chair_3': chair_3, 'chair_4': chair_4, 'chair_5': chair_5,
                        "computer_1": computer_1, "computer_2": computer_2, "computer_3": computer_3,
                        "computer_4": computer_4, 'computer_5': computer_5, 'computer_6': computer_6,
                        'computer_7': computer_7, 'computer_8': computer_8, 'computer_9': computer_9,
                        "sofa_1": sofa_1, "sofa_2": sofa_2,
                        "avtomvat_1": avtomat_1, "avtomvat_2": avtomat_2,
                        'clock': clock}
        for k, v in walls.items():
            self.objects[k] = v
        self.list_objects = list(self.objects.values())
        # ------------------
        self.dop_objects = {}
        for k, v in dop_walls.items():
            self.dop_objects[k] = v
        self.list_dop_objects = list(self.dop_objects.values())

        self.texture_floor = pygame.image.load('sprites/floor.png')

        # self.buttons = []
        # # self.init_button_menu()
        # button_ps = {
        #     "font": pygame.font.Font(self.base_style["font_path"], 30),
        #     "coords": (400, 400, 75, 37),# (111 - 260 + 480, 111, 75, 37),
        #     "text": "",
        #     "color": {
        #         "inactive": self.base_style["colors"]["black"],
        #         "hover": self.base_style["colors"]["base1"],
        #         "pressed": self.base_style["colors"]["light"],
        #         "text": self.base_style["colors"]["light"]
        #     },
        #     "func": lambda: self.game.change_game('ps')
        # }
        # button_ps["button"] = self.parent.button(coords=button_ps["coords"],
        #                                          text=button_ps["text"],
        #                                          color=button_ps["color"],
        #                                          font=button_ps["font"],
        #                                          func=button_ps["func"])
        # self.buttons.append(button_ps)
        self.init_buttons()

    def enter_rooms(self):
        self.game.character.respawn([self.parent.display_w // 2, self.parent.display_h-self.game.character.character["coords"][3]-THIKNESS_WALL-20])
        self.game.floor.blit(self.texture_floor, (0, 0))
        self.game.data_layers = [0] * len(self.buttons)
        self.game.old_data_layers = [0] * len(self.buttons)

    def init_buttons(self):
        button_computer_1 = Hitbox_Button(parent=self.parent, game=self.game, object=self.objects["computer_1"], layer=self.parent.display,
                                    # self.game.layer_buttons_1
                                    func=lambda: self.game.change_game('dash_hex'), coords=TYPE_BUTTONS["comp_cord"],
                                    size=TYPE_BUTTONS["comp_size"],
                                    colors=TYPE_BUTTONS["color"])
        self.buttons.append(button_computer_1)

        button_computer_8 = Hitbox_Button(parent=self.parent, game=self.game, object=self.objects["computer_8"],
                                          layer=self.parent.display,
                                          # self.game.layer_buttons_1
                                          func=lambda: self.game.change_game('hyper_dash'),
                                          coords=TYPE_BUTTONS["comp_cord"],
                                          size=TYPE_BUTTONS["comp_size"],
                                          colors=TYPE_BUTTONS["color"])
        self.buttons.append(button_computer_8)
        button_computer_4 = Hitbox_Button(parent=self.parent, game=self.game, object=self.objects["computer_4"], layer=self.parent.display,
                                    # self.game.layer_buttons_1
                                    func=lambda: self.game.change_game('circle'), coords=TYPE_BUTTONS["comp_cord"],
                                    size=TYPE_BUTTONS["comp_size"],
                                    colors=TYPE_BUTTONS["color"])
        self.buttons.append(button_computer_4)
        button_computer_6 = Hitbox_Button(parent=self.parent, game=self.game, object=self.objects["computer_6"],
                                    layer=self.parent.display,
                                    # self.game.layer_buttons_1
                                    func=lambda: self.game.change_game('dino'), coords=TYPE_BUTTONS["comp_cord"],
                                    size=TYPE_BUTTONS["comp_size"],
                                    colors=TYPE_BUTTONS["color"])
        self.buttons.append(button_computer_6)
        button_avtomat_1 = Hitbox_Button(parent=self.parent, game=self.game, object=self.objects["avtomvat_1"],
                                            layer=self.parent.display,
                                            func=lambda: self.game.energy_character_up(
                                                price=TYPE_ENERGY["blue"]["price"],
                                                val=TYPE_ENERGY["blue"]["val"]),
                                            coords=TYPE_BUTTONS["avtomat_cord"],
                                            size=TYPE_BUTTONS["avtomat_size"],
                                            colors=TYPE_BUTTONS["color"])
        self.buttons.append(button_avtomat_1)
        button_avtomat_green = Hitbox_Button(parent=self.parent, game=self.game, object=self.objects["avtomvat_2"],
                                         layer=self.parent.display,
                                         func=lambda: self.game.energy_character_up(
                                             price=TYPE_ENERGY["green"]["price"],
                                             val=TYPE_ENERGY["green"]["val"]),
                                         coords=TYPE_BUTTONS["avtomat_green_cord"],
                                         size=TYPE_BUTTONS["avtomat_green_size"],
                                         colors=TYPE_BUTTONS["color"])
        self.buttons.append(button_avtomat_green)

    def delete_buttons(self):
        for j in range(len(self.buttons) - 1, -1, -1):
            del self.buttons[j]

    def delete_all(self):
        self.delete_buttons()

    def draw(self):
        self.animate_computer_sprites()
        self.game.render_objects(self.list_objects, buttons=self.buttons, dop_objects=self.list_dop_objects, draw_rects=False)
        if self.passages["down"][0][0] < self.game.character.character["absolute_coords_rect"][0] < self.passages["down"][0][1] and self.game.character.character["absolute_coords_rect"][1] >= self.passages["down"][1]:
            self.game.character.respawn([self.parent.display_w // 2, HEIGHT_WALL])
            self.game.room_change("reception")

    def animate_computer_sprites(self):
        self.sprite_computer_for_1 = self.game.animate_sprite(self.sprite_computer_for_1, reverse=True)
        self.sprite_computer_isprite_1 = int(self.sprite_computer_for_1[0])
        if  self.sprite_computer_isprite_1 != self.sprite_computer_isprite_1_OLD:
            self.objects["computer_1"].update_sprite(self.computer_sprites[self.sprite_computer_isprite_1])
        self.sprite_computer_isprite_1_OLD = self.sprite_computer_isprite_1

        self.sprite_computer_for_2 = self.game.animate_sprite(self.sprite_computer_for_2, reverse=True)
        self.sprite_computer_isprite_2 = int(self.sprite_computer_for_2[0])
        if self.sprite_computer_isprite_2 != self.sprite_computer_isprite_2_OLD:
            self.objects["computer_2"].update_sprite(self.computer_sprites[self.sprite_computer_isprite_2])
        self.sprite_computer_isprite_2_OLD = self.sprite_computer_isprite_2

        self.sprite_computer_for_3 = self.game.animate_sprite(self.sprite_computer_for_3, reverse=True)
        self.sprite_computer_isprite_3 = int(self.sprite_computer_for_3[0])
        if self.sprite_computer_isprite_3 != self.sprite_computer_isprite_3_OLD:
            self.objects["computer_3"].update_sprite(self.computer_sprites[self.sprite_computer_isprite_3])
        self.sprite_computer_isprite_3_OLD = self.sprite_computer_isprite_3

        self.sprite_computer_for_4 = self.game.animate_sprite(self.sprite_computer_for_4, reverse=True)
        self.sprite_computer_isprite_4 = int(self.sprite_computer_for_4[0])
        if self.sprite_computer_isprite_4 != self.sprite_computer_isprite_4_OLD:
            self.objects["computer_4"].update_sprite(self.computer_sprites[self.sprite_computer_isprite_4])
        self.sprite_computer_isprite_4_OLD = self.sprite_computer_isprite_4

        self.sprite_computer_for_5 = self.game.animate_sprite(self.sprite_computer_for_4, reverse=True)
        self.sprite_computer_isprite_5 = int(self.sprite_computer_for_5[0])
        if self.sprite_computer_isprite_5 != self.sprite_computer_isprite_5_OLD:
            self.objects["computer_5"].update_sprite(self.computer_sprites[self.sprite_computer_isprite_5])
        self.sprite_computer_isprite_5_OLD = self.sprite_computer_isprite_5

        self.sprite_computer_for_6 = self.game.animate_sprite(self.sprite_computer_for_6, reverse=True)
        self.sprite_computer_isprite_6 = int(self.sprite_computer_for_6[0])
        if self.sprite_computer_isprite_6 != self.sprite_computer_isprite_6_OLD:
            self.objects["computer_6"].update_sprite(self.computer_sprites[self.sprite_computer_isprite_6])
        self.sprite_computer_isprite_6_OLD = self.sprite_computer_isprite_6

        self.sprite_computer_for_7 = self.game.animate_sprite(self.sprite_computer_for_7, reverse=True)
        self.sprite_computer_isprite_7 = int(self.sprite_computer_for_7[0])
        if self.sprite_computer_isprite_7 != self.sprite_computer_isprite_7_OLD:
            self.objects["computer_7"].update_sprite(self.computer_sprites[self.sprite_computer_isprite_7])
        self.sprite_computer_isprite_7_OLD = self.sprite_computer_isprite_7

        self.sprite_computer_for_8 = self.game.animate_sprite(self.sprite_computer_for_8, reverse=True)
        self.sprite_computer_isprite_8 = int(self.sprite_computer_for_8[0])
        if self.sprite_computer_isprite_8 != self.sprite_computer_isprite_8_OLD:
            self.objects["computer_8"].update_sprite(self.computer_sprites[self.sprite_computer_isprite_8])
        self.sprite_computer_isprite_8_OLD = self.sprite_computer_isprite_8

        self.sprite_computer_for_9 = self.game.animate_sprite(self.sprite_computer_for_9, reverse=True)
        self.sprite_computer_isprite_9 = int(self.sprite_computer_for_9[0])
        if self.sprite_computer_isprite_9 != self.sprite_computer_isprite_9_OLD:
            self.objects["computer_9"].update_sprite(self.computer_sprites[self.sprite_computer_isprite_9])
        self.sprite_computer_isprite_9_OLD = self.sprite_computer_isprite_9



class PS_room:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game


        avtomat = Object(self.parent, self.game, self.base_style, [30, TYPE_SPRITES["avtomat_y_up"]], TYPE_SPRITES["avtomat_size"], 'sprites/avtomat/avtomat_1.png',  size_rect=(0, 0))
        ps_room_logo = Object(self.parent, self.game, self.base_style, [710, 30], (250, 150), 'sprites/titles/ps_room_logo.png')
        tv = Object(self.parent, self.game, self.base_style, [340, 50], (300, 125), 'sprites/comp/TV_for_PS.png')
        ps_table = Object(self.parent, self.game, self.base_style, [400, 150], (180, 110), 'sprites/play station/ps_table.png')
        speaker_left = Object(self.parent, self.game, self.base_style, [280, 100],
                        (48, 120), 'sprites/loudspeaker/loudspeaker_1.png', size_rect=(0, 0))
        speaker_right = Object(self.parent, self.game, self.base_style, [650, 100],
                              (48, 120), 'sprites/loudspeaker/loudspeaker_1.png',  size_rect=(0, 0))
        tables = Object(self.parent, self.game, self.base_style, [200, 600],
                              (500, 120), 'sprites/_other/tables.png')
        chair1 = Object(self.parent, self.game, self.base_style, [140, 590],
                        (50, 100), 'sprites/_other/chair_left_side.png')
        chair2 = Object(self.parent, self.game, self.base_style, [235, 520],
                              (50, 100), 'sprites/_other/chair_front_side.png')
        chair3 = Object(self.parent, self.game, self.base_style, [360, 520],
                        (50, 100), 'sprites/_other/chair_front_side.png')
        chair4 = Object(self.parent, self.game, self.base_style, [485, 520],
                        (50, 100), 'sprites/_other/chair_front_side.png')
        chair5 = Object(self.parent, self.game, self.base_style, [610, 520],
                        (50, 100), 'sprites/_other/chair_front_side.png')
        chair6 = Object(self.parent, self.game, self.base_style, [710, 590],
                        (50, 100), 'sprites/_other/chair_right_side.png')


        rotated_armchair = Object(self.parent, self.game, self.base_style, [570, 320],
                              (70, 70), 'sprites/_other/rotated_armchair.png')
        pufik1 = Object(self.parent, self.game, self.base_style, [475, 335],
                        (70, 70), 'sprites/_other/pufik.png')
        armchair = Object(self.parent, self.game, self.base_style, [340, 335],
                        (70, 70), 'sprites/_other/armchair.png')
        pufik2 = Object(self.parent, self.game, self.base_style, [400, 285],
                        (70, 70), 'sprites/_other/back_side_pufik.png')
        pufik3 = Object(self.parent, self.game, self.base_style, [485, 255],
                        (70, 70), 'sprites/_other/back_side_pufik.png')

        self.sprite_coolers = ['sprites/kuler/1.png', 'sprites/kuler/2.png', 'sprites/kuler/3.png', 'sprites/kuler/4.png',
                        'sprites/kuler/5.png', 'sprites/kuler/6.png', 'sprites/kuler/7.png', 'sprites/kuler/8.png',
                        'sprites/kuler/9.png']
        self.sprite_cooler_for = [1, 0.1, 8]
        self.sprite_cooler_isprite = self.sprite_cooler_for[0]
        self.sprite_cooler_isprite_OLD = self.sprite_cooler_isprite
        current_cooler = Object(self.parent, self.game, self.base_style, [140, 110], (40, 140), self.sprite_coolers[0],  size_rect=(0, 0))

        walls, self.passages = self.game.draw_walls(color_left=["black"], color_up=["black"],
                                     color_right=["black", "black"],
                                     thinkess=THIKNESS_WALL, height=HEIGHT_WALL, width_door=150, down="wall")
        print("ps passages", *self.passages.items())
        dop_walls = dict(list(filter(lambda x: x[0] in ["wall_up"], walls.items())))
        walls = dict(list(filter(lambda x: x[0] not in dop_walls.keys(), walls.items())))

        self.buttons = []
        # ------------------
        self.objects = {"avtomat": avtomat, "ps_room_logo": ps_room_logo, "tv": tv, "ps_table": ps_table,
                        "cooler": current_cooler,
                        "speaker_left": speaker_left, "speaker_right": speaker_right, "tables": tables,
                        "rotated_armchair": rotated_armchair, "pufik1": pufik1, "armchair": armchair, "pufik2": pufik2,
                        "pufik3": pufik3, "chair1": chair1, "chair2": chair2, "chair3": chair3, "chair4": chair4,
                        "chair5": chair5, "chair6": chair6}
        for k, v in walls.items():
            self.objects[k] = v
        self.list_objects = list(self.objects.values())
        # ------------------
        self.dop_objects = {}
        for k, v in dop_walls.items():
            self.dop_objects[k] = v
        self.list_dop_objects = list(self.dop_objects.values())

        self.texture_floor = pygame.image.load('sprites/floor.png')

        self.init_buttons()

    def enter_rooms(self):
        self.game.character.respawn([self.parent.display_w-self.game.character.character["coords"][2], self.parent.display_h // 2])
        self.game.floor.blit(self.texture_floor, (0, 0))
        self.game.data_layers = [0] * len(self.buttons)
        self.game.old_data_layers = [0] * len(self.buttons)

    def init_buttons(self):
        button_tv = Hitbox_Button(parent=self.parent, game=self.game, object=self.objects["tv"],
                                    layer=self.parent.display,
                                    # self.game.layer_buttons_1
                                    func=lambda: self.game.change_game('ps'), coords=TYPE_BUTTONS["tv_ps_cord"],
                                    size=TYPE_BUTTONS["tv_ps_size"],
                                    colors=TYPE_BUTTONS["color"])
        self.buttons.append(button_tv)
        button_avtomat_green = Hitbox_Button(parent=self.parent, game=self.game, object=self.objects["avtomat"],
                                             layer=self.parent.display,
                                             func=lambda: self.game.energy_character_up(
                                                 price=TYPE_ENERGY["green"]["price"],
                                                 val=TYPE_ENERGY["green"]["val"]),
                                             coords=TYPE_BUTTONS["avtomat_green_cord"],
                                             size=TYPE_BUTTONS["avtomat_green_size"],
                                             colors=TYPE_BUTTONS["color"])
        self.buttons.append(button_avtomat_green)

    def delete_buttons(self):
        for j in range(len(self.buttons) - 1, -1, -1):
            del self.buttons[j]

    def delete_all(self):
        self.delete_buttons()

    def draw(self):
        self.sprite_cooler_for = self.game.animate_sprite(self.sprite_cooler_for)
        self.sprite_cooler_isprite = int(self.sprite_cooler_for[0])
        if self.sprite_cooler_isprite != self.sprite_cooler_isprite_OLD:
            self.objects["cooler"].update_sprite(self.sprite_coolers[self.sprite_cooler_isprite])
        self.sprite_cooler_isprite_OLD = self.sprite_cooler_isprite


        self.game.render_objects(self.list_objects, buttons=self.buttons, dop_objects=self.list_dop_objects)
        if self.game.character.character["absolute_coords_rect"][0] >= self.passages["right"][0] and self.passages["right"][1][0] < self.game.character.character["absolute_coords_rect"][1] < self.passages["right"][1][1]:
            self.game.character.respawn([self.game.character.character["coords"][2], self.parent.display_h // 2])
            self.game.room_change("reception")



class VR_room:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game

        #avtomat = Object(self.parent, self.game, self.base_style, [300, TYPE_SPRITES["avtomat_y_up"]], TYPE_SPRITES["avtomat_size"],
                         #'sprites/avtomat/avtomat_1.png')

        walls, self.passages = self.game.draw_walls(color_left=["black", "black"], color_up=["black"],
                                     color_right=["black"],
                                     thinkess=THIKNESS_WALL, height=HEIGHT_WALL, width_door=150, down="wall")
        print("ps passages", *self.passages.items())

        table_1 = Object(self.parent, self.game, self.base_style, [45, 145], (150, 100),
                         'sprites/vr_room/vr_table_1.png', size_rect=(0, 0))
        table_2 = Object(self.parent, self.game, self.base_style, [220, 145], (150, 100),
                         'sprites/vr_room/vr_table_2.png', size_rect=(0, 0))
        table_3 = Object(self.parent, self.game, self.base_style, [395, 145], (150, 100),
                         'sprites/vr_room/vr_table_3.png', size_rect=(0, 0))
        table_4 = Object(self.parent, self.game, self.base_style, [570, 145], (150, 100),
                         'sprites/vr_room/vr_table_4.png', size_rect=(0, 0))

        screen_1 = Object(self.parent, self.game, self.base_style, [75, 75], (100, 50),
                          'sprites/comp/TV_for_PS.png')
        screen_2 = Object(self.parent, self.game, self.base_style, [250, 75], (100, 50),
                          'sprites/comp/TV_for_PS.png')
        screen_3 = Object(self.parent, self.game, self.base_style, [425, 75], (100, 50),
                          'sprites/comp/TV_for_PS.png')
        screen_4 = Object(self.parent, self.game, self.base_style, [600, 75], (100, 50),
                          'sprites/comp/TV_for_PS.png')

        # Еще объекты
        sofa_0 = Object(self.parent, self.game, self.base_style, [750, 145], (200, 91),
                        'sprites/_other/sofa.png', size_rect=(0, 0))


        title_room = Object(self.parent, self.game, self.base_style, [717, 24], (260, 160),
                              'sprites/titles/vr_room_logo.png')

        play_avtomat = Object(self.parent, self.game, self.base_style, [875, 500], (90, 160),
                        'sprites/_other/play_game.png', size_rect=(-30, -150))

        racing_armchair = Object(self.parent, self.game, self.base_style, [65, 550], (220, 170),
                        'sprites/_other/pixel_driving_armchair.png')

        dop_walls = dict(list(filter(lambda x: x[0] in ["wall_up"], walls.items())))
        walls = dict(list(filter(lambda x: x[0] not in dop_walls.keys(), walls.items())))

        self.buttons = []
        # ------------------
        self.objects = {"title_room": title_room,
                        #"avtomat": avtomat,
        "table_1": table_1, "table_2": table_2, "table_3": table_3, "table_4": table_4,
        "screen_1": screen_1, "screen_2": screen_2, "screen_3": screen_3, "screen_4": screen_4,
                        'sofa_0': sofa_0, 'play_avtomat': play_avtomat, 'racing_chair': racing_armchair}
        for k, v in walls.items():
            self.objects[k] = v
        self.list_objects = list(self.objects.values())
        # ------------------
        self.dop_objects = {}
        for k, v in dop_walls.items():
            self.dop_objects[k] = v
        self.list_dop_objects = list(self.dop_objects.values())

        self.texture_floor = pygame.image.load('sprites/floor.png')

        self.init_buttons()

    def enter_rooms(self):
        self.game.character.respawn([self.game.character.character["coords"][2], self.parent.display_h // 2])
        self.game.floor.blit(self.texture_floor, (0, 0))
        self.game.data_layers = [0] * len(self.buttons)
        self.game.old_data_layers = [0] * len(self.buttons)

    def init_buttons(self):
        for i in range(1, 4+1):
            button_screen = Hitbox_Button(parent=self.parent, game=self.game, object=self.objects[f"screen_{i}"],
                                      layer=self.parent.display,
                                      func=lambda: self.game.change_game('d_game'), coords=TYPE_BUTTONS["tv_vr_cord"],
                                      size=TYPE_BUTTONS["tv_vr_size"],
                                      colors=TYPE_BUTTONS["color"])

            button_tv = Hitbox_Button(parent=self.parent, game=self.game, object=self.objects['play_avtomat'],
                                      layer=self.parent.display,
                                      func=lambda: self.game.change_game('flappy_bird'), coords=(0, -5),
                                      size=(95, 165),
                                      colors=TYPE_BUTTONS["color"])
            self.buttons.append(button_screen)
            self.buttons.append(button_tv)

    def delete_buttons(self):
        for j in range(len(self.buttons) - 1, -1, -1):
            del self.buttons[j]

    def delete_all(self):
        self.delete_buttons()

    def draw(self):
        self.game.render_objects(self.list_objects, buttons=self.buttons, dop_objects=self.list_dop_objects)
        if self.game.character.character["absolute_coords_rect"][0] <= self.passages["left"][0] and self.passages["left"][1][0] < self.game.character.character["absolute_coords_rect"][1] < self.passages["left"][1][1]:
            self.game.character.respawn([self.parent.display_w - self.game.character.character["coords"][2], self.parent.display_h // 2])
            self.game.room_change("reception")