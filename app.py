from pickle import FALSE
from re import T
import sys
from PySide6.QtWidgets import QApplication, QMainWindow,QMessageBox,QFileDialog,QLineEdit
from PySide6.QtCore import QFile
from PySide6.QtCore import Slot
#from numpy import equal
#from pyparsing import empty
from lzss_io import PZYPContext
from ui.app import Ui_MainWindow
import PZYP

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        msg = QMessageBox()
        self.ui.txtPass.setEchoMode(QLineEdit.Password)
        self.ui.txtConf_Pass.setEchoMode(QLineEdit.Password)
        #Class Functions
        def get_pw():
            if self.ui.checkPw.isChecked():
                if self.ui.txtPass.text() == self.ui.txtConf_Pass.text() and self.ui.txtPass.text() != '':
                    return self.ui.txtConf_Pass.text()
                else:
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("A password está vazia ou não coincide.")
                    msg.show()
                    return "error"
        
        def get_operation():
            if self.ui.rBtnCompressao.isChecked() or self.ui.rBtnDescompressao.isChecked():
                if self.ui.rBtnCompressao.isChecked():
                    return "compress"
                elif self.ui.rBtnDescompressao.isChecked():
                    return "uncompress"
            else:
                msg.setIcon(QMessageBox.Information)
                msg.setText("Não selecionou nenhuma opção (comprimir ou descomprimir).")
                msg.show()
                return "error"
        
        def get_level():
            return self.ui.horizontalSlider.value()

        def get_summary():
            if self.ui.checkSummary.isChecked():
                return (bool(True))
            return(bool(False))

        def get_file():
            while True:
                if get_operation() == 'error':
                    break
                elif get_operation() == 'compress':
                    fname = QFileDialog.getOpenFileName(self, 'Open file', "All Files")
                    self.ui.progressBar.setValue(0)
                    self.ui.lblfile.setText(str(fname[0]))
                    break
                elif get_operation() == 'uncompress':
                    fname = QFileDialog.getOpenFileName(self, 'Open file', "*.lzs")
                    self.ui.progressBar.setValue(0)
                    self.ui.lblfile.setText(str(fname[0]))
                    break
 
        def get_file_name():
            if self.ui.lblfile.text() != '...' or '':
                fname = self.ui.lblfile.text()
                return fname
            else:
                msg.setIcon(QMessageBox.Information)
                msg.setText("Não selecionou nenhum ficheiro.")
                msg.show()
                return "error"

        def send_settings():
            while(True):
                if get_pw() == 'error':
                    break
                if get_operation() == 'error':
                    break
                if get_file_name() == 'error':
                    break
                else:
                    PZYP.ui_main(get_operation(),get_level(),get_pw(),get_summary(),get_file_name())
                    msg.setIcon(QMessageBox.Information)
                    msg.setText(PZYP.status())
                    msg.exec()
                    self.ui.progressBar.setValue(100)
                    #Inteface reset
                    if msg.close():
                        self.ui.checkPw.setChecked(False)
                        self.ui.checkSummary.setChecked(False)
                        self.ui.txtPass.clear()
                        self.ui.txtConf_Pass.clear()
                        self.ui.lblfile.setText('...')
                    break
        
        self.ui.checkPw.stateChanged.connect(self.ui.txtPass.setEnabled)
        self.ui.checkPw.stateChanged.connect(self.ui.txtConf_Pass.setEnabled)
        self.ui.horizontalSlider.valueChanged.connect(self.ui.lbllvl.setNum)
        self.ui.rBtnCompressao.clicked["bool"].connect(self.ui.rBtnCompressao.setChecked)
        self.ui.rBtnDescompressao.clicked["bool"].connect(self.ui.rBtnDescompressao.setChecked)
        self.ui.btnStart.clicked.connect(send_settings)
        self.ui.btnfile.clicked.connect(get_file)
        self.ui.checkSummary.stateChanged.connect(self.ui.checkSummary.setChecked)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

    