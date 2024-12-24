import pygame

from rooms import Reception, Computer_room, PS_room, VR_room, Object
from circle import curcle
from gost import game_from_ps
#from GhostBusters.main import game_from_ps

class Character:
    def __init__(self, parent, game, base_style):
        self.parent = parent
        self.game = game
        self.base_style = base_style
        self.flag_idle = 0
        self.flag_walk = 1

        self.init_shell()
        self.commands = { # если val - list тогда, [(f1, flag1), (f2, flag2)], где 0-ой элемент на нажатие а 1-ый на отпускание,
            pygame.KEYDOWN: {
                (pygame.K_DOWN, pygame.K_s): lambda: self.set_flag("key_down", 1), # lambda: print("character - front"),
                (pygame.K_UP, pygame.K_w): lambda: self.set_flag("key_up", 1), # lambda: print("character - back"),
                (pygame.K_LEFT, pygame.K_a): lambda: self.set_flag("key_left", 1), # lambda: print("character - left"),
                (pygame.K_RIGHT, pygame.K_d): lambda: self.set_flag("key_right", 1), # lambda: print("character - right")
                (pygame.K_RCTRL, pygame.K_LCTRL): lambda: self.set_move("sneak"),
                (pygame.K_RSHIFT, pygame.K_LSHIFT): lambda: self.set_move("run")
            },
            pygame.KEYUP: {
                (pygame.K_DOWN, pygame.K_s): lambda: self.set_flag("key_down", 0),
                (pygame.K_UP, pygame.K_w): lambda: self.set_flag("key_up", 0),
                (pygame.K_LEFT, pygame.K_a): lambda: self.set_flag("key_left", 0),
                (pygame.K_RIGHT, pygame.K_d): lambda: self.set_flag("key_right", 0),
                (pygame.K_RCTRL, pygame.K_LCTRL, pygame.K_RSHIFT, pygame.K_LSHIFT): lambda: self.set_move("walk")
            }
        }
        self.commands = self.parent.format_commands(self.commands)
        print("CHARACTER: ", self.commands)

    def set_flag(self, key, val):
        self.character["flags"][key] = val
        if self.flag_walk == 1:
            self.set_move("walk")
            self.flag_walk = 0

    def set_move(self, cond):
        if list(self.character["flags"].values()) != [0, 0, 0, 0] or cond == "idle":
            self.character["val_speed"] = self.character["speed"][cond]
            self.character["cond"] = cond
            # print(self.character["cond"])
            self.character["freq_sprite"] = self.character["speed_TO_freq"][cond]

    def respawn(self, coords):
        if coords[0] != None: self.character["coords"][0] = coords[0]
        if coords[1] != None: self.character["coords"][1] = coords[1]

    def set_sprite(self):
        self.character["sprite"] = self.character["type_cond"][self.character["cond"]][self.character["dir"]][self.character["number_sprite"]]
        self.character["sprite"] = pygame.transform.scale(self.character["sprite"],(self.character["coords"][2], self.character["coords"][3]))
        self.character["rect"].x = self.character["coords"][0]
        self.character["rect"].y = self.character["coords"][1] + self.character["coords"][3] - self.character["coord_rect"]
        self.character["rect"].w = self.character["coords"][2]
        self.character["rect"].h = self.character["coord_rect"] # self.character["coords"][3]

    def udpate(self, objects):
        # pygame.draw.rect(self.parent.display, (255, 0, 0), self.character["rect"])
        # pygame.draw.rect(self.parent.display, (255, 255, 255), self.game.room_now.rect_objs[0])
        # !!! Если нужно будет, перепишем алгос коллизии в отдельный метод

        # print(set(dir_collides))
        self.game.func_collide_other_obj(objects)
        # print(flag_changes)
        if self.character["counter_sprite"] >= self.character["freq_sprite"]:
            if self.character["number_sprite"] >= len(self.character["type_cond"][self.character["cond"]][self.character["dir"]])-1:
                self.character["number_sprite"] = 0
            else:
                self.character["number_sprite"] += 1
            self.character["counter_sprite"] = 0
        self.character["counter_sprite"] += 1
        self.character["number_sprite"] = min(self.character["number_sprite"], len(self.character["type_cond"][self.character["cond"]][self.character["dir"]]) - 1)
        self.set_sprite()
        self.draw() # !!! Для оптиммизации можно добавить основной флаг, который будет отслеживать изменился ли персонаж
        # print(flag_change, self.character["cond"], self.character["freq_sprite"])

    def init_shell(self):
        part_file_path = r"sprites/character/base_choice" + '/'
        print(part_file_path)
        self.character = {
            "type_cond": {
                # !!! Написать позже отдельную функцию загрузку спрайтов под нужны направления (dir) и cond
                "walk": {
                    "front": list(map(lambda x: pygame.image.load(part_file_path+"walk/"+f"walk_front_{x}.png").convert_alpha(), range(6))),
                    "back": list(map(lambda x: pygame.image.load(part_file_path+"walk/"+f"walk_back_{x}.png").convert_alpha(), range(6))),
                    "left": list(map(lambda x: pygame.image.load(part_file_path+"walk/"+f"walk_side_{x}.png").convert_alpha(), range(6))),
                    "right": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path+"walk/"+f"walk_side_{x}.png").convert_alpha(), 1, 0), range(6)))
                },
                "run": {
                    "front": list(map(lambda x: pygame.image.load(part_file_path+"walk/"+f"walk_front_{x}.png").convert_alpha(), range(6))),
                    "back": list(map(lambda x: pygame.image.load(part_file_path+"walk/"+f"walk_back_{x}.png").convert_alpha(), range(6))),
                    "left": list(map(lambda x: pygame.image.load(part_file_path+"walk/"+f"walk_side_{x}.png").convert_alpha(), range(6))),
                    "right": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path+"walk/"+f"walk_side_{x}.png").convert_alpha(), 1, 0), range(6)))
                },
                "sneak": {
                    "front": list(map(lambda x: pygame.image.load(part_file_path+"walk/"+f"walk_front_{x}.png").convert_alpha(), range(6))),
                    "back": list(map(lambda x: pygame.image.load(part_file_path+"walk/"+f"walk_back_{x}.png").convert_alpha(), range(6))),
                    "left": list(map(lambda x: pygame.image.load(part_file_path+"walk/"+f"walk_side_{x}.png").convert_alpha(), range(6))),
                    "right": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path+"walk/"+f"walk_side_{x}.png").convert_alpha(), 1, 0), range(6)))

                },
                "idle": {
                    "front": list(map(lambda x: pygame.image.load(part_file_path+"idle/"+f"idle_front_{x}.png").convert_alpha(), range(5))),
                    "back": list(map(lambda x: pygame.image.load(part_file_path + "idle/" + f"idle_back_{x}.png").convert_alpha(), range(5))),
                    "left": list(map(lambda x: pygame.image.load(part_file_path + "idle/" + f"idle_side_{x}.png").convert_alpha(), range(5))),
                    "right": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path+"idle/"+f"idle_side_{x}.png").convert_alpha(), 1, 0), range(5)))
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
            "freq_sprite": 20,
            "counter_sprite": 0,
            "speed": {"idle": 0, "sneak": 2, "walk": 4, "run": 6},
            "speed_TO_freq": {"idle": 20, "sneak": 8, "walk": 7, "run": 4},
            "coord_rect": 20,
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

        self.donats_many = 10
        self.labels = []
        self.init_label_title()

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

        self.layer_buttons_1 = pygame.Surface((1000, 800), pygame.SRCALPHA, 32)
        self.layer_buttons_1 = self.layer_buttons_1.convert_alpha()
        self.layer_buttons_2 = pygame.Surface((1000, 800), pygame.SRCALPHA, 32)
        self.layer_buttons_2 = self.layer_buttons_2.convert_alpha()
        self.old_data_layers = [0, 0]
        self.data_layers = [0, 0]
        self.list_rooms = {'reception': Reception,
                           'comp_room': Computer_room,
                           'ps_room': PS_room,
                           'vr_room': VR_room}

        self.mini_game_change = False
        self.mini_games = {'comp_room':
                          {'circle': lambda: curcle(self.parent.display),
                           'ps': lambda: game_from_ps(self.parent.display)
                           #game_from_ps(self.parent.display)
                           },
                      'ps_room':
                          {},
                      'vr_room':
                          {},
                      }

        self.room_now = self.list_rooms[self.type_room](self.parent, self, self.base_style)
        self.room_now.draw()
        self.room_now.enter_rooms()

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
            "func": lambda: self.parent.display_change('menu')
        }
        button_ToMenu["button"] = self.parent.button(coords=button_ToMenu["coords"],
                                                              text=button_ToMenu["text"],
                                                              color=button_ToMenu["color"],
                                                              font=button_ToMenu["font"],
                                                              func=button_ToMenu["func"])
        self.buttons.append(button_ToMenu)

    def change_game(self, name_game):
        if self.donats_many - 3 > 0:
            self.mini_game_change = 1
            update_manu_for_mini_game = self.mini_games[self.type_room][name_game]()
            self.donats_many -= 3
            self.donats_many += update_manu_for_mini_game
            self.init_label_title()

    def room_change(self, type_room):
        print(self.type_room, "->", type_room)
        self.type_room = type_room
        self.flag_change_room = 1

    def draw(self):
        if self.flag_change_room:
            self.flag_change_room = 0
            self.room_now.delete_all()
            self.room_now = self.list_rooms[self.type_room](self.parent, self, self.base_style)
            self.room_now.enter_rooms()
        self.parent.display.blit(self.floor, (0, 0))
        # self.parent.display.fill(self.base_style["colors"]["black"])
        self.room_now.draw()
        for i in self.labels: self.parent.display.blit(i["label"], i["coords"])
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

    def init_label_title(self):
        label_title = {
            "coords": (30, 0),
            "text": f"Монет: {self.donats_many}",
            "font": pygame.font.Font(self.base_style["font_path"], 30)
        }
        label_title["label"] = self.parent.label_text(coords=label_title["coords"],
                                                      text=label_title["text"],
                                                      font=label_title["font"],
                                                      color=(255, 0, 0))
        # label_title["text"] = self.parent.add_distance_between_letters(label_title["text"], 2)
        self.labels = []
        print(label_title["text"])
        self.labels.append(label_title)

    def render_objects(self, objects, buttons=None, dop_objects=None):
        if dop_objects is not None: all_objects = objects + dop_objects
        else: all_objects = objects
        for obj in objects:
            obj.draw()
            if self.character.character["rect"].centery > obj.data["rect"].centery:
                obj.data["type_render"] = 1
            else:
                obj.data["type_render"] = 0
        if buttons is not None:
            for i in range(len(buttons)):
                # buttons[i].delete()
                # if i == 1: print(self.character.character["coords"][1], buttons[i].data["coords"][1]-buttons[i].data["coords"][3])
                if self.character.character["coords"][1] > (buttons[i].data["coords"][1]-buttons[i].data["coords"][3]//2):
                    buttons[i].create(self.layer_buttons_1)
                    self.data_layers[i] = 1
                else:
                    buttons[i].create(self.layer_buttons_2)
                    self.data_layers[i] = 0
        if dop_objects is not None:
            for obj in sorted(list(filter(lambda obj: obj.data["type_render"] == 1, dop_objects)), key=lambda obj: (obj.data["rect"].y, obj.data["rect"].h)):
                obj.draw()
        if buttons is not None:
            self.parent.display.blit(self.layer_buttons_1, (0, 0))
        for obj in sorted(list(filter(lambda obj: obj.data["type_render"] == 1, objects)), key=lambda obj: (obj.data["rect"].y, obj.data["rect"].h)):
            obj.draw()
        self.character.udpate(all_objects)
        if buttons is not None:
            self.parent.display.blit(self.layer_buttons_2, (0, 0))
        for obj in sorted(list(filter(lambda obj: obj.data["type_render"] == 0, objects)), key=lambda obj: (obj.data["rect"].y, obj.data["rect"].h)):
            obj.draw()
        # print(self.data_layers, self.old_data_layers)
        if buttons is not None:
            if self.data_layers != self.old_data_layers:
                # print("INTO")
                self.layer_buttons_1.fill(pygame.Color(0, 0, 0, 0))
                self.layer_buttons_2.fill(pygame.Color(0, 0, 0, 0))
        self.old_data_layers = self.data_layers.copy()

    def draw_walls(self, color_left, color_up, color_right, thinkess, height, width_door):
        # print(color_left, color_up, color_right)
        walls = {}
        def append(key, obj):
            walls[key] = obj
        if len(color_up) == 1: # передняя - нет двери
            append("wall_up", Object(self.parent, self, self.base_style, [0, 0],
                      (self.parent.display_w, height), f'sprites/walls/front_{color_up[0]}_wall.png', coord_rect=0))
        elif len(color_up) == 2: # передняя - есть дверь
            append("wall_up_1", Object(self.parent, self, self.base_style, [0, 0],
                      ((self.parent.display_w-width_door)//2, height), f'sprites/walls/front_{color_up[0]}_wall.png', coord_rect=0))
            append("wall_up_2", Object(self.parent, self, self.base_style, [(self.parent.display_w+width_door)//2, 0],
                      ((self.parent.display_w+width_door)//2, height), f'sprites/walls/front_{color_up[1]}_wall.png', coord_rect=0))

        if len(color_left) == 1: # левая - нет двери
            append("wall_left", Object(self.parent, self, self.base_style, [0, 0],
                              (thinkess, self.parent.display_h), f'sprites/walls/side_{color_left[0]}_wall.png', coord_rect=0))
        elif len(color_left) == 2: # левая - есть стена
            append("wall_left_1", Object(self.parent, self, self.base_style, [0, (self.parent.display_h + width_door) // 2],
                                (thinkess, (self.parent.display_h + width_door) // 2), f'sprites/walls/side_{color_left[0]}_wall.png', coord_rect=0))
            append("wall_left_2", Object(self.parent, self, self.base_style, [0, 0],
                                (thinkess, (self.parent.display_h-width_door)//2), f'sprites/walls/side_{color_left[1]}_wall.png', coord_rect=0))

        if len(color_right) == 1: # правая - нет двери
            append("wall_right", Object(self.parent, self, self.base_style, [self.parent.display_w-thinkess, 0],
                       (thinkess, self.parent.display_h), f'sprites/walls/side_{color_right[0]}_wall.png', coord_rect=0))
        elif len(color_right) == 2: # правая - есть дверь
            append("wall_right_1", Object(self.parent, self, self.base_style, [self.parent.display_w - thinkess, 0],
                                (thinkess, (self.parent.display_h-width_door)//2), f'sprites/walls/side_{color_right[0]}_wall.png', coord_rect=0))
            append("wall_right_2", Object(self.parent, self, self.base_style, [self.parent.display_w - thinkess, (self.parent.display_h+width_door)//2],
                                (thinkess, (self.parent.display_h+width_door)//2), f'sprites/walls/side_{color_right[1]}_wall.png', coord_rect=0))
        return walls

    def func_collide_other_obj(self, objects):
        dir_collides = []
        for obj_rect in list(map(lambda x: x.data["rect"], objects)):
            if self.character.character["rect"].colliderect(obj_rect):
                collision_area = self.character.character["rect"].clip(obj_rect)
                if collision_area.width > collision_area.height:
                    if self.character.character["rect"].centery < obj_rect.centery:
                        dir_collides.append("down")
                    else:
                        dir_collides.append("up")
                else:
                    if self.character.character["rect"].centerx < obj_rect.centerx:
                        dir_collides.append("right")
                    else:
                        dir_collides.append("left")
        if dir_collides == []: dir_collides = [None]
        dir_collides = list(set(dir_collides))
        flag_change = 0
        flag_changes = {"down": 1, "up": 1, "right": 1, "left": 1}
        if "down" not in dir_collides and self.character.character["flags"]["key_down"] and flag_changes["down"] == 1:
            self.character.character["coords"][1] += self.character.character["val_speed"]
            self.character.character["dir"] = "front"
            flag_changes["down"] = 0
            flag_change, self.character.flag_idle = 1, 1
        if "up" not in dir_collides and self.character.character["flags"]["key_up"] and flag_changes["up"] == 1:
            self.character.character["coords"][1] -= self.character.character["val_speed"]
            self.character.character["dir"] = "back"
            flag_changes["up"] = 0
            flag_change, self.character.flag_idle = 1, 1
        if "left" not in dir_collides and self.character.character["flags"]["key_left"] and flag_changes["left"] == 1:
            self.character.character["coords"][0] -= self.character.character["val_speed"]
            self.character.character["dir"] = "left"
            flag_changes["left"] = 0
            flag_change, self.character.flag_idle = 1, 1
        if "right" not in dir_collides and self.character.character["flags"]["key_right"] and flag_changes["right"] == 1:
            self.character.character["coords"][0] += self.character.character["val_speed"]
            self.character.character["dir"] = "right"
            flag_changes["right"] = 0
            flag_change, self.character.flag_idle = 1, 1
        if flag_change == 0 and self.character.flag_idle == 1:
            self.character.set_move("idle")
            self.character.flag_idle = 0
            self.character.flag_walk = 1
            # print(self.character["flags"], self.character["cond"])

    def animate_sprite(self, for_data):
        for_data[0] += for_data[1]
        # print(for_data[2])
        if for_data[0] > for_data[2]+1:
            for_data[0] = 1
        for_data[0] = for_data[0]
        return for_data

    def check_event(self, event):
        for commands in self.list_comands:
            if event.type in commands.keys() and event.key in commands[event.type].keys():
                commands[event.type][event.key]()

    def delete_all(self):
        for j in range(len(self.buttons)): del self.buttons[j]
        self.room_now.delete_all()