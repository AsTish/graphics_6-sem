import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
    QButtonGroup,
    QPushButton,
    QStatusBar,
    QSpinBox,
    QFormLayout,
    QGroupBox,
    QColorDialog,
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

from lenticular_galaxy import LenticularGalaxy
from spiral_galaxy import SpiralGalaxy

sys.path.append(os.path.abspath("."))


class GalaxyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Galaxy Viewer")
        self.setGeometry(100, 100, 1200, 800)

        # Image dimensions
        self.width = 800
        self.height = 800
        self.galaxy = None

        # Initial colors
        self.start_color = (255, 255, 255)
        self.end_color = (0, 100, 255)

        # Tilt angle for lenticular galaxy
        self.tilt_angle = 0

        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Image display
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.image_label)

        # Controls layout
        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)

        # Left panel: galaxy parameters
        type_group = QGroupBox("Galaxy Settings")
        type_layout = QFormLayout()
        type_group.setLayout(type_layout)
        control_layout.addWidget(type_group)

        # Galaxy type selection
        self.radio_group = QButtonGroup(self)
        self.radio_lenticular = QRadioButton("Lenticular")
        self.radio_spiral = QRadioButton("Spiral")
        self.radio_lenticular.setChecked(True)
        self.radio_group.addButton(self.radio_lenticular)
        self.radio_group.addButton(self.radio_spiral)
        type_layout.addRow(self.radio_lenticular, self.radio_spiral)

        # Connect radio buttons to update control visibility
        self.radio_lenticular.toggled.connect(self.update_controls_visibility)
        self.radio_spiral.toggled.connect(self.update_controls_visibility)

        # Radius control (applies to both galaxies)
        self.radius_spin = QSpinBox()
        self.radius_spin.setRange(50, 1000)
        self.radius_spin.setValue(400)
        self.radius_spin.valueChanged.connect(self.update_galaxy)
        type_layout.addRow("Radius:", self.radius_spin)

        # Tilt angle buttons for lenticular galaxy
        self.angle_label = QLabel("Tilt angle:")
        self.angle_minus_btn = QPushButton("⟲")
        self.angle_plus_btn = QPushButton("⟳")
        self.angle_minus_btn.clicked.connect(lambda: self.change_angle(-5))
        self.angle_plus_btn.clicked.connect(lambda: self.change_angle(5))
        self.angle_layout = QHBoxLayout()
        self.angle_layout.addWidget(self.angle_minus_btn)
        self.angle_layout.addWidget(self.angle_plus_btn)
        type_layout.addRow(self.angle_label, self.angle_layout)

        # Spiral arms control for spiral galaxy
        self.spiral_arms_spin = QSpinBox()
        self.spiral_arms_spin.setRange(1, 10)
        self.spiral_arms_spin.setValue(2)
        self.spiral_arms_spin.valueChanged.connect(self.update_galaxy)
        self.spiral_arms_label = QLabel("Spiral arms:")
        type_layout.addRow(self.spiral_arms_label, self.spiral_arms_spin)

        # Galaxy colors
        self.start_color_btn = QPushButton("Start Color")
        self.start_color_btn.clicked.connect(self.choose_start_color)
        type_layout.addRow("Center Color:", self.start_color_btn)

        self.end_color_btn = QPushButton("End Color")
        self.end_color_btn.clicked.connect(self.choose_end_color)
        type_layout.addRow("Edge Color:", self.end_color_btn)

        # Status bar
        self.status_bar = QStatusBar()
        main_layout.addWidget(self.status_bar)

        # Initial setup
        self.update_controls_visibility()
        self.update_galaxy()

    # Change tilt angle by delta
    def change_angle(self, delta):
        self.tilt_angle = (self.tilt_angle + delta) % 360
        self.update_galaxy()

    # Choose center color
    def choose_start_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.start_color = (color.red(), color.green(), color.blue())
            self.update_galaxy()

    # Choose edge color
    def choose_end_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.end_color = (color.red(), color.green(), color.blue())
            self.update_galaxy()

    # Update visibility of controls depending on galaxy type
    def update_controls_visibility(self):
        if self.radio_lenticular.isChecked():
            self.spiral_arms_spin.hide()
            self.spiral_arms_label.hide()
            self.angle_minus_btn.show()
            self.angle_plus_btn.show()
        else:
            self.spiral_arms_spin.show()
            self.spiral_arms_label.show()
            self.angle_minus_btn.hide()
            self.angle_plus_btn.hide()

    # Generate and display galaxy
    def update_galaxy(self):
        gal_type = "lenticular" if self.radio_lenticular.isChecked() else "spiral"
        radius = self.radius_spin.value()

        if gal_type == "lenticular":
            a = radius
            b = a // 2
            self.galaxy = LenticularGalaxy(
                width=self.width,
                height=self.height,
                a=a,
                b=b,
                angle=self.tilt_angle,
                center_color=self.start_color,
                edge_color=self.end_color
            )
        else:
            arms = self.spiral_arms_spin.value()
            self.galaxy = SpiralGalaxy(
                width=self.width,
                height=self.height,
                radius=radius,
                arms=arms,
                center_color=self.start_color,
                edge_color=self.end_color
            )

        # Generate image
        image = self.galaxy.render()
        image_qt = self.pil_to_qimage(image)
        self.image_label.setPixmap(QPixmap.fromImage(image_qt))

        # Update status bar
        status_msg = f"Rendered {gal_type} galaxy | Radius: {radius} | Center: {self.start_color} | Edge: {self.end_color}"
        if gal_type == "spiral":
            status_msg += f" | Arms: {self.spiral_arms_spin.value()}"
        self.status_bar.showMessage(status_msg)

    # Convert PIL image to QImage
    @staticmethod
    def pil_to_qimage(pil_image):
        if pil_image.mode != "RGBA":
            pil_image = pil_image.convert("RGBA")
        data = pil_image.tobytes("raw", "RGBA")
        qimage = QImage(data, pil_image.width, pil_image.height,
                        QImage.Format.Format_RGBA8888)
        return qimage


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GalaxyWindow()
    window.show()
    sys.exit(app.exec())