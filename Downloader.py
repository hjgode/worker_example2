from urllib.request import urlopen

from PyQt5.QtCore import QThread, pyqtSignal, QMutex
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtWidgets import QProgressBar


class Downloader(QThread):

    # Signal for the window to establish the maximum value
    # of the progress bar.
    signal_setTotalProgress = pyqtSignal(int)
    # Signal to increase the progress.
    signal_setCurrentProgress = pyqtSignal(int)
    # Signal to be emitted when the file has been downloaded successfully.
    signal_succeeded = pyqtSignal()

    myMutex=QMutex()

    myStopThread=False

    def __init__(self, url, filename):
        super().__init__()
        self._url = url
        self._filename = filename

    def stopDownload(self):
        self.myMutex.lock()
        self.myStopThread=True
        self.myMutex.unlock()
        pass
    
    def run(self):
        url = "https://www.python.org/ftp/python/3.7.2/python-3.7.2.exe"
        filename = "python-3.7.2.exe"
        readBytes = 0
        chunkSize = 1024
        # Open the URL address.
        with urlopen(url) as r:
            # Tell the window the amount of bytes to be downloaded.
            self.signal_setTotalProgress.emit(int(r.info()["Content-Length"]))
            stopThread=False
            with open(filename, "ab") as f:
                while True and not stopThread:
                  self.myMutex.lock()
                  stopThread=self.myStopThread
                  self.myMutex.unlock()
                  if self.myStopThread:
                      print("QThread quit()...")
                      self.quit()
                      
                  # Read a piece of the file we are downloading.
                  chunk = r.read(chunkSize)
                  # If the result is `None`, that means data is not
                  # downloaded yet. Just keep waiting.
                  if chunk is None:
                      continue
                  # If the result is an empty `bytes` instance, then
                  # the file is complete.
                  elif chunk == b"":
                      break
                  # Write into the local file the downloaded chunk.
                  f.write(chunk)
                  readBytes += chunkSize
                  # Tell the window how many bytes we have received.
                  self.signal_setCurrentProgress.emit(readBytes)
        # If this line is reached then no exception has ocurred in
        # the previous lines.
        self.signal_succeeded.emit()

class DownloadWindow(QMainWindow):
    # Signal for the caller window to establish the maximum value
    # of the progress bar.
    signal_startDownload = pyqtSignal(int)
    # Signal to increase the progress.
    #signal_setCurrentProgress = pyqtSignal(int)
    # Signal to be emitted when the file has been downloaded successfully.
    signal_DownloadSucceeded = pyqtSignal()
    # Signal to be emitted when finished.
    signal_DownloadFinshed = pyqtSignal()
    signal_DownloadStop = pyqtSignal()
    signal_DownloadStarted = pyqtSignal()

    downloader=None
    remote_file=""
    local_file=""

    def __init__(self, download_url:str, localfile:str):
        super().__init__()
        self.remote_file=download_url
        self.local_file=localfile
        self.setWindowTitle("Download with progress in PyQt")
        self.resize(400, 300)
        self.label = QLabel("Press the button to start downloading.", self)
        self.label.setGeometry(20, 20, 200, 25)
        self.button = QPushButton("Start download", self)
        self.button.move(20, 60)
        self.button.pressed.connect(self.startDownload)
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(20, 115, 300, 25)

    def stopDownload(self):
        print("stopDownload called")
        if self.downloader!=None:
            self.downloader.stopDownload()    
            self.downloader.wait()
        pass
    
    def startDownload(self):
        self.label.setText("Downloading file...")
        # Disable the button while the file is downloading.
        self.button.setEnabled(False)
        # Run the download in a new thread.
        self.downloader = Downloader(self.remote_file, self.local_file)
        #    "https://www.python.org/ftp/python/3.7.2/python-3.7.2.exe",
        #    "python-3.7.2.exe" )
        # Connect the signals which send information about the download
        # progress with the proper methods of the progress bar.
        self.downloader.signal_setTotalProgress.connect(self.progressBar.setMaximum)
        self.downloader.signal_setCurrentProgress.connect(self.progressBar.setValue)
        # Qt will invoke the `signal_succeeded()` method when the file has been
        # downloaded successfully and `downloadFinished()` when the
        # child thread finishes.
        self.downloader.signal_succeeded.connect(self.downloadSucceeded)
        self.downloader.finished.connect(self.downloadFinished)
        #self.downloader.signal_.connect(self.stopDownload)
        self.downloader.start()
        self.signal_DownloadStarted.emit()

    def downloadSucceeded(self):
        # Set the progress at 100%.
        self.progressBar.setValue(self.progressBar.maximum())
        self.label.setText("The file has been downloaded!")
        self.signal_DownloadSucceeded.emit()

    def downloadFinished(self):
        # Restore the button.
        self.button.setEnabled(True)
        
        # Delete the thread when no longer needed.
        del self.downloader


#if __name__ == "__main__":
#    app = QApplication([])
#    window = MainWindow()
#    window.show()
#    app.exec()

