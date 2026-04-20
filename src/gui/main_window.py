from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
)
from calculator.service import CalculatorService
from calculator.parser import parse_input
from calculator.evaluator import InterPreter
from calculator.errors import CalculationError


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.service = CalculatorService()

        self.setWindowTitle("calculator")
        self.resize(800, 500)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("式を入力して下さい。例: 3 * 5 - 7")

        self.run_button = QPushButton("計算")
        self.result_label = QLabel("結果: ")

        self.ast_tree = QTreeWidget()
        self.ast_tree.setHeaderLabel("AST")

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.input_box)
        left_layout.addWidget(self.run_button)
        left_layout.addWidget(self.result_label)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 1)
        main_layout.addWidget(self.ast_tree, 1)
        self.setLayout(main_layout)

        self.run_button.clicked.connect(self.calculate)
        self.input_box.returnPressed.connect(self.calculate)

    def calculate(self) -> None:
        interpreter = InterPreter()
        text = self.input_box.text()

        try:
            ast = parse_input(text)

            self.ast_tree.clear()
            root_item = self.build_tree(ast)
            self.ast_tree.addTopLevelItem(root_item)
            self.ast_tree.expandAll()

            result = interpreter.run(ast)

            self.result_label.setText(f"結果: {result}")

        except CalculationError as e:
            self.result_label.setText(f"エラー: {e}")
            self.ast_tree.clear()

    def build_tree(self, node):
        label = node._label()
        item = QTreeWidgetItem([label])

        for child in node._children():
            child_item = self.build_tree(child)
            item.addChild(child_item)

        return item
