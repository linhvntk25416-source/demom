from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QApplication, QDialog, QInputDialog
from PyQt6.uic import loadUi
import sys
from datetime import datetime
from Cdstaikhoan import Cdstaikhoan
from Cdsnguoihien import Cdsnguoihien
from Cnguoihien import Cnguoihien


class DangNhapWindow(QMainWindow):
    def __init__(self):
        super(DangNhapWindow, self).__init__()
        loadUi('dangnhap.ui', self)
        self.setWindowTitle("Đăng Nhập")
        self.ds_taikhoan = Cdstaikhoan()
        self.ptb_dangnhap.clicked.connect(self.dangnhap)
        self.ptb_dangky.clicked.connect(self.dangky)

    def dangnhap(self):
        tk = self.txt_taikhoan.text()
        mk = self.txt_matkhau.text()

        if tk == "" or mk == "":
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tài khoản và mật khẩu!")
            return

        user = self.ds_taikhoan.kiem_tra_dang_nhap(tk, mk)

        if user == None:
            QMessageBox.warning(self, "Lỗi", "Sai tài khoản hoặc mật khẩu!")
            self.txt_taikhoan.clear()
            self.txt_matkhau.clear()
            return

        if user.phanquyen == "admin":
            self.w = AdminWindow()
            self.w.show()
        else:
            self.w = UserWindow(user)
            self.w.show()

        self.close()

    def dangky(self):
        tk = self.txt_taikhoan.text()
        mk = self.txt_matkhau.text()
        if tk != "" and mk != "":
            kq = self.ds_taikhoan.them_tai_khoan(tk, mk, "user")
            if kq == True:
                QMessageBox.information(self, "OK", "Đăng ký thành công!")
            else:
                QMessageBox.warning(self, "Lỗi", "Tài khoản đã tồn tại!")
        else:
            QMessageBox.warning(self, "Lỗi", "Nhập đủ thông tin đi!")


class UserWindow(QMainWindow):
    def __init__(self, username):
        super(UserWindow, self).__init__()
        loadUi('gd_user.ui', self)
        self.setWindowTitle("Đăng Ký Hiến Máu")
        self.ds_nguoihien = Cdsnguoihien()
        self.ptb_dangki.clicked.connect(self.dangky_hienmau)

    def dangky_hienmau(self):
        ho_ten = self.led_hvt.text()
        tuoi_text = self.led_tuoi.text()
        gioi_tinh = self.cbb_gioitinh.currentText()
        nhom_mau = self.cbb_nhommau.currentText()
        tinh_thanh = self.cbb_tinh.currentText()
        benh_nen = self.led_benhnen.text()
        sdt = self.led_sdt.text()
        noi_hien = self.cbb_noihien.currentText()
        luong_mau = self.cbb_luongmau.currentText()
        can_nang = self.led_cannang.text()

        cccd = self.led_cccd.text()

        if ho_ten == "" or sdt == "":
            QMessageBox.warning(self, "Lỗi", "Họ tên và SĐT không được bỏ trống!")
            return

        # kiem tra cccd trung
        if cccd != "":
            for nh in self.ds_nguoihien.danh_sach:
                if nh.cccd == cccd:
                    QMessageBox.warning(self, "Lỗi", "CCCD này đã được đăng ký rồi!")
                    return

        # kiem tra tuoi
        try:
            tuoi = int(tuoi_text)
        except:
            QMessageBox.warning(self, "Lỗi", "Tuổi phải là số!")
            return

        if tuoi < 18:
            QMessageBox.warning(self, "Lỗi", "Phải đủ 18 tuổi mới được hiến máu!")
            return
        if tuoi > 120:
            QMessageBox.warning(self, "Lỗi", "Tuổi không hợp lệ!")
            return

        so_lan_hien_text = self.led_lanhien.text().strip()

        # lay ngay hien
        lan_gan_nhat = self.date.date().toString("dd/MM/yyyy")

        if so_lan_hien_text != "" and so_lan_hien_text != "0":
            try:
                so_lan_nhap = int(so_lan_hien_text)
            except:
                QMessageBox.warning(self, "Lỗi", "Số lần hiến phải là số!")
                return

            if so_lan_nhap < 0:
                QMessageBox.warning(self, "Lỗi", "Số lần hiến không được âm!")
                return

            if so_lan_nhap >= 1:
                if lan_gan_nhat == "Chưa có" or lan_gan_nhat == "":
                    QMessageBox.warning(self, "Lỗi", "Đã từng hiến thì phải chọn ngày hiến gần nhất!")
                    return

            so_lan_hien = -(so_lan_nhap + 1)
        else:
            so_lan_hien = -1
            lan_gan_nhat = "Chưa có"

        nguoi_moi = Cnguoihien(ho_ten, tuoi_text, gioi_tinh, can_nang, benh_nen,
                               tinh_thanh, nhom_mau, so_lan_hien, lan_gan_nhat, luong_mau, sdt, noi_hien, cccd)

        self.ds_nguoihien.them_nguoi_hien(nguoi_moi)
        QMessageBox.information(self, "Thành công", "Đăng ký hiến máu thành công!")
        self.close()


class AdminWindow(QMainWindow):
    def __init__(self):
        super(AdminWindow, self).__init__()
        loadUi('hienmaumoi.ui', self)
        self.setWindowTitle("Quản Lý Hiến Máu - Admin")
        self.ds_nguoihien = Cdsnguoihien()

        self.btn_lammoi.clicked.connect(self.load_lai)
        self.btn_xoa.clicked.connect(self.xoa)
        self.btn_sua.clicked.connect(self.sua)
        self.timkhancap.clicked.connect(self.tim_khan_cap)
        self.ptb_chapnhan.clicked.connect(self.chap_nhan)
        self.ptb_tuchoi.clicked.connect(self.tu_choi)

        self.load_lai()

    def load_lai(self):
        self.ds_nguoihien.load_data()
        self.hien_thi_cho_duyet()
        self.hien_thi_danh_sach()

    def hien_thi_cho_duyet(self):
        self.table_xacnhan.setRowCount(0)
        self.ds_cho_duyet = []
        i = 0
        for nh in self.ds_nguoihien.danh_sach:
            if nh.so_lan_hien < 0:
                self.ds_cho_duyet.append(nh)
                self.table_xacnhan.insertRow(i)
                self.table_xacnhan.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                self.table_xacnhan.setItem(i, 1, QTableWidgetItem(nh.ho_ten))
                self.table_xacnhan.setItem(i, 2, QTableWidgetItem(nh.luong_mau))
                self.table_xacnhan.setItem(i, 3, QTableWidgetItem(nh.lan_gan_nhat))
                self.table_xacnhan.setItem(i, 4, QTableWidgetItem(nh.noi_hien))
                self.table_xacnhan.setItem(i, 5, QTableWidgetItem("Đang chờ"))
                i += 1

    def chap_nhan(self):
        row = self.table_xacnhan.currentRow()
        if row >= 0:
            nguoi = self.ds_cho_duyet[row]
            if nguoi.so_lan_hien < 0:
                nguoi.so_lan_hien = -nguoi.so_lan_hien - 1
            self.ds_nguoihien.save_data()
            self.load_lai()
            QMessageBox.information(self, "OK", "Đã duyệt đơn của " + nguoi.ho_ten)
        else:
            QMessageBox.warning(self, "Lưu ý", "Chọn người cần duyệt trước!")

    def tu_choi(self):
        row = self.table_xacnhan.currentRow()
        if row >= 0:
            nguoi = self.ds_cho_duyet[row]
            tl = QMessageBox.question(self, "Xác nhận", "Từ chối đơn của " + nguoi.ho_ten + "?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if tl == QMessageBox.StandardButton.Yes:
                i = self.ds_nguoihien.danh_sach.index(nguoi)
                self.ds_nguoihien.xoa_nguoi_hien(i)
                self.load_lai()
                QMessageBox.information(self, "OK", "Đã từ chối!")
        else:
            QMessageBox.warning(self, "Lưu ý", "Chọn người cần từ chối trước!")

    def hien_thi_danh_sach(self):
        self.table_danhsach.setRowCount(0)
        self.ds_chinh_thuc = []
        i = 0
        for nh in self.ds_nguoihien.danh_sach:
            if nh.so_lan_hien >= 0:
                self.ds_chinh_thuc.append(nh)
                self.table_danhsach.insertRow(i)
                self.table_danhsach.setItem(i, 0, QTableWidgetItem(nh.ho_ten))
                self.table_danhsach.setItem(i, 1, QTableWidgetItem(str(nh.tuoi)))
                self.table_danhsach.setItem(i, 2, QTableWidgetItem(nh.gioi_tinh))
                self.table_danhsach.setItem(i, 3, QTableWidgetItem(str(nh.can_nang)))
                self.table_danhsach.setItem(i, 4, QTableWidgetItem(nh.benh_nen))
                self.table_danhsach.setItem(i, 5, QTableWidgetItem(nh.tinh_thanh))
                self.table_danhsach.setItem(i, 6, QTableWidgetItem(nh.nhom_mau))
                self.table_danhsach.setItem(i, 7, QTableWidgetItem(str(nh.so_lan_hien)))
                if nh.so_lan_hien <= 0:
                    lgn = "Chưa hiến"
                else:
                    lgn = nh.lan_gan_nhat
                self.table_danhsach.setItem(i, 8, QTableWidgetItem(lgn))
                self.table_danhsach.setItem(i, 9, QTableWidgetItem(nh.sdt))
                self.table_danhsach.setItem(i, 10, QTableWidgetItem(nh.noi_hien))
                self.table_danhsach.setItem(i, 11, QTableWidgetItem(nh.luong_mau))
                i += 1

    def xoa(self):
        row = self.table_danhsach.currentRow()
        if row >= 0:
            nguoi_xoa = self.ds_chinh_thuc[row]
            tl = QMessageBox.question(self, "Xác nhận xóa", "Xóa thông tin của " + nguoi_xoa.ho_ten + "?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if tl == QMessageBox.StandardButton.Yes:
                i = self.ds_nguoihien.danh_sach.index(nguoi_xoa)
                self.ds_nguoihien.xoa_nguoi_hien(i)
                self.load_lai()
                QMessageBox.information(self, "OK", "Xóa thành công!")
        else:
            QMessageBox.warning(self, "Lưu ý", "Chọn người cần xóa ở bảng danh sách!")

    def sua(self):
        row = self.table_danhsach.currentRow()
        if row >= 0:
            nguoi_sua = self.ds_chinh_thuc[row]
            self.w_sua = EditWindow(self, nguoi_sua, self.ds_nguoihien)
            self.w_sua.show()
        else:
            QMessageBox.warning(self, "Lưu ý", "Chọn người cần sửa ở bảng danh sách!")

    def tim_khan_cap(self):
        nm = self.nhommau.currentText().strip()
        tt = self.cbb_tinh.currentText().strip()
        self.tableWidget.setRowCount(0)
        row = 0
        for nh in self.ds_nguoihien.danh_sach:
            solan = int(nh.so_lan_hien)
            if nh.nhom_mau.strip() == nm and nh.tinh_thanh.strip() == tt and solan >= 0:
                self.tableWidget.insertRow(row)
                self.tableWidget.setItem(row, 0, QTableWidgetItem(nh.ho_ten))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(str(nh.tuoi)))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(nh.gioi_tinh))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(str(nh.can_nang)))
                self.tableWidget.setItem(row, 4, QTableWidgetItem(nh.benh_nen))
                self.tableWidget.setItem(row, 5, QTableWidgetItem(nh.tinh_thanh))
                self.tableWidget.setItem(row, 6, QTableWidgetItem(nh.nhom_mau))
                self.tableWidget.setItem(row, 7, QTableWidgetItem(nh.sdt))
                row += 1


class EditWindow(QMainWindow):
    def __init__(self, admin_window, nguoi_hien, ds_nguoihien):
        super(EditWindow, self).__init__(admin_window)
        self.setWindowTitle("Sửa thông tin người hiến máu")


        self.admin_window = admin_window
        self.nguoi_hien = nguoi_hien
        self.ds_nguoihien = ds_nguoihien

        loadUi('gd_user.ui', self)

        # dien thong tin cu vao form
        self.led_hvt.setText(self.nguoi_hien.ho_ten)
        self.led_tuoi.setText(str(self.nguoi_hien.tuoi))
        self.led_cannang.setText(str(self.nguoi_hien.can_nang))
        self.led_sdt.setText(self.nguoi_hien.sdt)
        self.led_benhnen.setText(self.nguoi_hien.benh_nen)

        self.led_lanhien.setText(str(self.nguoi_hien.lan_gan_nhat))
        if self.nguoi_hien.so_lan_hien >= 1:
            self.led_lanhien.setEnabled(True)
        else:
            self.led_lanhien.setEnabled(False)

        # set gia tri combobox
        self.set_combo(self.cbb_gioitinh, self.nguoi_hien.gioi_tinh)
        self.set_combo(self.cbb_nhommau, self.nguoi_hien.nhom_mau)
        self.set_combo(self.cbb_tinh, self.nguoi_hien.tinh_thanh)
        self.set_combo(self.cbb_noihien, self.nguoi_hien.noi_hien)
        self.set_combo(self.cbb_luongmau, self.nguoi_hien.luong_mau)

        self.ptb_dangki.setText("Cập nhật")
        self.ptb_dangki.clicked.connect(self.cap_nhat)

    def set_combo(self, combo, value):
        index = combo.findText(value)
        if index >= 0:
            combo.setCurrentIndex(index)
        else:
            combo.addItem(value)
            combo.setCurrentText(value)

    def cap_nhat(self):
        try:
            tuoi = int(self.led_tuoi.text())
            can_nang = float(self.led_cannang.text())
        except:
            QMessageBox.warning(self, "Lỗi", "Tuổi và cân nặng phải là số!")
            return

        # tim nguoi trong danh sach
        target = None
        for nh in self.ds_nguoihien.danh_sach:
            if nh.sdt == self.nguoi_hien.sdt and nh.ho_ten == self.nguoi_hien.ho_ten:
                target = nh
                break

        if target == None:
            target = self.nguoi_hien

        target.ho_ten = self.led_hvt.text()
        target.tuoi = tuoi
        target.can_nang = can_nang
        target.sdt = self.led_sdt.text()
        target.benh_nen = self.led_benhnen.text()
        target.gioi_tinh = self.cbb_gioitinh.currentText()
        target.nhom_mau = self.cbb_nhommau.currentText()
        target.tinh_thanh = self.cbb_tinh.currentText()
        target.noi_hien = self.cbb_noihien.currentText()
        target.luong_mau = self.cbb_luongmau.currentText()

        if target.so_lan_hien >= 1:
            lan_moi = self.led_lanhien.text()
            if lan_moi != "Chưa có" and lan_moi != "Chưa hiến":
                target.lan_gan_nhat = lan_moi

        self.ds_nguoihien.save_data()
        QMessageBox.information(self, "OK", "Cập nhật thành công!")
        self.admin_window.load_lai()
        self.close()
