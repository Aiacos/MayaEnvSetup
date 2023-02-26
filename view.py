import sys
import pathlib

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

import control
import model


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.workspace_control = control.ProjectParser()
        self.maya_env_manager = control.EnvVarManager()

        self.setWindowTitle('Environment Setup')

        # set Layout
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)

        self.project_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.project_layout)

        self.env_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.env_layout)

        self.variables_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.variables_layout)

        # Project Label
        self.project_label = QtWidgets.QLabel()
        self.project_layout.addWidget(self.project_label)
        self.project_label.setText('Project:')

        #  Project WidgetList
        self.project_listWidget = QtWidgets.QTreeWidget()
        self.project_listWidget.setHeaderHidden(True)
        self.project_listWidget.adjustSize()
        self.project_layout.addWidget(self.project_listWidget)

        # Env Label
        self.env_label = QtWidgets.QLabel()
        self.env_layout.addWidget(self.env_label)
        self.env_label.setText('Maya.env:')

        # Env WidgetList
        self.env_listWidget = QtWidgets.QListWidget()
        self.env_listWidget.adjustSize()
        self.env_layout.addWidget(self.env_listWidget)

        # Variables Button
        self.env_button_layout = QtWidgets.QHBoxLayout()
        self.env_addall_button = QtWidgets.QPushButton('Add All')
        self.env_removeall_button = QtWidgets.QPushButton('Remove All')
        self.env_button_layout.addWidget(self.env_addall_button)
        self.env_button_layout.addWidget(self.env_removeall_button)
        self.env_layout.addLayout(self.env_button_layout)

        # Variables Label
        self.variables_label = QtWidgets.QLabel()
        self.variables_layout.addWidget(self.variables_label)
        self.variables_label.setText('Variables:')

        # Variables WidgetList
        self.variables_listWidget = QtWidgets.QListWidget()
        self.variables_listWidget.adjustSize()
        self.variables_layout.addWidget(self.variables_listWidget)

        # Variables Button
        self.variable_button_layout = QtWidgets.QHBoxLayout()
        self.variable_clear_button = QtWidgets.QPushButton('Clear')
        self.variable_write_button = QtWidgets.QPushButton('Write')
        self.variable_button_layout.addWidget(self.variable_clear_button)
        self.variable_button_layout.addWidget(self.variable_write_button)
        self.variables_layout.addLayout(self.variable_button_layout)

        # Connects Interactions
        self.project_listWidget.itemClicked.connect(self.onItemClicked)
        self.env_listWidget.itemDoubleClicked.connect(self.check_onItemDoubleClicked)
        self.variables_listWidget.itemDoubleClicked.connect(self.remove_onItemDoubleClicked)

        # Connects Variables Button
        self.variable_clear_button.clicked.connect(self.clear_variable_list)
        self.variable_write_button.clicked.connect(self.write_env_var)

        # Connect Env Button
        self.env_addall_button.clicked.connect(self.add_all_variables)
        self.env_removeall_button.clicked.connect(self.remove_all_variables)

        self.fill_projects()

        self.show()

    def onItemClicked(self):
        item = self.project_listWidget.currentItem()
        if item.parent():
            self.env_listWidget.clear()
            var_dict = model.parse_maya_env(item.text(0))
            for key, value in var_dict.items():
                line = ''
                if isinstance(value, str):
                    line = key + ' = ' + value
                if isinstance(value, list):
                    line = key + ' = ' + ';'.join(value)

                self.env_listWidget.addItem(line)

    def check_onItemDoubleClicked(self):
        env_variable = self.env_listWidget.currentItem().text()
        if not self.maya_env_manager.check_variable(env_variable):
            self.add_onItemDoubleClicked()
        else:
            self.removeValue_onItemDoubleClicked()

    def add_onItemDoubleClicked(self):
        self.variables_listWidget.clear()

        env_variable = self.env_listWidget.currentItem().text()
        self.maya_env_manager.add_variable(env_variable)

        for line in self.maya_env_manager.get_env_as_list():
            self.variables_listWidget.addItem(line)

    def remove_onItemDoubleClicked(self):
        item = self.variables_listWidget.currentItem().text()

        self.maya_env_manager.remove_variable(item)

        self.variables_listWidget.clear()
        for line in self.maya_env_manager.get_env_as_list():
            self.variables_listWidget.addItem(line)

    def removeValue_onItemDoubleClicked(self):
        item = self.env_listWidget.currentItem().text()

        self.maya_env_manager.remove_variable_value(item)

        self.variables_listWidget.clear()
        for line in self.maya_env_manager.get_env_as_list():
            self.variables_listWidget.addItem(line)

    def clear_variable_list(self):
        key_list = []
        for key, value in self.maya_env_manager.maya_env_dict.items():
            key_list.append(key)

        for key in key_list:
            del self.maya_env_manager.maya_env_dict[key]

        self.variables_listWidget.clear()

    def fill_projects(self):
        workspace_list = self.workspace_control.get_projects()

        for project_path in workspace_list:
            element = QtWidgets.QTreeWidgetItem([project_path])
            self.project_listWidget.addTopLevelItem(element)

            env_path_list = self.workspace_control.search_env_file(project_path)
            for env_path in env_path_list:
                sub_element = QtWidgets.QTreeWidgetItem([env_path])
                element.addChild(sub_element)

    def fill_env_files(self):
        workspace_list = self.workspace_control.get_projects()
        for project_path in workspace_list:
            env_path_list = self.workspace_control.search_env_file(project_path)
            for env_path in env_path_list:
                self.env_listWidget.addItem(env_path)

    def write_env_var(self):
        self.maya_env_manager.write_env_file()

    def add_all_variables(self):
        self.variables_listWidget.clear()

        for i in range(self.env_listWidget.count()):
            item = self.env_listWidget.item(i)
            env_variable = item.text()
            self.maya_env_manager.add_variable(env_variable)

        for line in self.maya_env_manager.get_env_as_list():
            self.variables_listWidget.addItem(line)

    def remove_all_variables(self):
        for i in range(self.env_listWidget.count()):
            item = self.env_listWidget.item(i)
            env_variable = item.text()
            self.maya_env_manager.remove_variable_value(env_variable)

        self.variables_listWidget.clear()
        for line in self.maya_env_manager.get_env_as_list():
            self.variables_listWidget.addItem(line)


class PluginQListItem(QtWidgets.QWidget):
    def __init__(self, text='', var_dict={}, maya_env_manager=None, version_list=['2022'], parent=None):
        super(PluginQListItem, self).__init__(parent)

        self.text = text
        self.variable_dict = var_dict
        self.version_list = version_list
        self.maya_env_manager = maya_env_manager

        # Layout
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)

        # Widgets
        # label
        self.label = QtWidgets.QLabel()
        self.label.setText(self.text)
        # self.main_layout.addWidget(self.label)

        # Version Checkbox
        self.checkbox_list = []
        for v in self.version_list:
            version_check_box = QtWidgets.QCheckBox(v + ':')
            self.checkbox_list.append(version_check_box)
            # self.main_layout.addWidget(version_check_box)

            self.connect_checkbox(version_check_box)

    def connect_checkbox(self, checkbox_widget):
        checkbox_widget.stateChanged.connect(self.call_onCheckbox_stateChanged)

    def call_onCheckbox_stateChanged(self):
        sender = self.sender()
        version = sender.text().replace(':', '')
        if sender.isChecked():
            self.add_all_variables(self.variable_dict)
        else:
            self.remove_all_variables(self.variable_dict)

        self.maya_env_manager.write_env_file(version)

    def write_env_var(self):
        self.maya_env_manager.write_env_file()

    def add_all_variables(self, var_dict):
        for key, value in var_dict.items():
            line = ''
            if isinstance(value, str):
                line = key + ' = ' + value
            if isinstance(value, list):
                line = key + ' = ' + ';'.join(value)

            self.maya_env_manager.add_variable(line)

    def remove_all_variables(self, var_dict):
        for key, value in var_dict.items():
            line = ''
            if isinstance(value, str):
                line = key + ' = ' + value
            if isinstance(value, list):
                line = key + ' = ' + ';'.join(value)

            self.maya_env_manager.remove_variable_value(line)


class MainWindowPlugin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindowPlugin, self).__init__(parent)

        # init control istances
        self.workspace_control = control.ProjectParser()
        self.maya_env_manager = control.EnvVarManager()

        self.setWindowTitle('Environment Setup')
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)

        # set Layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        # Row List
        self.row_widget_list = []
        self.workspace_list = self.workspace_control.get_projects()

        for project_path in self.workspace_list:
            env_path_list = self.workspace_control.search_env_file(project_path)
            for env_path in env_path_list:
                var_dict = model.parse_maya_env(env_path)
                row_widget = PluginQListItem(env_path, var_dict, self.maya_env_manager, self.workspace_control.get_maya_versions())
                self.row_widget_list.append(row_widget)

        # QTableWidget
        self.table_widget = QtWidgets.QTableWidget(len(self.row_widget_list), len(self.row_widget_list[-1].checkbox_list) + 1)
        self.table_widget.setShowGrid(False)
        self.table_widget.horizontalHeader().hide()
        self.table_widget.verticalHeader().hide()
        self.table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.main_layout.addWidget(self.table_widget)

        for widget, row in zip(self.row_widget_list, range(len(self.row_widget_list))):
            self.table_widget.setCellWidget(row, 0, widget.label)
            for checkbox, column in zip(widget.checkbox_list, range(len(widget.checkbox_list))):
                self.table_widget.setCellWidget(row, column + 1, checkbox)

        # set the headers to resize to their contents
        self.table_widget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        # set the cells' resize mode to ResizeToContents
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

        self.table_widget.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        self.table_widget.horizontalHeader().setStretchLastSection(True)

        # Buttons
        self.add_workspace_button = QtWidgets.QPushButton('Add Workspace')
        self.add_workspace_button.clicked.connect(self.open_dialog)
        self.main_layout.addWidget(self.add_workspace_button)

        # set Style
        self.table_widget.setStyleSheet("background-color: transparent; border: none;")
        self.table_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.adjustSize()
        self.show()

    def open_dialog(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        folder_path = str(pathlib.Path(folder_path))
        self.workspace_control.add_projects(folder_path)

        if folder_path:
            self.table_widget.clear()
            self.row_widget_list.clear()

            self.workspace_list = self.workspace_control.get_projects()
            for project_path in self.workspace_list:
                env_path_list = self.workspace_control.search_env_file(project_path)
                for env_path in env_path_list:
                    var_dict = model.parse_maya_env(env_path)
                    row_widget = PluginQListItem(env_path, var_dict, self.maya_env_manager, self.workspace_control.get_maya_versions())
                    self.row_widget_list.append(row_widget)

            self.table_widget.setRowCount(len(self.row_widget_list))
            for widget, row in zip(self.row_widget_list, range(len(self.row_widget_list))):
                self.table_widget.setCellWidget(row, 0, widget.label)
                for checkbox, column in zip(widget.checkbox_list, range(len(widget.checkbox_list))):
                    self.table_widget.setCellWidget(row, column + 1, checkbox)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindowPlugin()
    window.setGeometry(100, 100, 800, 300)
    window.show()
    sys.exit(app.exec_())
