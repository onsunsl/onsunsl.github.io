from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatIconButton, MDIconButton


class Example(MDApp):
    def build(self):
        # return MDRectangleFlatIconButton(
        #             text="MDRectangleFlatIconButton",
        #             icon="D:/workspace/cpos-df/ui/icon/weixin.png",
        #             line_color=(0, 0, 0, 0),
        #             pos_hint={"center_x": .5, "center_y": .5},
        #         )

        return MDIconButton(icon="D:/workspace/cpos-df/ui/icon/weixin.png")


Example().run()