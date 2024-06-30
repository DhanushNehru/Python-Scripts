import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLineEdit, \
    QPushButton, QSizePolicy
from PySide6.QtGui import QFont
class ToDoListApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyToDo: To-Do List App")
        self.setGeometry(200, 200, 400, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.task_list = QListWidget()
        self.layout.addWidget(self.task_list)

        self.task_input = QLineEdit()
        self.layout.addWidget(self.task_input)

        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)
        self.layout.addWidget(self.add_button)

        self.task_widgets = []

    def add_task(self):
        task_text = self.task_input.text()
        if task_text:
            task_widget = QWidget()
            task_layout = QHBoxLayout(task_widget)

            
            font = QFont()
            font.setPointSize(10)


            task_label = QPushButton(task_text)
            task_label.setCheckable(False)
            task_label.setChecked(False)
            task_label.clicked.connect(self.update_task_status)
            task_label.setFont(font)
            task_label.adjustSize()

            delete_button = QPushButton("Done")
            delete_button.clicked.connect(lambda: self.delete_task(task_widget))
            delete_button.setFixedWidth(70)  # Adjust the width as needed
            delete_button.setFont(font)
            delete_button.adjustSize()
            
            task_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            delete_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
            task_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)


            task_layout.addWidget(task_label)
            task_layout.addWidget(delete_button)
            task_layout.setContentsMargins(0, 0, 0, 0)
            task_layout.setSpacing(1)
            
            self.task_list.addItem("")
            self.task_list.setItemWidget(self.task_list.item(self.task_list.count() - 1), task_widget)
            self.task_widgets.append((task_widget, task_label, delete_button))

            self.task_input.clear()

    def delete_task(self, task_widget):
        for index, (widget, _, _) in enumerate(self.task_widgets):
            if widget == task_widget:
                self.task_list.takeItem(index)
                self.task_widgets.pop(index)
                break
    def update_task_status(self):
        task_label = self.sender()
        for _, label, _ in self.task_widgets:
            if label == task_label:
                label.setChecked(task_label.isChecked())
                break


if __name__ == "__main__":

    app = QApplication(sys.argv)
    todo_app = ToDoListApp()
    todo_app.show()
    sys.exit(app.exec_())