import os
from spiral_galaxy import SpiralGalaxy
from lenticular_galaxy import LenticularGalaxy


WIDTH = 800
HEIGHT = 800


COLOR_PRESETS = {
    "1": ("White", (255, 255, 255)),
    "2": ("Blue", (0, 100, 255)),
    "3": ("Red", (255, 50, 50)),
    "4": ("Yellow", (255, 255, 100)),
    "5": ("Purple", (180, 0, 255)),
    "6": ("Cyan", (0, 255, 255)),
    "7": ("Orange", (255, 140, 0)),
    "8": ("Green", (0, 200, 100)),
    "9": ("Pink", (255, 105, 180)),
    "10": ("Light Blue", (150, 200, 255)),
}


def choose_color(prompt):
    print(f"\n{prompt}")
    for key, (name, _) in COLOR_PRESETS.items():
        print(f"{key}. {name}")

    choice = input("Select option: ")
    return COLOR_PRESETS.get(choice, COLOR_PRESETS["1"])[1]


def choose_background():
    print("\nBackground options:")
    print("1. Black")
    print("2. White")
    print("3. Image file")

    choice = input("Select option: ")

    if choice == "1":
        return None, (0, 0, 0)
    elif choice == "2":
        return None, (255, 255, 255)
    elif choice == "3":
        path = input("Enter image file path: ")
        return path, None
    else:
        return None, (0, 0, 0)


def get_output_filename():
    name = input("\nEnter output file name: ").strip()

    if "." not in name:
        name += ".jpg"

    return name


def main():
    print("===================================")
    print("     Galaxy Generator (CLI)")
    print("===================================")

    print("\nSelect galaxy type:")
    print("1. Lenticular")
    print("2. Spiral")

    galaxy_choice = input("Enter choice: ")

    bg_path, bg_color = choose_background()

    center_color = choose_color("Select center color:")
    edge_color = choose_color("Select edge color:")

    if galaxy_choice == "1":
        angle = int(input("\nEnter tilt angle (degrees): "))

        galaxy = LenticularGalaxy(
            width=WIDTH,
            height=HEIGHT,
            a=280,
            b=100,
            angle=angle,
            background_path=bg_path,
            center_color=center_color,
            edge_color=edge_color,
        )

    elif galaxy_choice == "2":
        arms = int(input("\nEnter number of arms: "))

        galaxy = SpiralGalaxy(
            width=WIDTH,
            height=HEIGHT,
            arms=arms,
            arm_length=300,
            arm_width=100,
            radius=400,
            background_path=bg_path,
            center_color=center_color,
            edge_color=edge_color,
        )

    else:
        print("Invalid choice.")
        return

    print("\nGenerating galaxy...")
    image = galaxy.render()

    if bg_color is not None:
        image = image.convert("RGBA")
        background = image.copy()
        pixels = background.load()

        for x in range(WIDTH):
            for y in range(HEIGHT):
                if pixels[x, y][3] == 255 and pixels[x, y][:3] == (0, 0, 0):
                    pixels[x, y] = (*bg_color, 255)

        image = background

    filename = get_output_filename()
    image.convert("RGB").save(filename)

    print(f"\nGalaxy saved as: {filename}")
    print("Done.")


if __name__ == "__main__":
    main()