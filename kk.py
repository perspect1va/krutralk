import sys
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class EngineeringCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_input = "0"
        self.previous_input = ""
        self.operation = ""
        self.result = 0
        self.waiting_for_operand = True
        self.degree_mode = True
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Инженерный калькулятор")
        self.setFixedSize(500, 650)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(30)
        font = self.display.font()
        font.setPointSize(24)
        self.display.setFont(font)
        self.display.setStyleSheet("""
            QLineEdit {
                border: 2px solid #4CAF50;
                border-radius: 5px;
                padding: 10px;
                background-color: #f0f0f0;
                color: #000;
            }
        """)
        main_layout.addWidget(self.display)
        
        buttons_layout = QGridLayout()
        
        # Определение кнопок
        buttons = [
            # Ряд 0
            ('Deg', 0, 0), ('Rad', 0, 1), ('sin', 0, 2), ('cos', 0, 3), ('tan', 0, 4),
            # Ряд 1
            ('π', 1, 0), ('e', 1, 1), ('x²', 1, 2), ('x³', 1, 3), ('√', 1, 4),
            # Ряд 2
            ('log', 2, 0), ('ln', 2, 1), ('x!', 2, 2), ('(', 2, 3), (')', 2, 4),
            # Ряд 3
            ('C', 3, 0), ('CE', 3, 1), ('⌫', 3, 2), ('÷', 3, 3), ('×', 3, 4),
            # Ряд 4
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('-', 4, 3), ('^', 4, 4),
            # Ряд 5
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('+', 5, 3), ('1/x', 5, 4),
            # Ряд 6
            ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('=', 6, 3, 2, 1),  # занимает 2 строки
            # Ряд 7
            ('±', 7, 0), ('0', 7, 1), ('.', 7, 2)
        ]
        
        # Создание кнопок
        for button in buttons:
            text = button[0]
            row = button[1]
            col = button[2]
            
            if len(button) == 5:  # Кнопка занимает несколько строк
                btn = QPushButton(text)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn.setMinimumHeight(60)
                buttons_layout.addWidget(btn, row, col, button[3], button[4])
            else:
                btn = QPushButton(text)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn.setMinimumHeight(50)
                buttons_layout.addWidget(btn, row, col)
            
            # Настройка стилей в зависимости от типа кнопки
            if text in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '±'):
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #e0e0e0;
                        border: 1px solid #888;
                        border-radius: 3px;
                        font-size: 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #d0d0d0;
                    }
                    QPushButton:pressed {
                        background-color: #c0c0c0;
                    }
                """)
            elif text in ('+', '-', '×', '÷', '=', '^'):
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #ff9500;
                        color: white;
                        border: 1px solid #888;
                        border-radius: 3px;
                        font-size: 18px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #e08500;
                    }
                    QPushButton:pressed {
                        background-color: #c07500;
                    }
                """)
            elif text in ('C', 'CE', '⌫'):
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #ff3b30;
                        color: white;
                        border: 1px solid #888;
                        border-radius: 3px;
                        font-size: 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #e02b20;
                    }
                    QPushButton:pressed {
                        background-color: #c01b10;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #5ac8fa;
                        border: 1px solid #888;
                        border-radius: 3px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #4ab8ea;
                    }
                    QPushButton:pressed {
                        background-color: #3aa8da;
                    }
                """)
            
            btn.clicked.connect(self.button_clicked)
        
        main_layout.addLayout(buttons_layout)
        
        # Статус бар для режима углов
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_angle_mode()
    
    def update_angle_mode(self):
        mode = "DEG" if self.degree_mode else "RAD"
        self.status_bar.showMessage(f"Режим углов: {mode}")
    
    def button_clicked(self):
        button = self.sender()
        text = button.text()
        
        if text in '0123456789':
            self.digit_clicked(text)
        elif text == '.':
            self.point_clicked()
        elif text in ('+', '-', '×', '÷', '^'):
            self.operator_clicked(text)
        elif text == '=':
            self.equals_clicked()
        elif text == 'C':
            self.clear_all()
        elif text == 'CE':
            self.clear_entry()
        elif text == '⌫':
            self.backspace()
        elif text == '±':
            self.negate()
        elif text == '1/x':
            self.reciprocal()
        elif text == '√':
            self.square_root()
        elif text == 'x²':
            self.square()
        elif text == 'x³':
            self.cube()
        elif text in ('sin', 'cos', 'tan'):
            self.trig_function(text)
        elif text == 'π':
            self.pi()
        elif text == 'e':
            self.euler()
        elif text == 'log':
            self.log10()
        elif text == 'ln':
            self.ln()
        elif text == 'x!':
            self.factorial()
        elif text in ('(', ')'):
            self.parenthesis(text)
        elif text in ('Deg', 'Rad'):
            self.switch_angle_mode(text)
    
    def digit_clicked(self, digit):
        if self.waiting_for_operand:
            self.current_input = digit
            self.waiting_for_operand = False
        else:
            if self.current_input == "0":
                self.current_input = digit
            else:
                self.current_input += digit
        self.display.setText(self.current_input)
    
    def point_clicked(self):
        if self.waiting_for_operand:
            self.current_input = "0."
            self.waiting_for_operand = False
        elif '.' not in self.current_input:
            self.current_input += '.'
        self.display.setText(self.current_input)
    
    def operator_clicked(self, op):
        if self.operation and not self.waiting_for_operand:
            self.calculate()
        
        self.previous_input = self.current_input
        self.waiting_for_operand = True
        
        # Преобразуем символы операций в Python-операции
        if op == '×':
            self.operation = '*'
        elif op == '÷':
            self.operation = '/'
        elif op == '^':
            self.operation = '**'
        else:
            self.operation = op
    
    def equals_clicked(self):
        if self.operation and self.previous_input:
            self.calculate()
            self.operation = ""
        else:
            # Если нет операции, пытаемся вычислить выражение
            try:
                expression = self.current_input.replace('π', str(math.pi)).replace('e', str(math.e))
                # Заменяем математические функции
                expression = expression.replace('sin', 'math.sin')
                expression = expression.replace('cos', 'math.cos')
                expression = expression.replace('tan', 'math.tan')
                expression = expression.replace('log', 'math.log10')
                expression = expression.replace('ln', 'math.log')
                expression = expression.replace('√', 'math.sqrt')
                
                # Вычисляем
                result = eval(expression, {"__builtins__": None}, 
                             {"math": math, "pi": math.pi, "e": math.e})
                
                # Округление
                if isinstance(result, float):
                    if abs(result - round(result, 10)) < 1e-10:
                        result = round(result, 10)
                    # Убираем лишние нули
                    result_str = str(result).rstrip('0').rstrip('.')
                else:
                    result_str = str(result)
                
                self.current_input = result_str
                self.display.setText(self.current_input)
                self.waiting_for_operand = True
                
            except Exception as e:
                print(f"Ошибка: {e}")
                self.display.setText("Error")
                self.current_input = "0"
                self.waiting_for_operand = True
    
    def calculate(self):
        try:
            # Подготовка выражений
            expr1 = self.previous_input.replace('π', str(math.pi)).replace('e', str(math.e))
            expr2 = self.current_input.replace('π', str(math.pi)).replace('e', str(math.e))
            
            # Вычисление
            expression = f"{expr1} {self.operation} {expr2}"
            result = eval(expression, {"__builtins__": None}, 
                         {"math": math, "pi": math.pi, "e": math.e})
            
            # Округление
            if isinstance(result, float):
                if abs(result - round(result, 10)) < 1e-10:
                    result = round(result, 10)
                # Убираем лишние нули
                result_str = str(result).rstrip('0').rstrip('.')
            else:
                result_str = str(result)
            
            self.current_input = result_str
            self.display.setText(self.current_input)
            self.waiting_for_operand = True
            
        except Exception as e:
            print(f"Ошибка вычисления: {e}")
            self.display.setText("Error")
            self.current_input = "0"
            self.waiting_for_operand = True
    
    def clear_all(self):
        self.current_input = "0"
        self.previous_input = ""
        self.operation = ""
        self.display.setText(self.current_input)
        self.waiting_for_operand = True
    
    def clear_entry(self):
        self.current_input = "0"
        self.display.setText(self.current_input)
        self.waiting_for_operand = True
    
    def backspace(self):
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"
        self.display.setText(self.current_input)
    
    def negate(self):
        try:
            value = float(self.current_input)
            value = -value
            
            # Проверка на целое число
            if value.is_integer():
                self.current_input = str(int(value))
            else:
                self.current_input = str(value)
                
            self.display.setText(self.current_input)
        except:
            pass
    
    def reciprocal(self):
        try:
            value = float(self.current_input)
            if value != 0:
                result = 1 / value
                if abs(result - round(result, 10)) < 1e-10:
                    result = round(result, 10)
                # Убираем лишние нули
                result_str = str(result).rstrip('0').rstrip('.')
                self.current_input = result_str
                self.display.setText(self.current_input)
                self.waiting_for_operand = True
            else:
                self.display.setText("Error: Division by zero")
        except Exception as e:
            self.display.setText("Error")
    
    def square_root(self):
        try:
            value = float(self.current_input)
            if value >= 0:
                result = math.sqrt(value)
                if abs(result - round(result, 10)) < 1e-10:
                    result = round(result, 10)
                # Убираем лишние нули
                result_str = str(result).rstrip('0').rstrip('.')
                self.current_input = result_str
                self.display.setText(self.current_input)
                self.waiting_for_operand = True
            else:
                self.display.setText("Error: Negative number")
        except:
            self.display.setText("Error")
    
    def square(self):
        try:
            value = float(self.current_input)
            result = value ** 2
            if abs(result - round(result, 10)) < 1e-10:
                result = round(result, 10)
            # Убираем лишние нули
            result_str = str(result).rstrip('0').rstrip('.')
            self.current_input = result_str
            self.display.setText(self.current_input)
            self.waiting_for_operand = True
        except:
            self.display.setText("Error")
    
    def cube(self):
        try:
            value = float(self.current_input)
            result = value ** 3
            if abs(result - round(result, 10)) < 1e-10:
                result = round(result, 10)
            # Убираем лишние нули
            result_str = str(result).rstrip('0').rstrip('.')
            self.current_input = result_str
            self.display.setText(self.current_input)
            self.waiting_for_operand = True
        except:
            self.display.setText("Error")
    
    def trig_function(self, func):
        try:
            value = float(self.current_input)
            
            # Преобразование в радианы если нужно
            if self.degree_mode:
                value_rad = math.radians(value)
            else:
                value_rad = value
            
            if func == 'sin':
                result = math.sin(value_rad)
            elif func == 'cos':
                result = math.cos(value_rad)
            elif func == 'tan':
                # Проверка на особые случаи для тангенса
                cos_value = math.cos(value_rad)
                if abs(cos_value) < 1e-10:
                    self.display.setText("Error: Undefined")
                    return
                result = math.tan(value_rad)
            
            # Округление для избежания малых ошибок
            if abs(result) < 1e-10:
                result = 0
            
            # Форматирование результата
            if isinstance(result, float):
                if abs(result - round(result, 10)) < 1e-10:
                    result = round(result, 10)
                # Убираем лишние нули
                result_str = str(result).rstrip('0').rstrip('.')
            else:
                result_str = str(result)
            
            self.current_input = result_str
            self.display.setText(self.current_input)
            self.waiting_for_operand = True
        except Exception as e:
            print(f"Ошибка тригонометрии: {e}")
            self.display.setText("Error")
    
    def pi(self):
        if self.waiting_for_operand:
            self.current_input = str(math.pi)
            self.waiting_for_operand = False
        else:
            self.current_input += str(math.pi)
        self.display.setText(self.current_input)
    
    def euler(self):
        if self.waiting_for_operand:
            self.current_input = str(math.e)
            self.waiting_for_operand = False
        else:
            self.current_input += str(math.e)
        self.display.setText(self.current_input)
    
    def log10(self):
        try:
            value = float(self.current_input)
            if value > 0:
                result = math.log10(value)
                if abs(result - round(result, 10)) < 1e-10:
                    result = round(result, 10)
                # Убираем лишние нули
                result_str = str(result).rstrip('0').rstrip('.')
                self.current_input = result_str
                self.display.setText(self.current_input)
                self.waiting_for_operand = True
            else:
                self.display.setText("Error: Domain error")
        except:
            self.display.setText("Error")
    
    def ln(self):
        try:
            value = float(self.current_input)
            if value > 0:
                result = math.log(value)
                if abs(result - round(result, 10)) < 1e-10:
                    result = round(result, 10)
                # Убираем лишние нули
                result_str = str(result).rstrip('0').rstrip('.')
                self.current_input = result_str
                self.display.setText(self.current_input)
                self.waiting_for_operand = True
            else:
                self.display.setText("Error: Domain error")
        except:
            self.display.setText("Error")
    
    def factorial(self):
        try:
            value = float(self.current_input)
            if value.is_integer() and value >= 0 and value <= 100:  # Ограничиваем для производительности
                result = math.factorial(int(value))
                self.current_input = str(result)
                self.display.setText(self.current_input)
                self.waiting_for_operand = True
            else:
                self.display.setText("Error: Invalid input")
        except:
            self.display.setText("Error")
    
    def parenthesis(self, paren):
        if self.waiting_for_operand:
            self.current_input = paren
            self.waiting_for_operand = False
        else:
            self.current_input += paren
        self.display.setText(self.current_input)
    
    def switch_angle_mode(self, mode):
        if mode == 'Deg':
            self.degree_mode = True
        else:
            self.degree_mode = False
        self.update_angle_mode()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Устанавливаем современный стиль
    
    # Устанавливаем стиль для всего приложения
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QStatusBar {
            background-color: #e0e0e0;
            color: #333;
        }
    """)
    
    calculator = EngineeringCalculator()
    calculator.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()