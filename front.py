from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.uix.camera import Camera
import time
import cv2

Builder.load_string("""
<RoundSquare@Button>:
    background_color: 0,0,0,0  
    color: 1,1,0,1
    size: 150,150
    font_size: 20
    text_size: self.size
    halign: 'center'
    valign: 'bottom'
    canvas.before:
        Color:
            rgba: [0.3, 2.7, 0.3, 1] if self.state=='normal' else (0,.7,.7,1)  # visual feedback of press
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [25,]
 
<MainPage>:
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'plantimage.jpg'
    FloatLayout:
        RoundSquare:
            text: 'Auto Detect'
            on_release: root.manager.current = 'detect'
            size_hint: None, None
            pos: root.width /2-self.width/2-115, root.top/2+80
            Image:
                source: 'cameraicon.png'
                pos: root.width /2-self.width/2-115, root.top/2+105
                size: 110,110
        RoundSquare:
            text: 'Manual Input'
            on_release: root.manager.current = 'manual'
            size_hint: None,None
            pos: root.width /2-self.width/2+130, root.top/2+80
            Image:
                source: 'paperwrite.png'
                pos: root.width /2-self.width/2+140, root.top/2+115
                size: 100,100
        RoundSquare:
            text: 'Help'
            on_release: root.manager.current = 'help'
            size_hint: None,None
            pos: root.width /2-self.width/2-115, root.top/2-180
            Image:
                source: 'questionmark.png'
                pos: root.width /2-self.width/2-115, root.top/2-145
                size: 100,100
        RoundSquare:
            text: 'Exit'
            on_release: app.stop()
            size_hint: None,None
            pos: root.width /2-self.width/2+130, root.top/2-180
            Image:
                source: 'exitimage.png'
                pos: root.width /2-self.width/2+130, root.top/2-145
                size: 100,100
 
 
<DetectPage>:
    BoxLayout:
        orientation: 'vertical'
        Camera:
            id: camera
            resolution: (640, 480)
            play: False
        ToggleButton:
            text: 'Play'
            on_release: camera.play = not camera.play
            size_hint_y: None
            height: '48dp'
        Button:
            text: 'Capture'
            size_hint_y: None
            height: '48dp'
            on_press: root.capture()
        Button:
            text: 'Main Page'
            size_hint: 1, None
            height: '48dp'
            on_release: root.manager.current = 'main'
 
 
<ManualPage>:
    id: imageviewer
    BoxLayout:
        orientation: 'vertical'
        Image: 
            id: my_image
            source: ""
 
        FileChooserIconView:
            id: imagechooser
            on_selection: imageviewer.selected(imagechooser.selection)
        Button:
            text: 'Main Page'
            size_hint: 1, None
            on_release: root.manager.current = 'main'
 
<HelpPage>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Help Page'
        Button:
            text: 'Main Page'
            size_hint: 1, None
            on_release: root.manager.current = 'main'
""")
 
# Declare screens
 
 
class MainPage(Screen):
    pass
 
 
class DetectPage(Screen):
    def capture(self):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_" + timestr)
        print("Captured")
 
 
class ManualPage(Screen):
    def selected(self, filename):
        try:
            self.ids.my_image.source = filename[0]
        except:
            pass
 
 
class HelpPage(Screen):
    pass
 
 
class MainApp(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MainPage(name='main'))
        sm.add_widget(DetectPage(name='detect'))
        sm.add_widget(ManualPage(name='manual'))
        sm.add_widget(HelpPage(name='help'))
        Window.size = (525, 825)
        return sm
 
 
MainApp().run()
