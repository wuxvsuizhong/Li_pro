#coding:utf-8
import handlers,os
from basehandler import StaticFileHandler
import putfile

handlers=[
    (r'/',handlers.IndexHandler),
    (r'/html/(.*)',StaticFileHandler,
    dict(path=os.path.join(os.path.dirname(__file__),'html'),default_filename='index.html')),
    (r'/register',handlers.RegisterHandler),
    (r'/login',handlers.LoginHandler),
    (r'/check_login',handlers.CheckLogin),
    (r'/putphoto/revise_photo',putfile.SavePhoto),
    (r'/userlogout',handlers.LogoutHandler),
    (r'/getuserinfo',handlers.GetUserInfo),
    (r'/getareainfo',handlers.AreaInfoHandler),
    (r'/myhouselist',handlers.GetMyhouseList),
    (r'/pubnewhouse',handlers.PubNewHouse),
    (r'/gethouselist',handlers.GetHouseList),
    (r'/gethousedetail',handlers.GetHouseDetail),
    (r'/gethouseimages',handlers.GetHouseImages),
    (r'/removehouseimage',handlers.GetHouseImages),
    (r'/gethousebreif',handlers.GetHouseBreif),
    (r'/placeorder',handlers.PlaceOrder),
]
