import pygame
import math
import colorsys

main_text = ('      Добро пожаловать в репозиторий "Геймификация рекламы для',
             '                        компьютерного клуба" хакатона Game-Jam',
             '                      В игре главная цель: играть в игры!!!!',
             '      Перемещаться на WASD, в мини играх на WASD, мышь или стрелочки.',
             '',
             '          Для игры в мини игры нужна энергия',
             '      В игре присутствуют игровые автоматы, для покупки энергии',
             '          Цены в автоматах:',
             '              Зелёный: Цена: 2 монеты  Вознаграждение: 1 энергия',
             '              Жёлтый:  Цена: 4 монеты  Вознаграждение: 3 энергии',
             '              Синий:   Цена: 6 монет   Вознаграждение: 5 энергии',
             '')


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


class Refer:
    def __init__(self, parent, base_style):
        self.labels = []
        self.base_style = base_style
        self.parent = parent
        self.buttons = []

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.hue = 0
        self.D_WIDTH = 1000
        self.D_HEIGHT = 800

        self.x_start, self.y_start = 0, 0
        self.x_separator = 10
        self.y_separator = 20
        self.rows = self.D_HEIGHT // self.y_separator
        self.columns = self.D_WIDTH // self.x_separator
        self.screen_size = self.rows * self.columns
        self.x_offset = self.columns / 2
        self.y_offset = self.rows / 2
        self.A, self.B = 0, 0
        self.theta_spacing = 10
        self.phi_spacing = 1
        self.chars = ".,-~:;=!*#$@"
        self.font = pygame.font.SysFont('Arial', 18, bold=True)

        self.init_label_title()
        self.draw_donut()
        self.init_main_text()
        self.init_button_menu()


    def init_label_title(self):
        label_title = {
            "coords": (100, 10),
            "text": "Справка",
            "font": pygame.font.Font(self.base_style["font_path"], 50)
        }
        label_title["label"] = self.parent.label_text(coords=label_title["coords"],
                                                      text=label_title["text"],
                                                      font=label_title["font"])
        label_title["label"], label_title["coords"] = self.parent.align(label_title["label"], label_title["coords"],
                                                                        inacurr=-20, type_blit=False,
                                                                        type_align="horizontal")
        self.labels.append(label_title)

    def init_main_text(self):
        txt = [text for text in main_text]
        for i, mini_t in enumerate(txt):
            label_title = {
                "coords": (25, 80 + i * 30),
                "text": mini_t,
                "font": pygame.font.Font(self.base_style["font_path"], 15)
            }
            label_title["label"] = self.parent.label_text(coords=label_title["coords"],
                                                          text=label_title["text"],
                                                          font=label_title["font"])
            # label_title["label"], label_title["coords"] = self.parent.align(label_title["label"], label_title["coords"],
            #                                                                inacurr=-20, type_blit=False)
            self.labels.append(label_title)

    def init_button_menu(self):
        w, h = 80, 50
        button_ToMenu = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": (self.parent.display_w - w, 0, w, h),
            "color": {
                "inactive": self.base_style["colors"]["base2"],
                "hover": self.base_style["colors"]["base1"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            },
            "text": "...",
            "func": lambda: self.parent.display_change("menu"),
            "inv_clr": 1
        }
        button_ToMenu = self.parent.button(coords=button_ToMenu["coords"],
                                           text=button_ToMenu["text"],
                                           color=button_ToMenu["color"],
                                           font=button_ToMenu["font"],
                                           func=button_ToMenu["func"])
        self.buttons.append(button_ToMenu)

    ##############################Donut-Time#######################################
    def draw_donut(self):
        print("donut time")
        z = [0] * self.screen_size
        b = [' '] * self.screen_size

        for j in range(0, 628, self.theta_spacing):
            for i in range(0, 628, self.phi_spacing):
                c = math.sin(i)
                d = math.cos(j)
                e = math.sin(self.A)
                f = math.sin(j)
                g = math.cos(self.A)
                h = d + 2
                D = 1 / (c * h * e + f * g + 5)
                l = math.cos(i)
                m = math.cos(self.B)
                n = math.sin(self.B)
                t = c * h * g - f * e
                x = int(self.x_offset + 40 * D * (l * h * m - t * n))
                y = int(self.y_offset + 20 * D * (l * h * n + t * m))
                o = int(x + self.columns * y)
                N = int(8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n))
                if self.rows > y > 0 and 0 < x < self.columns and D > z[o]:
                    z[o] = D
                    b[o] = self.chars[N if N > 0 else 0]

        if self.y_start == self.rows * self.y_separator - self.y_separator:
            self.y_start = 0

        for i in range(len(b)):
            self.A += 0.00004
            self.B += 0.00002
            if i == 0 or i % self.columns:
                self.text_display(b[i], self.x_start, self.y_start)
                self.x_start += self.x_separator
            else:
                self.y_start += self.y_separator
                self.x_start = 0
                self.text_display(b[i], self.x_start, self.y_start)
                self.x_start += self.x_separator

        self.hue += 0.005

    def text_display(self, letter, x_start, y_start):
        text = self.font.render(str(letter), True, hsv2rgb(self.hue, 1, 1))
        self.parent.display.blit(text, (x_start, y_start))

    #################################################################################
    def delete_all(self):
        print(self.buttons)
        for i in range(len(self.buttons)): del self.buttons[i]
        for i in self.labels: del i

    def draw(self):
        self.parent.display.fill(self.base_style["colors"]["dark"])
        for i in self.buttons: i.show()
        for i in self.labels: self.parent.display.blit(i["label"], i["coords"])
