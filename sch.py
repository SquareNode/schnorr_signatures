from ec import EC, EC_point
from random import randint

def schnorr(ec):

	k = randint(1, ec.size)
	K = ec.n_times_g(k)
	
	print(f'(k, K) = ({k} , {K})')
	
	#1. prover generates a random int a belonging to Zp*
	#computes a*G and sends to verifier
	a = randint(1,ec.size)
	res = ec.n_times_g(a)
	print(f'step 1: a = {a}, res = {res}')
		
	#2. the verifier generates a random challenge c belongig to Zp*
	#sends c to prover
	
	c = randint(1,ec.size)
	print('step 2, c = ', c)
	
	#3. the prover computes the response r = a + c * k
	#and sends it to verifier
	r = a + c * k
	print(f'step 3, r = {r}')
	
	#4. the verifier computes R = r*G and R'= a*G + c*K 
	#and checks R = R'
	
	R = ec.n_times_g(r)
	R_prime = EC_point.add(ec.n_times_g(a), ec.n_times_point(K, c), ec)
	
	print(f'step 4: R = {R}, R_prime = {R_prime}')
	print("SCHNORR SUCCESSFULL == ", R == R_prime)

#hash function for demonstration purposes
def h(point):
	return point.x + point.y if not EC_point.is_inf(point) else 1

def get_sign(k, K, ec):
	
	#1. generate a random num a belonging to Zp*
	#and compute a*G
	a = randint(1, ec.size)
	res = ec.n_times_g(a)
	
	#2.calculate a challenge using h()
	c = h(res)
	
	#3. define the response r = a + c * k
	r = (a + c * k) % ec.size
	
	#4. publish the pair (res, r)
	return (res, r)
	

def verify(sign, ec, K):
	#sign = (a*G, r)
	#1. calculate the challenge using h()
	c_prime = h(sign[0])
	#2. compute R = r*G and R' = a*G + c'*K
	R = ec.n_times_g(sign[1])
	R_prime = EC_point.add(sign[0], ec.n_times_point(K, c_prime), ec)
	
	#3. if R = R' then the prover must know k
	# print(R, R_prime)
	print('verfication successfull == ', R_prime == R)
	

def not_interactive_schnorr(ec):
	
	k = randint(1, ec.size)
	K = ec.n_times_g(k)
	
	sign = get_sign(k, K, ec)
	
	verify(sign, ec, K)

#hash function for demonstration purposes
def h_msg(msg, point):
	return sum([ord(x) for x in msg]) % 13 + \
	((point.x + point.y) if not EC_point.is_inf(point) else 1)

def get_msg_sign(msg, k, K, ec):
	
	#1. generate a random num a belongin to Zp*
	#and compute a*G
	a = randint(1, ec.size)
	res = ec.n_times_g(a)
	
	#2.calculate a challenge using h()
	c = h_msg(msg, res)
	
	#3. define response such that a = r + c * k, r = a - c * k
	r = (a - c * k)  % ec.size
	
	#4. publish signature  pair (c,r)
	return (c, r)
	
def verify_msg_sign(msg, sign, K, ec):
		
	#1. calculate challenge c' = h(msg, [r*G + c*K])
	c_prime = h_msg(msg, EC_point.add(ec.n_times_g(sign[1]),
									ec.n_times_point(K, sign[0]), ec))
	
	#2. if c' = c signature is valid
	print('msg verfication successfull == ', sign[0] == c_prime)


def msg_signing(msg, ec):
	
	k = randint(1, ec.p)
	K = ec.n_times_g(k)
	
	sign = get_msg_sign(msg, k, K, ec)
	
	verify_msg_sign(msg, sign, K, ec)

if __name__ == '__main__':

	ec = EC(2,2,17,EC_point(5,1))
	# ec = EC(5,3,137,EC_point(1,3))
	
	# schnorr(ec)
	# not_interactive_schnorr(ec)
	msg_signing('Greetings verifier!', ec)
	