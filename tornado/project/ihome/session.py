#coding:utf-8

import uuid,logging,json

class Session(object):
	def __init__(self,request_handler):
		self.request_handler = request_handler
		self.data={}

		#在cookie中获取session_id
		self.session_key=self.request_handler.get_secure_cookie("session_id")
		print("session_key")
		print(self.session_key)

		#如果cookie中拿到了session_id那么，去redis里获取
		if self.session_key:
			#redis里存在session_id,那么去redis中获取看是否存在
			redis_session=None
			try:
				redis_session = self.request_handler.redis.get(self.session_key)
			except Exception as e:
				logging.error(e.message)
				raise Exception
			if redis_session:
				#redis里存在				
				print(redis_session)
				try:
					session_dic=json.loads(redis_session)
					user_name=request_handler.get_argument('user_name',default='')
					user_phone=request_handler.get_argument('user_phone',default='')
					print('session--user_name:')
					print(user_name)
					if(user_name != ''):
						if session_dic['user_name'] != user_name:							
							#身份已经过期
							raise Exception


					self.data["session_id"]=session_dic['session_id']
					self.data["user_name"]=session_dic['user_name']
					self.data["user_id"]=session_dic['user_id']
					self.data["user_phone"]=session_dic['user_phone']
				except Exception as e:
					logging.error(e.message)

			else:
				#redis里不存在
				self.request_handler.clear_cookie("session_id")

		else:
			#没拿到（cookie里没有)
			self.data={}

			

	def save(self):
		self.data["session_id"]=str(uuid.uuid4().get_hex())
		self.data["user_key"]=str(uuid.uuid4().get_hex())#用户一次登录的标识，用于url中识别登录是否过期
		if not getattr(self,'session_key'):
			self.session_key=self.data["session_id"]

		self.data["user_name"]=self.request_handler.user_name
		self.data["user_id"]=self.request_handler.user_id
		self.data["user_phone"]=self.request_handler.user_phone
		# self.data["user_key"]=

		#满足某种条件才执行保存操作
		if self.data["session_id"]:			
			#重新登录保存会话
			try:
				print("save to redis")
				print(self.data['session_id'])
				print(self.session_key)
				self.request_handler.set_secure_cookie("session_id",self.session_key)
				

				#保存
				self.request_handler.redis.setex(self.session_key,3600*24,json.dumps(self.data))

			except Exception as e:
				logging.error(e.message)
				raise "save session_id fail"

	def clear(self):

		try:
			self.request_handler.redis.delete(self.session_key)
			self.request_handler.clear_cookie("session_id")
		except Exception as e:
			logging.error(e.message)
			raise "clear Session error"
		self.data={}
