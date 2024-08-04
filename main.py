from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys

from worker_win import FileTransferWindow
from Downloader import DownloadWindow

class MainWindow(QMainWindow):
    remote="https://www.python.org/ftp/python/3.7.2/python-3.7.2.exe"
    local="python-3.7.2.exe"
    def __init__(self):
        super().__init__()
        self.w = None  # No external window yet.
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    def show_new_window(self, checked):
        if self.w is None:
            self.w = DownloadWindow(download_url=self.remote, localfile=self.local)# FileTransferWindow()
            self.w.show()
            # connect to the signals emitted by the class
            self.w.signal_startDownload.connect(self.downloadStarted)
            self.w.signal_DownloadSucceeded.connect(self.downloadSucceeded)
            self.w.signal_DownloadFinshed.connect(self.downloadFinished)
            self.w.signal_DownloadStarted.connect(self.downloadStarted)
            self.w.signal_DownloadFinshed.connect(self.download_finished)
            self.w.signal_DownloadFailed.connect(self.downloadFailed)
            # start the download
            self.w.startDownload()

        else:
            self.w.stopDownload()
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

    def downloadFailed(self, reason:str):
      print("MainWindow: downloadFailed, reason="+reason)
      pass
     

    def download_finished(self):
      print("MainWindow: downloadFinished")
      pass
     
    def downloadStarted(self):
      print("MainWindow: downloadStarted")
      pass
    def downloadFinished(self):
      print("MainWindow: downloadFinishedd")
      pass
    def downloadSucceeded(self):
      print("MainWindow: downloadSucceeded")
      self.w.close()
      self.w=None
      pass

    ## close downloader win if any
    def closeEvent(self, event):
        # do stuff
      if self.w!=None:
        self.w.close()
      event.accept()
      #event.ignore()

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()