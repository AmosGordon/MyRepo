# microbit-module: shift@0.8.0
from Extras.BitBot.cyberbot import *
class shift():
	def __init__(self,p=33,q=33):
		self.pA=p
		self.pB=q
	def tx(self,s,b,d):
		bot(self.pB,self.pA).send_c(18,s,b,d)
	def rx(self,s,b):
		bot(self.pB,self.pA).send_c(17,s,b)
		return bot().read_r()