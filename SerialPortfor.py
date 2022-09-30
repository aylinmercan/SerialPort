import sys
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets,QtGui,QtCore
 
class serialThreadClass(QtCore.QThread):  # Seri Porttan veri okuma işlemi için QThread Kullanıldı.
 
    message = QtCore.pyqtSignal(str)
    def __init__(self,parent = None):
 
        super(serialThreadClass,self).__init__(parent)
        self.serialPort = serial.Serial()
        self.stopflag = False
    def stop(self):
        self.stopflag = True
    def run(self):
        while True:
            if (self.stopflag):
                self.stopflag = False
                break
            elif(self.serialPort.isOpen()): # eğer seri Port bağlı değil iken veri okumayı denersek hata verir.
                try:                        # bu hatayı yakalayabilmek için "try" bloğu kullanıldı.
                    self.data = self.serialPort.readline()
                except:
                    print("HATA\n")
                self.message.emit(str(self.data.decode()))
class Pencere(QtWidgets.QWidget):  # arayüz sınıfı
    def __init__(self):
        super().__init__()
        self.initUi()
 
    def initUi(self):
        ############### Com Port Combo box ###############
        self.portComboBox = QtWidgets.QComboBox()
        self.ports = serial.tools.list_ports.comports() # Com portlar listelendi.
        for i in self.ports:
            self.portComboBox.addItem(str(i))
        ################### Baudrate Combo Box########################
        self.baudComboBox = QtWidgets.QComboBox()
        baud = ["300", "1200", "2400", "4800", "9600", "19200", "38400", "57600", "74880", "115200", "230400", "250000",
                "500000", "1000000", "2000000"]
        for i in baud:
            self.baudComboBox.addItem(i)  # baud dizisinin içerisindeki değerler eklendi.
        self.baudComboBox.setCurrentText(baud[4]) # pencere ilk açıldığında baudrate 9600 olsun.
        ########################## Butonlar ##################################
 
        self.baglan = QtWidgets.QPushButton("Bağlan")
        self.baglantiKes = QtWidgets.QPushButton("Bağlantıyı Kes")
        self.led1on = QtWidgets.QPushButton("LED1 ON")
        self.led1off = QtWidgets.QPushButton("LED1 OFF")
        self.led2on = QtWidgets.QPushButton("LED2 ON")
        self.led2off = QtWidgets.QPushButton("LED2 OFF")
        self.led3on = QtWidgets.QPushButton("LED3 ON")
        self.led3off = QtWidgets.QPushButton("LED3 OFF")
        self.led4on = QtWidgets.QPushButton("LED4 ON")
        self.led4off = QtWidgets.QPushButton("LED4 OFF")
 
        ######################################################################
        self.label1 = QtWidgets.QLabel('<font color=red>COM port bağlı değil!!!</font>')# böyle yazıldığı zaman yazı rengi kırmızı olacak.
 
        portVbox = QtWidgets.QVBoxLayout()
        portVbox.addWidget(self.portComboBox)
        portVbox.addWidget(self.baudComboBox)
        portVbox.addWidget(self.baglan)
        portVbox.addWidget(self.baglantiKes)
        portVbox.addWidget(self.label1)
 
        self.portGroup = QtWidgets.QGroupBox("Port Seçme")
        self.portGroup.setLayout(portVbox)
 
        buttonHbox1 = QtWidgets.QHBoxLayout()
        buttonHbox1.addWidget(self.led1on)
        buttonHbox1.addWidget(self.led1off)
 
        buttonHbox2 = QtWidgets.QHBoxLayout()
        buttonHbox2.addWidget(self.led2on)
        buttonHbox2.addWidget(self.led2off)
 
        buttonHbox3 = QtWidgets.QHBoxLayout()
        buttonHbox3.addWidget(self.led3on)
        buttonHbox3.addWidget(self.led3off)
 
        buttonHbox4 = QtWidgets.QHBoxLayout()
        buttonHbox4.addWidget(self.led4on)
        buttonHbox4.addWidget(self.led4off)
 
        self.message = QtWidgets.QTextEdit()
        self.message.setReadOnly(True) # bu satırda text edit sadece okunabilir olarak ayarlandı. Yani textedit'in içine yazı yazılamaz.
        self.messageTitle = QtWidgets.QLabel("Gelen Mesaj")
 
        self.title1 = QtWidgets.QLabel('<font color=reds>Python-Arduino Uygulaması</font>')
        self.title1.setFont(QtGui.QFont("Roboto Mono",20,QtGui.QFont.Bold))
        self.title2 = QtWidgets.QLabel("busraaylinmercan@gmail.com / danışman hoca: İlyas Özer")
        self.title2.setFont(QtGui.QFont("Roboto Mono", 10, QtGui.QFont.Normal))
 
        vBox = QtWidgets.QVBoxLayout()
        vBox.addStretch()
        vBox.addWidget(self.title1)
        vBox.addWidget(self.title2)
        vBox.addWidget(self.portGroup)
        vBox.addLayout(buttonHbox1)
        vBox.addLayout(buttonHbox2)
        vBox.addLayout(buttonHbox3)
        vBox.addLayout(buttonHbox4)
        vBox.addWidget(self.messageTitle)
        vBox.addWidget(self.message)
        vBox.addStretch()
 
        hBox = QtWidgets.QHBoxLayout()
        hBox.addStretch()
        hBox.addLayout(vBox)
        hBox.addStretch()
 
 
        self.setLayout(hBox)
        self.setWindowTitle("ArdunioPy")
        self.mySerial = serialThreadClass()  # pencere sınıfının içerisinde serialThreadClass nesnesi oluşturuldu.
        self.mySerial.message.connect(self.messageTextEdit)  # seri porttan mesaj geldiğinde messageTextEdit fonksiyonuna dallan.
        self.mySerial.start()                #thread işlemi başlatıldı.
 
        self.baglan.clicked.connect(self.serialConnect) # Butona tıklandığında serialConnection isimli fonksiyona dallan.
        self.baglantiKes.clicked.connect(self.serialDisconnect)
        self.led1on.clicked.connect(lambda: self.leds(self.led1on))   # hangi led butonuna tıklanırsa tıklansın program
        self.led1off.clicked.connect(lambda: self.leds(self.led1off)) # tek bir fonksiyona dallanacak.
        self.led2on.clicked.connect(lambda: self.leds(self.led2on))   # Bu yüzden leds fonksiyonunun içine buton parametresi
        self.led2off.clicked.connect(lambda: self.leds(self.led2off)) # yazıldı.
        self.led3on.clicked.connect(lambda: self.leds(self.led3on))
        self.led3off.clicked.connect(lambda: self.leds(self.led3off))
        self.led4on.clicked.connect(lambda: self.leds(self.led4on))
        self.led4off.clicked.connect(lambda: self.leds(self.led4off))
 
 
        self.show()
    def serialConnect(self): # "Bağlan" butonuna tıklandığında bu fonksiyona dallanacak.
        self.portText = self.portComboBox.currentText() # port combobox'ın içinde hangi değer varsa çekildi.
        self.port = self.portText.split() # combo box'ın içerisinde bize lazım olan sadece "COM13" kısmı. Bu yüzden split ile kelimeler ayrıldı.
        self.baudrate = self.baudComboBox.currentText()# comboBox'ın içindeki baudrate değeri çekildi.
        self.mySerial.serialPort.baudrate = int(self.baudrate) # seriport baudrate ayarı tanımlandı.
        self.mySerial.serialPort.port = self.port[0]
        try:
            self.mySerial.serialPort.open() # seri porta bağlanma komutu verildi.
        except:
            self.message.append("Bağlantı Hatası!!")
        if(self.mySerial.serialPort.isOpen()):
            self.label1.setText('<font color=green>Bağlandı</font>') # bağlantı sağlandıysa label1 yeşile dönsün.
            self.baglan.setEnabled(False)       # Bağlantı varken tekrar bağlan butonuna tıklanmasın diye butonu pasif ediyoruz.
            self.portComboBox.setEnabled(False) # Bağlantı varken port ve baudrate seçimi yapılmasın diye
            self.baudComboBox.setEnabled(False) # kullanıcının seçim yapmasını engelliyoruz.
 
    def serialDisconnect(self): # "Bağlantı Kes" butonuna tıklandığında bu fonksiyona dallanacak.
        if self.mySerial.serialPort.isOpen():
            self.mySerial.serialPort.close()
            if self.mySerial.serialPort.isOpen()== False:
                self.label1.setText('<font color=blue>Bağlantı Kesildi</font>')
                self.baglan.setEnabled(True)
                self.portComboBox.setEnabled(True)
                self.baudComboBox.setEnabled(True)
        else:
            self.message.append("Seriport Zaten Kapalı.")
    def messageTextEdit(self):  # seri porttan mesaj geldiğinde bu fonksiyon çalıştırılacak.
        self.incomingMessage = str(self.mySerial.data.decode())
        self.message.append(self.incomingMessage)
    def leds(self,led): # led butonlarından herhangi birine tıklandığında  bu fonksiyona dallanacak.
        if led == self.led1on:
            if self.mySerial.serialPort.isOpen():
                self.mySerial.serialPort.write("1".encode())  # seri porttan Arduino'ya 1 karakteri gönderildi.
            else:
                self.message.append("Seri Port Bağlı Değil.")
        elif led == self.led1off:
            if self.mySerial.serialPort.isOpen():
                self.mySerial.serialPort.write("2".encode())
            else:
                self.message.append("Seri Port Bağlı Değil.")
        elif led == self.led2on:
            if self.mySerial.serialPort.isOpen():
                self.mySerial.serialPort.write("3".encode())
            else:
                self.message.append("Seri Port Bağlı Değil.")
        elif led == self.led2off:
            if self.mySerial.serialPort.isOpen():
                self.mySerial.serialPort.write("4".encode())
            else:
                self.message.append("Seri Port Bağlı Değil.")
        elif led == self.led3on:
            if self.mySerial.serialPort.isOpen():
                self.mySerial.serialPort.write("5".encode())
            else:
                self.message.append("Seri Port Bağlı Değil.")
        elif led == self.led3off:
            if self.mySerial.serialPort.isOpen():
                self.mySerial.serialPort.write("6".encode())
            else:
                self.message.append("Seri Port Bağlı Değil.")
        elif led == self.led4on:
            if self.mySerial.serialPort.isOpen():
                self.mySerial.serialPort.write("7".encode())
            else:
                self.message.append("Seri Port Bağlı Değil.")
        elif led == self.led4off:
            if self.mySerial.serialPort.isOpen():
                self.mySerial.serialPort.write("8".encode())
            else:
                self.message.append("Seri Port Bağlı Değil.")
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    pen = Pencere()
    sys.exit(app.exec_())
        
