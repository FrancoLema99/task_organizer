import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, 
    QListWidget, QLineEdit, QMessageBox, QHBoxLayout,
    QListWidgetItem
)
from PyQt5.QtGui import QFont, QBrush, QColor

file = 'tasks.txt'

# Función para la lectura de las tareas
def load_tasks():
    if os.path.exists(file):
        with open(file, 'r', encoding='UTF-8') as content:
            for line in content:
                task, status_task = line.strip().split('|')
                list_element = create_element_list_widget(task, status_task=='✓')
                tasks_list.addItem(list_element)
                
# Función para crear las tareas
def create_element_list_widget(text, completed=False):
    list_element = QListWidgetItem(text)
    font = QFont()
    font.setStrikeOut(completed)
    list_element.setFont(font)

    if completed:
        list_element.setForeground(QBrush(QColor('gray')))

    return list_element

# Función para agregar las tareas
def add_tasks():
    text = tasks_input_text.text().strip()

    if text:
        list_element = create_element_list_widget(text)
        tasks_list.addItem(list_element)
        tasks_input_text.clear()
        save_tasks()
    
    else:
        QMessageBox.warning(window, 'Advertencia', '¡Escribe una tarea!')

# Función para guardar el texto en el archivo .txt
def save_tasks():
    with open(file, 'w', encoding='UTF-8') as file_text:
        for index_element in range(tasks_list.count()):
            list_element = tasks_list.item(index_element)
            text = list_element.text()
            completed_task = '✓' if list_element.font().strikeOut() else '✗'
            file_text.write(f'{text}|{completed_task}\n')

# Función para eliminar las tareas
def delete_tasks():
    list_element = tasks_list.currentItem()

    if list_element:
        index_element = tasks_list.row(list_element)
        tasks_list.takeItem(index_element)
        save_tasks() # Llama a la función para actualizar la lista una vez que elimino una tarea

    else:
        QMessageBox.warning(window, 'Advertencia', 'Debes seleccionar una tarea para poder eliminarla')

# Función para finalizar las tareas
def complete_tasks():
    list_element = tasks_list.currentItem()

    if list_element:
        font = list_element.font()
        completed = not font.strikeOut()
        font.setStrikeOut(completed)
        list_element.setFont(font)
        list_element.setForeground(QBrush(QColor('gray') if completed else QColor('black')))
        save_tasks()
    
    else:
        QMessageBox.warning(window, 'Advertencia', 'Debese seleccionar una tarea.')

app = QApplication(sys.argv)

# Ajustes de la ventana de interfaz 
window = QWidget()
window.setWindowTitle('Lista de tareas')
window.setGeometry(100, 100, 400, 500)

# Layouts dentro de la ventana
main_layout = QVBoxLayout() # Vertical
tasks_input_text = QLineEdit()
tasks_input_text.setPlaceholderText('Agrega una nueva tarea...')
main_layout.addWidget(tasks_input_text)

# Botones
buttons_layout = QHBoxLayout() # Horizontal

button_add = QPushButton('Agregar')
button_add.clicked.connect(add_tasks)
buttons_layout.addWidget(button_add)

button_delete = QPushButton('Eliminar')
button_delete.clicked.connect(delete_tasks)
buttons_layout.addWidget(button_delete)

button_complete = QPushButton('¡Finalizar tarea!')
button_complete.clicked.connect(complete_tasks)
buttons_layout.addWidget(button_complete)


main_layout.addLayout(buttons_layout)


# Creamos la lista de teareas
tasks_list = QListWidget()
main_layout.addWidget(tasks_list)


window.setLayout(main_layout)
load_tasks()
window.show()
sys.exit(app.exec_())