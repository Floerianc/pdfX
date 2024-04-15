import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from GUI_v4 import *
import PyPDF2
import os

class Application(Ui_MainWindow):
    def __init__(self, Form) -> None:
        super().__init__()
        self.pdfs = []
        self.added_pdfs = 0
        self.scans_range = False
        self.scans_one_page = False
        self.setupUi(Form)
        self.OpenButton.clicked.connect(self.open_file)
        self.DeleteButton.clicked.connect(self.delete_entry)
        self.ScanButton.clicked.connect(self.scan_pdfs)
    
    def open_file(self):
        if self.added_pdfs < 5:
            widget = QtWidgets.QWidget()
            option = QFileDialog.Options()
            try:
                file = QFileDialog.getOpenFileName(widget, "Open File", "C:\\", "PDF files (*.pdf)", options=option)
                self.pdfs.append(file[0])
                self.added_pdfs += 1
                self.PdfList.addItem(f"{file[0]}")
            
            except Exception as e:
                print(e)
        else:
            return
        
    
    def delete_entry(self):
        if self.added_pdfs <= 0:
            return
        else:
            pass
        try:
            self.added_pdfs -= 1
            self.PdfList.takeItem(self.added_pdfs+2)
            self.pdfs.remove(self.pdfs[self.added_pdfs-1])
        except Exception as e:
            print(e)
    
    def scan_pdfs(self):
        start_page = 0
        last_page = 0
        try:
            start_page = self.textEdit.toPlainText()
            sp_int = int(start_page)
            last_page = self.textEdit_2.toPlainText()
            lp_int = int(last_page)
        except Exception as e:
            sp_int = 0
            lp_int = 0
            print(e)

        if len(self.pdfs) == 0:
            return
        
        if sp_int == 0 and lp_int == 0:
            self.scans_range = False
            pass
        else:
            if sp_int > lp_int:
                return
            elif sp_int == lp_int:
                pdf_pages = sp_int
                self.scans_one_page = True
                self.scans_range = True
            else:
                self.scans_range = True
                pass

        current_dir = os.path.abspath(os.getcwd())
        for i in range(len(self.pdfs)):
            txt_name = f"{current_dir}\\PDF {i+1}.txt"
            pdf = self.pdfs[i]
            content = PyPDF2.PdfReader(pdf)
            pdf_pages = len(content.pages)
            
            def scan_range_pages():
                with open(txt_name, "w", encoding="UTF-8") as txt_range:
                    for l in range(sp_int-1,lp_int-1):
                        current_page = content.pages[l]
                        page_content = current_page.extract_text()
                        txt_range.write(f"\n\n---------- START OF PAGE {l+1} ----------\n\n")
                        txt_range.write(page_content)
                        txt_range.write(f"\n\n---------- END OF PAGE {l+1} ----------\n\n")

            def scan_all_pages():
                with open(txt_name, "w", encoding="UTF-8") as txt:
                    for k in range(pdf_pages):
                        current_page = content.pages[k]
                        page_content = current_page.extract_text()

                        txt.write(f"\n\n---------- START OF PAGE {k+1} ----------\n\n")
                        txt.write(page_content)
                        txt.write(f"\n\n---------- END OF PAGE {k+1} ----------\n\n")
            
            def scan_one_page():
                with open(txt_name, "w", encoding="UTF-8") as txt_exact:
                    current_page = content.pages[sp_int-1]
                    page_content = current_page.extract_text()

                    txt_exact.write(f"\n\n---------- START OF PAGE {sp_int} ----------\n\n")
                    txt_exact.write(page_content)
                    txt_exact.write(f"\n\n---------- END OF PAGE {sp_int} ----------\n\n")

            if self.scans_range == True:
                if self.scans_one_page == True:
                    scan_one_page()
                else:
                    scan_range_pages()
            else:
                scan_all_pages()

# add custom pages, folder and better design :D

app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QMainWindow()
ui = Application(Form)
Form.show()
app.exec()