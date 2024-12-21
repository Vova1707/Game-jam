import pygame

class Menu:
    def __init__(self, parent, base_color):
        self.base_color = base_color
        self.parent = parent
        self.labels = []
        self.init_buttons_general()
        self.init_label_title()

    def init_buttons_general(self):
        self.buttons_general = {
            "font": pygame.font.SysFont("Century Gothic", 40),
                "coords": (375, 200, 250, 100),
            "layout": [1, 4],
        }
        param_button_start = {"text": "играть", "func":lambda: self.parent.display_change("game")}
        param_button_sett = {"text": "настройки", "func":lambda: self.parent.display_change("settings")}
        param_button_refer = {"text": "справка", "func":lambda: self.parent.display_change("refer")}
        param_button_quit = {"text": "выход", "func":self.parent.display_quit}
        array_buttons = [param_button_start, param_button_sett, param_button_refer, param_button_quit]
        self.buttons_general["layout"][1] = len(array_buttons)

        for key in array_buttons[0].keys(): self.buttons_general[key+"s"] = list(map(lambda b: b[key], array_buttons))
        self.buttons_general["buttons"] = self.parent.buttons(coords=self.buttons_general["coords"],
                                                          layout=self.buttons_general["layout"],
                                                          fonts=[self.buttons_general["font"]] * len(array_buttons),
                                                          texts=self.buttons_general["texts"],
                                                          funcs=self.buttons_general["funcs"])

    def init_label_title(self):
        label_title = {
            "coords": (350, 80),
            "text": f"Ultimate",
            "font": pygame.font.SysFont("Century Gothic", 80)
        }
        label_title["label"] = self.parent.label_text(coords=label_title["coords"],
                                                      text=label_title["text"],
                                                      font=label_title["font"])
        self.labels.append(label_title)


    def reinstall(self, _type):
        if _type == "hide":
            self.buttons_general["buttons"].hide()
        elif _type == "show":
            self.parent.display.fill(self.base_color["dark"])
            self.buttons_general["buttons"].show()
            for i in self.labels: self.parent.display.blit(i["label"], i["coords"])

