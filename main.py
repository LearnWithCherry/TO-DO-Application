import sys
import json
import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QListWidgetItem, QLineEdit, QPushButton, QLabel, QComboBox,
    QDateEdit, QMessageBox, QCheckBox, QMenu, QInputDialog
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIcon, QColor, QBrush

# File to save tasks
DATA_FILE = "todo_data.json"

class TodoItem:
    def __init__(self, text, completed=False, deadline=None, priority="Medium"):
        self.text = text
        self.completed = completed
        self.deadline = deadline  # string in 'YYYY-MM-DD'
        self.priority = priority  # Low, Medium, High

    def to_dict(self):
        return {
            "text": self.text,
            "completed": self.completed,
            "deadline": self.deadline,
            "priority": self.priority
        }

    @staticmethod
    def from_dict(data):
        return TodoItem(
            text=data["text"],
            completed=data.get("completed", False),
            deadline=data.get("deadline"),
            priority=data.get("priority", "Medium")
        )

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced To-Do List")
        self.setGeometry(300, 200, 600, 600)
        self.tasks = []

        self.init_ui()
        self.load_tasks()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("<h1>Advanced To-Do List</h1>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Input row
        input_layout = QHBoxLayout()

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task...")
        input_layout.addWidget(self.task_input)

        self.deadline_edit = QDateEdit()
        self.deadline_edit.setCalendarPopup(True)
        self.deadline_edit.setDate(QDate.currentDate())
        self.deadline_edit.setMinimumWidth(120)
        input_layout.addWidget(QLabel("Due:"))
        input_layout.addWidget(self.deadline_edit)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])
        self.priority_combo.setCurrentIndex(1)
        input_layout.addWidget(QLabel("Priority:"))
        input_layout.addWidget(self.priority_combo)

        add_btn = QPushButton("Add Task")
        add_btn.clicked.connect(self.add_task)
        input_layout.addWidget(add_btn)

        main_layout.addLayout(input_layout)

        # Task list
        self.task_list = QListWidget()
        self.task_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.task_list.customContextMenuRequested.connect(self.show_context_menu)
        main_layout.addWidget(self.task_list)

        # Bottom buttons
        bottom_layout = QHBoxLayout()

        sort_btn = QPushButton("Sort by Deadline")
        sort_btn.clicked.connect(self.sort_by_deadline)
        bottom_layout.addWidget(sort_btn)

        sort_priority_btn = QPushButton("Sort by Priority")
        sort_priority_btn.clicked.connect(self.sort_by_priority)
        bottom_layout.addWidget(sort_priority_btn)

        clear_completed_btn = QPushButton("Clear Completed")
        clear_completed_btn.clicked.connect(self.clear_completed)
        bottom_layout.addWidget(clear_completed_btn)

        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        # Allow Enter key to add task
        self.task_input.returnPressed.connect(add_btn.click)

    def add_task(self):
        text = self.task_input.text().strip()
        if not text:
            QMessageBox.warning(self, "Empty Task", "Please enter a task description!")
            return

        deadline = self.deadline_edit.date().toString("yyyy-MM-dd")
        if self.deadline_edit.date() < QDate.currentDate():
            reply = QMessageBox.question(self, "Past Deadline",
                                         "The selected deadline is in the past. Continue?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return

        priority = self.priority_combo.currentText()

        task = TodoItem(text=text, deadline=deadline, priority=priority)
        self.tasks.append(task)
        self.refresh_task_list()

        self.task_input.clear()
        self.save_tasks()

    def refresh_task_list(self):
        self.task_list.clear()
        for task in self.tasks:
            item_widget = self.create_task_widget(task)
            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())
            list_item.setData(Qt.ItemDataRole.UserRole, task)

            self.task_list.addItem(list_item)
            self.task_list.setItemWidget(list_item, item_widget)

    def create_task_widget(self, task):
        widget = QWidget()
        layout = QHBoxLayout()

        checkbox = QCheckBox()
        checkbox.setChecked(task.completed)
        checkbox.stateChanged.connect(lambda state, t=task: self.toggle_complete(t, state))
        layout.addWidget(checkbox)

        text_label = QLabel(task.text)
        if task.completed:
            text_label.setStyleSheet("text-decoration: line-through; color: gray;")
        layout.addWidget(text_label, stretch=1)

        # Priority color indicator
        priority_colors = {
            "High": QColor("red"),
            "Medium": QColor("orange"),
            "Low": QColor("green")
        }
        priority_label = QLabel(task.priority)
        priority_label.setStyleSheet(f"color: white; background-color: {priority_colors[task.priority].name()}; padding: 2px 8px; border-radius: 4px;")
        layout.addWidget(priority_label)

        # Deadline
        deadline_str = task.deadline if task.deadline else "No deadline"
        deadline_label = QLabel(deadline_str)
        if task.deadline and datetime.strptime(task.deadline, "%Y-%m-%d").date() < datetime.now().date():
            deadline_label.setStyleSheet("color: red; font-weight: bold;")
        layout.addWidget(deadline_label)

        widget.setLayout(layout)
        return widget

    def toggle_complete(self, task, state):
        task.completed = (state == Qt.CheckState.Checked.value)
        self.refresh_task_list()
        self.save_tasks()

    def show_context_menu(self, position):
        item = self.task_list.itemAt(position)
        if not item:
            return

        task = item.data(Qt.ItemDataRole.UserRole)
        menu = QMenu()

        edit_action = menu.addAction("Edit Task")
        delete_action = menu.addAction("Delete Task")

        action = menu.exec(self.task_list.mapToGlobal(position))

        if action == edit_action:
            self.edit_task(task)
        elif action == delete_action:
            self.delete_task(task)

    def edit_task(self, task):
        new_text, ok = QInputDialog.getText(self, "Edit Task", "Task description:", text=task.text)
        if ok and new_text.strip():
            task.text = new_text.strip()
            self.refresh_task_list()
            self.save_tasks()

    def delete_task(self, task):
        reply = QMessageBox.question(self, "Delete Task", "Delete this task permanently?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.tasks.remove(task)
            self.refresh_task_list()
            self.save_tasks()

    def sort_by_deadline(self):
        def key(t):
            if t.deadline:
                return datetime.strptime(t.deadline, "%Y-%m-%d")
            return datetime.max
        self.tasks.sort(key=key)
        self.refresh_task_list()

    def sort_by_priority(self):
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        self.tasks.sort(key=lambda t: priority_order[t.priority])
        self.refresh_task_list()

    def clear_completed(self):
        remaining = [t for t in self.tasks if not t.completed]
        if len(remaining) == len(self.tasks):
            QMessageBox.information(self, "No Completed Tasks", "There are no completed tasks to clear.")
            return
        self.tasks = remaining
        self.refresh_task_list()
        self.save_tasks()

    def save_tasks(self):
        data = [task.to_dict() for task in self.tasks]
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print("Error saving tasks:", e)

    def load_tasks(self):
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.tasks = [TodoItem.from_dict(item) for item in data]
                self.refresh_task_list()
        except Exception as e:
            print("Error loading tasks:", e)

    def closeEvent(self, event):
        self.save_tasks()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Optional: set a nice app icon if you have one
    # app.setWindowIcon(QIcon("icon.png"))

    window = TodoApp()
    window.show()
    sys.exit(app.exec())