# Main file for ThumbnailDownloader program
# Opens GUI that allows you to download or copy the most recent
# video thumbnail of specified user
# Jackson Greene 10/12/2019


from PyQt5.QtWidgets import QMainWindow, QStatusBar, QFrame, QApplication, QTextEdit, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLineEdit, QLabel
from PyQt5.QtCore import QCoreApplication, QMetaObject, QMimeData, QRect, QSize, Qt
from PyQt5.QtGui import QBrush, QClipboard, QColor, QFont, QGuiApplication, QImage, QPalette, QPixmap
from urllib.request import urlopen, urlretrieve
import YouTube
import os


#class that contains the gui for the program
class TDWinUI(object):
    
    #for storing the thumbnail url and iamge data
    imageUrl = None
    thumbnailImage = None


    #set up the ui in the imported window
    def setupUi(self, TDWin):
        
        #window settings
        TDWin.setObjectName("TDWin")
        TDWin.setEnabled(True)
        TDWin.resize(380, 340)
        TDWin.setMinimumSize(QSize(380, 340))
        TDWin.setMaximumSize(QSize(380, 340))
        TDWin.setAutoFillBackground(False)

        #central widget
        self.centralwidget = QWidget(TDWin)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")


        #label for channel name/url
        self.channelUrlLabel = QLabel(self.centralwidget)
        self.channelUrlLabel.setGeometry(QRect(10, 10, 121, 41))
        font = QFont()
        font.setFamily("Yu Gothic Light")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.channelUrlLabel.setFont(font)
        self.channelUrlLabel.setObjectName("channelUrlLabel")

        #box where text gets put in for name/url
        self.channelUrlLineEdit = QLineEdit(self.centralwidget)
        self.channelUrlLineEdit.setGeometry(QRect(132, 20, 110, 21))
        self.channelUrlLineEdit.setObjectName("channelUrlLineEdit")

        #button to retrive thumbnail
        self.retrievePushButton = QPushButton(self.centralwidget)
        self.retrievePushButton.setGeometry(QRect(250, 20, 121, 21))
        self.retrievePushButton.setObjectName("retrievePushButton")


        #label that says preview
        self.previewLabel = QLabel(self.centralwidget)
        self.previewLabel.setGeometry(QRect(10, 50, 131, 41))
        font = QFont()
        font.setFamily("Yu Gothic Light")
        font.setPointSize(10)
        font.setKerning(True)
        self.previewLabel.setFont(font)
        self.previewLabel.setObjectName("previewLabel")

        #label that stores image for thumbnail
        self.previewImageLabel = QLabel(self.centralwidget)
        self.previewImageLabel.setGeometry(QRect(10, 83, 361, 203))
        self.previewImageLabel.setAutoFillBackground(True)
        self.previewImageLabel.setFrameShape(QFrame.Box)
        self.previewImageLabel.setText("")
        self.previewImageLabel.setObjectName("previewImageLabel")


        #button to copy
        self.copyPushButton = QPushButton(self.centralwidget)
        self.copyPushButton.setGeometry(QRect(10, 297, 180, 21))
        self.copyPushButton.setObjectName("copyPushButton")

        #button to save
        self.savePushButton = QPushButton(self.centralwidget)
        self.savePushButton.setGeometry(QRect(196, 297, 119, 21))
        self.savePushButton.setObjectName("savePushButton")


        TDWin.setCentralWidget(self.centralwidget)


        #statusbar for window
        self.statusbar = QStatusBar(TDWin)
        self.statusbar.setObjectName("statusbar")
        TDWin.setStatusBar(self.statusbar)

        #set up names in ui
        self.retranslateUi(TDWin)

        QMetaObject.connectSlotsByName(TDWin)

        #connecting the button presses to functions
        self.retrievePushButton.clicked.connect(lambda: self.retrievePushButtonClicked())
        self.copyPushButton.clicked.connect(lambda: self.copyPushButtonClicked())
        self.savePushButton.clicked.connect(lambda: self.savePushButtonClicked())

        self.statusbar.showMessage("Thumbnail Downloader 1.0 by Jackson Greene", 3000)


    ######## actions for the button presses ######## 
    def retrievePushButtonClicked(self):
        #set class field image url to return url of lastest thumb or None if not exist
        self.imageUrl = YouTube.getThumbnailUrl(self.channelUrlLineEdit.text())
        if (self.imageUrl == None):
            self.setPreviewImageInvalidUrl()
            self.statusbar.showMessage("Name/url was invalid", 4000)
        else:
            self.setPreviewImage(self.imageUrl)
            self.statusbar.showMessage("Thumbnail retreved", 4000)


    def copyPushButtonClicked(self):
        #setting clipboard contents to thumb if it exists
        if (self.imageUrl != None):
            clipboard = QGuiApplication.clipboard() 
            data = QMimeData()
            data.setImageData(self.thumbnailImage)
            clipboard.setMimeData(data)
            self.statusbar.showMessage("Thumbnail copied", 4000)
        else:
            self.statusbar.showMessage("No thumbnail to copy", 4000)
    

    def savePushButtonClicked(self):
        #opens native file explorer and gets name and path to save to
        #then uses that to save thumb to that path
        if (self.imageUrl != None):
            fileName = QFileDialog.getSaveFileName(None, "Save Thumbnail", os.getenv("HOME"), "*.png")
            self.thumbnailImage.save(fileName[0])
            self.statusbar.showMessage(("File saved to " + fileName[0]), 4000)
        else:
            self.statusbar.showMessage("No thumbnail to save", 4000)


    def setPreviewImage(self, imageUrl):
        #opens the url using urlli and reads the data
        with urlopen(imageUrl) as url:
            data = url.read()
        #thumb is a type of image
        self.thumbnailImage = QImage()
        #set thumb to image data form url
        self.thumbnailImage.loadFromData(data)
        self.previewImageLabel.setPixmap((QPixmap(self.thumbnailImage)).scaled(361, 203))
    

    def setPreviewImageInvalidUrl(self):
        #if invalid url load image from resouces file showing it's invalid
        self.thumbnailImage = QImage("./resources/invalidurl.jpg")
        self.previewImageLabel.setPixmap((QPixmap(self.thumbnailImage)).scaled(361, 203))
    ###################################################


    #sets all names of elements to display in ui
    def retranslateUi(self, TDWin):
        _translate = QCoreApplication.translate
        TDWin.setWindowTitle(_translate("TDWin", "Thumbnail Downloader"))
        self.channelUrlLabel.setText(_translate("TDWin", "Channel Name/URL"))
        self.copyPushButton.setText(_translate("TDWin", "Copy To Clipboard (Ctrl+Shift+C)"))
        self.copyPushButton.setShortcut(_translate("TDWin", "Ctrl+Shift+C"))
        self.savePushButton.setText(_translate("TDWin", "Save To File (Ctrl+S)"))
        self.savePushButton.setShortcut(_translate("TDWin", "Ctrl+S"))
        self.previewLabel.setText(_translate("TDWin", "Preview"))
        self.retrievePushButton.setText(_translate("TDWin", "Retrieve Thumbnail"))


#main set up of program
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    TDWin = QMainWindow()
    ui = TDWinUI()
    ui.setupUi(TDWin)
    TDWin.show()
    sys.exit(app.exec_())
