import pygame

class Refer:
    def __init__(self, parent, base_color):
        self.base_color = base_color
        self.parent = parent

    def initing(self):
        self.init_label_title()
        self.init_button_menu()

    def init_label_title(self):
        self.labels = []
        label_title = {
            "coords": (100, 20),
            "text":"Справка",
            "font": pygame.font.SysFont("Century Gothic", 50)
        }
        label_title["label"] = self.parent.label_text(coords=label_title["coords"],
                                                           text=label_title["text"],
                                                           font=label_title["font"])
        label_title["label"], label_title["coords"] = self.parent.align(label_title["label"], label_title["coords"],
                                                            inacurr=-20, type_blit=False, type_align="horizontal")
        self.labels.append(label_title["label"])

    def init_button_menu(self):
        w, h = 80, 50
        self.buttons = []
        button_ToMenu = {
            "font": pygame.font.SysFont("Century Gothic", 30),
            "coords": (self.parent.display_w - w, 0, w, h),
            "text": "...",
            "func": lambda: self.parent.display_change("menu"),
            "inv_clr": 1
        }
        button_ToMenu = self.parent.button(coords=button_ToMenu["coords"],
                                                          text=button_ToMenu["text"],
                                                          font=button_ToMenu["font"],
                                                          func=button_ToMenu["func"],
                                                          inv_clr=button_ToMenu["inv_clr"])
        self.buttons.append(button_ToMenu)


    def delete_all(self):
        del self.buttons
        del self.labels

    def draw(self):
        self.parent.display.fill((255, 200, 100))