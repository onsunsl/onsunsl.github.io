from kivy.uix.button import Button
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.uix.recycleview.views import RecycleDataViewBehavior

kv = """
<MyView>:
    viewclass: "MyButton"
    id: view
    RecycleGridLayout:
        cols: 3
        key_selection: 'selectable'
        default_size: None, dp(26)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        multiselect: False
        touch_multiselect: False
"""

class MyButton(Button, RecycleDataViewBehavior):
    def on_release(self):
        print(self.text)

    def refresh_view_attrs(self, rv, index, data):
        # self.index = index
        # on_release = data.pop("on_release", None)
        # if callable(on_release):
        #     self.bind(on_release=on_release)
        super(MyButton, self).refresh_view_attrs(rv, index, data)
        print(f"Set PayMethodButton: {self}")

class MyView(RecycleView):
    pass



Builder.load_string(kv)
v = MyView()
v.data = [
    dict(text="1243")
]

runTouchApp(v)