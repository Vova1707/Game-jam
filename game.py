import pygame
import numpy as np
import time

from rooms import Reception, Computer_room, PS_room, VR_room

class Character:
    def __init__(self, parent, game, base_style):
        self.parent = parent
        self.game = game
        self.base_style = base_style

        self.init_shell()
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

    def respawn(self, coords):
        if coords[0] != None: self.character["coords"][0] = coords[0]
        if coords[1] != None: self.character["coords"][1] = coords[1]

    def set_sprite(self):
        self.character["sprite"] = self.character["type_cond"][self.character["cond"]][self.character["dir"]][self.character["number_sprite"]]
        self.character["sprite"] = pygame.transform.scale(self.character["sprite"],(self.character["coords"][2], self.character["coords"][3]))
        self.character["rect"].x, self.character["rect"].y, self.character["rect"].w, self.character["rect"].h = self.character["coords"]

    def udpate(self):
        flag_change = 0
        # !!! Если нужно будет, перепишем алгос коллизии в отдельный метод
        type_collide = None
        for obj_rect in self.game.room_now.rect_objs:
            if self.character["rect"].colliderect(obj_rect):
                collision_area = self.character["rect"].clip(obj_rect)
                if collision_area.width > collision_area.height:
                    if self.character["rect"].centery < obj_rect.centery: type_collide = "down"
                    else: type_collide = "up"
                else:
                    if self.character["rect"].centerx < obj_rect.centerx: type_collide = "right"
                    else: type_collide = "left"
                break
        for obj_rect in self.game.room_now.rect_objs:
            if type_collide != "down" and self.character["flags"]["key_down"]:
                self.character["coords"][1] += self.character["val_speed"]
                self.character["dir"] = "front"
                flag_change = 1
            if type_collide != "up" and self.character["flags"]["key_up"]:
                self.character["coords"][1] -= self.character["val_speed"]
                self.character["dir"] = "back"
                flag_change = 1
            if type_collide != "left" and self.character["flags"]["key_left"]:
                self.character["coords"][0] -= self.character["val_speed"]
                self.character["dir"] = "left"
                flag_change = 1
            if type_collide != "right" and self.character["flags"]["key_right"]:
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
            "number_sprite": 0,
            "freq_sprite": 3,
            "counter_sprite": 0,
            "speed": {"idle": 0, "sneak": 2, "walk": 4, "run": 6},
            "speed_TO_freq": {"idle": 9, "sneak": 8, "walk": 7, "run": 4},
            # "key_press_TO_": {[0, 0, 0, 0]: "", "key_up": 0, "key_left": 0, "key_right": 0},
            "val_speed": 4,
            "coords": [self.parent.display_w // 2, self.parent.display_h // 2, 100, 140] # 50, 70
        }
        self.character["sprite"] = self.character["type_cond"][self.character["cond"]][self.character["dir"]][self.character["number_sprite"]]
        self.character["rect"] = self.character["sprite"].get_rect()
        self.set_sprite()
        print(self.character)
        self.character["coords"][0] -= self.character["coords"][2] / 2
        self.character["coords"][1] -= self.character["coords"][3] / 2

    def draw(self):
        # print(self.character["coords"])
        # self.character["rect"] = pygame.Rect(self.character["coords"])
        # Максимально плохая проверка на то что спрайт на вышел за границы
        if self.character["coords"][0] + self.character["coords"][2] > 1000:
            self.character["coords"][0] = 1000 - self.character["coords"][2]
        if self.character["coords"][1] + self.character["coords"][3] > 800:
            self.character["coords"][1] = 800 - self.character["coords"][3]
        if self.character["coords"][0] < 0:
            self.character["coords"][0] = 0
        if self.character["coords"][1] < 0:
            self.character["coords"][1] = 0

        # self.floor.blit(self.default_floor, (0, 0))
        self.parent.display.blit(self.character["sprite"], self.character["coords"])
        # pygame.draw.rect(self.parent.display, self.character["type_cond"][self.character["cond"]][self.character["dir"]], self.character["rect"])




class Game:
    def __init__(self, parent, base_style):
        self.base_style = base_style
        self.parent = parent

        self.floor = pygame.Surface((1000, 800))
        self.type_room = "reception"
        self.flag_change_room = 0

        self.character = Character(self.parent, self, self.base_style)

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

        self.buttons = []
        self.init_button_menu()

        self.list_rooms = {'reception': Reception,
                           'comp_room': Computer_room,
                           'ps_room': PS_room,
                           'vr_room': VR_room}
        self.room_now = self.list_rooms[self.type_room](self.parent, self, self.base_style)
        self.room_now.draw()
        self.parent.display.fill(self.base_style["colors"]["black"])

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


    def room_change(self, type_room):
        print(self.type_room, "->", type_room)
        self.type_room = type_room
        self.flag_change_room = 1

    def draw(self):
        if self.flag_change_room:
            self.flag_change_room = 0
            self.room_now.delete_all()
            self.room_now = self.list_rooms[self.type_room](self.parent, self, self.base_style)
            self.room_now.draw()
        self.parent.display.blit(self.floor, (0, 0))
        # self.parent.display.fill(self.base_style["colors"]["black"])
        self.room_now.enter_rooms()
        self.character.udpate()
        # -------------------------------------------------------------------------------
        # if self.character.room == 'main_room':
        #     self.parent.display.fill((255, 255, 255))
        # if self.character.room == 'vr_room':
        #     self.parent.display.fill((255, 200, 100))
        #
        # if self.character.room == 'ps_room':
        #     self.parent.display.fill((200, 255, 100))
        # self.parent.display.blit(self.floor, (0, 0))
        # self.character.udpate()

    def check_event(self, event):
        for commands in self.list_comands:
            if event.type in commands.keys() and event.key in commands[event.type].keys():
                commands[event.type][event.key]()

    def delete_all(self):
        for j in range(len(self.buttons)): del self.buttons[j]