class Foo(object):
	def __init__(self):
		pass
	'''	
	def __getattr__(self,item):
		print(item,end=" ")
		return self
	'''

	#def __getattribute__(self):
		
	
	def __str__(self):
		return ""

	def say_hello(self):
		pass
	


#print(Foo().think.different.it)
