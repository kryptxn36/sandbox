def sqmod(a, p):
    sq_roots = []
    for x in range(p):
        if (x * x) % p == a:
            sq_roots.append(x)
        else:
            continue
    return sq_roots

def inverse(u, v):
    if v == 0:
        raise ZeroDivisionError("Modulus cannot be zero")
    if v < 0:
        raise ValueError("Modulus cannot be negative")
    u3, v3 = u, v
    u1, v1 = 1, 0
    while v3 > 0:
        q = u3 // v3
        u1, v1 = v1, u1 - v1*q
        u3, v3 = v3, u3 - v3*q
    if u3 != 1:
        raise ValueError("No inverse value can be computed")
    while u1 < 0:
        u1 = u1 + v
    return u1

class EC_Weierstrass:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def __repr__(self):
        a = self.a
        b = self.b

        if a < 0 and b > 0:
            equation = f'y^2 = x^3 - {abs(a)}x + {b}'
        elif a > 0 and b < 0:
            equation = f'y^2 = x^3 + {a}x - {abs(b)}'
        elif a < 0 and b < 0:
            equation = f'y^2 = x^3 - {abs(a)}x - {abs(b)}'
        elif a > 0 and b > 0:
            equation = f'y^2 = x^3 + {a}x + {b}'
        return equation

    def sum_double(self, q1, q2):
        a = self.a
        p = self.p
        
        x1 = q1[0]
        y1 = q1[1]
        x2 = q2[0]
        y2 = q2[1]
        if x1 != x2:
            l = pow((y2 - y1) * inverse(x2 - x1, p), 1, p)
            x3 = pow((l ** 2) - x1 - x2, 1, p)
            y3 = pow(l * (x1 - x3) - y1, 1, p)
            return x3, y3
        elif x1 == x2 and y1 == y2 and y1 != 0 and y2 != 0:
            l = pow((3*(x1 ** 2) + a) * inverse(2 * y1, p), 1, p)
            x3 = pow(l ** 2 - 2 * x1, 1, p)
            y3 = pow(l * (x1 - x3) - y1, 1, p)
            return x3, y3
        elif x1 == x2 and y1 == (self.p - y2):
            return 0, 0
    
    def points(self):
        a = self.a
        b = self.b
        p = self.p

        fp = [x % p for x in range(p)]
        fp2 = [pow(x, 2, p) for x in range(p)]
        yy = [pow(x ** 3 + a * x + b, 1, p) for x in fp]
        idx = 0
        points = []
        for y in yy:
            if y in fp2:
                roots = sqmod(y,p)
                if len(roots) == 2:
                    x = fp[idx]
                    y1, y2 = roots[0], roots[1]
                    pt1, pt2 = (x, y1), (x, y2)
                    points.append(pt1)
                    points.append(pt2)
                elif len(roots) == 1:
                    x = fp[idx]
                    y = roots[0]
                    pt = (x, y)
                    points.append(pt)
            idx += 1
        points.append('O')
        return points
     
    def group_order(self):
        points = self.points()
        order = len(points)
        return order

    def montgomery_ladder(self, q, k):
        x = q[0]
        y = q[1]
        order = self.group_order()
        if pow(k, 1, order) == 0:
            return 'O'
        else:
            k = pow(k, 1, order)
            r0 = (x, y)
            r1 = self.sum_double(q, q)
            k = bin(k)[2:]
            l = len(k)
            for i in range(1, l):
                if k[i] == '0':
                    r1 = self.sum_double(r0, r1)
                    r0 = self.sum_double(r0, r0)
                else:
                    r0 = self.sum_double(r0, r1)
                    r1 = self.sum_double(r1, r1)
            return r0
