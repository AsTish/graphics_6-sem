import lenticular_galaxy
from spiral_galaxy import SpiralGalaxy
from lenticular_galaxy import LenticularGalaxy

if __name__ == "__main__":
    spiral_galaxy = SpiralGalaxy(
        width=800,
        height=800,
        center_color=(255, 255, 255),
        edge_color=(240, 118, 139),
        arms=5,
        arm_length=300,
        arm_width=100,
        radius=400,
        background_path="galaxy_bg.jpg"
    )

    image = spiral_galaxy.render()
    image.save("spiral.png")

    lenticular_galaxy = LenticularGalaxy(
        a=280,
        b=100,
        angle=35,
        center_color=(242, 243, 244),
        edge_color=(18, 10, 143),
        width=800,
        height=800
    )

    img = lenticular_galaxy.render()
    img.save("ellipse.png")