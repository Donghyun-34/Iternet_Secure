class ECM_Point:
    O = "inf"

    def __init__(self, x: int, y: int, ec: 'EC'):
        self.x = x
        self.y = y
        self.ec = ec


class EC:
    def __init__(self, a: int, b: int, mod: int):  # 기본 생성자
        self.a = a
        self.b = b
        self.n = [ECM_Point]  # O(Inf)
        self.mod = mod
        self.size = 1

    def eval_x(self, x: int):
        x = x % self.mod
        return (x ** 3 + self.a * x + self.b) % self.mod

    def eval_y(self, x):
        y_square = self.eval_x(x)
        for y in range(self.mod):
            if y ** 2 % self.mod == y_square:
                self.size += 1
                self.point(x, y)

    def find_point(self):
        for i in range(self.mod):
            self.eval_y(i)

    def point(self, x, y):
        self.n.append(ECM_Point(x, y, self))

    def inv_mod(self, x):
        if x == 0:
            return 0
        for i in range(self.mod):
            if (i*x) % self.mod == 1:
                return i

    def add(self, p: ECM_Point, q: ECM_Point):
        if p == q:
            inv = self.inv_mod(2 * p.y)
            if inv == 0:
                return ECM_Point.O
            else:
                cal = (3 * p.x ** 2 + self.a) * inv
        else:
            inv = self.inv_mod(q.x - p.x)
            if inv == 0:
                return ECM_Point.O
            else:
                cal = (q.y - p.y) * inv

        x = int((cal ** 2 - p.x - q.x) % self.mod)
        y = int((cal * (p.x - x) - p.y) % self.mod)
        result = ECM_Point(x, y, self)

        return result

    def order(self, p: ECM_Point):
        q = p
        cnt = 1

        while 1:
            if q == ECM_Point.O:
                return cnt
            else:
                cnt += 1
                q = self.add(p, q)

    def DLP(self, g: ECM_Point, y: ECM_Point): # G : Source, Y : Destination
        q = g
        cnt = 1

        while 1:
            if q.x == y.x and q.y == y.y:
                return cnt
            else:
                cnt += 1
                q = self.add(g, q)


if __name__ == '__main__':
    ec = EC(9, 17, 23)
    ec.find_point()

    for i in range(ec.size):
        if i == 0:
            print(" O, Inf")
        else:
            print("({}, {}) - Order : {}".format(ec.n[i].x, ec.n[i].y, ec.order(ec.n[i])))

    print("ECDLP (4, 5) = x * (16, 5), x = {}".format(ec.DLP(ec.n[23], ec.n[5])))