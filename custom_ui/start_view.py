import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class StartView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Set up algorithm selector combo box
        self.selected_algorithm = 0
        self.algorithm_selector = QComboBox(self)
        self.algorithm_selector.setFixedSize(120, 20)
        self.algorithm_selector.currentIndexChanged.connect(self.__algorithm_selected)

        # Welcome text
        self.figure = plt.figure(figsize=(50, 50))
        welcome_text = "This is a process mining tool.\nIt can create nice looking graphs out of CSV files!"
        plt.text(0.5, 0.5, welcome_text, fontsize=24, ha='center', va='center')
        plt.axis('off')
        self.canvas = FigureCanvas(self.figure)

        # Two buttons 'LOAD EXISTING PROCESS' 'MINE NEW PROCESS FROM CSV'
        load_button = QPushButton("LOAD EXISTING PROCESS")
        load_button.setFixedSize(150, 70)
        load_button.setStyleSheet("background-color: rgb(0, 128, 0)")
        load_button.clicked.connect(self.mine_existing_process)

        mine_button = QPushButton("MINE NEW PROCESS FROM CSV")
        mine_button.setFixedSize(180, 70)
        mine_button.setStyleSheet("background-color: rgb(30, 144, 255)")
        mine_button.clicked.connect(self.mine_new_process)

        # 'LOAD EXISTING PROCESS' needs a drop down menu to its side
        load_process_layout = QHBoxLayout()
        load_process_layout.addWidget(self.algorithm_selector)
        load_process_layout.addWidget(load_button)

        # Wrap together the 2 buttons.
        button_layout = QHBoxLayout()
        button_layout.addLayout(load_process_layout)
        button_layout.addWidget(mine_button)

        # Wrap together the Welcome Text and the 2 buttons
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    # CALL BEFORE INIT
    def load_algorithms(self, array):
        for element in array:
            self.algorithm_selector.addItem(element)

    def mine_existing_process(self):
        cases = self.__load()
        if not cases:
            return
        
        self.parent.mine_process(cases, self.selected_algorithm)

    def mine_new_process(self):
        self.parent.mine_new_process()
        
    def __algorithm_selected(self, index):
        self.algorithm_selector.setCurrentIndex(index)
        self.selected_algorithm = index

    # loads a saved txt file back into arrays
    def __load(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Select file", "saves/", "Text files (*.txt)")

        # If the user cancels the file dialog, return
        if not file_path:
            return
        
        # Convert the txt content back to array
        with open(file_path, "r") as f:
            array = []
            for line in f:
                array.append(line.strip().split())
        return array
    
    def clear(self):
        self.algorithm_selector.clear()