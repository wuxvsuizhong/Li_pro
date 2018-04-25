#coding:utf-8
from basehandler import BaseHandler
import logging
import os

USER_PHOTO_OPPOSITE_PATH='static/user_photo/'
HOUSE_IMAGE_OPPOSITE_PATH='static/image/'
# USER_PHOTO_PATH=os.path.join(os.path.dirname(__file__),USER_PHOTO_OPPOSITE_PATH)
# HOUSE_IMAGE_PATH=os.path.join(os.path.dirname(__file__),HOUSE_IMAGE_OPPOSITE_PATH)

class SavePhoto(BaseHandler):
    def post(self):
        self.map={
            "user_photo":self.save_photo,
            "house_image":self.save_houseimage
        }
        try:
            image_data=self.request.files["choose_photo"][0]["body"]
            file_name=self.request.files["choose_photo"][0]["filename"]
            file_type=self.get_argument("image_type",default='')
            if file_type == '':
                return self.write({"ret":"-1"})
            
            # self.save_photo(image_data,file_name)
            print('file_type'+file_type)
            self.map[file_type](image_data,file_name)            
        except Exception as e:
            logging.error(e.message)
            return self.write({"ret":"0"})

    def save_photo(self,image_data,file_name,file_dir=USER_PHOTO_OPPOSITE_PATH):        
        try:
            result=self.save_image2local(image_data,file_name,file_dir)
            if not result:
                return self.write({"ret":"-1"})
        except Exception as e:
            logging.error(e.message)
            return self.write({"ret":"-1"})
        else:            
            #获取用户id
            ret=self.get_current_user()
            if ret:
                user_id=ret["user_id"]
                print("user_id:"+str(user_id))
                #保存文件路径到数据库
                sql="update user_info set user_photo=%(user_photo)s  where user_id=%(user_id)s"
                try:
                    self.db.execute(sql,user_photo=photo_src, user_id=user_id)   
                except Exception as e:
                    logging.error("save user photo to mysql error")
                    self.write({"ret":"0","msg":"系统错误!"})
                else:
                    self.write({"ret":"1","url":"/static/user_photo/"+file_name,"msg":"上传成功!"})
                    print("save to mysql")

            else:
                self.write({"ret":"2","msg":"会话已过期,请重新登录！"})
            
    def save_houseimage(self,image_data,file_name,file_dir=USER_PHOTO_OPPOSITE_PATH):
        try:
            result=self.save_image2local(image_data,file_name,file_dir)
            if not result:
                return self.write({"ret":"-1"})
        except Exception as e:
            logging.error(e.message)
            return self.write({"ret":"-1"}) 
        else:
            #获取房屋id
            house_id=self.get_argument('house_id',default='')
            if house_id == '':
                return self.write({"ret":"3","msg":"请求错误！"})
            sql='insert into house_image (house_id,image_path) values( %(house_id)s, %(image_path)s );'
            sel_time='select upd_time from house_image where image_id=%(image_id)s;'
            try:
                self.img_id=self.db.execute(sql,house_id=house_id,image_path='/'+file_dir+file_name)
                self.img_time=(self.db.get(sel_time,image_id=self.img_id)).get('upd_time','')
            except Exception as e:
                logging.error(e.message)
                self.write({"ret":"0","msg":"系统错误!"})
            else:
                ret_data={
                    "ret":"1",
                    "img_src":'/'+file_dir+file_name,
                    "img_id":self.img_id,
                    "img_time":str(self.img_time)
                }
                self.write(ret_data)

    def save_image2local(self,image_data,file_name,file_dir):
        try:
            whole_path=file_dir+file_name
            with open(whole_path,'wb') as f:
                f.write(image_data)
                print("save image to local")
        except Exception as e:
            logging.error(e.message)
            print("save user_photo error")
            raise Exception

        return True
