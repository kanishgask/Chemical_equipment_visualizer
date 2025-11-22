import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QFileDialog, QTableWidget, QTableWidgetItem, 
                             QListWidget, QMessageBox, QStackedWidget, QFormLayout,
                             QGroupBox, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


API_URL = 'http://localhost:8000/api'


class AuthWorker(QThread):
    """Worker thread for authentication"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, endpoint, data):
        super().__init__()
        self.endpoint = endpoint
        self.data = data
    
    def run(self):
        try:
            response = requests.post(f"{API_URL}{self.endpoint}", json=self.data)
            if response.status_code in [200, 201]:
                self.finished.emit(response.json())
            else:
                self.error.emit(response.json().get('error', 'Authentication failed'))
        except Exception as e:
            self.error.emit(str(e))


class DataWorker(QThread):
    """Worker thread for data operations"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, method, url, headers, data=None, files=None):
        super().__init__()
        self.method = method
        self.url = url
        self.headers = headers
        self.data = data
        self.files = files
    
    def run(self):
        try:
            if self.method == 'GET':
                response = requests.get(self.url, headers=self.headers)
            elif self.method == 'POST':
                response = requests.post(self.url, headers=self.headers, 
                                       data=self.data, files=self.files)
            
            if response.status_code in [200, 201]:
                self.finished.emit(response.json())
            else:
                self.error.emit(response.json().get('error', 'Operation failed'))
        except Exception as e:
            self.error.emit(str(e))


class ChartWidget(QWidget):
    """Widget for displaying matplotlib charts"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    
    def plot_bar_chart(self, labels, values, title):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(labels, values, color=['#36A2EB', '#FF6384', '#FFCE56'])
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel('Value')
        ax.grid(axis='y', alpha=0.3)
        self.canvas.draw()
    
    def plot_pie_chart(self, labels, values, title):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
        ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax.set_title(title, fontsize=14, fontweight='bold')
        self.canvas.draw()


class LoginWidget(QWidget):
    """Login/Register widget"""
    login_success = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def __del__(self):
        """Cleanup when widget is destroyed"""
        if self.worker and self.worker.isRunning():
            self.worker.quit()
            self.worker.wait(1000)
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Title
        title = QLabel('Chemical Equipment Visualizer')
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Form
        form_widget = QWidget()
        form_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.email_input = QLineEdit()
        
        form_layout.addRow('Username:', self.username_input)
        form_layout.addRow('Password:', self.password_input)
        form_layout.addRow('Email (optional):', self.email_input)
        
        form_widget.setLayout(form_layout)
        layout.addWidget(form_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.login_btn = QPushButton('Login')
        self.login_btn.clicked.connect(self.handle_login)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                padding: 10px 30px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
        """)
        
        self.register_btn = QPushButton('Register')
        self.register_btn.clicked.connect(self.handle_register)
        self.register_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 10px 30px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(self.register_btn)
        layout.addLayout(button_layout)
        
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_error('Please enter username and password')
            return
        
        self.login_btn.setEnabled(False)
        self.register_btn.setEnabled(False)
        self.status_label.setText('Logging in...')

        if self.worker:
            self.worker.quit()
            self.worker.wait()
        
        self.worker = AuthWorker('/auth/login/', {
            'username': username,
            'password': password
        })
        self.worker.finished.connect(self.on_auth_success)
        self.worker.error.connect(self.on_auth_error)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.worker.deleteLater)
        self.worker.start()
    
    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text()
        
        if not username or not password:
            self.show_error('Please enter username and password')
            return
        
        self.login_btn.setEnabled(False)
        self.register_btn.setEnabled(False)
        self.status_label.setText('Registering...')
        
        if self.worker:
            self.worker.quit()
            self.worker.wait()
        
        self.worker = AuthWorker('/auth/register/', {
            'username': username,
            'password': password,
            'email': email
        })
        self.worker.finished.connect(self.on_auth_success)
        self.worker.error.connect(self.on_auth_error)
        # Clean up after thread finishes
        self.worker.finished.connect(lambda: self.cleanup_worker())
        self.worker.error.connect(lambda: self.cleanup_worker())
        self.worker.start()
    
    def cleanup_worker(self):
        """Safely cleanup worker thread"""
        if self.worker:
            self.worker.quit()
            self.worker.wait()
            self.worker = None
    
    def on_auth_success(self, data):
        token = data.get('token')
        self.login_success.emit(token)
        self.username_input.clear()
        self.password_input.clear()
        self.email_input.clear()
        self.status_label.setText('')
        self.login_btn.setEnabled(True)
        self.register_btn.setEnabled(True)
    
    def on_auth_error(self, error):
        self.show_error(error)
        self.login_btn.setEnabled(True)
        self.register_btn.setEnabled(True)
        self.status_label.setText('')
    
    def show_error(self, message):
        QMessageBox.warning(self, 'Error', message)


class MainWidget(QWidget):
    """Main application widget"""
    logout = pyqtSignal()
    
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.headers = {'Authorization': f'Token {token}'}
        self.selected_dataset = None
        self.init_ui()
        self.load_datasets()
    
    def init_ui(self):
        main_layout = QHBoxLayout()
        
        # Left sidebar
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()
        sidebar.setMaximumWidth(300)
        
        # Upload section
        upload_group = QGroupBox('Upload CSV')
        upload_layout = QVBoxLayout()
        
        self.upload_btn = QPushButton('Select File')
        self.upload_btn.clicked.connect(self.select_file)
        upload_layout.addWidget(self.upload_btn)
        
        self.file_label = QLabel('No file selected')
        self.file_label.setWordWrap(True)
        upload_layout.addWidget(self.file_label)
        
        self.upload_submit_btn = QPushButton('Upload')
        self.upload_submit_btn.clicked.connect(self.upload_file)
        self.upload_submit_btn.setEnabled(False)
        upload_layout.addWidget(self.upload_submit_btn)
        
        upload_group.setLayout(upload_layout)
        sidebar_layout.addWidget(upload_group)
        
        # Dataset history
        history_group = QGroupBox('Recent Datasets (Last 5)')
        history_layout = QVBoxLayout()
        
        self.dataset_list = QListWidget()
        self.dataset_list.itemClicked.connect(self.on_dataset_selected)
        history_layout.addWidget(self.dataset_list)
        
        history_group.setLayout(history_layout)
        sidebar_layout.addWidget(history_group)
        
        # Logout button
        logout_btn = QPushButton('Logout')
        logout_btn.clicked.connect(self.logout.emit)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        sidebar_layout.addWidget(logout_btn)
        
        sidebar.setLayout(sidebar_layout)
        main_layout.addWidget(sidebar)
        
        # Main content area
        content = QWidget()
        content_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        self.title_label = QLabel('Welcome!')
        self.title_label.setFont(QFont('Arial', 16, QFont.Bold))
        header_layout.addWidget(self.title_label)
        
        self.pdf_btn = QPushButton('Download PDF Report')
        self.pdf_btn.clicked.connect(self.download_pdf)
        self.pdf_btn.hide()
        header_layout.addWidget(self.pdf_btn)
        
        content_layout.addLayout(header_layout)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        scroll_content.setLayout(self.scroll_layout)
        scroll.setWidget(scroll_content)
        content_layout.addWidget(scroll)
        
        content.setLayout(content_layout)
        main_layout.addWidget(content, 1)
        
        self.setLayout(main_layout)
        self.selected_file = None
    
    def load_datasets(self):
        worker = DataWorker('GET', f'{API_URL}/datasets/', self.headers)
        worker.finished.connect(self.on_datasets_loaded)
        worker.error.connect(self.show_error)
        worker.start()
    
    def on_datasets_loaded(self, data):
        self.dataset_list.clear()
        for ds in data:
            item_text = f"{ds['filename']}\n{ds['uploaded_at'][:16]}\n{ds['total_records']} records"
            self.dataset_list.addItem(item_text)
            self.dataset_list.item(self.dataset_list.count() - 1).setData(Qt.UserRole, ds['id'])
    
    def select_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')
        if filename:
            self.selected_file = filename
            self.file_label.setText(filename.split('/')[-1])
            self.upload_submit_btn.setEnabled(True)
    
    def upload_file(self):
        if not self.selected_file:
            return
        
        self.upload_btn.setEnabled(False)
        self.upload_submit_btn.setEnabled(False)
        
        with open(self.selected_file, 'rb') as f:
            files = {'file': f}
            worker = DataWorker('POST', f'{API_URL}/datasets/upload/', 
                              self.headers, files=files)
            worker.finished.connect(self.on_upload_success)
            worker.error.connect(self.on_upload_error)
            worker.start()
    
    def on_upload_success(self, data):
        self.selected_dataset = data
        self.display_dataset(data)
        self.load_datasets()
        self.file_label.setText('No file selected')
        self.selected_file = None
        self.upload_btn.setEnabled(True)
        self.upload_submit_btn.setEnabled(False)
        QMessageBox.information(self, 'Success', 'File uploaded successfully!')
    
    def on_upload_error(self, error):
        self.show_error(error)
        self.upload_btn.setEnabled(True)
        self.upload_submit_btn.setEnabled(False)
    
    def on_dataset_selected(self, item):
        dataset_id = item.data(Qt.UserRole)
        worker = DataWorker('GET', f'{API_URL}/datasets/{dataset_id}/summary/', 
                          self.headers)
        worker.finished.connect(self.display_dataset)
        worker.error.connect(self.show_error)
        worker.start()
    
    def display_dataset(self, data):
        self.selected_dataset = data
        
        # Clear existing content
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.title_label.setText(data['filename'])
        self.pdf_btn.show()
        
        # Stats
        stats_widget = QWidget()
        stats_layout = QHBoxLayout()
        
        stats = [
            ('Total Records', data['total_records']),
            ('Avg Flowrate', f"{data['avg_flowrate']:.2f}"),
            ('Avg Pressure', f"{data['avg_pressure']:.2f}"),
            ('Avg Temperature', f"{data['avg_temperature']:.2f}")
        ]
        
        for label, value in stats:
            stat_widget = QWidget()
            stat_layout = QVBoxLayout()
            
            label_widget = QLabel(label)
            label_widget.setFont(QFont('Arial', 10))
            value_widget = QLabel(str(value))
            value_widget.setFont(QFont('Arial', 16, QFont.Bold))
            
            stat_layout.addWidget(label_widget)
            stat_layout.addWidget(value_widget)
            stat_widget.setLayout(stat_layout)
            stat_widget.setStyleSheet("""
                QWidget {
                    background-color: #667eea;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                }
            """)
            stats_layout.addWidget(stat_widget)
        
        stats_widget.setLayout(stats_layout)
        self.scroll_layout.addWidget(stats_widget)
        
        # Charts
        chart_widget = QWidget()
        chart_layout = QHBoxLayout()
        
        # Average values chart
        avg_chart = ChartWidget()
        avg_chart.plot_bar_chart(
            ['Flowrate', 'Pressure', 'Temperature'],
            [data['avg_flowrate'], data['avg_pressure'], data['avg_temperature']],
            'Average Parameter Values'
        )
        chart_layout.addWidget(avg_chart)
        
        # Type distribution chart
        if data.get('type_distribution'):
            type_chart = ChartWidget()
            types = list(data['type_distribution'].keys())
            counts = list(data['type_distribution'].values())
            type_chart.plot_pie_chart(types, counts, 'Equipment Type Distribution')
            chart_layout.addWidget(type_chart)
        
        chart_widget.setLayout(chart_layout)
        self.scroll_layout.addWidget(chart_widget)
        
        # Table
        table_label = QLabel('Equipment Details')
        table_label.setFont(QFont('Arial', 14, QFont.Bold))
        self.scroll_layout.addWidget(table_label)
        
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        
        equipment = data.get('equipment', [])
        table.setRowCount(len(equipment))
        
        for i, eq in enumerate(equipment):
            table.setItem(i, 0, QTableWidgetItem(eq['equipment_name']))
            table.setItem(i, 1, QTableWidgetItem(eq['equipment_type']))
            table.setItem(i, 2, QTableWidgetItem(f"{eq['flowrate']:.2f}"))
            table.setItem(i, 3, QTableWidgetItem(f"{eq['pressure']:.2f}"))
            table.setItem(i, 4, QTableWidgetItem(f"{eq['temperature']:.2f}"))
        
        table.resizeColumnsToContents()
        self.scroll_layout.addWidget(table)
    
    def download_pdf(self):
        if not self.selected_dataset:
            return
        
        dataset_id = self.selected_dataset['id']
        
        try:
            response = requests.get(
                f'{API_URL}/datasets/{dataset_id}/generate_pdf/',
                headers=self.headers
            )
            
            if response.status_code == 200:
                filename, _ = QFileDialog.getSaveFileName(
                    self, 'Save PDF', f'equipment_report_{dataset_id}.pdf',
                    'PDF Files (*.pdf)'
                )
                
                if filename:
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    QMessageBox.information(self, 'Success', 'PDF downloaded successfully!')
            else:
                self.show_error('Failed to download PDF')
        except Exception as e:
            self.show_error(str(e))
    
    def show_error(self, message):
        QMessageBox.warning(self, 'Error', message)


class MainWindow(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chemical Equipment Parameter Visualizer')
        self.setGeometry(100, 100, 1200, 800)
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # Login widget
        self.login_widget = LoginWidget()
        self.login_widget.login_success.connect(self.on_login_success)
        self.stack.addWidget(self.login_widget)
        
        self.main_widget = None
    
    def on_login_success(self, token):
        if self.main_widget:
            self.stack.removeWidget(self.main_widget)
        
        self.main_widget = MainWidget(token)
        self.main_widget.logout.connect(self.on_logout)
        self.stack.addWidget(self.main_widget)
        self.stack.setCurrentWidget(self.main_widget)
    
    def on_logout(self):
        self.stack.setCurrentWidget(self.login_widget)

   


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

class MainWindow(QMainWindow):
    # ... existing code ...
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Stop any running workers
        if hasattr(self, 'main_widget') and self.main_widget:
            if hasattr(self.main_widget, 'worker'):
                if self.main_widget.worker and self.main_widget.worker.isRunning():
                    self.main_widget.worker.quit()
                    self.main_widget.worker.wait(1000)
        event.accept()