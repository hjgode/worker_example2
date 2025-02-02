import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QProgressBar
from PyQt5.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
import time


class Worker(QObject):
    progress = Signal(int)
    completed = Signal(int)
    finished = Signal()

    @Slot(int)
    def do_work(self, n):
        for i in range(1, n+1):
            time.sleep(1)
            self.progress.emit(i)

        self.completed.emit(i)
        self.finished.emit()


class FileTransferWindow(QMainWindow):
    work_requested = Signal(int)
    finished = Signal

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setGeometry(100, 100, 300, 50)
        self.setWindowTitle('QThread Demo')

        # setup widget
        self.widget = QWidget()
        layout = QVBoxLayout()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)       

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)

        self.btn_start = QPushButton('Start', clicked=self.start)

        layout.addWidget(self.progress_bar)
        layout.addWidget(self.btn_start)

        self.worker = Worker()
        self.worker_thread = QThread()

        self.worker.progress.connect(self.update_progress)
        self.worker.completed.connect(self.complete)

        self.work_requested.connect(self.worker.do_work)

        # move worker to the worker thread
        self.worker.moveToThread(self.worker_thread)

        # start the thread
        self.worker_thread.start()
        #self.worker_thread.finished.connect(self.finished)
        #self.worker.finished.connect(self.worker_thread.quit)
        # show the window
#        self.show()

    def start(self):
        self.btn_start.setEnabled(False)
        n = 5
        self.progress_bar.setMaximum(n)
        self.work_requested.emit(n)

    def update_progress(self, v):
        self.progress_bar.setValue(v)

    def complete(self, v):
        self.progress_bar.setValue(v)
        self.btn_start.setEnabled(True)

    def close(self):
        
        self.worker_thread.quit()      
        self.worker_thread.wait()
'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileTransferWindow()
    sys.exit(app.exec())
'''