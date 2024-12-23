import pygame
import pygame_widgets
from pygame_widgets.button import ButtonArray, Button
from pygame_widgets.textbox import TextBox
import numpy as np

from menu import Menu
from game import Game
from final import Final
from settings import Settings
from refer import Refer


from databases import Database_With_Users
from avtorize import Avtorize


class Main:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.display_w, self.display_h = pygame.display.Info().current_w-10,pygame.display.Info().current_h-50
        self.FPS = 60

        # Добавил класс который отслеживает базу данных
        self.database_users = Database_With_Users()
        self.user = None


        self.running = 1
        #self.type_display, self.flag_type_display = "menu", 1 # 0 - None | 1 - menu | 2 - game | 3 - final
        self.type_display, self.flag_type_display = "avtorize", 6
        self.list_type_display = np.array([None, "menu", "game", "final", "settings", "refer", "avtorize"])
        self.colors = {
            "light": (187, 148, 87),
            "base1": (153, 88, 42),
            "base2": (111, 29, 27),
            "dark": (67, 40, 24),
            "black": (0, 0, 0)
        }

        self.display = pygame.display.set_mode((self.display_w, self.display_h))

        self.menu = Menu(self, self.colors)
        self.game = Game(self, self.colors)
        self.final = Final(self, self.colors)
        self.sett = Settings(self, self.colors)
        self.refer = Refer(self, self.colors)
        self.avtorize = Avtorize(self, self.colors)
        self.list_displays = [self.menu, self.game, self.final, self.sett, self.refer, self.avtorize]

        self.display.fill(self.colors["dark"])
        pygame.display.set_caption("Office Nightmare")
        self.clock = pygame.time.Clock()


    def buttons(self, coords, layout, texts, fonts, funcs):
        # !!! Если понадобиться разные цвета кнопок - делаем именованный аргумент colors
        # print(texts, coords[0], coords[1], coords[2]*layout[0], coords[3]*layout[1])
        return ButtonArray(
            self.display,  # Surface to place button array on
            coords[0], coords[1], coords[2]*layout[0], coords[3]*layout[1],
            layout,
            # border=100,  # Distance between buttons and edge of array
            texts=texts,
            fonts=fonts,
            colour=self.colors["base2"],
            inactiveColours=[self.colors["base1"]]*len(texts),  # Colour of button when not being interacted with
            hoverColours=[self.colors["base2"]]*len(texts),  # Colour of button when being hovered over
            pressedColours=[self.colors["light"]]*len(texts),  # Colour of button when being clicked
            textColours=[self.colors["light"]]*len(texts),
            onClicks=funcs
        )

    def button(self, coords, text, font, func, inv_clr=0):
        if inv_clr == 1:
            colour, hoverColour = self.colors["base2"], self.colors["base1"]
        else:
            colour, hoverColour = self.colors["base1"], self.colors["base2"]
        return Button(
            self.display,  # Surface to place button array on
            coords[0], coords[1], coords[2], coords[3],
            # border=100,  # Distance between buttons and edge of array
            text=text,
            font=font,
            colour=colour,
            hoverColour=hoverColour,  # Colour of button when being hovered over
            pressedColour=self.colors["light"],  # Colour of button when being clicked
            textColour=self.colors["light"],
            onClick=func
        )

    def label_text(self, coords, text, font):
        f = font
        res_label = f.render(text, True, self.colors["light"])
        self.display.blit(res_label, coords)
        pygame.display.update()
        return res_label

    def create_textbox(self, coords, size, border_colour=(0, 0, 0), text_colour=(0, 0, 0), r=10, bd=5):
        textbox = TextBox(
        self.display,
        x=coords[0],
        y=coords[1],
        width=size[0],
        height=size[1],
        fontSize=50,
        borderColour=border_colour,
        textColour=text_colour,
        radius=r,
        borderThickness=bd)
        return textbox

    def align(self, obj, coords, inacurr=(0, 0), type_blit=False, type_align="center"):
        # Это будет общая функция централизации любого объекта
        if type(coords) == tuple: coords = list(coords)
        inacurr_w, inacurr_h = 0, 0
        if type(inacurr) == int: inacurr_w = inacurr
        if type(inacurr) == tuple: inacurr = list(inacurr)
        if type(inacurr) == list:
            if len(inacurr) == 1: inacurr_w = inacurr[0]
            elif len(inacurr) == 2: inacurr_w, inacurr_h = inacurr
        print(type(obj))
        if type_align == "horizontal":
            if type(obj) == pygame.surface.Surface:
                coords[0] = (self.display.get_width() - obj.get_width()) // 2 + inacurr_w
        elif type_align == "vertical":
            if type(obj) == pygame.surface.Surface:
                coords[1] = (self.display.get_height() - obj.get_height()) // 2 + inacurr_h
        elif type_align == "center":
            if type(obj) == pygame.surface.Surface:
                coords[0] = (self.display.get_width() - obj.get_width()) // 2 + inacurr_w
                coords[1] = (self.display.get_height() - obj.get_height()) // 2 + inacurr_h
        else:
            raise TypeError("Align type must be 'horizontal' or 'vertical' or 'center'")
        if type_blit == True:
            if type(obj) == pygame.surface.Surface:
                self.display.blit(obj, coords)
        return obj, coords

    def format_commands(self, commands):
        res_commands = {}
        for type_key, type_val in commands.items():
            res_commands[type_key] = {}
            # print("---------------")
            # print(type_val)
            for key, val in type_val.items():
                if type(key) in (list, tuple):
                    for mini_key in key: res_commands[type_key][mini_key] = val
                else:
                    res_commands[type_key][key] = val
        return res_commands

    def display_quit(self):
        self.running = 0

    def display_change(self, type_display, dop_type=None):
        self.flag_type_display = np.where(self.list_type_display==type_display)[0][0]
        if type_display == "final": self.final.set_final(dop_type)
        self.type_display = type_display

    def log_in(self, login, passoword):
        print(login, passoword)
        if len(login) > 8 and len(passoword) > 8:
            if self.database_users.add_user("Новый пользователь", login, passoword):
                self.user = self.database_users.find_user(login, passoword)
                self.display_change("menu")


    def log_up(self, login, passoword):
        if len(login) > 8 and len(passoword) > 8:
            self.user = self.database_users.find_user(login, passoword)
            if self.user:
                self.display_change("menu")

    def show(self):
        while self.running:
            events = pygame.event.get()

            if self.type_display == "menu" and self.flag_type_display == 1:
                for disp in self.list_displays: disp.reinstall("hide")
                self.menu.reinstall("show")
                self.flag_type_display = 0
            elif self.type_display == "game" and self.flag_type_display == 2:
                for disp in self.list_displays: disp.reinstall("hide")
                self.game.reinstall("show")
                self.flag_type_display = 0
            elif self.type_display == "final" and self.flag_type_display == 3:
                for disp in self.list_displays: disp.reinstall("hide")
                self.final.reinstall("show")
                self.flag_type_display = 0
            elif self.type_display == "settings" and self.flag_type_display == 4:
                for disp in self.list_displays: disp.reinstall("hide")
                self.sett.reinstall("show")
                self.flag_type_display = 0
            elif self.type_display == "refer" and self.flag_type_display == 5:
                for disp in self.list_displays: disp.reinstall("hide")
                self.refer.reinstall("show")
                self.flag_type_display = 0

            elif self.type_display == "avtorize" and self.flag_type_display == 6:
                for disp in self.list_displays:disp.reinstall("hide")
                self.avtorize.reinstall("show")
                self.flag_type_display = 0

            if self.flag_type_display != 0:
                print(self.type_display, self.flag_type_display)
                self.flag_type_display = 0


            for event in events:
                if event.type == pygame.QUIT: self.running = False
                if self.type_display == "game":
                    self.game.check_event(event)
            if self.type_display == "game":
                self.game.draw()

            pygame_widgets.update(events)
            pygame.display.update()

            self.clock.tick(self.FPS)

if __name__ == "__main__":
    menu = Main()
    menu.show()