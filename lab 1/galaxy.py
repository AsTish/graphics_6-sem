import numpy as np
from PIL import Image
import math
import random


class GalaxyBase:
    def __init__(
        self,
        width=1000,
        height=1000,
        background_path=None,
        center_color=(255, 255, 255),
        edge_color=(0, 100, 255),
    ):
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.center_color = center_color
        self.edge_color = edge_color

        # Background initialization
        if background_path:
            bg = Image.open(background_path).convert("RGBA")

            bg_width, bg_height = bg.size

            # Calculate crop coordinates for centered crop
            left = max((bg_width - width) // 2, 0)
            top = max((bg_height - height) // 2, 0)
            right = left + width
            bottom = top + height

            cropped = bg.crop((left, top, right, bottom))

            # If original image is smaller than required size
            if cropped.size != (width, height):
                canvas = Image.new("RGBA", (width, height), (0, 0, 0, 255))

                paste_x = (width - cropped.size[0]) // 2
                paste_y = (height - cropped.size[1]) // 2

                canvas.paste(cropped, (paste_x, paste_y))
                self.background = canvas
            else:
                self.background = cropped
        else:
            self.background = Image.new(
                "RGBA", (width, height), (0, 0, 0, 255))

    # Color gradient calculation
    def _color_gradient(self, distance, max_radius):
        t = min(distance / max_radius, 1.0)

        r = int((1 - t) * self.center_color[0] + t * self.edge_color[0])
        g = int((1 - t) * self.center_color[1] + t * self.edge_color[1])
        b = int((1 - t) * self.center_color[2] + t * self.edge_color[2])

        return r, g, b

    # Alpha gradient calculation
    def _alpha_gradient(self, distance, max_radius):
        t = min(distance / max_radius, 1.0)
        return int(255 * (1 - t))

    # Abstract render method
    def render(self):
        raise NotImplementedError(
            "Render method must be implemented in subclass")