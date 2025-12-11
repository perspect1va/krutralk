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
        self.waiting_for_operand = True
        self.degree_mode = True
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("крутой калькулятор")
        self.setFixedSize(500, 650)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0a14;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(30)
        font = self.display.font()
        font.setPointSize(24)
        font.setBold(True)
        self.display.setFont(font)
        self.display.setStyleSheet("""
            QLineEdit {
                border: 3px solid #ff00ff;
                border-radius: 10px;
                padding: 15px;
                background-color: #1a1a2e;
                color: #ff00ff;
                font-weight: bold;
                text-shadow: 0 0 10px rgba(255, 0, 255, 0.7);
                box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
            }
        """)
        main_layout.addWidget(self.display)
        
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(8)
        
        # кнопки
        buttons = [
            # Ряд 0
            ('Deg', 0, 0), ('Rad', 0, 1), ('sin', 0, 2), ('cos', 0, 3), ('tan', 0, 4),
            # Ряд 1
            ('π', 1, 0), ('e', 1, 1), ('x²', 1, 2), ('x³', 1, 3), ('√', 1, 4),
            # Ряд 2
            ('log', 2, 0), ('ln', 2, 1), ('x!', 2, 2), ('(', 2, 3), (')', 2, 4),
            # Ряд 3
            ('C', 3, 0), ('CE', 3, 1), ('DEL', 3, 2), ('÷', 3, 3), ('×', 3, 4),
            # Ряд 4
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('-', 4, 3), ('^', 4, 4),
            # Ряд 5
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('+', 5, 3), ('1/x', 5, 4),
            # Ряд 6
            ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('=', 6, 3, 2, 1),
            # Ряд 7
            ('±', 7, 0), ('0', 7, 1), ('.', 7, 2)
        ]
        
        # Цветовые стили
        dark_bg = "#1a1a2e"
        neon_pink = "#ff00ff"
        neon_blue = "#00ffff"
        neon_green = "#00ff00"
        dark_purple = "#2d2d44"
        
        for button in buttons:
            text = button[0]
            btn = QPushButton(text)
            btn.setMinimumSize(60, 50)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            
            base_style = f"""
                QPushButton {{
                    border: 2px solid {neon_pink};
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: bold;
                    color: white;
                    background-color: {dark_bg};
                    margin: 2px;
                }}
                QPushButton:hover {{
                    background-color: #2d2d44;
                    border-color: #ff66ff;
                }}
                QPushButton:pressed {{
                    background-color: #3d3d54;
                }}
            """
            
            if text in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'):
                btn.setStyleSheet(base_style + f"""
                    QPushButton {{
                        background-color: {dark_purple};
                        color: {neon_blue};
                        border-color: {neon_blue};
                    }}
                """)
            elif text in ('+', '-', '×', '÷', '=', '^'):
                btn.setStyleSheet(base_style + f"""
                    QPushButton {{
                        background-color: #2d0044;
                        color: {neon_pink};
                        border-color: {neon_pink};
                        font-size: 18px;
                    }}
                """)
            elif text in ('C', 'CE', 'DEL'):
                btn.setStyleSheet(base_style + f"""
                    QPushButton {{
                        background-color: #440022;
                        color: #ff3366;
                        border-color: #ff3366;
                    }}
                """)
            elif text in ('Deg', 'Rad'):
                btn.setStyleSheet(base_style + f"""
                    QPushButton {{
                        background-color: #004422;
                        color: {neon_green};
                        border-color: {neon_green};
                    }}
                """)
            else:
                btn.setStyleSheet(base_style + f"""
                    QPushButton {{
                        background-color: #002244;
                        color: {neon_blue};
                        border-color: {neon_blue};
                    }}
                """)
            
            # Добавление glow эффекта при наведении
            btn.setGraphicsEffect(QGraphicsDropShadowEffect(
                blurRadius=15, 
                xOffset=0, 
                yOffset=0,
                color=QColor(255, 0, 255, 100)
            ))
            
            # Добавление в layout
            if len(button) == 5:
                buttons_layout.addWidget(btn, button[1], button[2], button[3], button[4])
            else:
                buttons_layout.addWidget(btn, button[1], button[2])
            
            btn.clicked.connect(self.button_clicked)
        
        main_layout.addLayout(buttons_layout)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet(f"""
            QStatusBar {{
                background-color: {dark_bg};
                color: {neon_pink};
                font-weight: bold;
            }}
        """)
        self.update_angle_mode()
    
    def update_angle_mode(self):
        mode = "DEG" if self.degree_mode else "RAD"
        self.status_bar.showMessage(f"Режим: {mode} | Используйте 'Deg'/'Rad' для переключения")
    
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
        elif text == 'DEL':
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
            self.current_input = digit if self.current_input == "0" else self.current_input + digit
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
        self.operation = '*' if op == '×' else '/' if op == '÷' else '**' if op == '^' else op
    
    def equals_clicked(self):
        if self.operation and self.previous_input:
            self.calculate()
            self.operation = ""
        else:
            try:
                expr = self.current_input.replace('π', str(math.pi)).replace('e', str(math.e))
                expr = expr.replace('sin', 'math.sin').replace('cos', 'math.cos')
                expr = expr.replace('tan', 'math.tan').replace('log', 'math.log10')
                expr = expr.replace('ln', 'math.log').replace('√', 'math.sqrt')
                
                result = eval(expr, {"__builtins__": None}, {"math": math})
                
                if isinstance(result, float):
                    if abs(result - round(result, 10)) < 1e-10:
                        result = round(result, 10)
                    result_str = str(result).rstrip('0').rstrip('.')
                else:
                    result_str = str(result)
                
                self.current_input = result_str
                self.display.setText(self.current_input)
                self.waiting_for_operand = True
            except:
                self.display.setText("ERROR")
                self.current_input = "0"
                self.waiting_for_operand = True
    
    def calculate(self):
        try:
            expr1 = self.previous_input.replace('π', str(math.pi)).replace('e', str(math.e))
            expr2 = self.current_input.replace('π', str(math.pi)).replace('e', str(math.e))
            expression = f"{expr1} {self.operation} {expr2}"
            result = eval(expression, {"__builtins__": None}, {"math": math})
            
            if isinstance(result, float):
                if abs(result - round(result, 10)) < 1e-10:
                    result = round(result, 10)
                result_str = str(result).rstrip('0').rstrip('.')
            else:
                result_str = str(result)
            
            self.current_input = result_str
            self.display.setText(self.current_input)
            self.waiting_for_operand = True
        except:
            self.display.setText("ERROR")
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
        self.current_input = self.current_input[:-1] if len(self.current_input) > 1 else "0"
        self.display.setText(self.current_input)
    
    def negate(self):
        try:
            value = float(self.current_input)
            value = -value
            self.current_input = str(int(value)) if value.is_integer() else str(value)
            self.display.setText(self.current_input)
        except:
            pass
    
    def reciprocal(self):
        try:
            value = float(self.current_input)
            if value != 0:
                result = 1 / value
                result_str = str(round(result, 10)).rstrip('0').rstrip('.')
                self.current_input = result_str
                self.display.setText(self.current_input)
                self.waiting_for_operand = True
            else:
                self.display.setText("DIV BY ZERO")
        except:
            self.display.setText("ERROR")
    
    def square_root(self):
        try:
            value = float(self.current_input)
            if value >= 0:
                result = math.sqrt(value)
                result_str = str(round(result, 10)).rstrip('0').rstrip('.')
                self.current_input = result_str
                self.display.setText(self.current_input)
                self.waiting_for_operand = True
            else:
                self.display.setText("NEGATIVE")
        except:
            self.display.setText("ERROR")
    
    def square(self):
        try:
            value = float(self.current_input)
            result = value ** 2
            result_str = str(round(result, 10)).rstrip('0').rstrip('.')
            self.current_input = result_str
            self.display.setText(self.current_input)
            self.waiting_for_operand = True
        except:
            self.display.setText("ERROR")
    
    def cube(self):
        try:
            value = float(self.current_input)
            result = value ** 3
            result_str = str(round(result, 10)).rstrip('0').rstrip('.')
            self.current_input = result_str
            self.display.setText(self.current_input)
            self.waiting_for_operand = True
        except:
            self.display.setText("ERROR")
    
    def trig_function(self, func):
        try:
            value = float(self.current_input)
            value_rad = math.radians(value) if self.degree_mode else value
            
            if func == 'sin':
                result = math.sin(value_rad)
            elif func == 'cos':
                result = math.cos(value_rad)
            elif func == 'tan':
                if abs(math.cos(value_rad)) < 1e-10:
                    self.display.setText("UNDEFINED")
                    return
                result = math.tan(value_rad)
            
            result = 0 if abs(result) < 1e-10 else result
            result_str = str(round(result, 10)).rstrip('0').rstrip('.')
            
            self.current_input = result_str
            self.display.setText(self.current_input)
            self.waiting_for_operand = True
        except:
            self.display.setText("ERROR")
    
    def pi(self):
        self.current_input = str(math.pi) if self.waiting_for_operand else self.current_input + str(math.pi)
        self.waiting_for_operand = False
        self.display.setText(self.current_input)
    
    def euler(self):
        self.current_input = str(math.e) if self.waiting_for_operand else self.current_input + str(math.e)
        self.waiting_for_operand = False
        self.display.setText(self.current_input)
    
    def log10(self):
        try:
            value = float(self.current_input)
            if value > 0:
                result = math.log10(value)
                result_str = str(round(result, 10)).rstrip('0').rstrip('.')
                self.current_input = result_str
                self.display.setText(self.current_input)
                self.waiting_for_operand = True
            else:
                self.display.setText("DOMAIN ERROR")
        except:
            self.display.setText("ERROR")
    
    def ln(self):
        try:
            value = float(self.current_input)
            if value > 0:
                result = math.log(value)
                result_str = str(round(result, 10)).rstrip('0').rstrip('.')
                self.current_input = result_str
                self.display.setText(self.current_input)
                self.waiting_for_operand = True
            else:
                self.display.setText("DOMAIN ERROR")
        except:
            self.display.setText("ERROR")
    
    def factorial(self):
        try:
            value = float(self.current_input)
            if value.is_integer() and 0 <= value <= 100:
                result = math.factorial(int(value))
                self.current_input = str(result)
                self.display.setText(self.current_input)
                self.waiting_for_operand = True
            else:
                self.display.setText("INVALID")
        except:
            self.display.setText("ERROR")
    
    def parenthesis(self, paren):
        self.current_input = paren if self.waiting_for_operand else self.current_input + paren
        self.waiting_for_operand = False
        self.display.setText(self.current_input)
    
    def switch_angle_mode(self, mode):
        self.degree_mode = mode == 'Deg'
        self.update_angle_mode()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    app.setStyleSheet("""
        * {
            font-family: 'Segoe UI', Arial;
        }
        QPushButton {
            transition: all 0.2s;
        }
    """)
    
    calculator = EngineeringCalculator()
    calculator.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
