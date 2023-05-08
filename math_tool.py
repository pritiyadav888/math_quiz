import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtGui import QPixmap, QLinearGradient, QPalette, QPainter, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout


class StoryCard(QDialog):
    def __init__(self, story_title, story_text):
        super().__init__()

        self.setWindowTitle(story_title)

        layout = QVBoxLayout()

        title_label = QLabel(story_title)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)

        text_label = QLabel(story_text)
        text_label.setWordWrap(True)
        layout.addWidget(text_label)

        close_button = QPushButton("Close")
        close_button.setStyleSheet("color: black;")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, alignment=Qt.AlignRight)

        self.setLayout(layout)

class GradientWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paintEvent(self, event):
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(255, 128, 0))
        gradient.setColorAt(1, QColor(255, 228, 150))

        painter = QPainter(self)
        painter.setBrush(gradient)
        painter.drawRect(self.rect())

class MathApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.incorrect_count = 0
        self.stories = {
            "addition": ["The Cookie Jar Story", "The Toy Store Story", "The Fruit Bowl Story", "The Garden Story", "The Party"],
            "subtraction": ["The Fish Tank Story", "The Toy Box", "The Playground", "The Fruit Salad", "The Park"]
        }
        self.current_category = "addition" # start with addition problems
        self.current_story_index = 0

        self.central_widget = GradientWidget()
        self.setCentralWidget(self.central_widget)

        self.setWindowTitle("Math Learning Tool")
        self.resize(800, 600)

        layout = QVBoxLayout()

        self.example_label = QLabel("Example: 🐘🐘🐘 + 2 = 5")
        layout.addWidget(self.example_label)

        self.question_label = QLabel()
        layout.addWidget(self.question_label)

        self.answer_entry = QLineEdit()
        layout.addWidget(self.answer_entry)

        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet("color: black;")
        self.submit_button.clicked.connect(self.check_answer)
        layout.addWidget(self.submit_button)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.quit_button = QPushButton("Quit")
        self.quit_button.setStyleSheet("color: black;")
        self.quit_button.clicked.connect(self.close)
        layout.addWidget(self.quit_button)

        self.central_widget.setLayout(layout)
        self.generate_problem()

    def generate_problem(self):
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        self.operation = random.choice(["+", "-"])
        self.animal = random.choice(["🦖", "🐦", "🐘"])
        

        if self.operation == "-" and num1 < num2:
            num1, num2 = num2, num1

        self.correct_answer = num1 + num2 if self.operation == "+" else num1 - num2

        display_num1 = f'<span style="font-size:24px;">{num1}</span>' if num1 > 3 else ' '.join([f'<span style="font-size:24px;">{self.animal}</span>'] * num1)
        display_num2 = f'<span style="font-size:24px;">{num2}</span>' if num2 > 3 else ' '.join([f'<span style="font-size:24px;">{self.animal}</span>'] * num2)
        display_operation = f'<span style="font-size:24px;">{self.operation}</span>'
        display_equals = '<span style="font-size:24px;">=</span>'
        display_question_mark = '<span style="font-size:24px;">?</span>'
        self.question_label.setText(f"{display_num1} {display_operation} {display_num2} {display_equals} {display_question_mark}")
        self.answer_entry.clear()
        self.question_label.setTextFormat(Qt.RichText)

    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.text())
            if user_answer == self.correct_answer:
                self.result_label.setText("Correct! 🎉")
                self.incorrect_count = 0
            else:
                self.result_label.setText(f"Oops! The correct answer is {self.correct_answer}. Keep trying!")
                self.incorrect_count += 1
                if self.incorrect_count == 2:
                    self.generate_recommendation()
            self.generate_problem()
        except ValueError:
            self.result_label.setText("Please enter a valid number!")


    def switch_story_category(self):
            if self.current_category == "addition":
                self.current_category = "subtraction"
            else:
                self.current_category = "addition"
            self.stories[self.current_category] = random.shuffle(self.stories[self.current_category]) # randomize story order
            self.current_story_index = 0
            self.incorrect_count = 0
            self.generate_recommendation()
            
    def generate_recommendation(self):
        if self.incorrect_count == 2:
            if self.current_story_index < len(self.stories[self.current_category]):
                story_title = f"{self.current_category.capitalize()} Story #{self.current_story_index + 1}"
                story_text = self.stories[self.current_category][self.current_story_index]
                self.result_label.setText(f"Looks like you're struggling with {self.current_category}! Try this story: {story_text}")
                story_card = StoryCard(story_title, story_text)
                story_card.exec_()
                self.current_story_index += 1
                self.incorrect_count = 0
            else:
                self.result_label.setText(f"You've completed all the {self.current_category} stories! Switching to the other category.")
                self.switch_story_category()
        else:
            self.incorrect_count += 1
      
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MathApp()
    main_win.show()
    sys.exit(app.exec_())