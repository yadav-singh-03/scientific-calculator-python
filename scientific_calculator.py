import tkinter as tk
from tkinter import ttk, messagebox
import math
import numpy as np
from collections import deque

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Scientific Calculator")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        
        # Variables
        self.current_expression = ""
        self.total_expression = ""
        self.history = deque(maxlen=10)
        self.memory = 0
        self.angle_mode = "DEG"  # DEG or RAD
        
        # Configure style
        self.setup_styles()
        
        # Create UI
        self.create_widgets()
        
        # Bind keyboard events
        self.bind_keyboard()
        
    def setup_styles(self):
        """Configure modern styling"""
        self.root.configure(bg='#1e1e1e')
        
        # Define color scheme
        self.colors = {
            'bg': '#1e1e1e',
            'display_bg': '#2d2d30',
            'display_fg': '#ffffff',
            'num_btn': '#3c3c3c',
            'op_btn': '#007acc',
            'func_btn': '#5a5a5a',
            'equal_btn': '#0e7490',
            'clear_btn': '#dc2626',
            'memory_btn': '#7c3aed',
            'btn_fg': '#ffffff',
            'btn_hover': '#4a4a4a'
        }
        
    def create_widgets(self):
        """Create all calculator widgets"""
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Display frame
        self.create_display(main_frame)
        
        # Mode and memory display
        self.create_status_bar(main_frame)
        
        # History dropdown
        self.create_history_dropdown(main_frame)
        
        # Buttons frame
        self.create_buttons(main_frame)
        
    def create_display(self, parent):
        """Create calculator display"""
        display_frame = tk.Frame(parent, bg=self.colors['display_bg'], height=120)
        display_frame.pack(fill=tk.X, pady=(0, 10))
        display_frame.pack_propagate(False)
        
        # Small expression label
        self.expression_label = tk.Label(
            display_frame,
            text="",
            anchor="e",
            bg=self.colors['display_bg'],
            fg='#888888',
            font=('Arial', 12),
            padx=10,
            pady=5
        )
        self.expression_label.pack(fill=tk.X)
        
        # Main display label
        self.display_label = tk.Label(
            display_frame,
            text="0",
            anchor="e",
            bg=self.colors['display_bg'],
            fg=self.colors['display_fg'],
            font=('Arial', 28, 'bold'),
            padx=10,
            pady=5
        )
        self.display_label.pack(fill=tk.BOTH, expand=True)
        
    def create_status_bar(self, parent):
        """Create status bar for angle mode and memory"""
        status_frame = tk.Frame(parent, bg=self.colors['bg'], height=30)
        status_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Angle mode indicator
        self.angle_label = tk.Label(
            status_frame,
            text=f"Mode: {self.angle_mode}",
            bg=self.colors['bg'],
            fg='#00ff00',
            font=('Arial', 10, 'bold')
        )
        self.angle_label.pack(side=tk.LEFT, padx=5)
        
        # Memory indicator
        self.memory_label = tk.Label(
            status_frame,
            text="M: 0",
            bg=self.colors['bg'],
            fg='#ffa500',
            font=('Arial', 10, 'bold')
        )
        self.memory_label.pack(side=tk.LEFT, padx=20)
        
    def create_history_dropdown(self, parent):
        """Create history dropdown"""
        history_frame = tk.Frame(parent, bg=self.colors['bg'])
        history_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            history_frame,
            text="History:",
            bg=self.colors['bg'],
            fg=self.colors['display_fg'],
            font=('Arial', 10)
        ).pack(side=tk.LEFT, padx=5)
        
        self.history_var = tk.StringVar()
        self.history_dropdown = ttk.Combobox(
            history_frame,
            textvariable=self.history_var,
            state='readonly',
            width=40,
            font=('Arial', 10)
        )
        self.history_dropdown.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.history_dropdown.bind('<<ComboboxSelected>>', self.load_from_history)
        
    def create_buttons(self, parent):
        """Create calculator buttons"""
        button_frame = tk.Frame(parent, bg=self.colors['bg'])
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button layout
        buttons = [
            # Row 0 - Scientific functions
            [('sin', 'func'), ('cos', 'func'), ('tan', 'func'), ('log', 'func'), ('ln', 'func')],
            # Row 1 - More functions
            [('x²', 'func'), ('√', 'func'), ('xⁿ', 'func'), ('1/x', 'func'), ('|x|', 'func')],
            # Row 2 - Memory and mode
            [('MC', 'memory'), ('MR', 'memory'), ('M+', 'memory'), ('M-', 'memory'), ('DEG/RAD', 'memory')],
            # Row 3 - Constants and parentheses
            [('π', 'func'), ('e', 'func'), ('(', 'op'), (')', 'op'), ('!', 'func')],
            # Row 4 - Clear and basic ops
            [('CE', 'clear'), ('C', 'clear'), ('⌫', 'clear'), ('÷', 'op'), ('%', 'op')],
            # Row 5 - Numbers 7-9 and multiply
            [('7', 'num'), ('8', 'num'), ('9', 'num'), ('×', 'op'), ('exp', 'func')],
            # Row 6 - Numbers 4-6 and subtract
            [('4', 'num'), ('5', 'num'), ('6', 'num'), ('-', 'op'), ('mod', 'func')],
            # Row 7 - Numbers 1-3 and add
            [('1', 'num'), ('2', 'num'), ('3', 'num'), ('+', 'op'), ('±', 'func')],
            # Row 8 - 0, decimal and equals
            [('0', 'num'), ('00', 'num'), ('.', 'num'), ('=', 'equal'), ('Ans', 'func')]
        ]
        
        # Create buttons
        for row_num, row in enumerate(buttons):
            for col_num, (text, btn_type) in enumerate(row):
                self.create_button(button_frame, text, btn_type, row_num, col_num)
                
    def create_button(self, parent, text, btn_type, row, col):
        """Create individual button"""
        # Determine button color based on type
        if btn_type == 'num':
            bg = self.colors['num_btn']
        elif btn_type == 'op':
            bg = self.colors['op_btn']
        elif btn_type == 'func':
            bg = self.colors['func_btn']
        elif btn_type == 'equal':
            bg = self.colors['equal_btn']
        elif btn_type == 'clear':
            bg = self.colors['clear_btn']
        elif btn_type == 'memory':
            bg = self.colors['memory_btn']
        else:
            bg = self.colors['num_btn']
            
        btn = tk.Button(
            parent,
            text=text,
            bg=bg,
            fg=self.colors['btn_fg'],
            font=('Arial', 14, 'bold'),
            bd=0,
            padx=5,
            pady=5,
            activebackground=self.colors['btn_hover'],
            activeforeground=self.colors['btn_fg'],
            command=lambda t=text: self.button_click(t)
        )
        
        # Configure grid
        if text == '=':
            btn.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        else:
            btn.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
            
        # Configure grid weights
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Hover effect
        btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.colors['btn_hover']))
        btn.bind('<Leave>', lambda e, b=btn, c=bg: b.config(bg=c))
        
    def button_click(self, value):
        """Handle button clicks"""
        try:
            if value in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '00']:
                self.append_number(value)
            elif value in ['+', '-', '×', '÷', '%']:
                self.append_operator(value)
            elif value == '=':
                self.calculate()
            elif value == 'C':
                self.clear_all()
            elif value == 'CE':
                self.clear_entry()
            elif value == '⌫':
                self.backspace()
            elif value == '(':
                self.append_number('(')
            elif value == ')':
                self.append_number(')')
            elif value in ['sin', 'cos', 'tan', 'log', 'ln']:
                self.scientific_function(value)
            elif value == 'x²':
                self.power_function(2)
            elif value == '√':
                self.sqrt_function()
            elif value == 'xⁿ':
                self.append_operator('**')
            elif value == '1/x':
                self.reciprocal()
            elif value == '|x|':
                self.absolute()
            elif value == 'π':
                self.append_number(str(math.pi))
            elif value == 'e':
                self.append_number(str(math.e))
            elif value == '!':
                self.factorial()
            elif value == '±':
                self.negate()
            elif value == 'exp':
                self.append_operator('e')
            elif value == 'mod':
                self.append_operator(' mod ')
            elif value == 'DEG/RAD':
                self.toggle_angle_mode()
            elif value == 'MC':
                self.memory_clear()
            elif value == 'MR':
                self.memory_recall()
            elif value == 'M+':
                self.memory_add()
            elif value == 'M-':
                self.memory_subtract()
            elif value == 'Ans':
                self.use_last_answer()
                
        except Exception as e:
            self.display_label.config(text="Error")
            
    def append_number(self, value):
        """Append number or decimal to expression"""
        self.current_expression += str(value)
        self.update_display()
        
    def append_operator(self, value):
        """Append operator to expression"""
        if value == '×':
            value = '*'
        elif value == '÷':
            value = '/'
            
        self.current_expression += str(value)
        self.update_display()
        
    def scientific_function(self, func):
        """Apply scientific function"""
        try:
            current = self.get_current_number()
            if current:
                angle = float(current)
                
                # Convert angle if in degree mode
                if self.angle_mode == "DEG" and func in ['sin', 'cos', 'tan']:
                    angle = math.radians(angle)
                    
                if func == 'sin':
                    result = math.sin(angle)
                elif func == 'cos':
                    result = math.cos(angle)
                elif func == 'tan':
                    result = math.tan(angle)
                elif func == 'log':
                    result = math.log10(float(current))
                elif func == 'ln':
                    result = math.log(float(current))
                    
                self.current_expression = str(result)
                self.update_display()
        except:
            self.display_label.config(text="Error")
            
    def power_function(self, power):
        """Calculate power"""
        try:
            current = self.get_current_number()
            if current:
                result = float(current) ** power
                self.current_expression = str(result)
                self.update_display()
        except:
            self.display_label.config(text="Error")
            
    def sqrt_function(self):
        """Calculate square root"""
        try:
            current = self.get_current_number()
            if current:
                result = math.sqrt(float(current))
                self.current_expression = str(result)
                self.update_display()
        except:
            self.display_label.config(text="Error")
            
    def reciprocal(self):
        """Calculate reciprocal"""
        try:
            current = self.get_current_number()
            if current and float(current) != 0:
                result = 1 / float(current)
                self.current_expression = str(result)
                self.update_display()
        except:
            self.display_label.config(text="Error")
            
    def absolute(self):
        """Calculate absolute value"""
        try:
            current = self.get_current_number()
            if current:
                result = abs(float(current))
                self.current_expression = str(result)
                self.update_display()
        except:
            self.display_label.config(text="Error")
            
    def factorial(self):
        """Calculate factorial"""
        try:
            current = self.get_current_number()
            if current:
                n = int(float(current))
                if n >= 0 and n <= 170:  # Prevent overflow
                    result = math.factorial(n)
                    self.current_expression = str(result)
                    self.update_display()
        except:
            self.display_label.config(text="Error")
            
    def negate(self):
        """Negate current number"""
        try:
            current = self.get_current_number()
            if current:
                result = -float(current)
                self.current_expression = str(result)
                self.update_display()
        except:
            self.display_label.config(text="Error")
            
    def toggle_angle_mode(self):
        """Toggle between DEG and RAD mode"""
        self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"
        self.angle_label.config(text=f"Mode: {self.angle_mode}")
        
    def memory_clear(self):
        """Clear memory"""
        self.memory = 0
        self.memory_label.config(text="M: 0")
        
    def memory_recall(self):
        """Recall memory value"""
        self.current_expression = str(self.memory)
        self.update_display()
        
    def memory_add(self):
        """Add current value to memory"""
        try:
            current = self.get_current_number()
            if current:
                self.memory += float(current)
                self.memory_label.config(text=f"M: {self.memory:.4g}")
        except:
            pass
            
    def memory_subtract(self):
        """Subtract current value from memory"""
        try:
            current = self.get_current_number()
            if current:
                self.memory -= float(current)
                self.memory_label.config(text=f"M: {self.memory:.4g}")
        except:
            pass
            
    def use_last_answer(self):
        """Use last calculation answer"""
        if self.history:
            last = self.history[-1].split('=')[-1].strip()
            self.current_expression = last
            self.update_display()
            
    def get_current_number(self):
        """Extract current number from expression"""
        try:
            # Try to evaluate the entire expression
            if self.current_expression:
                return self.current_expression
            return "0"
        except:
            return "0"
            
    def calculate(self):
        """Calculate the expression"""
        try:
            if not self.current_expression:
                return
                
            # Store original expression
            self.total_expression = self.current_expression
            
            # Replace symbols for evaluation
            expression = self.current_expression
            expression = expression.replace('×', '*')
            expression = expression.replace('÷', '/')
            expression = expression.replace('mod', '%')
            expression = expression.replace('e', '*10**')
            
            # Evaluate expression
            result = eval(expression)
            
            # Round to avoid floating point issues
            if isinstance(result, float):
                result = round(result, 10)
                
            # Add to history
            history_entry = f"{self.total_expression} = {result}"
            self.history.append(history_entry)
            self.update_history_dropdown()
            
            # Update display
            self.expression_label.config(text=self.total_expression)
            self.current_expression = str(result)
            self.update_display()
            
        except ZeroDivisionError:
            self.display_label.config(text="Cannot divide by zero")
            self.current_expression = ""
        except Exception as e:
            self.display_label.config(text="Error")
            self.current_expression = ""
            
    def clear_all(self):
        """Clear all"""
        self.current_expression = ""
        self.total_expression = ""
        self.expression_label.config(text="")
        self.display_label.config(text="0")
        
    def clear_entry(self):
        """Clear current entry"""
        self.current_expression = ""
        self.display_label.config(text="0")
        
    def backspace(self):
        """Remove last character"""
        self.current_expression = self.current_expression[:-1]
        if not self.current_expression:
            self.display_label.config(text="0")
        else:
            self.update_display()
            
    def update_display(self):
        """Update the display"""
        if self.current_expression:
            # Limit display length
            display_text = self.current_expression
            if len(display_text) > 20:
                display_text = display_text[:20] + "..."
            self.display_label.config(text=display_text)
        else:
            self.display_label.config(text="0")
            
    def update_history_dropdown(self):
        """Update history dropdown"""
        history_list = list(self.history)
        history_list.reverse()
        self.history_dropdown['values'] = history_list
        
    def load_from_history(self, event):
        """Load calculation from history"""
        selected = self.history_var.get()
        if selected:
            parts = selected.split('=')
            if len(parts) == 2:
                self.current_expression = parts[0].strip()
                self.update_display()
                
    def bind_keyboard(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<Key-0>', lambda e: self.button_click('0'))
        self.root.bind('<Key-1>', lambda e: self.button_click('1'))
        self.root.bind('<Key-2>', lambda e: self.button_click('2'))
        self.root.bind('<Key-3>', lambda e: self.button_click('3'))
        self.root.bind('<Key-4>', lambda e: self.button_click('4'))
        self.root.bind('<Key-5>', lambda e: self.button_click('5'))
        self.root.bind('<Key-6>', lambda e: self.button_click('6'))
        self.root.bind('<Key-7>', lambda e: self.button_click('7'))
        self.root.bind('<Key-8>', lambda e: self.button_click('8'))
        self.root.bind('<Key-9>', lambda e: self.button_click('9'))
        self.root.bind('<period>', lambda e: self.button_click('.'))
        self.root.bind('<plus>', lambda e: self.button_click('+'))
        self.root.bind('<minus>', lambda e: self.button_click('-'))
        self.root.bind('<asterisk>', lambda e: self.button_click('×'))
        self.root.bind('<slash>', lambda e: self.button_click('÷'))
        self.root.bind('<Return>', lambda e: self.button_click('='))
        self.root.bind('<BackSpace>', lambda e: self.button_click('⌫'))
        self.root.bind('<Escape>', lambda e: self.button_click('C'))
        self.root.bind('<parenleft>', lambda e: self.button_click('('))
        self.root.bind('<parenright>', lambda e: self.button_click(')'))


def main():
    root = tk.Tk()
    calculator = ScientificCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()