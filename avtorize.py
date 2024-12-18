import pygame


class Avtorize:
    def __init__(self, parent, base_color):
        self.base_color = base_color
        self.parent = parent
        self.init_textbox()
        self.init_buttons_general()
        self.labels = []
        self.init_label_title()

    def init_buttons_general(self):
        self.buttons_general = {
            "font": pygame.font.SysFont("Century Gothic", 40),
            "coords": (250, 400, 500, 100),
            "layout": [1, 2],
        }
        param_button_log_in = {"text": "зарегистрироваться", "func": lambda: self.parent.log_in(''.join(self.textboxs[0].text), ''.join(self.textboxs[1].text))}
        param_button_log_up = {"text": "вход", "func": lambda: self.parent.log_up(''.join(self.textboxs[0].text), ''.join(self.textboxs[1].text))}
        array_buttons = [param_button_log_in, param_button_log_up]
        self.buttons_general["layout"][1] = len(array_buttons)


        for key in array_buttons[0].keys(): self.buttons_general[key + "s"] = list(map(lambda b: b[key], array_buttons))
        self.buttons_general["buttons"] = self.parent.buttons(coords=self.buttons_general["coords"],
                                                              layout=self.buttons_general["layout"],
                                                              fonts=[self.buttons_general["font"]] * len(array_buttons),
                                                              texts=self.buttons_general["texts"],
                                                              funcs=self.buttons_general["funcs"])

    def init_textbox(self):
        self.textboxs = []
        self.textboxs.append(self.parent.create_textbox((300, 150), (400, 80)))
        self.textboxs.append(self.parent.create_textbox((300, 250), (400, 80)))

    def init_label_title(self):

        label = {
            "coords": (375, 80),
            "text":"Авторизация",
            "font": pygame.font.SysFont("Century Gothic", 40)
        }
        label['label'] = self.parent.label_text(coords=label["coords"],
                                        text=label["text"],
                                        font=label["font"])
        self.labels.append(label)

        label = {
            "coords": (150, 150),
            "text": "Логин",
            "font": pygame.font.SysFont("Century Gothic", 40)
        }
        label['label'] = self.parent.label_text(coords=label["coords"],
                                                text=label["text"],
                                                font=label["font"])
        self.labels.append(label)

        label = {
            "coords": (150, 250),
            "text": "Пароль",
            "font": pygame.font.SysFont("Century Gothic", 40)
        }
        label['label'] = self.parent.label_text(coords=label["coords"],
                                                text=label["text"],
                                                font=label["font"])
        self.labels.append(label)


    def reinstall(self, _type):
        if _type == "hide":
            self.buttons_general["buttons"].hide()
            for i in self.textboxs: i.hide()
        elif _type == "show":
            self.parent.display.fill(self.base_color["dark"])
            self.buttons_general["buttons"].show()
            for i in self.textboxs: i.show()
            for i in self.labels: self.parent.display.blit(i["label"], i["coords"])
