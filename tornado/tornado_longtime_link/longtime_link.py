#coding:utf-8

from tornado import web,ioloop,httpserver,options
from uuid import uuid4


class ShoppingCart(object):
    totalInventory=10
    callbacks=[]
    carts={}

    def register(self,callback):
        self.callbacks.append(callback)

    def moveItemToCart(self,session):
        if session in self.carts:
            return

        self.carts[session]=True
        self.notifyCallBacks()


    def removeItemFromCart(self,session):
        if session not in self.carts:
            return

        del(self.carts[session])
        self.notifyCallBacks()

    def notifyCallBacks(self):
        print('callback_list')
        print(self.callbacks)
        
        for c in self.callbacks:
            print 'forloop'
            self.callbackHelper(c)

        self.callbacks=[]

    def callbackHelper(self,callback):
        callback(self.getInventoryCount())

    def getInventoryCount(self):
        return self.totalInventory - len(self.carts)


class DetailHandler(web.RequestHandler):
    def get(self):
        session=uuid4()
        count=self.application.shoppingCart.getInventoryCount()
        self.render("index.html",session=session,count=count)

class CartHandler(web.RequestHandler):
    def post(self):
        action=self.get_argument('action')
        session=self.get_argument('session')

        print("action:"+action)
        print('session'+session)

        if not session:
            self.set_status(400)
            return

        if action =='add':
            self.application.shoppingCart.moveItemToCart(session)
            # self.write({"ret":"0"})
        elif action == 'remove':
            self.application.shoppingCart.removeItemFromCart(session)
        else:
            self.set_status(400)

class StatusHandler(web.RequestHandler):
    @web.asynchronous
    def get(self):
        self.application.shoppingCart.register(self.on_message)

    def on_message(self,count):
        self.write('{"inventoryCount":%d}'%count)
        print('inventoryCount')
        self.finish()


class Application(web.Application):
    def __init__(self):
        self.shoppingCart=ShoppingCart()

        handlers=[
            (r'/',DetailHandler),
            (r'/cart',CartHandler),
            (r'/cart/status',StatusHandler),
        ]

        settings={
            'template_path':'template',
            'static_path':'static',
            'debug':'true',
        }

        web.Application.__init__(self,handlers,**settings)


if __name__ == '__main__':
    options.parse_command_line()

    app=Application()
    server = httpserver.HTTPServer(app)
    server.listen(8000)
    ioloop.IOLoop.current().start()