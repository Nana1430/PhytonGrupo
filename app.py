from pickle import FALSE
from re import T
import sys
from PySide6.QtWidgets import QApplication, QMainWindow,QMessageBox,QFileDialog,QLineEdit
from PySide6.QtCore import QFile
from PySide6.QtCore import Slot
#from numpy import equal
#from pyparsing import empty
from lzss_io import PZYPContext
import app_ui 
import PZYP

class MainWindow(QMainWindow, app_ui.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        msg = QMessageBox()
        self.txtPass.setEchoMode(QLineEdit.Password)
        self.txtConf_Pass.setEchoMode(QLineEdit.Password)
        #Class Functions
        def get_pw():
            if self.checkPw.isChecked():
                if self.txtPass.text() == self.txtConf_Pass.text() and self.txtPass.text() != '':
                    return self.txtConf_Pass.text()
                else:
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("A password está vazia ou não coincide.")
                    msg.show()
                    return "error"
        
        def get_operation():
            if self.rBtnCompressao.isChecked() or self.rBtnDescompressao.isChecked():
                if self.rBtnCompressao.isChecked():
                    return "compress"
                elif self.rBtnDescompressao.isChecked():
                    return "uncompress"
            else:
                msg.setIcon(QMessageBox.Information)
                msg.setText("Não selecionou nenhuma opção (comprimir ou descomprimir).")
                msg.show()
                return "error"
        
        def get_level():
            return self.horizontalSlider.value()

        def get_summary():
            if self.checkSummary.isChecked():
                return (bool(True))
            return(bool(False))

        def get_file():
            while True:
                if get_operation() == 'error':
                    break
                elif get_operation() == 'compress':
                    fname = QFileDialog.getOpenFileName(self, 'Open file', "All Files")
                    self.progressBar.setValue(0)
                    self.lblfile.setText(str(fname[0]))
                    break
                elif get_operation() == 'uncompress':
                    fname = QFileDialog.getOpenFileName(self, 'Open file', "*.lzs")
                    self.progressBar.setValue(0)
                    self.lblfile.setText(str(fname[0]))
                    break
 
        def get_file_name():
            if self.lblfile.text() != '...' or '':
                fname = self.lblfile.text()
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
                    self.progressBar.setValue(100)
                    msg.setIcon(QMessageBox.Information)
                    msg.setText(PZYP.status())
                    msg.exec()                    
                    #Inteface reset
                    if msg.close():
                        self.checkPw.setChecked(False)
                        self.checkSummary.setChecked(False)
                        self.txtPass.clear()
                        self.txtConf_Pass.clear()
                        self.rBtnCompressao.setChecked(False)
                        self.rBtnDescompressao.setChecked(False)                        
                        self.lblfile.setText('...')
                    break
        
        self.checkPw.stateChanged.connect(self.txtPass.setEnabled)
        self.checkPw.stateChanged.connect(self.txtConf_Pass.setEnabled)
        self.horizontalSlider.valueChanged.connect(self.lbllvl.setNum)
        self.rBtnCompressao.clicked["bool"].connect(self.rBtnCompressao.setChecked)
        self.rBtnDescompressao.clicked["bool"].connect(self.rBtnDescompressao.setChecked)
        self.btnStart.clicked.connect(send_settings)
        self.btnfile.clicked.connect(get_file)
        self.checkSummary.stateChanged.connect(self.checkSummary.setChecked)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

    