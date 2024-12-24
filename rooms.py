import pygame
from pygame_widgets.button import Button

THIKNESS_WALL = 30
HEIGHT_WALL = 200
TYPE_BUTTONS = {
    "comp_cord": (77, -5), "comp_size": (83, 47), # (63, 28)
    "avtomat_cord": (15, 23), "avtomat_size": (95, 182), # (63, 28)
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




class Object:
    def __init__(self, parent, game, base_style, coords, size, image, size_rect=(0, 20), coords_rect=(0, 0)):
        self.base_style = base_style
        self.parent = parent
        self.game = game
        self.img = image
        self.size = size

        self.coords = coords
        self.size_rect = list(size_rect)
        self.coords_rect = coords_rect
        self.init_data()

    def init_data(self):
        self.data = {
            "color": self.base_style["colors"]["light"],
            "coords": [self.coords[0], self.coords[1], self.size[0], self.size[1]],  # 50, 70
            "size_rect": self.size_rect,
            "coords_rect": self.coords_rect,
            "type_render": 1
        }
        self.data["sprite"] = pygame.image.load(self.img).convert_alpha()
        self.data["rect"] = self.data["sprite"].get_rect()
        for i in range(len(self.size_rect)):
            if self.data["size_rect"][i] == 0:
                self.data["size_rect"][i] = self.size[i]
            elif self.data["size_rect"][i] < 0:
                self.data["size_rect"][i] = self.size[i] - abs(self.size_rect[i])
            else:
                self.data["size_rect"][i] = self.size_rect[i]
        # if self.data["coords_rect"][0] <= 0:
        #     self.data["coords_rect"][0] = self.data["coords"][0] + self.size[0]
        # else:
        #     self.data["coords_rect"][0] = self.data["coords_rect"][0]
        self.set_sprite()

    def set_sprite(self):
        self.data["sprite"] = pygame.transform.scale(self.data["sprite"],(self.data["coords"][2], self.data["coords"][3]))
        self.data["rect"].x = self.data["coords"][0] + self.data["coords_rect"][0]
        self.data["rect"].y = self.data["coords"][1] + self.data["coords"][3] - self.data["size_rect"][1] - self.data["coords_rect"][1]
        self.data["rect"].w = self.data["size_rect"][0] # self.data["coords"][2]
        self.data["rect"].h = self.data["size_rect"][1] # self.character["coords"][3]

    def update_sprite(self, img):
        self.img = img
        self.data["sprite"] = pygame.image.load(self.img).convert_alpha()
        self.set_sprite()

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
        avtomat_1 = Object(self.parent, self.game, self.base_style,
                               [20, TYPE_SPRITES["avtomat_y_up"]],
                         TYPE_SPRITES["avtomat_size"],
                               'sprites/avtomat/avtomat_2.png')
        button_avtomat_1 = Buttons(parent=self.parent, game=self.game, object=avtomat_1, layer=self.parent.display,
                                    # self.game.layer_buttons_1
                                    func=lambda: self.game.energy_character_up(price=3, val=1), coords=TYPE_BUTTONS["avtomat_cord"],
                                    size=TYPE_BUTTONS["avtomat_size"],
                                    colors=TYPE_BUTTONS["color"])
        avtomat_2 = Object(self.parent, self.game, self.base_style,
                         [110, TYPE_SPRITES["avtomat_y_up"]],
                         TYPE_SPRITES["avtomat_size"],
                         'sprites/avtomat/avtomat_3.png')
        title_room = Object(self.parent, self.game, self.base_style, [590, 15],
                                     (280, 190), 'sprites/titles/ultimate_reseption_logo.png')

        reception_table = Object(self.parent, self.game, self.base_style, [400, 350],
                                      (200, 140), 'sprites/_other/reseption_table.png')
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

        walls = self.game.draw_walls(color_left=["black", "blue"], color_up=["blue", "black"],  color_right=["black", "black"],
                                     thinkess=THIKNESS_WALL, height=HEIGHT_WALL, width_door=150)
        dop_walls = dict(list(filter(lambda x: x[0] in ["wall_up_1", "wall_up_2"], walls.items())))
        print(dop_walls)
        walls = dict(list(filter(lambda x: x[0] not in dop_walls.keys(), walls.items())))

        self.buttons = [button_avtomat_1]
        # ------------------
        self.objects = {"avtomat_1": avtomat_1, "avtomat_2": avtomat_2, "title_room": title_room,
                        "reception_table": reception_table,
                        "plant_1": plant_1, "sofa_1": sofa_1, "sofa_2": sofa_2, "sofa_3": sofa_3, "sofa_4": sofa_4}
        for k, v in walls.items():
            self.objects[k] = v
        self.list_objects = list(self.objects.values())
        # ------------------
        self.dop_objects = {}
        for k, v in dop_walls.items():
            self.dop_objects[k] = v
        self.list_dop_objects = list(self.dop_objects.values())
        print(self.list_objects, self.list_dop_objects)

        self.texture_floor = pygame.image.load('sprites/floor.png')

    def enter_rooms(self):
        self.game.floor.blit(self.texture_floor, (0, 0))
        self.game.data_layers = [0] * len(self.buttons)
        self.game.old_data_layers = [0] * len(self.buttons)

    def delete_all(self):
        pass

    def draw(self):
        self.game.render_objects(self.list_objects, buttons=self.buttons, dop_objects=self.list_dop_objects)
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

        chair_2 = Object(self.parent, self.game, self.base_style, [530, 120],
                         TYPE_SPRITES["chair"], 'sprites/_other/chair_2.png', size_rect=(0, -100))

        chair_3 = Object(self.parent, self.game, self.base_style, [300, 250],
                         TYPE_SPRITES["chair"], 'sprites/_other/chair_2.png', size_rect=(0, -100))

        chair_4 = Object(self.parent, self.game, self.base_style, [520, 400],
                         TYPE_SPRITES["chair"], 'sprites/_other/chair_1.png', size_rect=(0, -100))

        computer_1 = Object(self.parent, self.game, self.base_style, [30, 110],
                                     TYPE_SPRITES["comp_size"], 'sprites/comp/comp_1.png', size_rect=(0, -100))
        button_computer_1 = Buttons(parent=self.parent, game=self.game, object=computer_1, layer=self.parent.display,
                                    # self.game.layer_buttons_1
                                    func=lambda: self.game.change_game('ps'), coords=TYPE_BUTTONS["comp_cord"],
                                    size=TYPE_BUTTONS["comp_size"],
                                    colors=TYPE_BUTTONS["color"])
        computer_2 = Object(self.parent, self.game, self.base_style, [250, 110],
                          TYPE_SPRITES["comp_size"], 'sprites/comp/comp_1.png', size_rect=(0, -100))
        computer_3 = Object(self.parent, self.game, self.base_style, [480, 110],
                            TYPE_SPRITES["comp_size"], 'sprites/comp/comp_1.png') #, coords_rect=0
        computer_4 = Object(self.parent, self.game, self.base_style, [30, 300], # 300
                            TYPE_SPRITES["comp_size"], 'sprites/comp/comp_1.png', size_rect=(0, -100))
        computer_4 = Object(self.parent, self.game, self.base_style, [30, 250], # 300
                            TYPE_SPRITES["comp_size"], 'sprites/comp/comp_1.png', size_rect=(0, -100))

        computer_5 = Object(self.parent, self.game, self.base_style, [250, 250], # 300
                            TYPE_SPRITES["comp_size"], 'sprites/comp/comp_1.png', size_rect=(0, -100))

        computer_6 = Object(self.parent, self.game, self.base_style, [480, 250],  # 300
                            TYPE_SPRITES["comp_size"], 'sprites/comp/comp_1.png', size_rect=(0, -100))

        computer_7 = Object(self.parent, self.game, self.base_style, [30, 400],  # 300
                            TYPE_SPRITES["comp_size"], 'sprites/comp/comp_1.png', size_rect=(0, -100))

        computer_8 = Object(self.parent, self.game, self.base_style, [250, 400],  # 300
                            TYPE_SPRITES["comp_size"], 'sprites/comp/comp_1.png', size_rect=(0, -100))

        computer_9 = Object(self.parent, self.game, self.base_style, [480, 400],  # 300
                            TYPE_SPRITES["comp_size"], 'sprites/comp/comp_1.png', size_rect=(0, -100))

        sofa_1 = Object(self.parent, self.game, self.base_style, [23, 700],
                         TYPE_SPRITES["sofa_size"], 'sprites/sofas/black_sofa.png', size_rect=(0, -40))
        sofa_2 = Object(self.parent, self.game, self.base_style, [211, 700],
                         TYPE_SPRITES["sofa_size"], 'sprites/sofas/black_sofa.png', size_rect=(0, -40))
        # def __init__(self, parent, game, object, layer, func, coords, size, colors):
        button_computer_4 = Buttons(parent=self.parent, game=self.game, object=computer_4, layer=self.parent.display, # self.game.layer_buttons_1
                                    func=lambda: self.game.change_game('circle'), coords=TYPE_BUTTONS["comp_cord"], size=TYPE_BUTTONS["comp_size"],
                                    colors=TYPE_BUTTONS["color"])

        button_computer_6 = Buttons(parent=self.parent, game=self.game, object=computer_6, layer=self.parent.display,
                                    # self.game.layer_buttons_1
                                    func=lambda: self.game.change_game('dino'), coords=TYPE_BUTTONS["comp_cord"],
                                    size=TYPE_BUTTONS["comp_size"],
                                    colors=TYPE_BUTTONS["color"])

        walls = self.game.draw_walls(color_left=["black"], color_up=["blue"],
                                     color_right=["black"],
                                     thinkess=THIKNESS_WALL, height=HEIGHT_WALL, width_door=150)
        dop_walls = dict(list(filter(lambda x: x[0] in ["wall_up"], walls.items())))
        print(dop_walls)
        walls = dict(list(filter(lambda x: x[0] not in dop_walls.keys(), walls.items())))

        self.buttons = [button_computer_1, button_computer_4, button_computer_6]
        # ------------------
        self.objects = {"title_room": title_room,
                        'chair_2': chair_2, 'chair_1': chair_1, 'chair_3': chair_3, 'chair_4': chair_4,
                        "computer_1": computer_1, "computer_2": computer_2, "computer_3": computer_3, "computer_4": computer_4, 'computer_5': computer_5, 'computer_6': computer_6, 'computer_7': computer_7, 'computer_8': computer_8, 'computer_9': computer_9,
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
        print(self.list_objects, self.list_dop_objects)

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

    def enter_rooms(self):
        self.game.character.respawn([self.parent.display_w // 2, self.parent.display_h-self.game.character.character["coords"][3]-THIKNESS_WALL-20])
        self.game.floor.blit(self.texture_floor, (0, 0))
        self.game.data_layers = [0] * len(self.buttons)
        self.game.old_data_layers = [0] * len(self.buttons)

    def delete_all(self):
        for j in range(len(self.buttons) - 1, -1, -1):
            del self.buttons[j]

    def draw(self):
        self.game.render_objects(self.list_objects, buttons=self.buttons, dop_objects=self.list_dop_objects, draw_rects=False)
        if self.game.character.character["coords"][1] == 800 - self.game.character.character["coords"][3] and 300 < self.game.character.character["coords"][0] < 700:
            print([self.parent.display_w // 2, self.game.character.character["coords"][3]+HEIGHT_WALL])
            self.game.character.respawn([self.parent.display_w // 2, HEIGHT_WALL])
            self.game.room_change("reception")



class PS_room:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game


        avtomat = Object(self.parent, self.game, self.base_style, [30, TYPE_SPRITES["avtomat_y_up"]], TYPE_SPRITES["avtomat_size"], 'sprites/avtomat/avtomat_1.png')
        ps_room_logo = Object(self.parent, self.game, self.base_style, [690, 30], (250, 150), 'sprites/titles/ps_room_logo.png')
        tv = Object(self.parent, self.game, self.base_style, [340, 50], (300, 125), 'sprites/comp/TV_for_PS.png')
        ps_table = Object(self.parent, self.game, self.base_style, [480, 150], (180, 110), 'sprites/play station/ps_table.png')
        blue_sofa_1 = Object(self.parent, self.game, self.base_style, [370, 300], TYPE_SPRITES["sofa_size"], 'sprites/sofas/blue_sofa.png')
        self.sprite_coolers = ['sprites/kuler/1.png', 'sprites/kuler/2.png', 'sprites/kuler/3.png', 'sprites/kuler/4.png',
                        'sprites/kuler/5.png', 'sprites/kuler/6.png', 'sprites/kuler/7.png', 'sprites/kuler/8.png',
                        'sprites/kuler/9.png']
        self.sprite_cooler_for = [1, 0.1, 8]
        current_cooler = Object(self.parent, self.game, self.base_style, [150, 110], (40, 140), self.sprite_coolers[0])
        walls = self.game.draw_walls(color_left=["black"], color_up=["black"],
                                     color_right=["black", "black"],
                                     thinkess=THIKNESS_WALL, height=HEIGHT_WALL, width_door=150)
        dop_walls = dict(list(filter(lambda x: x[0] in ["wall_up"], walls.items())))
        print(dop_walls)
        walls = dict(list(filter(lambda x: x[0] not in dop_walls.keys(), walls.items())))

        self.objects = {"avtomat": avtomat, "ps_room_logo": ps_room_logo, "tv": tv, "ps_table": ps_table,
                        "blue_sofa_1": blue_sofa_1, "cooler": current_cooler}
        for k, v in walls.items():
            self.objects[k] = v
        self.list_objects = list(self.objects.values())
        # ------------------
        self.dop_objects = {}
        for k, v in dop_walls.items():
            self.dop_objects[k] = v
        self.list_dop_objects = list(self.dop_objects.values())
        print(self.list_objects, self.list_dop_objects)

        self.texture_floor = pygame.image.load('sprites/floor.png')

    def enter_rooms(self):
        self.game.character.respawn([self.parent.display_w-self.game.character.character["coords"][2], self.parent.display_h // 2])
        self.game.floor.blit(self.texture_floor, (0, 0))

    def delete_all(self):
        pass

    def draw(self):
        self.sprite_cooler_for = self.game.animate_sprite(self.sprite_cooler_for)
        # print(self.sprite_cooler_for)
        self.objects["cooler"].update_sprite(self.sprite_coolers[int(self.sprite_cooler_for[0])])
        self.game.render_objects(self.list_objects, dop_objects=self.list_dop_objects)
        if self.game.character.character["coords"][0] == 1000 - self.game.character.character["coords"][2] and 200 < self.game.character.character["coords"][1] < 500:
            self.game.character.respawn([self.game.character.character["coords"][2], self.parent.display_h // 2])
            self.game.room_change("reception")



class VR_room:
    def __init__(self, parent, game, base_style):
        self.base_style = base_style
        self.parent = parent
        self.game = game

        avtomat = Object(self.parent, self.game, self.base_style, [300, TYPE_SPRITES["avtomat_y_up"]], TYPE_SPRITES["avtomat_size"],
                         'sprites/avtomat/avtomat_1.png')

        walls = self.game.draw_walls(color_left=["black", "black"], color_up=["black"],
                                     color_right=["black"],
                                     thinkess=THIKNESS_WALL, height=HEIGHT_WALL, width_door=150)

        table_1 = Object(self.parent, self.game, self.base_style, [45, 145], (150, 100),
                         'sprites/vr_room/vr_table_1.png')
        table_2 = Object(self.parent, self.game, self.base_style, [220, 145], (150, 100),
                         'sprites/vr_room/vr_table_2.png')
        table_3 = Object(self.parent, self.game, self.base_style, [395, 145], (150, 100),
                         'sprites/vr_room/vr_table_3.png')
        table_4 = Object(self.parent, self.game, self.base_style, [570, 145], (150, 100),
                         'sprites/vr_room/vr_table_4.png')

        screen_1 = Object(self.parent, self.game, self.base_style, [75, 75], (100, 50),
                          'sprites/comp/TV_for_PS.png')
        screen_2 = Object(self.parent, self.game, self.base_style, [250, 75], (100, 50),
                          'sprites/comp/TV_for_PS.png')
        screen_3 = Object(self.parent, self.game, self.base_style, [425, 75], (100, 50),
                          'sprites/comp/TV_for_PS.png')
        screen_4 = Object(self.parent, self.game, self.base_style, [600, 75], (100, 50),
                          'sprites/comp/TV_for_PS.png')

        title_room = Object(self.parent, self.game, self.base_style, [717, 32], (260, 160),
                              'sprites/titles/vr_room_logo.png')

        dop_walls = dict(list(filter(lambda x: x[0] in ["wall_up"], walls.items())))
        walls = dict(list(filter(lambda x: x[0] not in dop_walls.keys(), walls.items())))

        # self.buttons = []
        # ------------------
        self.objects = {"title_room": title_room,
                        #"avtomat": avtomat,
        "table_1": table_1, "table_2": table_2, "table_3": table_3, "table_4": table_4,
        "screen_1": screen_1, "screen_2": screen_2, "screen_3": screen_3, "screen_4": screen_4}
        for k, v in walls.items():
            self.objects[k] = v
        self.list_objects = list(self.objects.values())
        # ------------------
        self.dop_objects = {}
        for k, v in dop_walls.items():
            self.dop_objects[k] = v
        self.list_dop_objects = list(self.dop_objects.values())
        print(self.list_objects, self.list_dop_objects)

        self.texture_floor = pygame.image.load('sprites/floor.png')

    def enter_rooms(self):
        self.game.character.respawn([self.game.character.character["coords"][2], self.parent.display_h // 2])
        self.game.floor.blit(self.texture_floor, (0, 0))

    def delete_all(self):
        pass

    def draw(self):
        self.game.render_objects(self.list_objects, dop_objects=self.list_dop_objects)
        if self.game.character.character["coords"][0] == 0 and 200 < self.game.character.character["coords"][1] < 500:
            self.game.character.respawn([self.parent.display_w - self.game.character.character["coords"][2], self.parent.display_h // 2])
            self.game.room_change("reception")