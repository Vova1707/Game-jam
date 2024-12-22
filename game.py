import time

import pygame
import numpy as np

class Map:
    def __init__(self):
        self.info = {
            "#": {
                "w": 50, "h": 50,
                "sprite": (0, 0, 255)
            }
        }
        self.map = []


class Character:
    def __init__(self, parent, base_style, container_flags, floor):
        self.container_flags = container_flags
        self.parent = parent
        self.base_style = base_style

        self.room = 'main_room' # ['main_room', 'vr_room', 'ps_room']
        self.floor = floor
        self.default_floor = pygame.image.load('sprites/floor/floor_on_main.png')

        self.init_shell()
        self.container_flags["character"] = 0
        self.commands = { # если val - list тогда, [(f1, flag1), (f2, flag2)], где 0-ой элемент на нажатие а 1-ый на отпускание,
            pygame.KEYDOWN: {
                (pygame.K_DOWN, pygame.K_s): lambda: self.set_flag("key_down", 1), # lambda: print("character - front"),
                (pygame.K_UP, pygame.K_w): lambda: self.set_flag("key_up", 1), # lambda: print("character - back"),
                (pygame.K_LEFT, pygame.K_a): lambda: self.set_flag("key_left", 1), # lambda: print("character - left"),
                (pygame.K_RIGHT, pygame.K_d): lambda: self.set_flag("key_right", 1), # lambda: print("character - right")
                (pygame.K_RCTRL, pygame.K_LCTRL): lambda: self.set_speed_move(self.character["speed"]["sneak"]),
                (pygame.K_RSHIFT, pygame.K_LSHIFT): lambda: self.set_speed_move(self.character["speed"]["run"])
            },
            pygame.KEYUP: {
                (pygame.K_DOWN, pygame.K_s): lambda: self.set_flag("key_down", 0),
                (pygame.K_UP, pygame.K_w): lambda: self.set_flag("key_up", 0),
                (pygame.K_LEFT, pygame.K_a): lambda: self.set_flag("key_left", 0),
                (pygame.K_RIGHT, pygame.K_d): lambda: self.set_flag("key_right", 0),
                (pygame.K_RCTRL, pygame.K_LCTRL, pygame.K_RSHIFT, pygame.K_LSHIFT): lambda: self.set_speed_move(self.character["speed"]["walk"])
            }
        }
        self.commands = self.parent.format_commands(self.commands)
        print("CHARACTER: ", self.commands)

    def set_flag(self, key, val):
        # self.character["val_speed"] = self.character[key][]
        self.character["flags"][key] = val

    def set_speed_move(self, speed):
        # print(delta)
        self.character["val_speed"] = speed
        self.character["cond"] = list(self.character["speed"].keys())[list(self.character["speed"].values()).index(speed)]
        self.character["freq_sprite"] = self.character["speed_TO_freq"][self.character["cond"]]
        # print(self.character["freq_sprite"], speed, self.character["cond"])

    def set_sprite(self):
        self.character["sprite"] = self.character["type_cond"][self.character["cond"]][self.character["dir"]][self.character["number_sprite"]]

    def udpate(self):
        flag_change = 0
        if self.character["flags"]["key_down"]:
            self.character["coords"][1] += self.character["val_speed"]
            self.character["dir"] = "front"
            flag_change = 1
        if self.character["flags"]["key_up"]:
            self.character["coords"][1] -= self.character["val_speed"]
            self.character["dir"] = "back"
            flag_change = 1
        if self.character["flags"]["key_left"]:
            self.character["coords"][0] -= self.character["val_speed"]
            self.character["dir"] = "left"
            flag_change = 1
        if self.character["flags"]["key_right"]:
            self.character["coords"][0] += self.character["val_speed"]
            self.character["dir"] = "right"
            flag_change = 1
        if flag_change == 0:
            self.character["cond"] = "idle"
            self.character["dir"] = "front"
        else:
            self.set_speed_move(self.character["val_speed"])
        if self.character["counter_sprite"] >= self.character["freq_sprite"]:
            if self.character["number_sprite"] >= len(self.character["type_cond"][self.character["cond"]][self.character["dir"]])-1:
                self.character["number_sprite"] = 0
            else:
                self.character["number_sprite"] += 1
            self.character["counter_sprite"] = 0
        self.character["counter_sprite"] += 1
        self.character["number_sprite"] = min(self.character["number_sprite"], len(self.character["type_cond"][self.character["cond"]][self.character["dir"]]) - 1)
        # print(self.character["cond"], self.character["dir"])
        self.set_sprite()
        self.draw() # !!! Для оптиммизации можно добавить основной флаг, который будет отслеживать изменился ли персонаж
        # print(*self.character["flags"].items())
        # print(self.character["dir"], type_move)

    def init_shell(self):
        part_file_path = r"sprites\character\base_choice" + '\\'
        print(part_file_path)
        self.character = {
            "type_cond": {
                # "move": {
                #     "front": (150, 0, 0),
                #     "back": (150, 150, 0),
                #     "left": (0, 150, 0),
                #     "right": (70, 150, 70)
                # },
                # "run": {
                #     "front": (255, 0, 0),
                #     "back": (255, 255, 0),
                #     "left": (0, 255, 0),
                #     "right": (100, 255, 150)
                # },
                # "sneak": {
                #     "front": (80, 0, 0),
                #     "back": (80, 80, 0),
                #     "left": (0, 80, 0),
                #     "right": (40, 80, 40)
                # },
                # "stand": {
                #     "base": (255, 255, 255)
                # }
                # !!! Написать позже отдельную функцию загрузку спрайтов под нужны направления (dir) и cond
                "walk": {
                    "front": list(map(lambda x: pygame.image.load(part_file_path+"walk\\"+f"walk_front_{x}.png").convert_alpha(), range(6))),
                    "back": list(map(lambda x: pygame.image.load(part_file_path+"walk\\"+f"walk_back_{x}.png").convert_alpha(), range(6))),
                    "left": list(map(lambda x: pygame.image.load(part_file_path+"walk\\"+f"walk_side_{x}.png").convert_alpha(), range(6))),
                    "right": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path+"walk\\"+f"walk_side_{x}.png").convert_alpha(), 1, 0), range(6)))
                },
                "run": {
                    "front": list(map(lambda x: pygame.image.load(part_file_path+"walk\\"+f"walk_front_{x}.png").convert_alpha(), range(6))),
                    "back": list(map(lambda x: pygame.image.load(part_file_path+"walk\\"+f"walk_back_{x}.png").convert_alpha(), range(6))),
                    "left": list(map(lambda x: pygame.image.load(part_file_path+"walk\\"+f"walk_side_{x}.png").convert_alpha(), range(6))),
                    "right": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path+"walk\\"+f"walk_side_{x}.png").convert_alpha(), 1, 0), range(6)))
                },
                "sneak": {
                    "front": list(map(lambda x: pygame.image.load(part_file_path+"walk\\"+f"walk_front_{x}.png").convert_alpha(), range(6))),
                    "back": list(map(lambda x: pygame.image.load(part_file_path+"walk\\"+f"walk_back_{x}.png").convert_alpha(), range(6))),
                    "left": list(map(lambda x: pygame.image.load(part_file_path+"walk\\"+f"walk_side_{x}.png").convert_alpha(), range(6))),
                    "right": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path+"walk\\"+f"walk_side_{x}.png").convert_alpha(), 1, 0), range(6)))

                },
                "idle": {
                    "front": list(map(lambda x: pygame.image.load(part_file_path+"idle\\"+f"idle_front_{x}.png").convert_alpha(), range(5))),
                    "back": list(map(lambda x: pygame.image.load(part_file_path + "idle\\" + f"idle_back_{x}.png").convert_alpha(), range(5))),
                    "left": list(map(lambda x: pygame.image.load(part_file_path + "idle\\" + f"idle_side_{x}.png").convert_alpha(), range(5))),
                    "right": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path+"idle\\"+f"idle_side_{x}.png").convert_alpha(), 1, 0), range(5)))
                }
            },
            "flags": {
                "key_down": 0,  # front
                "key_up": 0,  # back
                "key_left": 0,  # left
                "key_right": 0  # right
            },
            "dir" : "front",
            "cond": "idle",
            "sprite": None,
            "number_sprite": 0,
            "freq_sprite": 3,
            "counter_sprite": 0,
            "speed": {"idle": 0, "sneak": 2, "walk": 4, "run": 6},
            "speed_TO_freq": {"idle": 9, "sneak": 8, "walk": 7, "run": 4},
            # "key_press_TO_": {[0, 0, 0, 0]: "", "key_up": 0, "key_left": 0, "key_right": 0},
            "val_speed": 4,
            "coords": [self.parent.display_w // 2, self.parent.display_h // 2, 100, 140] # 50, 70
        }
        print(self.character)
        self.character["coords"][0] -= self.character["coords"][2] / 2
        self.character["coords"][1] -= self.character["coords"][3] / 2
        self.set_sprite()

    def draw(self):
        print(self.character["coords"])
        self.character["rect"] = pygame.Rect(self.character["coords"])
        sprite = pygame.transform.scale(self.character["sprite"], (self.character["coords"][2], self.character["coords"][3]))
        # Максимально плохая проверка на то что спрайт на вышел за границы
        if self.character["coords"][0] + self.character["coords"][2] > 1000:
            self.character["coords"][0] = 1000 - self.character["coords"][2]
        if self.character["coords"][1] + self.character["coords"][3] > 800:
            self.character["coords"][1] = 800 - self.character["coords"][3]
        if self.character["coords"][0] < 0:
            self.character["coords"][0] = 0
        if self.character["coords"][1] < 0:
            self.character["coords"][1] = 0
        # Проверка в какой комнате персонаж

        if self.character["coords"][0] == 1000 - self.character["coords"][2] and 200 < self.character["coords"][1] < 500 and  self.room == 'main_room':
            self.room = 'vr_room'
            self.default_floor = pygame.Surface((1000, 800))
            self.default_floor.fill((200, 100, 150))
            self.character["coords"][0] = 50

        if self.character["coords"][0] == 0 and 200 < self.character["coords"][1] < 500 and self.room == 'main_room':
            self.room = 'ps_room'
            self.default_floor = pygame.Surface((1000, 800))
            self.default_floor.fill((200, 20, 150))
            self.character["coords"][0] = 750

        if self.character["coords"][1] == 0 and 200 < self.character["coords"][0] < 500 and self.room == 'main_room':
            self.room = 'computer_room'
            self.default_floor = pygame.Surface((1000, 800))
            self.default_floor.fill((100, 120, 150))
            self.character["coords"][1] = 600




        if self.character["coords"][0] == 0 and 200 < self.character["coords"][1] < 500 and  self.room == 'vr_room':
            self.room = 'main_room'
            self.default_floor = pygame.image.load('sprites/floor/floor_on_main.png')
            self.character["coords"][0] = 450
            self.character["coords"][1] = 300

        if self.character["coords"][0] == 1000 - self.character["coords"][2] and 200 < self.character["coords"][1] < 500 and  self.room == 'ps_room':
            self.room = 'main_room'
            self.default_floor = pygame.image.load('sprites/floor/floor_on_main.png')
            self.character["coords"][0] = 100
            self.character["coords"][1] = 330


        if self.character["coords"][1] == 800 - self.character["coords"][3] and 300 < self.character["coords"][0] < 700 and self.room == 'computer_room':
            self.room = 'main_room'
            self.default_floor = pygame.image.load('sprites/floor/floor_on_main.png')
            self.character["coords"][1] = 150

        self.floor.blit(self.default_floor, (0, 0))
        self.floor.blit(sprite, self.character["coords"])
        # pygame.draw.rect(self.parent.display, self.character["type_cond"][self.character["cond"]][self.character["dir"]], self.character["rect"])




class Game:
    def __init__(self, parent, base_style):
        self.base_style = base_style
        self.parent = parent
        self.container_flags = {}
        self.buttons = []
        self.floor = pygame.Surface((1000, 800))
        self.character = Character(self.parent, self.base_style, self.container_flags, self.floor)

        self.commands = {
            pygame.KEYDOWN: {
                pygame.K_ESCAPE: lambda: self.parent.display_change("menu"),
                pygame.K_0: lambda: self.parent.display_change("final", dop_type="victory"),
                pygame.K_9: lambda: self.parent.display_change("final", dop_type="fail")
            }
        }
        self.commands = self.parent.format_commands(self.commands)
        print("GAME: ", self.commands)
        self.list_comands = [self.commands, self.character.commands]
        self.init_button_menu()

    def init_button_menu(self):
        w, h = 80, 50
        button_ToMenu = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": (self.parent.display_w-w, 0, w, h),
            "text": "...",
            "color": {
                "inactive": self.base_style["colors"]["base2"],
                "hover": self.base_style["colors"]["base1"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            },
            "func": lambda: self.parent.display_change("menu")
        }
        button_ToMenu["button"] = self.parent.button(coords=button_ToMenu["coords"],
                                                              text=button_ToMenu["text"],
                                                              color=button_ToMenu["color"],
                                                              font=button_ToMenu["font"],
                                                              func=button_ToMenu["func"])
        self.buttons.append(button_ToMenu)

    def draw(self):
        if self.character.room == 'main_room':
            self.parent.display.fill((255, 255, 255))
        if self.character.room == 'vr_room':
            self.parent.display.fill((255, 200, 100))

        if self.character.room == 'ps_room':
            self.parent.display.fill((200, 255, 100))
        self.parent.display.blit(self.floor, (0, 0))
        self.character.udpate()

    def check_event(self, event):
        for commands in self.list_comands:
            if event.type in commands.keys() and event.key in commands[event.type].keys():
                commands[event.type][event.key]()

    def delete_all(self):
        for j in range(len(self.buttons)): del self.buttons[j]