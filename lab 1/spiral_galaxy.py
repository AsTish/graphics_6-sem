import math
import random
from PIL import Image
from galaxy import GalaxyBase


class SpiralGalaxy(GalaxyBase):
    def __init__(
        self,
        arms=2,
        arm_length=200,
        arm_width=100,
        radius=400,
        edge_power=20,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.arms = arms
        self.arm_length = arm_length
        self.arm_width = arm_width
        self.radius = radius
        self.edge_power = edge_power

    def _f(self, d, r):
        # Probability decay function
        return math.exp(-d / r)

    def render(self):
        # Background copy
        background = self.background.copy().convert("RGBA")

        # Background stars generation
        bg_pixels = background.load()
        for _ in range(4000):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            brightness = random.randint(120, 255)
            bg_pixels[x, y] = (brightness, brightness, brightness, 255)

        # Galaxy layer creation
        galaxy_layer = Image.new(
            "RGBA", (self.width, self.height), (0, 0, 0, 0))
        gal_pixels = galaxy_layer.load()

        delta = 0.2 * math.pi * self.radius

        # Galaxy generation
        for x in range(self.width):
            for y in range(self.height):
                dx = x - self.center_x
                dy = y - self.center_y

                d_center = math.hypot(dx, dy)
                if d_center > self.radius:
                    continue

                # Width scaling by distance
                width_factor = max(1, self.arm_width *
                                   (d_center / self.radius))

                # Probability evaluation
                prob = self._f(dx * dx, self.arm_length ** 2) * \
                    self._f(dy * dy, width_factor ** 2)
                if random.random() > prob:
                    continue

                if self.arms % 2 == 1 and dx <= 0:
                    continue

                # Spiral twisting
                alpha_angle = delta / d_center if d_center != 0 else 0
                cos_a = math.cos(alpha_angle)
                sin_a = math.sin(alpha_angle)

                x_rot = dx * cos_a - dy * sin_a
                y_rot = dx * sin_a + dy * cos_a

                # Arm placement
                for i in range(self.arms):
                    angle = (2 * math.pi / self.arms) * i
                    cos_arm = math.cos(angle)
                    sin_arm = math.sin(angle)

                    final_x = int(self.center_x +
                                  x_rot * cos_arm - y_rot * sin_arm)
                    final_y = int(self.center_y +
                                  x_rot * sin_arm + y_rot * cos_arm)

                    if 0 <= final_x < self.width and 0 <= final_y < self.height:
                        r, g, b = self._color_gradient(d_center, self.radius)
                        alpha_val = self._alpha_gradient(d_center, self.radius)
                        gal_pixels[final_x, final_y] = (r, g, b, alpha_val)

        # Layer compositing
        result = Image.alpha_composite(background, galaxy_layer)
        return result