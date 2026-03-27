import json, os
from Cnguoihien import Cnguoihien

class Cdsnguoihien:
    def __init__(self, filename="nguoihien.json"):
        self.filename = filename
        self.danh_sach = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                info = json.load(f)
                self.danh_sach = [Cnguoihien.from_dict(item) for item in info]

    def save_data(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([nh.to_dict() for nh in self.danh_sach], f, ensure_ascii=False, indent=4)

    def them_nguoi_hien(self, nguoihien):
        self.danh_sach.append(nguoihien)
        self.save_data()

    def xoa_nguoi_hien(self, index):
        if 0 <= index < len(self.danh_sach):
            self.danh_sach.pop(index)
            self.save_data()