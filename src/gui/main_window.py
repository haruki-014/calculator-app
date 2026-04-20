from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from calculator.service import CalculatorService


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.service = CalculatorService()

        self.setWindowTitle("calculator")
        self.resize(500, 300)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("式を入力して下さい。例: 3 * 5 - 7")

        self.run_button = QPushButton("計算")
        self.result_label = QLabel("結果: ")

        layout = QVBoxLayout()
        layout.addWidget(self.input_box)
        layout.addWidget(self.run_button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

        self.run_button.clicked.connect(self.calculate)
        self.input_box.returnPressed.connect(self.calculate)

    def calculate(self) -> None:
        text = self.input_box.text()
        result = self.service.execute(text)
        self.result_label.setText(f"結果: {result}")
