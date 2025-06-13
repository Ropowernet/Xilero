from ursina import *


class Player(Entity):
    """Simple controllable character."""

    def __init__(self, **kwargs):
        super().__init__(
            model="cube",
            color=color.orange,
            scale_y=2,
            origin_y=-0.5,
            collider="box",
            **kwargs,
        )
        self.target = self.position
        self.speed = 5

    def update(self):
        if self.position != self.target:
            self.position = lerp(self.position, self.target, time.dt * self.speed)


def input(key):
    if key == "left mouse down" and mouse.world_point is not None:
        # keep the player on the ground plane (y = 0)
        player.target = Vec3(mouse.world_point.x, 0, mouse.world_point.z)


app = Ursina()

# basic ground plane
Entity(
    model="plane",
    scale=40,
    texture="white_cube",
    texture_scale=(40, 40),
    color=color.light_gray,
    collider="box",
)

player = Player(position=(0, 0, 0))

# configure an isometric camera
camera.orthographic = True
camera.fov = 10
camera.position = (20, 20, -20)
camera.look_at(player)


app.run()
