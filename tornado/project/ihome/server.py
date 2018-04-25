from tornado import web,httpserver,ioloop
from tornado.options import options,define

from urls import handlers
import config
import torndb
import redis


options.define('port',type=int,default=8000,help='server port')

class Application(web.Application):
    def __init__(self,*args,**kwargs):
        super(Application,self).__init__(*args,**kwargs)
        self.db=torndb.Connection(
            host=config.mysql_options['host'],
            database=config.mysql_options['database'],
            user=config.mysql_options['user'],
            password=config.mysql_options['password']
        )
        
        self.redis=redis.StrictRedis(
            host=config.redis_options['host'],
            port=config.redis_options['port']
        )





def main():
    options.logging=config.log_level
    options.log_file_prefix=config.log_file
    options.parse_command_line()
    app=Application(handlers,**config.settings)
    server=httpserver.HTTPServer(app)
    server.listen(options.port)
    ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
