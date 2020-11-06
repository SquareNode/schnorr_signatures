def eea(a, b):
	"""
	returns a tuple (x,y,z)
	where gcd(a,b) = x = y*a + z*b
	"""
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = eea(b % a, a)
		return (g, x - (b // a) * y, y)

def inverse(a, m):
	"""
	calculates modular inverse for a mod m 
	(a*x)%m = 1
	"""
	g, x, y = eea(a, m)
	if g != 1:
		raise Exception('modular inverse does not exist')
	else:
		return x % m

class EC:
	"""
	y^2 = x^3 + a*x + b % p
	with a generator point g
	where a,b belong to Zp
	and a 4a^3 + 27b^2 != 0 % p 
	"""
	def __init__(self, a,b,p,g):
		if a >= p or b >= p or 4*a**3 + 27*b**2 % p == 0:
			raise Exception('invalid ec params')
		self.a = a
		self.b = b
		self.p = p
		if self.on_curve(g):
			self.g = g
		else:
			raise Exception('generator point not on curve')
		self.size = self.get_size()
		
	
	def __str__(self):
		return f'y ^ 2 = x ^ 3 +{self.a} * x + {self.b} mod {self.p},' + \
		f'generator {self.g}, |G| = {self.size}'
	
	#naive approach
	def get_size(self):
		res, card = EC_point.add(self.g, self.g, self), 2
		while not EC_point.is_inf(res):
			res = EC_point.add(res, self.g, self)
			card += 1
		return card
	
	def on_curve(self, point):
		if point.x == point.y == 'inf':
			return True
		if point.y ** 2 % self.p == \
		(point.x ** 3 + self.a * point.x + self.b) % self.p:
			return True
		return False
	
	def n_times_g(self, n):
		if n == 0:
			return EC_point('inf', 'inf')
			
		res = self.g
		n = bin(n)[3:]
		for b in n:
			res = res.add(res, self)
			if b == '1':
				res = res.add(self.g, self)
		
		return res
		
	def n_times_point(self, point, n):
		
		if not self.on_curve(point):
			raise Exception('point not on curve')
		
		res = point
		n = bin(n)[3:]
		for b in n:
			res = res.add(res, self)
			if b == '1':
				res = res.add(point, self)
				
		return res

class EC_point:

	def __init__(self, x,y):
		self.x = x
		self.y = y
		
	def __eq__(self, other):
		if self.x == other.x and self.y == other.y:
			return True
		else:
			return False
	
	def __str__(self):
		return f'({self.x}, {self.y})'
	
	def is_inf(self):
		if self.x == self.y == 'inf':
			return True
		return False
		
	def double(self, ec):
		s = ((3 * self.x**2 + ec.a) % ec.p) * \
		inverse(2 * self.y % ec.p, ec.p)
		x = (s ** 2 - 2*self.x) % ec.p
		y = (s * ((self.x - x) % ec.p) - self.y) % ec.p
		
		return EC_point(x,y)
	
	def inverse(self, ec):
		return EC_point(self.x, -self.y % ec.p)
	
	def add(self,q,ec):
		if self.is_inf():
			return q
		if q.is_inf():
			return self
		if not ec.on_curve(self) and ec.on_curve(q):
			raise Exception('points not on curve')
		if self == q:
			return self.double(ec)
		if q == self.inverse(ec):
			return EC_point('inf', 'inf')
		
		s = (((q.y - self.y) % ec.p ) * \
		inverse((q.x - self.x) % ec.p, ec.p)) % ec.p
		x = (s ** 2 - self.x - q.x) % ec.p
		y = (s * ((self.x - x) % ec.p) - self.y) % ec.p
			
		return EC_point(x,y)	
		
if __name__ == '__main__':
	
	ec = EC(2,2,17,EC_point(6,3))
	print(ec)
	
	print(ec.n_times_g(3))
	print(ec.on_curve(EC_point(13,7)))
	print(EC_point(3,1).add(EC_point(3,1), ec))
	print(EC_point(3,1).add(EC_point(3,1).inverse(ec), ec))