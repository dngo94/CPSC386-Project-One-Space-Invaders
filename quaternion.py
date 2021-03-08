from math import sqrt, acos
from math import pi
from math import cos, sin, atan2
PI_2 = pi / 2.0
from vector import Vector
from matrix import Matrix


class Quaternion:
    def __init__(self, w, x=0, y=0, z=0):
        self.w = float(w)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    @classmethod
    def i(cls): return Quaternion(0.0, 1.0, 0.0, 0.0)
    @classmethod
    def j(cls): return Quaternion(0.0, 0.0, 1.0, 0.0)
    @classmethod
    def k(cls): return Quaternion(0.0, 0.0, 0.0, 1.0)

    @classmethod
    def ii(cls): return -1
    @classmethod
    def jj(cls): return -1
    @classmethod
    def kk(cls): return -1

    @classmethod
    def ij(cls): return Quaternion.k()
    @classmethod
    def ji(cls): return -Quaternion.k()

    @classmethod
    def jk(cls): return Quaternion.i()
    @classmethod
    def kj(cls): return -Quaternion.i()

    @classmethod
    def ki(cls): return Quaternion.j()
    @classmethod
    def ik(cls): return -Quaternion.j()

    @classmethod
    def ijk(cls): return -1

    def __str__(self):
        s = 'Quat('
        if self == Quaternion.i(): return s + 'i)'
        if self == -Quaternion.i(): return s + '-i)'
        if self == Quaternion.j(): return s + 'j)'
        if self == -Quaternion.j(): return s + '-j)'
        if self == Quaternion.k(): return s + 'k)'
        if self == -Quaternion.k(): return s + '-k)'
        if self.magnitude() == 0.0 and self.w == 0: return s + '0)'
        if self.magnitude() == 1.0 and self.w == 1: return s + '1)'
        if self.vector().magnitude() == 0.0: return f'{s}{self.w})'
        else: return s + f'{self.w:.1f} + {self.vector()})'

    def __add__(self, o):
        if isinstance(o, float):
            return Quaternion(o, self.x + o, self.y + o, self.z)
        return Quaternion(self.w + o.w, self.x + o.x, self.y + o.y, self.z + o.z)

    def __radd__(self, o): return self + o

    def __sub__(self, v): return self + -v

    def __rsub__(self, o): return -(o - self)

    def __rmul__(self, o): return self * o

    def __mul__(self, o):
        if isinstance(o, Quaternion):
            w1, x1, y1, z1 = self.w, self.x, self.y, self.z
            w2, x2, y2, z2 = o.w, o.x, o.y, o.z
            return Quaternion((w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2),
                              (w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2),
                              (w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2),
                              (w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2))
        val = o
        return Quaternion(val * self.w, val * self.x, val * self.y, val * self.z)

    def  __truediv__(self, val): return self * (1.0 / val)

    def __neg__(self): return Quaternion(-self.w, -self.x, -self.y, -self.z)

    def __eq__(self, v): return self.w == v.w and self.x == v.x and self.y == v.y and self.z == v.z

    def __ne__(self, v): return not (self == v)

    def vector(self): return Vector(self.x, self.y, self.z)

    def scalar(self): return self.w

    def unit_scalar(self): return Quaternion(1.0, Vector())

    def conjugate(self): return Quaternion(self.w, -self.x, -self.y, -self.z)

    def inverse(self): return self.conjugate() / self.magnitude() ** 2

    def unit(self): return self / self.magnitude()

    def norm(self): return sqrt(self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2)

    def magnitude(self): return self.norm()

    def dot(self, v): self.w * v.w + self.vector().dot(v.vector())

    def angle(self, v):
        if not isinstance(v, Quaternion): raise TypeError
        z = self.conjugate() * v
        zvnorm = z.vector().norm()
        zscalar = z.scalar()
        angle = atan2(zvnorm, zscalar)
        return angle * 180.0 / 3.1415

    def rot_matrix(self):
        w, x, y, z = self.w, self.x, self.y, self.z
        # print(w, x, y, z)
        return Matrix(3, 3, -2*(y**2 + z**2) + 1,  2*(x*y  - w*z),       2*(x*z  +  w*y),
                             2*(x*y  + w*z),      -2*(x**2 + z**2) + 1,  2*(y*z  -  w*x),
                             2*(x*z  - w*y),       2*(y*z  + w*x),      -2*(x**2 + y**2)+1)
        # return Matrix(3, 3, 2*(w**2 + x**2) - 1,  2*(x*y  - w*z),       2*(x*z  +  w*y),
        #                     2*(x*y  + w*z),       2*(w**2 + y**2) - 1,  2*(y*z  -  w*x),
        #                     2*(x*z  - w*y),       2*(y*z  + w*x),       2*(w**2 + z**2)-1)

    @staticmethod
    def rotate(pt, axis, theta):     # rotates a point pt (pt.x, pt.y, pt.z) about (axis.x, axis.y, axis.z) by theta
        costheta2 = cos(theta / 2.0)
        sintheta2 = sin(theta / 2.0)
        q = Quaternion(costheta2, axis.x * sintheta2, axis.y * sintheta2, axis.z * sintheta2)
        q_star = Quaternion(q.w, -q.x, -q.y, -q.z)
        p = Quaternion(0, pt.x, pt.y, pt.z)
        p_rot = q * p * q_star
        return Vector(p_rot.x, p_rot.y, p_rot.z)

    @staticmethod
    def run_tests():
        a = Quaternion(1, 2, 3, 4)
        b = Quaternion(4, 0, 0, 7)

        c = Quaternion(0, 1, 1, 0)
        d = Quaternion(0, 0, 1, 0)

        e = Quaternion(0, 0, 0, 1)
        f = Quaternion(0, 0, 0, 0)
        g = Quaternion(1, 0, 0, 0)
        h = Quaternion(3, 0, 0, 0)

        print('a = ' + str(a))
        print('b = ' + str(b))
        print('c = ' + str(c))
        print('d = ' + str(d))
        print('e = ' + str(e))
        print('f = ' + str(f))
        print('g = ' + str(g))
        print('h = ' + str(h), '\n')

        print('c + d = ', str(c + d))
        print('c + d + e = ', c + d + e, '\n')

        print(f'5 * h is: {5.0 * h}')
        print(f'h * 5 is: {h * 5.0}')
        print(f'h / 3.0 is: {h / 3.0}')
        print(f'h.magnitude() is: {h.magnitude()}')
        print(f'h.unit() is: {h.unit()}')
        print(f'g.unit() is: {g.unit()}')
        print(f'a.unit() is: {a.unit()}\n')

        print(f'a.vector() is: {a.vector()}')
        print(f'a.scalar() is: {a.scalar()}')
        print(f'a.conjugate() is: {a.conjugate()}')
        print(f'a.inverse() is: {a.inverse()}')
        print(f'a * a.inverse() is: {a * a.inverse()}\n')

        print(f'c == d is: {c == d}')
        print(f'c != d is: {c != d}')

        print(f'e == e is: {e == e}')
        print(f'e != e is: {e != e}\n')

        print(f'Quaternion.ij is: {Quaternion.ij()}')
        print(f'Quaternion.jk is: {Quaternion.jk()}')
        print(f'Quaternion.ki is: {Quaternion.ki()}\n')

        print(f'Quaternion.ji is: {Quaternion.ji()}')
        print(f'Quaternion.kj is: {Quaternion.kj()}')
        print(f'Quaternion.ik is: {Quaternion.ik()}\n')

        print(f'Quaternion.ijk is: {Quaternion.ijk()}')

        print(f'Quaternion.ii is: {Quaternion.ii()}')
        print(f'Quaternion.jj is: {Quaternion.jj()}')
        print(f'Quaternion.kk is: {Quaternion.kk()}\n')


        print(f'angle between c and d is: {c.angle(d):.3f} degrees')
        c_minus_d = c - d
        print(f'c_minus_d is: {c_minus_d}')
        rot_matrix = c_minus_d.rot_matrix()
        print(f'rot_matrix of c_minus_d is: {rot_matrix}')

        rad2_2 = sqrt(2)/2.0

        print("SEE THIS WEBSITE for DETAILED DIAGRAMS on the TESTS of the PLANE's rotations")
        print('https://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToMatrix/examples/index.htm')

        print('# -------------- LEVEL FLIGHT -------------------')
        plane = Quaternion(1)
        print(f'levelflight(E) is {plane}{plane.rot_matrix()}')

        plane = Quaternion(rad2_2, 0, rad2_2, 0)
        print(f'levelflight(N) is {plane}{plane.rot_matrix()}')

        plane = Quaternion(0, 0, 1, 0)
        print(f'levelflight(W) is {plane}{plane.rot_matrix()}')

        plane = Quaternion(rad2_2, 0, -rad2_2, 0)
        print(f'levelflight(S) is {plane}{plane.rot_matrix()}')
        print('# ----------------------------------------------------')


        print('\n\n# -------- STRAIGHT UP ---------------------')
        plane = Quaternion(rad2_2, 0, 0, rad2_2)
        print(f'plane_straightupE is {plane}{plane.rot_matrix()}')

        plane = Quaternion(0.5, 0.5, 0.5, 0.5)
        print(f'plane_straightupN is {plane}{plane.rot_matrix()}')

        plane = Quaternion(0, rad2_2, rad2_2, 0)
        print(f'plane_straightupW is {plane}{plane.rot_matrix()}')

        plane = Quaternion(0.5, -0.5, -0.5, 0.5)
        print(f'plane_straightupS is {plane}{plane.rot_matrix()}')
        print('# -------- end STRAIGHT UP ---------------------')


        print('\n\n# -------- STRAIGHT DOWN ---------------------')
        plane = Quaternion(rad2_2, 0, 0, -rad2_2)
        print(f'plane_straightdownE is {plane}{plane.rot_matrix()}')

        plane = Quaternion(0.5, -0.5, 0.5, -0.5)
        print(f'plane_straightdownN is {plane}{plane.rot_matrix()}')

        plane = Quaternion(0, -rad2_2, rad2_2, 0)
        print(f'plane_straightdownW is {plane}{plane.rot_matrix()}')

        plane = Quaternion(0.5, 0.5, -0.5, -0.5)
        print(f'plane_straightdownS is {plane}{plane.rot_matrix()}')
        print('# -------- end STRAIGHT UP ---------------------')


        print('\n\n# --------  BANK/ROLL ---------------------')
        plane = Quaternion(rad2_2, rad2_2, 0, 0)
        print(f'plane_E_bankLeft90 is {plane}{plane.rot_matrix()}')

        plane = Quaternion(0.5, 0.5, 0.5, -0.5)
        print(f'plane_N_bankLeft90 is {plane}{plane.rot_matrix()}')

        plane = Quaternion(0, 0, rad2_2, -rad2_2)
        print(f'plane_W_bankLeft90 is {plane}{plane.rot_matrix()}')

        plane = Quaternion(0.5, 0.5, -0.5, 0.5)
        print(f'plane_S_bankLeft90 is {plane}{plane.rot_matrix()}')

        print('\nBanking/Rolling 180 degrees')
        plane = Quaternion(0, 1, 0, 0)
        print(f'plane_E_bankLeft180 is {plane}{plane.rot_matrix()}')

        plane = Quaternion(0, rad2_2, 0, -rad2_2)
        print(f'plane_N_bankLeft180 is {plane}{plane.rot_matrix()}')

        plane = Quaternion(0, 0, 0, 1)
        print(f'plane_W_bankLeft180 is {plane}{plane.rot_matrix()}')

        plane = Quaternion(0, rad2_2, 0, rad2_2)
        print(f'plane_S_bankLeft180 is {plane}{plane.rot_matrix()}')


        print('\nBanking/Rolling Right 90 degrees')
        plane = Quaternion(rad2_2, -rad2_2, 0, 0)
        print(f'plane_E_bankRight180 is {plane}{plane.rot_matrix()}')

        plane = Quaternion(0.5, -0.5, 0.5, 0.5)
        print(f'plane_N_bankRight180 is {plane}{plane.rot_matrix()}')

        plane = Quaternion(0, 0, rad2_2, rad2_2)
        print(f'plane_W_bankRight80 is {plane}{plane.rot_matrix()}')

        plane = Quaternion(0.5, -0.5, -0.5, -0.5)
        print(f'plane_S_bankRight80 is {plane}{plane.rot_matrix()}')
        print('# -------- end BANK/ROLL ---------------------')

        print("SEE THIS WEBSITE for DETAILED DIAGRAMS on the TESTS of the PLANE's rotations")
        print('https://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToMatrix/examples/index.htm')


def main():
    # Vector.run_tests()
    Quaternion.run_tests()
    # Matrix.run_tests()


if __name__ == '__main__':
    main()

