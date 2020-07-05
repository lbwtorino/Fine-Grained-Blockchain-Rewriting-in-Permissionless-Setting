import charm.core.crypto.cryptobase
from charm.toolbox.pairinggroup import *
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.ABEnc import *
from fractions import Fraction
import random

class SHARING(ABEnc):
    def __init__(self, groupObj, verbose = False):
        ABEnc.__init__(self)
        global util, group
        group = groupObj
        util = SecretUtil(group, verbose)
        self.size_A = 5
        self.size_B = 5
        self.threshold = 2

    def compute_polynomial(self, constant, a1, a2, x):
        return constant + a1 * x + a2 * (x**2)
    
    def compute_polynomial_xy(self, S, a01, a10, a11, a02, a20, a22, x):
        res = []
        res.append(S + a01 * x + a02 * x**2)
        res.append(a10 + a11 * x)
        res.append(a20 + a22 * x**2)
        # res = constant + a1 * y + a2 * y^2
        return res


    def get_GroupA_shares(self, S):
        a01, a10, a11 = group.init(ZR, int(random.randrange(1000))), group.init(ZR, int(random.randrange(1000))), group.init(ZR, int(random.randrange(1000)))
        a02, a20, a22 = group.init(ZR, int(random.randrange(1000))), group.init(ZR, int(random.randrange(1000))), group.init(ZR, int(random.randrange(1000)))
        shares = []
        for i in range(self.size_A):
            shares.append(self.compute_polynomial_xy(S, a01, a10, a11, a02, a20, a22, i+1))
        return shares

    def reshare_GroupA_shares(self, share):
        constant = share[0]
        a1 = share[1]
        a2 = share[2]
        reshare_A = []
        for i in range(self.size_B):
            reshare_A.append(self.compute_polynomial(constant, a1, a2, i+1))
        return reshare_A

    def get_GroupB_shares(self, reshare_A):
        shares_B = []
        for i in range(self.size_B):
            share_Bi = []
            for j in range(self.size_A):
                share_Bi.append(reshare_A[j][i])
            shares_B.append(share_Bi)
        return shares_B
        # shares_B = []
        # for i in range(self.size_B):
        #     shares_B.append(reshare_A[i])
        # return shares_B


    def recover_secret(self, shares):
        points = [[2, shares[1]], [4, shares[3]], [5, shares[4]]]
        l_0 = self.compute_l(points[0][0], points[1], points[2])
        l_1 = self.compute_l(points[1][0], points[0], points[2])
        l_2 = self.compute_l(points[2][0], points[0], points[1])
        recovered_polynomial  = []
        for i in range(self.threshold+1):
            constant = Fraction(int(l_0['numerator'][i]) * int(points[0][1]), int(l_0['denominator']))
            x_exp_1 = Fraction(int(l_1['numerator'][i]) * int(points[1][1]), int(l_1['denominator']))
            x_exp_2 = Fraction(int(l_2['numerator'][i]) * int(points[2][1]), int(l_2['denominator']))
            recovered_polynomial.append(int(constant + x_exp_1 + x_exp_2))
        return {'constant':recovered_polynomial[0], 'x_exp_1':recovered_polynomial[1], 'x_exp_2':recovered_polynomial[2]}
            
    def compute_l(self, x_i, point_1, point_2):
        denominator = (x_i - point_1[0]) * (x_i - point_2[0])
        numerator = []
        numerator.append(point_1[0] * point_2[0])
        numerator.append((-point_1[0]) + (-point_2[0]))
        numerator.append(1)
        return {'numerator': numerator, 'denominator':denominator}




