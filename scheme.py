import charm.core.crypto.cryptobase
from charm.toolbox.pairinggroup import *
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.ABEnc import *
import time

class SCHEME(ABEnc):
    def __init__(self, groupObj, verbose = False):
        ABEnc.__init__(self)
        global util, group
        group = groupObj
        util = SecretUtil(group, verbose)
        self.k = 10
        self.index_i = 5
        self.index_j = 5

    def setup(self):
        # g, u, v, w, h
        # G2 --> H, G1 --> G
        h = group.random(G2)
        g, u, v, w = group.random(G1), group.random(G1), group.random(G1), group.random(G1)
        # alpha, beta, theta, e(g, g)^alpha
        alpha = group.random(ZR)
        beta = group.random(ZR)
        theta = group.random(ZR)
        egg = pair(g,h)**alpha
        # z_1,z_2......z_k, {g_1, g_2,....g_k}, and {h_1, h_2,....h_k}
        # {g1^alpha, g2^alpha,...gk^alpha}, and {h1^alpha, h2^alpha,...hk^alpha}
        # z = []
        vector_g, vector_h, vector_g_alpha, vector_h_alpha = [], [], [], []
        for i in range(self.k):
            tmp = group.random(ZR)
            vector_g.append(g**tmp)
            vector_h.append(h**tmp)
            vector_g_alpha.append(vector_g[i]**alpha)
            vector_h_alpha.append(vector_h[i]**alpha)
        # g^beta, h^1/alpha, h^beta/alpha, egg^theta/alpha
        g_beta =  g**beta 
        h_1_alpha = h**(1/alpha)
        h_beta_alpha =  h**(beta/alpha)
        egg_theta_alpha = egg**(theta/alpha)
        # mpk
        mpk = {'g':g, 'u':u, 'v':v, 'w':w, 'h':h, 'egg':egg, 'vector_g_alpha': vector_g_alpha, 'vector_h_alpha': vector_h_alpha, 'g_beta': g_beta, 'h_1_alpha': h_1_alpha, 'h_beta_alpha': h_beta_alpha, 'egg_theta_alpha': egg_theta_alpha}
        # msk
        msk = {'alpha':alpha, 'beta':beta, 'theta': theta}
        return (mpk, msk)



    def keygen(self, mpk, msk, policy_str):
        # the secret alpha will be shared according to the policy	
        policy = util.createPolicy(policy_str)
        # retrieve the attributes that occur in a policy tree in order (left to right)
        # print(time.time())
        a_list = util.getAttributeList(policy)
        # compute vector lambda
        # print(time.time())
        shares = util.calculateSharesDict(msk['alpha'], policy)
        # compute K{}, [t_1,t_2,....t_n], [r_1,r_2, .....r_n] 
        SK1, SK2, SK3 = {}, {}, {}
        t = []
        r = []
        for i in a_list:
            t_i = group.random(ZR)
            r_i = group.random(ZR)
            # remove index, only return attribute name
            inti = int(util.strip_index(i)) #NOTICE THE CONVERSION FROM STRING TO INT
            # compute K_(Tau,0)
            SK1[i] = mpk['g']**shares[i] * mpk['w']**t_i
            # compute K_(Tau,1)
            rho_i = group.init(ZR, inti)
            SK2[i] = (mpk['u']**rho_i * mpk['v'])**(-t_i)
            # compute K_(Tau,2)
            SK3[i] = mpk['h']**t_i
            t.append(t_i)
            r.append(r_i)
        # print(time.time())
        # sk_0
        sk_0 = {}
        sum_t, sum_r = sum(t), sum(r)
        ttt = 0
        for i in t:
            ttt += i
        sum_t = group.init(ZR, sum_t)
        sum_r = group.init(ZR, sum_r)
        g_t_alpha = mpk['g']**(sum_t/msk['alpha'])
        g_r = mpk['g']**sum_r
        sk_0['g_t_alpha'] = g_t_alpha
        sk_0['g_r'] = g_r
        # sk_1
        I = []
        vector_i = 1
        for i in range(self.index_i):
            tmp = group.random(ZR)
            vector_i *= mpk['vector_g_alpha'][self.k-1-i]**tmp
            I.append(tmp)
        vector_i *= mpk['g']
        sk_1 = mpk['g']**msk['theta'] * vector_i**sum_t * mpk['g']**(msk['beta']*sum_r)
        return {'Policy':policy_str, 'SK1':SK1, 'SK2':SK2, 'SK3':SK3, 'sk_0': sk_0, 'sk_1': sk_1}

    def helper_gen_ciphertext(self, mpk, msk, R, attri_list):
        s = group.random(ZR)	
        wS = mpk['w']**(-s)
        h, alpha, beta = mpk['h'], msk['alpha'], msk['beta']
        # compute C{}
        CT1, CT2 = {}, {}
        r = []
        for i in attri_list:
            tmp = group.random(ZR)
            # compute C_(Tau,0)
            CT1[i] = h**tmp
            # compute C_(Tau,1)
            A_T = group.init(ZR, int(i))
            CT2[i] = (mpk['u']**A_T * mpk['v'])**tmp * wS
        # ct
        input_for_hash = str(mpk['egg']**s) + str(pair(mpk['g'],h)**(msk['theta'] * s / alpha))
        hashed_value = group.hash(input_for_hash, ZR)
        _ct = int(R) ^ int(hashed_value)
        ct = group.init(ZR, int(_ct))
        # ct_0
        ct_0 ={}
        ct_0['h_s'] = h**s
        ct_0['h_s_alpha'] = h**(s/alpha)
        ct_0['h_beta_s_alpha'] = h**(beta*s/alpha)
        # ct_1
        I = []
        vector_j = 1
        for j in range(self.index_j):
            tmp = group.random(ZR)
            vector_j *= mpk['vector_h_alpha'][self.k-1-j]**tmp
            I.append(tmp)
        vector_j *= h
        ct_1 = vector_j**s
        # compute C{}
        return {'attri_list':attri_list, 'ct':ct, 'CT1':CT1, 'CT2':CT2, 'ct_0':ct_0, 'ct_1':ct_1} 

    def hash(self, mpk, msk, message, attri_list):
        # step 1
        g = mpk['g']
        random_r = group.random(ZR)
        R = group.random(ZR)
        e = group.hash(str(R), ZR)
        p_prime = g**e
        b = g**message * p_prime**random_r

        # step 2
        C = self.helper_gen_ciphertext(mpk, msk, R, attri_list)

        # step 3
        keypair_sk = group.random(ZR)
        keypair_pk = g**keypair_sk
        esk = group.random(ZR)
        epk = g**esk
        c = g**(keypair_sk + R) 
        sigma = esk + keypair_sk * group.hash((str(epk)+str(c)), ZR)
        print("b:", b, "\nmessage:", message)
        return {'message':message, 'p_prime':p_prime, 'b':b, 'random_r':random_r, 'C':C, 'c':c, 'epk':epk, 'sigma': sigma, 'keypair_pk':keypair_pk}

    def verify(self, mpk, message, p_prime, b, random_r, C, c, epk, sigma, keypair_pk):
        g = mpk['g']
        g_message_p_prime_r = g**message * p_prime**random_r
        epk_pk = epk * keypair_pk**group.hash(str(epk)+str(c), ZR)
        return (b == g_message_p_prime_r) and (g**sigma == epk_pk)


    # def decrypt(self, mpk, sk, ct, message):
    def adapt(self, mpk, msk, sk, message, p_prime, b, random_r, C, c, epk, sigma, keypair_pk):
        # step 1
        res = self.verify(mpk, message, p_prime, b, random_r, C, c, epk, sigma, keypair_pk)

        # step 2
        policy = util.createPolicy(sk['Policy'])  # Convert a Boolean formula represented as a string into a policy represented like a tree
        # compute w_i
        w = util.getCoefficients(policy)  # Given a policy, returns a coefficient for every attribute
        pruned_list = util.prune(policy, C['attri_list']) # determine whether a given set of attributes satisfies the policy
        if (pruned_list == False):
            return group.init(GT,1)
        # compute B
        B = 1
        for j in range(0, len(pruned_list)):
            # compute Tau, which is the index of attribute Gamma(i) in attri_list
            Tau = pruned_list[j].getAttribute( ) #without the underscore
            # compute i, I={i: rho(i) in attri_list}
            i = pruned_list[j].getAttributeAndIndex( ) #with the underscore
            # compute B
            B *= (pair(sk['SK1'][i], C['ct_0']['h_s']) * pair(sk['SK2'][i], C['CT1'][i]) * pair(C['CT2'][i], sk['SK3'][i])) ** w[i]
        # A
        numerator = pair(sk['sk_1'], C['ct_0']['h_s_alpha'])
        denominator = pair(sk['sk_0']['g_t_alpha'], C['ct_1']) * pair(sk['sk_0']['g_r'], C['ct_0']['h_beta_s_alpha'])
        A = numerator / denominator
        # decrypt R 
        input_for_hash = str(B) + str(A)
        hashed_value = group.hash(input_for_hash, ZR)
        _R = int(C['ct']) ^ int(hashed_value)
        R = group.init(ZR, int(_R))

        # step 3
        e = group.hash(str(R), ZR)
        message_prime = group.random(ZR)
        random_r_prime = random_r + (message - message_prime) / e

        # step 4
        C_prime = self.helper_gen_ciphertext(mpk, msk, R, C['attri_list'])

        # step 5
        keypair_sk_prime = group.random(ZR)
        keypair_pk_prime = mpk['g']**keypair_sk_prime
        esk_prime = group.random(ZR)
        epk_prime = mpk['g']**esk_prime
        c_prime = mpk['g']**(keypair_sk_prime + R) 
        sigma_prime = esk_prime + keypair_sk_prime * group.hash((str(epk_prime)+str(c_prime)), ZR)

        res_prime = self.verify(mpk, message_prime, p_prime, b, random_r_prime, C_prime, c_prime, epk_prime, sigma_prime, keypair_pk_prime)
        print(res_prime)
        # step 6
        print("b:", b, "\nmessage':", message_prime)

        return {'message_prime':message_prime, 'p_prime':p_prime, 'b':b, 'random_r_prime':random_r_prime, 'C_prime':C_prime, 'c_prime':c_prime, 'epk_prime': epk_prime, 'sigma_prime': sigma_prime}
