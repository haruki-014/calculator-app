from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
    QListWidget,
    QTableWidget,
    QTabWidget,
    QSplitter,
    QTableWidgetItem,
    QHeaderView,
)
from PySide6.QtCore import Qt
from calculator.service import CalculatorService
from calculator.parser import parse_input
from calculator.evaluator import InterPreter
from calculator.errors import CalculationError


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.interpreter = InterPreter()

        self.service = CalculatorService()

        self.setWindowTitle("calculator")
        self.resize(1000, 600)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("式を入力して下さい。例: 3 * 5 - 7")

        # 計算履歴
        self.history_list = QListWidget()

        self.run_button = QPushButton("計算")
        self.result_label = QLabel("結果: ")

        # AST
        self.ast_tree = QTreeWidget()
        self.ast_tree.setHeaderLabel("AST")

        # 変数一覧
        self.valiables_table = QTableWidget()
        self.valiables_table.setColumnCount(2)
        self.valiables_table.setHorizontalHeaderLabels(["変数", "値"])
        self.valiables_table.horizontalHeader().setStretchLastSection(True)

        header = self.valiables_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        # タブ
        self.tabs = QTabWidget()
        self.tabs.addTab(self.ast_tree, "AST")
        self.tabs.addTab(self.valiables_table, "Valiables")

        # 入力欄 ＋ 出力ボタン
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.run_button)

        # 左側 入力画面 + 履歴
        left_layout = QVBoxLayout()
        left_layout.addLayout(input_layout)
        left_layout.addWidget(QLabel("履歴"))
        left_layout.addWidget(self.history_list)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        # 右側 AST + 変数
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.tabs)

        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        # 画面分割
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 600])

        # メイン
        main_layout = QVBoxLayout()
        main_layout.addWidget(splitter)
        main_layout.addWidget(self.result_label)

        self.setLayout(main_layout)

        self.run_button.clicked.connect(self.calculate)
        self.input_box.returnPressed.connect(self.calculate)

    def calculate(self) -> None:
        text = self.input_box.text()

        try:
            # AST生成
            ast = parse_input(text)

            # ASTを初期化&表示
            self.ast_tree.clear()
            root_item = self.build_tree(ast)
            self.ast_tree.addTopLevelItem(root_item)
            self.ast_tree.expandAll()

            result = self.interpreter.run(ast)

            self.result_label.setText(f"結果: {result}")
            if "=" in text:
                self.history_list.addItem(text)
            else:
                self.history_list.addItem(f"{text} = {result}")
            self.update_valiables_table()

            # 入力欄を選択状態
            self.input_box.selectAll()
            self.input_box.setFocus()

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

    def update_valiables_table(self) -> None:
        env = self.interpreter.env

        self.valiables_table.clearContents()
        self.valiables_table.setRowCount(len(env))

        for row, (name, value) in enumerate(env.items()):
            name_item = QTableWidgetItem(str(name))
            value_item = QTableWidgetItem(str(value))

            self.valiables_table.setItem(row, 0, name_item)
            self.valiables_table.setItem(row, 1, value_item)

        self.valiables_table.resizeColumnsToContents()
        self.valiables_table.resizeRowsToContents()
