import json, os
from Ctaikhoan import Cphanquyen

class Cdstaikhoan:
    def __init__(self, filename = "taikhoan.json"):
        self.filename = filename
        self.ds = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding = 'utf-8') as json_taikhoan:
                data = json.load(json_taikhoan)
                self.ds = [Cphanquyen.from_dict(item) for item in data]
        else:
            self.ds.append(Cphanquyen("admin", "123456", "admin"))
            self.save_data()

    def save_data(self):
        with open(self.filename, "w", encoding='utf-8') as json_taikhoan:
            json.dump([tk.to_dict() for tk in self.ds], json_taikhoan, ensure_ascii=False, indent=4)

    def kiem_tra_dang_nhap(self, tk, matkhau):
        for taikhoan in self.ds:
            if taikhoan.taikhoan == tk and taikhoan.matkhau == matkhau:
                return taikhoan
        return None

    def them_tai_khoan(self, tk, mk, phanquyen):
        nguoi_moi = Cphanquyen(tk, mk, phanquyen)
        self.ds.append(nguoi_moi)
        self.save_data()
        return True




