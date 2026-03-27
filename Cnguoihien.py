class Cnguoihien:
    def __init__(self, ho_ten, tuoi, gioi_tinh, can_nang, benh_nen,
                 tinh_thanh, nhom_mau, so_lan_hien, lan_gan_nhat,
                 luong_mau, sdt, noi_hien, cccd=""):
        self.ho_ten = ho_ten
        self.tuoi = int(tuoi) if tuoi else 0
        self.gioi_tinh = gioi_tinh
        self.can_nang = float(can_nang) if can_nang else 0
        self.benh_nen = benh_nen
        self.tinh_thanh = tinh_thanh
        self.nhom_mau = nhom_mau
        self.so_lan_hien = int(so_lan_hien) if so_lan_hien else 0
        self.lan_gan_nhat = lan_gan_nhat
        self.luong_mau = luong_mau
        self.sdt = sdt
        self.noi_hien = noi_hien
        self.cccd = cccd

    def to_dict(self):
        return {
            'ho_ten': self.ho_ten,
            'tuoi': self.tuoi,
            'gioi_tinh': self.gioi_tinh,
            'can_nang': self.can_nang,
            'benh_nen': self.benh_nen,
            'tinh_thanh': self.tinh_thanh,
            'nhom_mau': self.nhom_mau,
            'so_lan_hien': self.so_lan_hien,
            'lan_gan_nhat': self.lan_gan_nhat,
            'luong_mau': self.luong_mau,
            'sdt': self.sdt,
            'noi_hien': self.noi_hien,
            'cccd': self.cccd
        }

    @staticmethod
    def from_dict(info):
        return Cnguoihien(
            info.get('ho_ten', ''),
            info.get('tuoi', 0),
            info.get('gioi_tinh', ''),
            info.get('can_nang', 0),
            info.get('benh_nen', ''),
            info.get('tinh_thanh', ''),
            info.get('nhom_mau', ''),
            info.get('so_lan_hien', 0),
            info.get('lan_gan_nhat', 'Chưa có'),
            info.get('luong_mau', ''),
            info.get('sdt', ''),
            info.get('noi_hien', ''),
            info.get('cccd', '')
        )