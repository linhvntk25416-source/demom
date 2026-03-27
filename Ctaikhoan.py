class Cphanquyen:
    def __init__(self, taikhoan, matkhau, phanquyen):
        self.taikhoan = taikhoan
        self.matkhau = matkhau
        self.phanquyen = phanquyen

    def to_dict(self):
        return {
            'taikhoan': self.taikhoan,
            'matkhau': self.matkhau,
            'phanquyen': self.phanquyen
        }
    @staticmethod
    def from_dict(info):
        return Cphanquyen(info['taikhoan'], info['matkhau'], info.get('phanquyen', 'user'))




