import os
import re
import sys
import json
import hashlib

from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.MainWindow import Ui_MainWindow
from gui.PasswordEditPrompt import Ui_Form as Ui_PasswordEditPrompt
from gui import resources


class Data:
    def __init__(self):
        self.opened = False
        self.path = ""
        self.db = {}
        self.saved = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(950, 600)

        self.connect_signals()
    
    def connect_signals(self):
        self.ui.menu01_open.clicked.connect(open_file)
        self.ui.menu01_new.clicked.connect(new_file)
        self.ui.menu02_button_1.clicked.connect(view)
        self.ui.menu02_button_2.clicked.connect(add_user)
        self.ui.menu02_button_3.clicked.connect(delete_user)
        self.ui.menu02_button_4.clicked.connect(edit_user)
        self.ui.menu02_button_5.clicked.connect(save)
        self.ui.menu02_button_6.clicked.connect(write_email)
        self.ui.menu02_button_7.clicked.connect(sort_ui)
        self.ui.menu02_button_8.clicked.connect(logout)
        self.ui.menu03_back.clicked.connect(back_to_main_menu)
        self.ui.menu04_back.clicked.connect(cancel_registration)
        self.ui.menu04_button_back.clicked.connect(cancel_registration)
        self.ui.menu04_button_continue.clicked.connect(register)
        self.ui.menu04_field_password.textChanged.connect(show_pass_strength)
        self.ui.menu04_toggle_visible.clicked.connect(lambda: toggle_pass_visible(mainWindow.ui.menu04_field_password))
        self.ui.menu05_back.clicked.connect(back_to_main_menu)
        self.ui.menu05_search_by_name.clicked.connect(lambda: search_criteria_change(1))
        self.ui.menu05_search_by_login.clicked.connect(lambda: search_criteria_change(2))
        self.ui.menu05_search_by_phone.clicked.connect(lambda: search_criteria_change(3))
        self.ui.menu05_search_button.clicked.connect(search)
        self.ui.menu05_one_field_edit.textChanged.connect(search_query_changed)
        self.ui.menu05_two_fields_edit_1.textChanged.connect(search_query_changed)
        self.ui.menu05_two_fields_edit_2.textChanged.connect(search_query_changed)
        self.ui.menu06_back.clicked.connect(cancel_email)
        self.ui.menu06_button_back.clicked.connect(cancel_email)
        self.ui.menu06_button_send.clicked.connect(send)
        self.ui.menu06_button_clear.clicked.connect(clear_email)
        self.ui.menu06_recipient_select.clicked.connect(select_user_button)
        self.ui.menu06_subject_field.textChanged.connect(subject_changed)
        self.ui.menu07_button_add.clicked.connect(add_user)
        self.ui.menu07_button_return.clicked.connect(back_to_main_menu)
        self.ui.menu08_back.clicked.connect(lambda: back_to_main_menu(confirmation="Выйти из режима редактирования?", title="Подтверждение"))
        self.ui.menu08_button_back.clicked.connect(edit_user)
        self.ui.menu08_button_change_pass.clicked.connect(edit_pass_window)
        self.ui.menu09_toggle_visible.clicked.connect(lambda: toggle_pass_visible(self.ui.menu09_field_password))
        self.ui.menu11_back.clicked.connect(back_to_main_menu)
        self.ui.menu11_button_back.clicked.connect(back_to_main_menu)
        self.ui.menu11_button_continue.clicked.connect(do_sorting)


    def closeEvent(self, event):
        if check_unsaved() == 1:
            event.accept()
        else:
            event.ignore()


def new_file():
    path = QFileDialog.getSaveFileName(parent=mainWindow,
                                       directory="users.json",
                                       caption="Выберите папку",
                                       filter="База данных (*.json);;Все файлы (*)")[0]
    dialog = QMessageBox
    if (path):
        data.path = os.path.abspath(path)
        data.db["signature"] = "AuthMe Database, version 1.0"
        data.db["users"] = []
        data.db["last_id"] = 0
        try:
            if (os.path.isfile(data.path)):
                backup_name = data.path.rsplit(".", 1)[0] + "_backup." + data.path.rsplit(".", 1)[1]
                backup_index = 0
                backup_name_new = backup_name
                while os.path.isfile(backup_name_new):
                    backup_index += 1
                    backup_name_new = backup_name.rsplit(".", 1)[0] + "_" + str(backup_index) + "." + backup_name.rsplit(".", 1)[1]
                os.rename(data.path, backup_name_new)
            json.dump(data.db, open(data.path, "w", encoding="utf-8"), ensure_ascii=False, indent=4)
            data.opened = True
            data.saved = True
            mainWindow.ui.menu02_button_5.setStyleSheet("")
            mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu02_page_main)
        except:
            dialog.critical(mainWindow, "Ошибка", f"Не удалось создать базу данных.")
            data.path = ""
            data.db = {}
            if (os.path.isfile(data.path)):
                os.remove(data.path)


def open_file():
    path = QFileDialog.getOpenFileName(parent=mainWindow,
                                       caption="Выберите файл базы данных (json)",
                                       filter="База данных (*.json);;Все файлы (*)")[0]
    dialog = QMessageBox
    if (path):
        data.path = os.path.abspath(path)
        if (os.path.isfile(data.path)):
            try:
                data.db = json.load(open(data.path, encoding="utf-8"))
                if "signature" in data.db:
                    if data.db["signature"] == "AuthMe Database, version 1.0":
                        data.opened = True
                        data.saved = True
                        if "last_id" not in data.db:
                            data.db["last_id"] = 0
                        if "users" not in data.db:
                            data.db["users"] = []
                        mainWindow.ui.menu02_button_5.setStyleSheet("")
                        mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu02_page_main)
                    else:
                        dialog.critical(mainWindow, "Ошибка при импорте базы данных", f"Файл {data.path} не поддерживается.")
                        data.path = ""
                else:
                    dialog.critical(mainWindow, "Ошибка при импорте базы данных", f"Файл {data.path} не поддерживается.")
                    data.path = ""
            except json.decoder.JSONDecodeError:
                dialog.critical(mainWindow, "Ошибка при импорте базы данных", f"Файл {data.path} не является корректным JSON файлом.")
                data.path = ""
            except UnicodeDecodeError:
                dialog.critical(mainWindow, "Ошибка при импорте базы данных", "Ошибка декодирования UTF-8.")
                data.path = ""
        else:
            dialog.critical(mainWindow, "Ошибка при импорте базы данных", f"Файл {data.path} не существует.")
            data.path = ""


def view():
    table = mainWindow.ui.menu03_tableWidget
    table.setStyleSheet("font-size: 8pt;")
    table.setRowCount(len(data.db["users"]))
    
    id_col_len = len(str(data.db["last_id"])) * 20
    table.setColumnWidth(0, id_col_len)
    table.setColumnWidth(1, 130)
    table.setColumnWidth(2, 130)
    table.setColumnWidth(3, 130)
    table.setColumnWidth(4, 140)
    table.setColumnWidth(5, (200 - id_col_len) if (id_col_len > 30 and id_col_len <= 180) else 170)
    table.setColumnWidth(6, 150)

    if table.columnCount() == 7:
        table.insertColumn(7)
        table.setHorizontalHeaderLabels(["ID", "Фамилия", "Имя", "Отчество", "Номер телефона", "E-mail", "Логин", "Хэшированный пароль (SHA-256)"])
        table.setColumnWidth(7, 64 * 8)

    for person in range(len(data.db["users"])):
        user_info = data.db["users"][person]
        table.setItem(person, 0, QTableWidgetItem(str(user_info["id"])))
        table.setItem(person, 1, QTableWidgetItem(user_info["surname"]))
        table.setItem(person, 2, QTableWidgetItem(user_info["name"]))
        table.setItem(person, 3, QTableWidgetItem(user_info["patronym"] if user_info["patronym"] else "-"))
        table.setItem(person, 4, QTableWidgetItem(user_info["phone"]))
        table.setItem(person, 5, QTableWidgetItem(user_info["e-mail"]))
        table.setItem(person, 6, QTableWidgetItem(user_info["login"]))

        table.setItem(person, 7, QTableWidgetItem(user_info["password"]))
    
    mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu03_page_view)


def add_user():
    mainWindow.ui.menu04_field_surname.clear()
    mainWindow.ui.menu04_field_name.clear()
    mainWindow.ui.menu04_field_patronym.clear()
    mainWindow.ui.menu04_field_phone.clear()
    mainWindow.ui.menu04_field_email.clear()
    mainWindow.ui.menu04_field_login.clear()
    mainWindow.ui.menu04_field_password.clear()
    mainWindow.ui.menu04_field_password.setEchoMode(QLineEdit.Password)

    mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu04_page_register)


def cancel_registration():
    if mainWindow.ui.menu04_field_surname.text() \
    or mainWindow.ui.menu04_field_name.text() \
    or mainWindow.ui.menu04_field_patronym.text() \
    or mainWindow.ui.menu04_field_phone.text() \
    or mainWindow.ui.menu04_field_email.text() \
    or mainWindow.ui.menu04_field_login.text() \
    or mainWindow.ui.menu04_field_password.text():
        back_to_main_menu(confirmation="Отменить регистрацию и вернуться в главное меню?")
    else:
        back_to_main_menu()


def toggle_pass_visible(obj):
    if (obj.echoMode() == QLineEdit.Password):
        obj.setEchoMode(QLineEdit.Normal)
    else:
        obj.setEchoMode(QLineEdit.Password)
    obj.setFocus()


def show_pass_strength(string):
    pwd = r"^[A-Za-z\d_\-\.@$!%*?&]+$"
    moderate = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d_\-\.@$!%*?&]{8,}$"
    strong = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d_\-\.@$!%*?&]{8,}$"

    if re.fullmatch(strong, string):
        mainWindow.ui.menu04_text_strength.setText("<html><head/><body><p><span style=\" color:#00b400;\">■■■■■■ </span><span style=\" color:#000000;\">Надёжный пароль</span></p></body></html>")
    elif re.fullmatch(moderate, string):
        mainWindow.ui.menu04_text_strength.setText("<html><head/><body><p><span style=\" color:#f9c300;\">■■■■</span><span style=\" color:#aaaaaa;\">■■ </span><span style=\" color:#000000;\">Умеренный пароль</span></p></body></html>")
    elif re.fullmatch(pwd, string):
        mainWindow.ui.menu04_text_strength.setText("<html><head/><body><p><span style=\" color:#ff0000;\">■■</span><span style=\" color:#aaaaaa;\">■■■■ </span><span style=\" color:#000000;\">Слабый пароль</span></p></body></html>")
    elif len(string) > 0:
        mainWindow.ui.menu04_text_strength.setText("<html><head/><body><p><span style=\" color:#ff0000;\">■■■■■■ </span><span style=\" color:#000000;\">Недопустимый пароль</span></p></body></html>")
    else:
        mainWindow.ui.menu04_text_strength.setText("<html><head/><body><p><span style=\" color:#aaaaaa;\">■■■■■■</span></p></body></html>")


def show_pass_strength_edit(string):
    pwd = r"^[A-Za-z\d_\-\.@$!%*?&]+$"
    moderate = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d_\-\.@$!%*?&]{8,}$"
    strong = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d_\-\.@$!%*?&]{8,}$"

    if re.fullmatch(strong, string):
        mainWindow.pass_edit.ui.text_strength.setText("<html><head/><body><p><span style=\" color:#00b400;\">■■■■■■ </span><span style=\" color:#000000;\">Надёжный пароль</span></p></body></html>")
        mainWindow.pass_edit.ui.ok.setEnabled(True)
    elif re.fullmatch(moderate, string):
        mainWindow.pass_edit.ui.text_strength.setText("<html><head/><body><p><span style=\" color:#f9c300;\">■■■■</span><span style=\" color:#aaaaaa;\">■■ </span><span style=\" color:#000000;\">Умеренный пароль</span></p></body></html>")
        mainWindow.pass_edit.ui.ok.setEnabled(False)
    elif re.fullmatch(pwd, string):
        mainWindow.pass_edit.ui.text_strength.setText("<html><head/><body><p><span style=\" color:#ff0000;\">■■</span><span style=\" color:#aaaaaa;\">■■■■ </span><span style=\" color:#000000;\">Слабый пароль</span></p></body></html>")
        mainWindow.pass_edit.ui.ok.setEnabled(False)
    elif len(string) > 0:
        mainWindow.pass_edit.ui.text_strength.setText("<html><head/><body><p><span style=\" color:#ff0000;\">■■■■■■ </span><span style=\" color:#000000;\">Недопустимый пароль</span></p></body></html>")
        mainWindow.pass_edit.ui.ok.setEnabled(False)
    else:
        mainWindow.pass_edit.ui.text_strength.setText("<html><head/><body><p><span style=\" color:#aaaaaa;\">■■■■■■</span></p></body></html>")
        mainWindow.pass_edit.ui.ok.setEnabled(False)


def register():
    surname  = mainWindow.ui.menu04_field_surname.text()
    name     = mainWindow.ui.menu04_field_name.text()
    patronym = mainWindow.ui.menu04_field_patronym.text()
    phone    = mainWindow.ui.menu04_field_phone.text()
    email    = mainWindow.ui.menu04_field_email.text()
    login    = mainWindow.ui.menu04_field_login.text()
    password = mainWindow.ui.menu04_field_password.text()

    dialog = QMessageBox

    name_regular  = r"^([А-ЯЁ]{1}[а-яё]+|[A-Z]{1}[a-z]+|[А-ЯЁ]{1}[а-яё]+\-[А-ЯЁ]{1}[а-яё]+|[A-Z]{1}[a-z]+\-[A-Z]{1}[a-z]+)$"
    phone_regular = r"^(\+7)[\- ]?\(?(\d{3})\)?[\- ]?(\d{3})[\- ]?(\d{2})[\- ]?(\d{2})$"
    email_regular = r"^([a-zA-Z0-9_\+-]+(?:\.[a-zA-Z0-9_\+-]+)*@[a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)+)$"
    login_regular = r"[\w\-_=.,$!%*?&]{3,}"
    pass_regular  = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d_\-\.@$!%*?&]{8,}$"

    if not re.fullmatch(name_regular, surname):
        if len(surname) > 0:
            message = "Фамилия введена неверно. Пожалуйста, укажите настоящую фамилию.\n\nФИО должны начинаться с большой буквы и не должны содержать никаких символов, кроме букв и, возможно, дефиса."
        else:
            message = "Поле \"Фамилия\" является обязательным."
        dialog.warning(mainWindow, "Некорректные данные", message)
        return
    if not re.fullmatch(name_regular, name):
        if len(name) > 0:
            message = "Имя введено неверно. Пожалуйста, укажите настоящее имя.\n\nФИО должны начинаться с большой буквы и не должны содержать никаких символов, кроме букв и, возможно, дефиса."
        else:
            message = "Поле \"Имя\" является обязательным."
        dialog.warning(mainWindow, "Некорректные данные", message)
        return
    if not re.fullmatch(name_regular, patronym) and len(patronym) > 0:
        message = "Отчество введено неверно. Пожалуйста, укажите настоящее отчество или оставьте поле пустым.\n\nФИО должны начинаться с большой буквы и не должны содержать никаких символов, кроме букв и, возможно, дефиса."
        dialog.warning(mainWindow, "Некорректные данные", message)
        return
    if not re.fullmatch(phone_regular, phone):
        if len(phone) > 0:
            message = "Телефон введён неверно. Номер телефона должен начинаться с +7 и иметь ещё 10 цифр. Например, +79876543210 или +7-(987)-654-32-10."
        else:
            message = "Поле \"Номер телефона\" является обязательным."
        dialog.warning(mainWindow, "Некорректные данные", message)
        return
    if not re.fullmatch(email_regular, email):
        if len(email) > 0:
            message = "Введён недействительный адрес электронной почты. Пожалуйста, укажите настоящий адрес."
        else:
            message = "Поле \"E-mail\" является обязательным."
        dialog.warning(mainWindow, "Некорректные данные", message)
        return
    if not re.fullmatch(login_regular, login):
        if len(login) > 0:
            message = "Логин должен состоять как минимум из 3 символов и может включать в себя только заглавные и строчные буквы русского и английского алфавита, цифры, а также следующие символы: _ - = . , $ ! % * ? &"
        else:
            message = "Поле \"Логин\" является обязательным."
        dialog.warning(mainWindow, "Некорректные данные", message)
        return
    if not re.fullmatch(pass_regular, password):
        if len(password) > 0:
            if (re.fullmatch(r"^[A-Za-z\d_\-\.@$!%*?&]+$", password)):
                message = "Слишком простой пароль.\n\nПароль должен быть длины 8 или более символов,\nа также содержать строчные и заглавные латинские буквы, цифры и хотя бы один из следующих символов:\n@ $ ! % * ? &"
            else:
                message = "Пароль содержит недопустимые символы.\n\nПароль должен быть длины 8 или более символов,\nа также содержать строчные и заглавные латинские буквы, цифры и хотя бы один из следующих символов:\n@ $ ! % * ? &"
        else:
            message = "Поле \"Пароль\" является обязательным."
        dialog.warning(mainWindow, "Некорректные данные", message)
        return

    for record in data.db["users"]:
        if email == record["e-mail"]:
            dialog.warning(mainWindow, "Не удалось завершить регистрацию", "Пользователь с данным E-mail адресом уже зарегистрирован.")
            return
        if login == record["login"]:
            dialog.warning(mainWindow, "Не удалось завершить регистрацию", f"Логин \"{login}\" занят. Придумайте другой логин.")
            return
    
    pass_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    
    number = re.fullmatch(phone_regular, phone)
    phone = number.group(1) + "-(" + number.group(2) + ")-" + number.group(3) + "-" + number.group(4) + "-" + number.group(5)

    data.saved = False
    data.db["last_id"] += 1
    data.db["users"].append({"id": data.db["last_id"],
                             "surname": surname,
                             "name": name,
                             "patronym": patronym,
                             "phone": phone,
                             "e-mail": email,
                             "login": login,
                             "password": pass_hash})

    mainWindow.ui.menu07_label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Завершение регистрации</span></p></body></html>")
    mainWindow.ui.menu07_message.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">✅</span></p><p align=\"center\"><span style=\" font-size:16pt;\">Пользователь успешно зарегистрирован</span></p></body></html>")
    mainWindow.ui.menu07_button_add.setText("Добавить ещё одного пользователя")
    mainWindow.ui.menu07_button_add.clicked.connect(add_user)
    mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu07_page_success)


def ask_for_password(user_string, user_index):
    global search_action

    mainWindow.ui.menu09_field_password.clear()
    
    try: mainWindow.ui.menu09_button_continue.clicked.disconnect()
    except TypeError: pass
    mainWindow.ui.menu09_button_continue.clicked.connect(lambda: check_password(user_string, user_index))
    
    try: mainWindow.ui.menu09_button_cancel.clicked.disconnect()
    except TypeError: pass
    if search_action == 1:
        mainWindow.ui.menu09_label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Удаление пользователя</span></p></body></html>")
        mainWindow.ui.menu09_button_cancel.clicked.connect(delete_user)
    elif search_action == 2:
        mainWindow.ui.menu09_label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Редактирование пользователя</span></p></body></html>")
        mainWindow.ui.menu09_button_cancel.clicked.connect(edit_user)
    
    mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu09_page_check_password)


def check_password(user_string, user_index):
    global search_action

    pwd_input = mainWindow.ui.menu09_field_password.text()
    if hashlib.sha256(pwd_input.encode("utf-8")).hexdigest() == data.db["users"][user_index]["password"]:
        if search_action == 1:
            dialog = QMessageBox()
            dialog.setWindowTitle("Подтверждение")
            dialog.setText(f"Вы действительно хотите удалить пользователя {user_string}?\n\nЭто действие отменить невозможно.")
            dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dialog.button(QMessageBox.Yes).setText('Да')
            dialog.button(QMessageBox.No).setText('Нет')
            dialog.setDefaultButton(QMessageBox.Yes)
            dialog.setIcon(QMessageBox.Question)
            act_delete = dialog.exec()
            if act_delete == QMessageBox.Yes:
                action_delete(user_string, user_index)
            dialog.deleteLater()
        elif search_action == 2:
            edit_screen_show(user_index)
    else:
        QMessageBox.warning(mainWindow, "Неверный пароль", "Введён неверный пароль. Попробуйте ещё раз.")
        mainWindow.ui.menu09_field_password.clear()


def delete_user():
    global search_criteria, search_action

    search_action = 1

    mainWindow.ui.menu05_stackedWidget_input.setCurrentIndex(1)
    mainWindow.ui.menu05_stackedWidget_results.setCurrentIndex(0)
    mainWindow.ui.menu05_label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Удаление пользователя</span></p></body></html>")
    mainWindow.ui.menu05_label_top.setText("Выбор пользователя для удаления:")
    mainWindow.ui.menu05_label_not_found.setText("Чтобы начать поиск, нажмите на кнопку выше.")

    mainWindow.ui.menu05_back.setText("◀  Главное меню")
    mainWindow.ui.menu05_back.clicked.disconnect()
    mainWindow.ui.menu05_back.clicked.connect(back_to_main_menu)

    if search_criteria == 1:
        mainWindow.ui.menu05_search_by_name.setChecked(True)
    elif search_criteria == 2:
        mainWindow.ui.menu05_search_by_login.setChecked(True)
    else:
        mainWindow.ui.menu05_search_by_phone.setChecked(True)
    
    search_criteria_change(search_criteria)

    mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu05_page_select_user)


def action_delete(user_string, user_index):
    del data.db["users"][user_index]
    data.saved = False
    mainWindow.ui.menu07_label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Удаление пользователя</span></p></body></html>")
    mainWindow.ui.menu07_message.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">✅</span></p><p align=\"center\"><span style=\" font-size:16pt;\">Пользователь удалён</span></p></body></html>")
    mainWindow.ui.menu07_button_add.setText("Удалить ещё одного пользователя")
    mainWindow.ui.menu07_button_add.clicked.connect(delete_user)
    mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu07_page_success)


def edit_user():
    global search_criteria, search_action

    search_action = 2

    mainWindow.ui.menu05_stackedWidget_input.setCurrentIndex(1)
    mainWindow.ui.menu05_stackedWidget_results.setCurrentIndex(0)
    mainWindow.ui.menu05_label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Редактирование пользователя</span></p></body></html>")
    mainWindow.ui.menu05_label_top.setText("Выбор пользователя для изменения:")
    mainWindow.ui.menu05_label_not_found.setText("Чтобы начать поиск, нажмите на кнопку выше.")

    mainWindow.ui.menu05_back.setText("◀  Главное меню")
    mainWindow.ui.menu05_back.clicked.disconnect()
    mainWindow.ui.menu05_back.clicked.connect(back_to_main_menu)

    if search_criteria == 1:
        mainWindow.ui.menu05_search_by_name.setChecked(True)
    elif search_criteria == 2:
        mainWindow.ui.menu05_search_by_login.setChecked(True)
    else:
        mainWindow.ui.menu05_search_by_phone.setChecked(True)
    
    search_criteria_change(search_criteria)

    mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu05_page_select_user)


def edit_screen_show(user_index):
    userdata = data.db["users"][user_index]
    edited_pass_hash = ""
    mainWindow.ui.menu08_field_surname.setText(userdata["surname"])
    mainWindow.ui.menu08_field_name.setText(userdata["name"])
    mainWindow.ui.menu08_field_patronym.setText(userdata["patronym"])
    mainWindow.ui.menu08_field_phone.setText(userdata["phone"])
    mainWindow.ui.menu08_field_email.setText(userdata["e-mail"])
    mainWindow.ui.menu08_field_login.setText(userdata["login"])

    try: mainWindow.ui.menu08_button_continue.clicked.disconnect()
    except TypeError: pass
    mainWindow.ui.menu08_button_continue.clicked.connect(lambda: action_edit(user_index))

    mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu08_page_edit)


def edit_pass_window():
    mainWindow.pass_edit = QWidget()
    mainWindow.pass_edit.setWindowModality(Qt.ApplicationModal)
    mainWindow.pass_edit.ui = Ui_PasswordEditPrompt()
    mainWindow.pass_edit.ui.setupUi(mainWindow.pass_edit)
    mainWindow.pass_edit.ui.cancel.clicked.connect(lambda: (mainWindow.pass_edit.close(), mainWindow.pass_edit.deleteLater()))
    mainWindow.pass_edit.ui.ok.clicked.connect(edit_pass)
    mainWindow.pass_edit.ui.field_password.textChanged.connect(show_pass_strength_edit)
    mainWindow.pass_edit.ui.toggle_visible.clicked.connect(lambda: toggle_pass_visible(mainWindow.pass_edit.ui.field_password))
    mainWindow.ui.menu04_field_password.setEchoMode(QLineEdit.Password)
    mainWindow.pass_edit.show()


def edit_pass():
    global edited_pass_hash
    password = mainWindow.pass_edit.ui.field_password.text()
    edited_pass_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    mainWindow.pass_edit.close()
    mainWindow.pass_edit.deleteLater()


def action_edit(user_index):
    global edited_pass_hash

    surname  = mainWindow.ui.menu08_field_surname.text()
    name     = mainWindow.ui.menu08_field_name.text()
    patronym = mainWindow.ui.menu08_field_patronym.text()
    phone    = mainWindow.ui.menu08_field_phone.text()
    email    = mainWindow.ui.menu08_field_email.text()
    login    = mainWindow.ui.menu08_field_login.text()

    dialog = QMessageBox

    if data.db["users"][user_index]["surname"] == surname and \
    data.db["users"][user_index]["name"] == name and \
    data.db["users"][user_index]["patronym"] == patronym and \
    data.db["users"][user_index]["phone"] == phone and \
    data.db["users"][user_index]["e-mail"] == email and \
    data.db["users"][user_index]["login"] == login and \
    (not edited_pass_hash or data.db["users"][user_index]["password"] == edited_pass_hash):
        dialog.information(mainWindow, "Информация", "Данные не были изменены.")
        return

    name_regular  = r"^([А-ЯЁ]{1}[а-яё]+|[A-Z]{1}[a-z]+|[А-ЯЁ]{1}[а-яё]+\-[А-ЯЁ]{1}[а-яё]+|[A-Z]{1}[a-z]+\-[A-Z]{1}[a-z]+)$"
    phone_regular = r"^(\+7)[\- ]?\(?(\d{3})\)?[\- ]?(\d{3})[\- ]?(\d{2})[\- ]?(\d{2})$"
    email_regular = r"^([a-zA-Z0-9_\+-]+(?:\.[a-zA-Z0-9_\+-]+)*@[a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)+)$"
    login_regular = r"[\w\-_=.,$!%*?&]{3,}"

    if not re.fullmatch(name_regular, surname):
        if len(surname) > 0:
            message = "Фамилия введена неверно. Пожалуйста, укажите настоящую фамилию.\n\nФИО должны начинаться с большой буквы и не должны содержать никаких символов, кроме букв и, возможно, дефиса."
        else:
            message = "Поле \"Фамилия\" является обязательным."
        dialog.warning(mainWindow, "Некорректные данные", message)
        return
    if not re.fullmatch(name_regular, name):
        if len(name) > 0:
            message = "Имя введено неверно. Пожалуйста, укажите настоящее имя.\n\nФИО должны начинаться с большой буквы и не должны содержать никаких символов, кроме букв и, возможно, дефиса."
        else:
            message = "Поле \"Имя\" является обязательным."
        dialog.warning(mainWindow, "Некорректные данные", message)
        return
    if not re.fullmatch(name_regular, patronym) and len(patronym) > 0:
        message = "Отчество введено неверно. Пожалуйста, укажите настоящее отчество или оставьте поле пустым.\n\nФИО должны начинаться с большой буквы и не должны содержать никаких символов, кроме букв и, возможно, дефиса."
        dialog.warning(mainWindow, "Некорректные данные", message)
        return
    if not re.fullmatch(phone_regular, phone):
        if len(phone) > 0:
            message = "Телефон введён неверно. Номер телефона должен начинаться с +7 и иметь ещё 10 цифр. Например, +79876543210 или +7-(987)-654-32-10."
        else:
            message = "Поле \"Номер телефона\" является обязательным."
        dialog.warning(mainWindow, "Некорректные данные", message)
        return
    if not re.fullmatch(email_regular, email):
        if len(email) > 0:
            message = "Введён недействительный адрес электронной почты. Пожалуйста, укажите настоящий адрес."
        else:
            message = "Поле \"E-mail\" является обязательным."
        dialog.warning(mainWindow, "Некорректные данные", message)
        return
    if not re.fullmatch(login_regular, login):
        if len(login) > 0:
            message = "Логин должен состоять как минимум из 3 символов и может включать в себя только заглавные и строчные буквы русского и английского алфавита, цифры, а также следующие символы: _ - = . , $ ! % * ? &"
        else:
            message = "Поле \"Логин\" является обязательным."
        dialog.warning(mainWindow, "Некорректные данные", message)
        return

    for record in enumerate(data.db["users"]):
        if email == record[1]["e-mail"] and user_index != record[0]:
            dialog.warning(mainWindow, "Не удалось изменить данные", "Пользователь с данным E-mail адресом уже зарегистрирован.")
            return
        if login == record[1]["login"] and user_index != record[0]:
            dialog.warning(mainWindow, "Не удалось изменить данные", f"Логин \"{login}\" занят. Придумайте другой логин.")
            return
    
    pass_hash = edited_pass_hash
    
    number = re.fullmatch(phone_regular, phone)
    phone = number.group(1) + "-(" + number.group(2) + ")-" + number.group(3) + "-" + number.group(4) + "-" + number.group(5)

    data.saved = False
    data.db["users"][user_index]["surname"] = surname
    data.db["users"][user_index]["name"] = name
    data.db["users"][user_index]["patronym"] = patronym
    data.db["users"][user_index]["phone"] = phone
    data.db["users"][user_index]["e-mail"] = email
    data.db["users"][user_index]["login"] = login
    if pass_hash:
        data.db["users"][user_index]["password"] = pass_hash

    mainWindow.ui.menu07_label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Редактирование пользователя</span></p></body></html>")
    mainWindow.ui.menu07_message.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">✅</span></p><p align=\"center\"><span style=\" font-size:16pt;\">Данные успешно обновлены</span></p></body></html>")
    mainWindow.ui.menu07_button_add.setText("Изменить ещё одного пользователя")
    mainWindow.ui.menu07_button_add.clicked.connect(edit_user)
    mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu07_page_success)


def search_criteria_change(criteria):
    global search_criteria
    search_criteria = criteria
    mainWindow.ui.menu05_one_field_edit.clear()
    mainWindow.ui.menu05_two_fields_edit_1.clear()
    mainWindow.ui.menu05_two_fields_edit_2.clear()
    if criteria == 2:
        mainWindow.ui.menu05_one_field_label.setText("Логин")
    elif criteria == 3:
        mainWindow.ui.menu05_one_field_label.setText("Номер телефона")
    mainWindow.ui.menu05_stackedWidget_input.setCurrentIndex(1 if criteria == 1 else 0)


def search_query_changed():
    mainWindow.ui.menu05_label_not_found.setText("Чтобы начать поиск, нажмите на кнопку выше.")
    mainWindow.ui.menu05_label_not_found.setStyleSheet("")
    mainWindow.ui.menu05_stackedWidget_results.setCurrentIndex(0)
    mainWindow.ui.menu05_user_list.clear()


def search():
    global search_criteria, search_action
    found_users = []

    mainWindow.ui.menu05_user_list.clear()

    if search_criteria == 1:
        surname = mainWindow.ui.menu05_two_fields_edit_1.text()
        name = mainWindow.ui.menu05_two_fields_edit_2.text()
        if ((not surname) and (not name)):
            QMessageBox.information(mainWindow, "Ошибка", "Критерий поиска не может быть пустым.\n\nВведите имя, или фамилию, или и то, и другое.")
            return

        for user in enumerate(data.db["users"]):
            if (user[1]["surname"] == surname or not surname) and (user[1]["name"] == name or not name):
                found_users.append((user[1]["login"] + " (" + user[1]["e-mail"] + ")", user[0]))

    elif search_criteria == 2:
        login = mainWindow.ui.menu05_one_field_edit.text()
        if (not login):
            QMessageBox.information(mainWindow, "Ошибка", "Критерий поиска не может быть пустым.\n\nВведите логин.")
            return

        for user in enumerate(data.db["users"]):
            if user[1]["login"] == login:
                found_users.append((user[1]["login"] + " (" + user[1]["e-mail"] + ")", user[0]))
        
    elif search_criteria == 3:
        phone = mainWindow.ui.menu05_one_field_edit.text()

        if (not phone):
            QMessageBox.information(mainWindow, "Ошибка", "Критерий поиска не может быть пустым.\n\nВведите номер телефона.")
            return
        
        phone_regular = r"^(\+7)[\- ]?\(?(\d{3})\)?[\- ]?(\d{3})[\- ]?(\d{2})[\- ]?(\d{2})$"
        number = re.fullmatch(phone_regular, phone)
        if not number:
            message = "Телефон введён неверно. Номер телефона должен начинаться с +7 и иметь ещё 10 цифр. Например, +79876543210 или +7-(987)-654-32-10."
            QMessageBox.warning(mainWindow, "Некорректные данные", message)
            return
        phone = number.group(1) + "-(" + number.group(2) + ")-" + number.group(3) + "-" + number.group(4) + "-" + number.group(5)


        for user in enumerate(data.db["users"]):
            if user[1]["phone"] == phone:
                found_users.append((user[1]["login"] + " (" + user[1]["e-mail"] + ")", user[0]))

    if (found_users):
        list_items = [user[0] for user in found_users]
        mainWindow.ui.menu05_user_list.addItems(list_items)
        mainWindow.ui.menu05_user_list.setCurrentRow(0)
        mainWindow.ui.menu05_label_found.setText(f"Пользователей найдено: {len(list_items)}\nВыберите пользователя, чтобы продолжить:")
        try: mainWindow.ui.menu05_button_action.clicked.disconnect()
        except TypeError: pass
        if search_action == 1:
            mainWindow.ui.menu05_button_action.setText("Удалить")
            mainWindow.ui.menu05_button_action.clicked.connect(lambda: ask_for_password(found_users[mainWindow.ui.menu05_user_list.currentRow()][0], found_users[mainWindow.ui.menu05_user_list.currentRow()][1]))
        elif search_action == 2:
            mainWindow.ui.menu05_button_action.setText("Изменить")
            mainWindow.ui.menu05_button_action.clicked.connect(lambda: ask_for_password(found_users[mainWindow.ui.menu05_user_list.currentRow()][0], found_users[mainWindow.ui.menu05_user_list.currentRow()][1]))
        elif search_action == 3:
            mainWindow.ui.menu05_button_action.setText("Выбрать")
            mainWindow.ui.menu05_button_action.clicked.connect(lambda: set_recipient(found_users[mainWindow.ui.menu05_user_list.currentRow()][1]))

        mainWindow.ui.menu05_stackedWidget_results.setCurrentIndex(1)
        mainWindow.ui.menu05_user_list.setFocus()
    else:
        mainWindow.ui.menu05_label_not_found.setText("Нет пользователей, удовлетворяющих условиям поиска.")
        mainWindow.ui.menu05_label_not_found.setStyleSheet("color: rgb(170, 0, 0);")
        mainWindow.ui.menu05_stackedWidget_results.setCurrentIndex(0)


def write_email():
    mainWindow.ui.menu06_recipient_field.clear()
    mainWindow.ui.menu06_subject_field.clear()
    mainWindow.ui.menu06_text_field.clear()
    mainWindow.ui.menu06_subject_length.setText("0 / 100")

    mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu06_page_send_email)


def select_user_button():
    global search_criteria, search_action

    search_action = 3

    mainWindow.ui.menu05_stackedWidget_input.setCurrentIndex(1)
    mainWindow.ui.menu05_stackedWidget_results.setCurrentIndex(0)
    mainWindow.ui.menu05_label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Выбор получателя</span></p></body></html>")
    mainWindow.ui.menu05_label_top.setText("Выбор пользователя:")
    mainWindow.ui.menu05_label_not_found.setText("Чтобы начать поиск, нажмите на кнопку выше.")

    mainWindow.ui.menu05_back.setText("◀  Назад")
    mainWindow.ui.menu05_back.clicked.disconnect()
    mainWindow.ui.menu05_back.clicked.connect(lambda: mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu06_page_send_email))


    if search_criteria == 1:
        mainWindow.ui.menu05_search_by_name.setChecked(True)
    elif search_criteria == 2:
        mainWindow.ui.menu05_search_by_login.setChecked(True)
    else:
        mainWindow.ui.menu05_search_by_phone.setChecked(True)
    
    search_criteria_change(search_criteria)

    mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu05_page_select_user)


def set_recipient(user_index):
    mainWindow.ui.menu06_recipient_field.setText(data.db["users"][user_index]["e-mail"])
    mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu06_page_send_email)


def subject_changed():
    mainWindow.ui.menu06_subject_length.setText(f"{len(mainWindow.ui.menu06_subject_field.text())} / 100")


def cancel_email():
    if mainWindow.ui.menu06_subject_field.text() or mainWindow.ui.menu06_text_field.toPlainText():
        back_to_main_menu(confirmation="Отменить написание письма и вернуться в главное меню?\n\nТема и текст письма не будут сохранены.", title="Подтверждение")
    else:
        back_to_main_menu()


def clear_email():
    if mainWindow.ui.menu06_subject_field.text() or mainWindow.ui.menu06_text_field.toPlainText():
        dialog = QMessageBox()
        dialog.setWindowTitle("Подтверждение")
        dialog.setText("Вы действительно хотите очистить тему и текст письма?")
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.button(QMessageBox.Yes).setText('Да')
        dialog.button(QMessageBox.No).setText('Нет')
        dialog.setDefaultButton(QMessageBox.Yes)
        dialog.setIcon(QMessageBox.Question)
        action = dialog.exec()

        if action == QMessageBox.Yes:
            mainWindow.ui.menu06_subject_field.clear()
            mainWindow.ui.menu06_text_field.clear()


def send():
    subject = mainWindow.ui.menu06_subject_field.text()
    if not subject:
        subject = "(Без темы)"
    text = mainWindow.ui.menu06_text_field.toPlainText()

    email = mainWindow.ui.menu06_recipient_field.text()
    email_regular = r"^([a-zA-Z0-9_\+-]+(?:\.[a-zA-Z0-9_\+-]+)*@[a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)+)$"

    if not re.fullmatch(email_regular, email):
        if len(email) > 0:
            message = "Введён недействительный адрес электронной почты получателя. Пожалуйста, укажите настоящий адрес."
        else:
            message = "Вы не ввели адрес получателя."
        QMessageBox.warning(mainWindow, "Не удалось отправить E-mail", message)
        return
    
    if not text:
        message = "Невозможно отправить пустое письмо."
        QMessageBox.warning(mainWindow, "Не удалось отправить E-mail", message)
        return

    path = os.path.join(os.getcwd(), "Почта", email)
    os.makedirs(path, exist_ok=True)

    time = datetime.now()
    filename = "inbox_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
    
    content = f"Входящее письмо\n\nДата:       {time.strftime('%d.%m.%Y')}\nВремя:      {time.strftime('%H:%M:%S')}\nПолучатель: {email}\nТема:       {subject}\n\n\n================== Начало письма =================\n{text}\n================== Конец письма =================="

    spinner = QMovie(":/gif/Spinner-1s-500px.gif")
    spinner.setScaledSize(QSize(100, 100))
    mainWindow.ui.menu10_spinner.setMovie(spinner)
    spinner.start()
    mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu10_page_sending)

    loop = QEventLoop()
    QTimer.singleShot(1234, loop.quit)
    loop.exec()

    try:
        open(os.path.join(path, filename), "w", encoding="utf-8").write(content)
    except Exception as e:
        spinner.stop()
        mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu06_page_send_email)
        QMessageBox.critical(mainWindow, "E-mail ", "Письмо не было доставлено.\n\nИнформация об ошибке: " + str(e))
        return
        
    mainWindow.ui.menu07_label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Отправка письма</span></p></body></html>")
    mainWindow.ui.menu07_message.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">✅</span></p><p align=\"center\"><span style=\" font-size:16pt;\">Письмо отправлено</span></p>" \
        + "<p align=\"center\"><span style=\" font-size:9pt;\">Подсказка: отправленные письма попадают в папку получателя.</span><br><br>" \
        + "<span style=\" font-size:9pt;\">Данное письмо находится по адресу<br>" + os.path.join(path, filename) + "</span></p></body></html>")
    mainWindow.ui.menu07_button_add.setText("Отправить ещё одно письмо")
    mainWindow.ui.menu07_button_add.clicked.connect(write_email)
    spinner.stop()
    mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu07_page_success)


def sort_ui():
    mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu11_page_sort)


def do_sorting():
    reverse = mainWindow.ui.menu11_group1_button2.isChecked()

    if   mainWindow.ui.menu11_group2_button1.isChecked(): field = "id"
    elif mainWindow.ui.menu11_group2_button2.isChecked(): field = "surname"
    elif mainWindow.ui.menu11_group2_button3.isChecked(): field = "name"
    elif mainWindow.ui.menu11_group2_button4.isChecked(): field = "patronym"
    elif mainWindow.ui.menu11_group2_button5.isChecked(): field = "phone"
    elif mainWindow.ui.menu11_group2_button6.isChecked(): field = "e-mail"
    else                                                : field = "login"

    data.db["users"].sort(reverse=reverse, key=lambda record: record[field])
    data.saved = False

    mainWindow.ui.menu07_label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Сортировка таблицы пользователей</span></p></body></html>")
    mainWindow.ui.menu07_message.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">✅</span></p><p align=\"center\"><span style=\" font-size:16pt;\">Записи о пользователях отсортированы</span></p></body></html>")
    mainWindow.ui.menu07_button_add.setText("Посмотреть")
    mainWindow.ui.menu07_button_add.clicked.connect(view)
    mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu07_page_success)


def back_to_main_menu(event=None, confirmation="", title="Регистрация не завершена"):
    if (confirmation):
        dialog = QMessageBox()
        dialog.setWindowTitle(title)
        dialog.setText(confirmation)
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.button(QMessageBox.Yes).setText('Да')
        dialog.button(QMessageBox.No).setText('Нет')
        dialog.setDefaultButton(QMessageBox.Yes)
        dialog.setIcon(QMessageBox.Question)
        action = dialog.exec()

        if action != QMessageBox.Yes: return
    
    mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu02_page_main)
    if data.saved:
        mainWindow.ui.menu02_button_5.setStyleSheet("")
    else:
        mainWindow.ui.menu02_button_5.setStyleSheet("font-weight: bold; color: rgb(0, 128, 0);")


def save(event=None, confirmation=True):
    dialog = QMessageBox
    try:
        json.dump(data.db, open(data.path, "w", encoding="utf-8"), ensure_ascii=False, indent=4)
        data.saved = True
        mainWindow.ui.menu02_button_5.setStyleSheet("")
        if confirmation:
            dialog.information(mainWindow, "Сохранение", f"Файл {data.path} сохранён.")
        return 1
    except:
        dialog.critical(mainWindow, "Ошибка", "Не удалось сохранить базу данных.")
        return 0


def check_unsaved():
    if data.opened == True and data.saved == False:
        dialog = QMessageBox()
        dialog.setWindowTitle("Подтверждение")
        dialog.setText("Вы хотите сохранить изменения в файл?")
        dialog.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        dialog.button(QMessageBox.Save).setText('Сохранить')
        dialog.button(QMessageBox.Discard).setText('Не сохранять')
        dialog.button(QMessageBox.Cancel).setText('Отмена')
        dialog.setDefaultButton(QMessageBox.Save)
        dialog.setIcon(QMessageBox.Question)
        action = dialog.exec()

        if action == QMessageBox.Save:
            return save(confirmation=False)
        elif action == QMessageBox.Discard:
            return 1
        else:
            return 0
    else:
        return 1


def logout():
    if check_unsaved() == 1:
        data.opened = False
        data.saved = False
        mainWindow.ui.menu02_button_5.setStyleSheet("")
        data.path = ""
        data.db = {}
        mainWindow.ui.stackedWidget.setCurrentWidget(mainWindow.ui.menu01_page_welcome)
        mainWindow.ui.menu01_label.setText(mainWindow.ui.menu01_label.text().replace("Добро пожаловать", "Вы вышли из системы.", 1).replace("в систему авторизации AuthMe!", "", 1))


if __name__ == "__main__":
    print("Загрузка...")

    # Global variables
    search_criteria = 1
    search_action = 1 # 1 = Delete, 2 = Edit, 3 = Send
    edited_pass_hash = ""
    
    
    app = QApplication(sys.argv)
    data = Data()
    mainWindow = MainWindow()
    mainWindow.show()

    os.system("cls")
    print("Окно программы запущено.")
    sys.exit(app.exec_())