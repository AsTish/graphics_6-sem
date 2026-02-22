import math
import random
from PIL import Image
from galaxy import GalaxyBase


class LenticularGalaxy(GalaxyBase):
    def __init__(
        self,
        a=280,
        b=100,
        edge_power=1.2,
        angle=0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.a = a
        self.b = b
        self.edge_power = edge_power
        self.angle = math.radians(angle)

        # Precompute trigonometric coefficients
        self.cos_a = math.cos(self.angle)
        self.sin_a = math.sin(self.angle)

    def _f(self, p):
        # Probability calculation
        return math.exp(-(p ** self.edge_power))

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

        for x in range(self.width):
            for y in range(self.height):

                dx = x - self.center_x
                dy = y - self.center_y

                # Coordinate rotation
                x_rot = dx * self.cos_a + dy * self.sin_a
                y_rot = -dx * self.sin_a + dy * self.cos_a

                # Elliptical metric calculation
                p = (x_rot * x_rot) / (self.a * self.a) + \
                    (y_rot * y_rot) / (self.b * self.b)

                # Probability evaluation
                prob = self._f(p)
                if random.random() > prob:
                    continue

                # Distance normalization
                distance_norm = math.sqrt(p)

                # Color and alpha computation
                r, g, b = self._color_gradient(distance_norm, 1.0)
                alpha_val = int(255 * prob)

                # Pixel assignment
                gal_pixels[x, y] = (r, g, b, alpha_val)

        # Layer compositing
        result = Image.alpha_composite(background, galaxy_layer)
        return result