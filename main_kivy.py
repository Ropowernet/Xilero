from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.vector import Vector


class Player(Widget):
    speed = NumericProperty(200)

    def move_towards(self, target, dt):
        if self.pos != target:
            direction = Vector(target) - self.pos
            distance = direction.length()
            if distance < self.speed * dt:
                self.pos = target
            else:
                direction = direction.normalize()
                self.pos = self.pos + direction * self.speed * dt


class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Player(size=(50, 50))
        self.add_widget(self.player)
        self.player.center = self.center
        self.target = self.player.pos
        Clock.schedule_interval(self.update, 0)

    def on_touch_down(self, touch):
        self.target = (touch.x - self.player.width / 2, touch.y - self.player.height / 2)

    def update(self, dt):
        self.player.move_towards(self.target, dt)


class GameApp(App):
    def build(self):
        return Game()


if __name__ == "__main__":
    GameApp().run()
