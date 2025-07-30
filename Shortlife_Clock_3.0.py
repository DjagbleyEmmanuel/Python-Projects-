import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QComboBox, 
                            QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, 
                            QMessageBox, QCheckBox, QTextEdit, QProgressBar, 
                            QDateEdit, QGroupBox, QFormLayout, QSpinBox, 
                            QDateTimeEdit, QPushButton, QScrollArea)
from PyQt5.QtCore import QTimer, QDate, Qt, QTime, QPropertyAnimation, QEasingCurve, QDateTime
from PyQt5.QtGui import QFont, QColor
from datetime import datetime
import random
import json
import random

# Expanded data
life_expectancy_data = {
    "World": {"Male": 70, "Female": 75, "Non-Binary": 72},
    "Africa": {"Male": 64, "Female": 67, "Non-Binary": 65},
    "Asia": {"Male": 72, "Female": 75, "Non-Binary": 73},
    "Europe": {"Male": 78, "Female": 83, "Non-Binary": 80},
    "North America": {"Male": 76, "Female": 81, "Non-Binary": 78},
    "South America": {"Male": 72, "Female": 79, "Non-Binary": 75},
    "Australia": {"Male": 81, "Female": 85, "Non-Binary": 83},
}

health_tips = [
    "Drink 8-10 glasses of water daily for optimal hydration.",
    "Engage in 30 minutes of moderate exercise 5 days a week.",
    "Incorporate leafy greens and colorful vegetables in your diet.",
    "Aim for 7-9 hours of quality sleep per night.",
    "Practice stress management through meditation or yoga.",
    "Limit processed foods and added sugars.",
    "Schedule regular health check-ups with your doctor."
]

motivational_quotes = [
    "The best time to plant a tree was 20 years ago. The second best time is now.",
    "Your time is limited, don't waste it living someone else's life.",
    "The purpose of life is to be useful, to be honorable, to be compassionate.",
    "Not how long, but how well you have lived is the main thing.",
    "Every moment is a fresh beginning."
]

symptoms_list = [
    "Fatigue", "Headache", "Fever", "Nausea", "Muscle Pain", 
    "Stress", "Insomnia", "Anxiety", "Joint Pain", "Dizziness"
]

class ShortlifeClock(QWidget):
    def __init__(self):
        super().__init__()
        self.dark_mode = False
        self.manual_age = False
        self.health_data = {"symptoms": [], "medications": []}
        self.load_health_data()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                font-family: 'Arial', sans-serif;
                font-size: 14px;
                background-color: #f0f2f5;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.2);
                transition: all 0.3s;
            }
            QPushButton:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 8px rgba(0,0,0,0.3);
                background-color: #45a049;
            }
            QPushButton:pressed {
                transform: translateY(1px);
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            QGroupBox {
                border: 1px solid #d1d5db;
                border-radius: 5px;
                margin-top: 20px;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
                color: #333;
            }
            QLineEdit, QComboBox, QDateEdit, QTextEdit {
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
        """)

        main_layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        layout = QGridLayout()

        # Basic Information Section
        basic_info_group = QGroupBox("Personal Information")
        basic_layout = QGridLayout()

        self.age_label = QLabel('Age:')
        self.age_input = QLineEdit()
        self.age_input.setEnabled(False)

        self.birthdate_label = QLabel('Birthdate:')
        self.birthdate_input = QDateEdit()
        self.birthdate_input.setCalendarPopup(True)
        self.birthdate_input.setDate(QDate.currentDate())

        self.age_option_checkbox = QCheckBox('Enter age manually')
        self.age_option_checkbox.stateChanged.connect(self.toggle_age_input)

        self.gender_label = QLabel('Gender:')
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female", "Non-Binary"])

        self.continent_label = QLabel('Continent:')
        self.continent_input = QComboBox()
        self.continent_input.addItems(list(life_expectancy_data.keys()))

        basic_layout.addWidget(self.age_label, 0, 0)
        basic_layout.addWidget(self.age_input, 0, 1)
        basic_layout.addWidget(self.birthdate_label, 1, 0)
        basic_layout.addWidget(self.birthdate_input, 1, 1)
        basic_layout.addWidget(self.age_option_checkbox, 2, 0, 1, 2)
        basic_layout.addWidget(self.gender_label, 3, 0)
        basic_layout.addWidget(self.gender_input, 3, 1)
        basic_layout.addWidget(self.continent_label, 4, 0)
        basic_layout.addWidget(self.continent_input, 4, 1)
        basic_info_group.setLayout(basic_layout)
        layout.addWidget(basic_info_group, 0, 0, 1, 2)

        # Symptoms Tracking Section
        symptoms_group = QGroupBox("Symptoms Tracking")
        symptoms_layout = QFormLayout()

        self.symptom_combo = QComboBox()
        self.symptom_combo.addItems(symptoms_list + ["Custom"])
        self.custom_symptom_input = QLineEdit()
        self.custom_symptom_input.setPlaceholderText("Enter custom symptom")
        self.custom_symptom_input.setVisible(False)
        self.symptom_combo.currentTextChanged.connect(self.toggle_custom_symptom)

        self.severity_spin = QSpinBox()
        self.severity_spin.setRange(1, 10)
        self.severity_spin.setValue(5)

        self.add_symptom_button = QPushButton("Add Symptom")
        self.add_symptom_button.clicked.connect(self.add_symptom)

        self.symptoms_display = QTextEdit()
        self.symptoms_display.setReadOnly(True)

        symptoms_layout.addRow("Symptom:", self.symptom_combo)
        symptoms_layout.addRow("Custom Symptom:", self.custom_symptom_input)
        symptoms_layout.addRow("Severity (1-10):", self.severity_spin)
        symptoms_layout.addRow(self.add_symptom_button)
        symptoms_layout.addRow("Recent Symptoms:", self.symptoms_display)
        symptoms_group.setLayout(symptoms_layout)
        layout.addWidget(symptoms_group, 1, 0, 1, 2)

        # Medication Tracking Section
        medication_group = QGroupBox("Medication Tracking")
        medication_layout = QFormLayout()

        self.med_name_input = QLineEdit()
        self.med_dosage_input = QLineEdit()
        self.med_schedule_input = QDateTimeEdit()
        self.med_schedule_input.setCalendarPopup(True)
        self.med_schedule_input.setDateTime(QDateTime.currentDateTime())

        self.add_med_button = QPushButton("Add Medication")
        self.add_med_button.clicked.connect(self.add_medication)

        self.medications_display = QTextEdit()
        self.medications_display.setReadOnly(True)

        medication_layout.addRow("Medication Name:", self.med_name_input)
        medication_layout.addRow("Dosage:", self.med_dosage_input)
        medication_layout.addRow("Schedule:", self.med_schedule_input)
        medication_layout.addRow(self.add_med_button)
        medication_layout.addRow("Current Medications:", self.medications_display)
        medication_group.setLayout(medication_layout)
        layout.addWidget(medication_group, 2, 0, 1, 2)

        # Results Section
        results_group = QGroupBox("Life Clock Results")
        results_layout = QGridLayout()

        self.health_tips_checkbox = QCheckBox('Show daily health tips')
        self.health_tips_checkbox.stateChanged.connect(self.toggle_health_tips)

        self.show_percentage_checkbox = QCheckBox('Show remaining days as percentage')
        self.show_percentage_checkbox.stateChanged.connect(self.update_remaining_display)

        self.calculate_button = QPushButton('Calculate Life Clock')
        self.calculate_button.clicked.connect(self.calculate_life_percentage)

        self.dark_mode_button = QPushButton('Toggle Dark/Light Mode')
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)

        self.health_score_label = QLabel('Health Score: Not calculated')
        self.result_label = QLabel('Life Percentage Used: ')
        self.days_lived_label = QLabel('Days Lived: ')
        self.remaining_days_label = QLabel('Remaining Days: ')
        self.progress_bar = QProgressBar()

        self.quote_label = QLabel('Motivational Quote:')
        self.quote_text = QTextEdit()
        self.quote_text.setReadOnly(True)

        self.health_tips_label = QLabel('Health Tips:')
        self.health_tips_text = QTextEdit()
        self.health_tips_text.setReadOnly(True)

        self.countdown_label = QLabel('Time Remaining:')
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.remaining_seconds = 0

        results_layout.addWidget(self.health_tips_checkbox, 0, 0, 1, 2)
        results_layout.addWidget(self.show_percentage_checkbox, 1, 0, 1, 2)
        results_layout.addWidget(self.calculate_button, 2, 0, 1, 2)
        results_layout.addWidget(self.dark_mode_button, 3, 0, 1, 2)
        results_layout.addWidget(self.health_score_label, 4, 0, 1, 2)
        results_layout.addWidget(self.result_label, 5, 0, 1, 2)
        results_layout.addWidget(self.days_lived_label, 6, 0, 1, 2)
        results_layout.addWidget(self.remaining_days_label, 7, 0, 1, 2)
        results_layout.addWidget(self.progress_bar, 8, 0, 1, 2)
        results_layout.addWidget(self.quote_label, 9, 0, 1, 2)
        results_layout.addWidget(self.quote_text, 10, 0, 1, 2)
        results_layout.addWidget(self.health_tips_label, 11, 0, 1, 2)
        results_layout.addWidget(self.health_tips_text, 12, 0, 1, 2)
        results_layout.addWidget(self.countdown_label, 13, 0, 1, 2)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group, 3, 0, 1, 2)

        scroll_widget.setLayout(layout)
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
        self.setWindowTitle('Shortlife Clock 4.0')
        self.setMinimumSize(600, 800)

        # Timer for daily health tips
        self.health_tips_timer = QTimer(self)
        self.health_tips_timer.timeout.connect(self.show_health_tip)

        # Animation for buttons
        self.animate_button(self.calculate_button)
        self.animate_button(self.dark_mode_button)
        self.animate_button(self.add_symptom_button)
        self.animate_button(self.add_med_button)

    def animate_button(self, button):
        anim = QPropertyAnimation(button, b"geometry")
        anim.setDuration(200)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        button.enterEvent = lambda event: self.start_button_animation(button, anim)
        button.leaveEvent = lambda event: self.reset_button_animation(button, anim)

    def start_button_animation(self, button, anim):
        rect = button.geometry()
        anim.setStartValue(rect)
        anim.setEndValue(rect.adjusted(-2, -2, 2, 2))
        anim.start()

    def reset_button_animation(self, button, anim):
        rect = button.geometry()
        anim.setStartValue(rect)
        anim.setEndValue(rect.adjusted(2, 2, -2, -2))
        anim.start()

    def toggle_age_input(self, state):
        self.age_input.setEnabled(state == Qt.Checked)
        self.birthdate_input.setEnabled(state != Qt.Checked)
        self.manual_age = state == Qt.Checked

    def toggle_custom_symptom(self, text):
        self.custom_symptom_input.setVisible(text == "Custom")

    def add_symptom(self):
        symptom = self.symptom_combo.currentText()
        if symptom == "Custom":
            symptom = self.custom_symptom_input.text().strip()
        if not symptom:
            QMessageBox.warning(self, "Input Error", "Please enter a valid symptom.")
            return

        severity = self.severity_spin.value()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.health_data["symptoms"].append({
            "symptom": symptom,
            "severity": severity,
            "timestamp": timestamp
        })
        self.save_health_data()
        self.update_symptoms_display()

    def add_medication(self):
        name = self.med_name_input.text().strip()
        dosage = self.med_dosage_input.text().strip()
        schedule = self.med_schedule_input.dateTime().toString()
        if not name or not dosage:
            QMessageBox.warning(self, "Input Error", "Please enter medication name and dosage.")
            return

        self.health_data["medications"].append({
            "name": name,
            "dosage": dosage,
            "schedule": schedule
        })
        self.save_health_data()
        self.update_medications_display()

    def update_symptoms_display(self):
        display_text = ""
        for symptom in self.health_data["symptoms"][-5:]:  # Show last 5 symptoms
            display_text += f"{symptom['timestamp']}: {symptom['symptom']} (Severity: {symptom['severity']}/10)\n"
        self.symptoms_display.setText(display_text)

    def update_medications_display(self):
        display_text = ""
        for med in self.health_data["medications"][-5:]:  # Show last 5 medications
            display_text += f"{med['name']} - {med['dosage']} (Schedule: {med['schedule']})\n"
        self.medications_display.setText(display_text)

    def load_health_data(self):
        try:
            with open('health_data.json', 'r') as f:
                self.health_data = json.load(f)
        except FileNotFoundError:
            self.health_data = {"symptoms": [], "medications": []}

    def save_health_data(self):
        with open('health_data.json', 'w') as f:
            json.dump(self.health_data, f, indent=2)

    def calculate_life_percentage(self):
        try:
            if self.manual_age:
                age = int(self.age_input.text())
            else:
                birthdate = self.birthdate_input.date().toPyDate()
                today = datetime.today().date()
                age = (today - birthdate).days // 365

            gender = self.gender_input.currentText()
            continent = self.continent_input.currentText()

            if age < 0:
                raise ValueError("Age cannot be negative")

            life_expectancy = life_expectancy_data[continent][gender]
            life_percentage_used = (age / life_expectancy) * 100

            # Calculate health score
            health_score = self.calculate_health_score()
            self.health_score_label.setText(f'Health Score: {health_score}/100')

            self.result_label.setText(f'Life Percentage Used: {life_percentage_used:.2f}%')
            days_lived = age * 365
            remaining_days = (life_expectancy * 365) - days_lived
            self.days_lived_label.setText(f'Days Lived: {days_lived}')
            self.remaining_days_label.setText(f'Remaining Days: {remaining_days}')

            self.progress_bar.setValue(int(life_percentage_used))
            self.show_motivational_quote()
            self.remaining_seconds = remaining_days * 24 * 3600
            self.countdown_timer.start(1000)
            self.update_countdown()
            self.update_remaining_display()

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid age.")

    def calculate_health_score(self):
        if not self.health_data["symptoms"]:
            return 100
        
        total_severity = sum(symptom["severity"] for symptom in self.health_data["symptoms"][-5:])
        count = len(self.health_data["symptoms"][-5:]) or 1
        avg_severity = total_severity / count
        score = max(0, 100 - (avg_severity * 10))
        return int(score)

    def update_remaining_display(self):
        if self.show_percentage_checkbox.isChecked():
            gender = self.gender_input.currentText()
            continent = self.continent_input.currentText()
            life_expectancy = life_expectancy_data[continent][gender]
            remaining_days = (self.remaining_seconds // 3600) // 24
            remaining_percentage = (remaining_days / (life_expectancy * 365)) * 100
            self.remaining_days_label.setText(f'Remaining Life: {remaining_percentage:.2f}%')
        else:
            remaining_days = (self.remaining_seconds // 3600) // 24
            self.remaining_days_label.setText(f'Remaining Days: {remaining_days}')

    def show_health_tip(self):
        tip = random.choice(health_tips)
        self.health_tips_text.setText(tip)

    def toggle_health_tips(self, state):
        if state == Qt.Checked:
            self.show_health_tip()
            self.health_tips_timer.start(86400000)
        else:
            self.health_tips_text.clear()
            self.health_tips_timer.stop()

    def toggle_dark_mode(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QWidget {
                    font-family: 'Arial', sans-serif;
                    font-size: 14px;
                    background-color: #f0f2f5;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
                    transition: all 0.3s;
                }
                QPushButton:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 6px 8px rgba(0,0,0,0.3);
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    transform: translateY(1px);
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                }
            """)
            self.dark_mode = False
        else:
            self.setStyleSheet("""
                QWidget {
                    font-family: 'Arial', sans-serif;
                    font-size: 14px;
                    background-color: #1a1a1a;
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.4);
                    transition: all 0.3s;
                }
                QPushButton:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 6px 8px rgba(0,0,0,0.5);
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    transform: translateY(1px);
                    box-shadow: 0 2px 4px rgba(0,0,0,0.4);
                }
            """)
            self.dark_mode = True

    def show_motivational_quote(self):
        quote = random.choice(motivational_quotes)
        self.quote_text.setText(quote)

    def update_countdown(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            days = self.remaining_seconds // (24 * 3600)
            hours = (self.remaining_seconds % (24 * 3600)) // 3600
            minutes = (self.remaining_seconds % 3600) // 60
            seconds = self.remaining_seconds % 60
            self.countdown_label.setText(f'Time Remaining: {days}d {hours}h {minutes}m {seconds}s')
        else:
            self.countdown_timer.stop()
            self.countdown_label.setText('Time Remaining: Expired')

def main():
    app = QApplication(sys.argv)
    clock = ShortlifeClock()
    clock.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
