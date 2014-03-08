import threading
import traceback

class M(object):
	def __init__(self):
		self.lck = threading.Lock()
		self.d = {}

	def get(self, k, df=None):
		with self.lck:
			v = self.d.get(k, None)

		if v is None and df is not None:
			try:
				v, store = df()
				if store:
					with self.lck:
						self.d[k] = v
			except Exception:
				v = None
				print(traceback.format_exc())

		return v

	def put(self, k, v):
		with self.lck:
			old_v = self.d.get(k, None)
			self.d[k] = v
			return old_v

	def delete(self, k):
		with self.lck:
			old_v = self.d.get(k, None)

			try:
				del self.d[k]
			except Exception:
				pass

			return old_v

	def incr(self, k, i=1):
		with self.lck:
			old_v = self.d.get(k, 0)
			self.d[k] = old_v + i
			return old_v

	def decr(self, k, i=1):
		with self.lck:
			old_v = self.d.get(k, 0)
			self.d[k] = old_v - i
			return old_v

	def dict(self):
		with self.lck:
			return self.d.copy()

	def keys(self):
		with self.lck:
			return list(self.d.keys())

	def values(self):
		with self.lck:
			return list(self.d.values())

	def clear(self, m={}):
		with self.lck:
			self.d = m

	def filter(self, f, keys=[]):
		with self.lck:
			if not keys:
				keys = list(self.d.keys())

			for k in keys:
				v = f(k, self.d.get(k))
				if v:
					self.d[k] = v
				else:
					try:
						del self.d[k]
					except KeyError:
						pass

	def __len__(self):
		with self.lck:
			return len(self.d)

class O(object):
	def __init__(self, **kw):
		self.__dict__.update(kw)

class Counter(object):
	def __init__(self):
		self.n = 0
		self.lck = threading.Lock()

	def next(self):
		with self.lck:
			self.n += 1
			return self.n

def filter_bool(it):
	return [v for v in it if v]

def filter_none(it):
	return [v for v in it if v is not None]

def id(v):
	return v

def filter_join(it, sep='', out=None):
	if not out:
		out = id
	return sep.join((out(v) for v in it if v))
