# TO-DO-Application
Advanced To-Do List App (PyQt6) A powerful, lightweight desktop To-Do List application built entirely with Python and PyQt6. This app provides an intuitive graphical interface for managing daily tasks with advanced features like checkboxes, due dates, priorities, editing, sorting, and automatic data persistence


Key Features

Task Creation: Add new tasks with a description, due date (via calendar picker), and priority level (Low, Medium, High).
Checkboxes for Completion: Each task has a checkbox to mark it as done—completed tasks automatically get strikethrough text and gray coloring.
Due Dates: Set deadlines with a pop-up calendar. Overdue tasks are highlighted in bold red for easy identification.
Priority Indicators: Tasks display colored badges—green for Low, orange for Medium, red for High.
Edit & Delete: Right-click any task to edit its description or delete it (with confirmation dialog).
Sorting Options:
Sort by Deadline (earliest due dates first)
Sort by Priority (High priority first)

Bulk Actions: Clear all completed tasks with one button.
Data Persistence: Tasks are automatically saved to a local todo_data.json file on every change and loaded when the app starts.
User-Friendly Touches:
Press Enter to quickly add tasks.
Warnings for empty inputs or past-due dates (with option to proceed).
Responsive and resizable window.


Requirements

Python 3.8 or higher
PyQt6 (installed via pip)

Installation & Setup

Install PyQt6:
  pip install pyqt6
Save the provided code as advanced_todo_app.py.

How to Run
Open a terminal in the folder containing the file and execute:
  python advanced_todo_app.py
The app window will appear, ready for use. All tasks persist between sessions via the auto-generated todo_data.json file.
Usage Guide

Adding a Task: Type in the input field, select a due date and priority, then click "Add Task" or press Enter.
Managing Tasks:
Check/uncheck the box to toggle completion.
Right-click a task for Edit/Delete options.

Organizing: Use the bottom buttons to sort or clear completed tasks.

Project Files

advanced_todo_app.py: The main executable script.
todo_data.json: Automatically created/saved—contains your task data (delete to reset).
