#coding:utf-8

from basehandler import BaseHandler
import logging
import hashlib,json,base64,uuid
from session import Session
from common import require_logined


def sha1(strs):
    """sha1加密"""
    m=hashlib.sha1()
    m.update(strs)
    ret=m.hexdigest()
    return ret

def randstr():
    """生成随机数"""
    randstr=base64.b64encode(uuid.uuid4().bytes)
    return randstr

class IndexHandler(BaseHandler):
    def get(self):        
        # self.write("hello tornade!  haha !")
        return self.redirect('/html/index.html');


class ImageCodeHandler(BaseHandler):
    def get(self):
        code_id=self.get_argument("codeid")
        pre_code_id=self.get_argument("pcodeid")
        if pre_code_id:
            try:
                self.redis.delete('')
            except Exception as e:
                logging.error(e.message)
        #生成验证码（生成新验证码id,以及验证码2进制数据
        new_img_code=1
        new_img=''
        try:
            self.redis.setecx('img_code',120,new_img)
        except Exception as e:
            logging.error(e.message)
            self.write("")

        self.write(new_img)
        self.set_header('Content-Type',"image/jpg")


class RegisterHandler(BaseHandler):
    def post(self):
        user_phone=self.get_argument("user_phone")
        user_password = self.get_argument("user_password")
        user_name=self.get_argument('user_name',randstr()[:6].lower())
        #print(user_phone)
        
        try:
            #先查询是否已存在手机号码
            sel_phone="select count(*) as count from user_info where user_phone=%(user_phone)s"
            ret_count=(self.db.get(sel_phone,user_phone=user_phone)).get('count',-1)
            print(ret_count)
            if(ret_count > 0 ):
                json_data={"ret":"2","msg":"手机号码已经注册!"}
                return self.write(json_data)

            user_password=sha1(user_password)
            sql="insert into user_info(user_phone,user_name,user_password) values(%(user_phone)s,%(user_name)s,%(user_password)s)"
            ret=self.db.execute_rowcount(sql,user_phone=user_phone,user_password=user_password,user_name=user_name)
        except Exception as e:
            logging.error(e.message)
            json_data={"ret":"0","msg":"注册失败!请稍后重试!"}
            self.write(json_data)
        else:
            if ret == 1:
                logging.debug("注册成功!")
                json_data={"ret":"1"}
            else:
                logging.debug("注册失败!");
                json_data={"ret":"0","msg":"注册失败!请稍后重试!"}
            self.write(json_data)
   
    def get(self):
        print('register grt')
        
class LoginHandler(BaseHandler):
    def post(self):
        user_phone=self.get_argument("user_phone")
        user_password = self.get_argument("user_password")
        try:
            sql="select user_password,user_name,user_id from user_info where user_phone=%(user_phone)s"
            ret=self.db.get(sql,user_phone=user_phone)
            
            sel_password=ret.get('user_password','') if ret else ''

            if sel_password == '':
                return self.write({"ret":"-1","err_msg":"号码不存在!"})
            else:
                self.user_name=ret.get('user_name','') if ret else ''
                self.user_id=ret.get('user_id','') if ret else ''
                self.user_phone=user_phone
        except Exception as e:
            logging.error(e.message)
            return self.write({"ret":"0","err_msg":e.message})
        else:
            if sha1(user_password) == sel_password:
                try:
                    session=Session(self)
                    session.save()
                except Exception as e:
                    return self.write({"ret":"0","msg":"会话已过期,请重新登录！"})
                else:
                    return self.write({"ret":"1"})
            else:
                print("err user_password")
                self.write({"ret":"2","err_msg":"密码错误!"})
    
class LogoutHandler(BaseHandler):
    def get(self):
        ret=self.get_current_user()
        if ret:
            self.session.clear()
            self.write({"ret":"1"})
            
class  CheckLogin(BaseHandler):
    """检查用户是否已经登录"""
    def post(self):
        ret=self.get_current_user()
        if ret and ret.get('user_id','') !='' and ret.get('user_name','')!='' and ret.get('user_phone','') !='' :
            self.write({"ret":"1","user_name":self.session.data["user_name"],"user_id":self.session.data["user_id"]})                 
        else:
            self.write({"ret":"0"})

class GetUserInfo(BaseHandler):
    @require_logined
    def get(self):
        ret_data={}
        ret=self.get_current_user()
        if ret:
            user_phone=ret.get("user_phone","")
            user_name=ret.get("user_name","")
            user_photo=""
            sql="select user_photo from user_info where user_phone=%(user_phone)s"
            try:
                ret=self.db.get(sql,user_phone=user_phone)
            except Exception as e:
                logging.error("get photo from mysql error")
                ret_data={
                        "ret":"0",
                        "msg":"获取用户信息失败!",
                }
            else:
                if ret:
                    user_photo=ret.get("user_photo",'')
                    print(user_photo)
                    ret_data={
                            "ret":"1",
                            "user_phone":user_phone,
                            "user_name":user_name,
                            "user_photo":user_photo
                    }
                    # print("ret_success")
            self.write(ret_data)

class AreaInfoHandler(BaseHandler):
    def get(self):
        self.set_header("Content-Type","application/json; charset=UTF-8")
        ret_data={}
        # 获取区县信息
        parent_id=self.get_argument("parent_id",'')
        if parent_id == '':
            ret_data={
                "ret":"0",
                "msg":"获取区域信息失败!",
            }
        else:
            #先去redis当中获取
            area_list=[]
            try:            
                ret=self.redis.get("parent_area_id")                
                if not ret:
                    #redis没查到
                    #redis中没有区域信息，那么再去mysql中获取
                    sql='select area_num,area_name from area_info where parent_area = %(parent_area)s'
                    area_list=self.db.query(sql,parent_area=parent_id)

                    area_li=[]
                    #保存到redis当中
                    try:
                        for each in area_list:
                            area_li.append({"area_num":str(each["area_num"]),"area_name":each["area_name"]})
                    except Exception as e:
                        logging.error(e.message)
                    else:
                        self.redis.setex("parent_area_id",3600*24,json.dumps(area_li))
                        area_list=json.dumps(area_li)
                        print('from mysql')
                else:
                    #从redis查到
                    area_list=ret
                    print("from redis")
                
                    
            except Exception as e:
                logging.error(e.message)
                ret_data={
                    "ret":"2",
                    "msg":"系统错误!",
                }
            else:
                ret_data={
                    "ret":"1",
                    "area_data":area_list
                }        
        self.write(ret_data)

class GetMyhouseList(BaseHandler):
    @require_logined
    def get(self):
        ret_data={}
        ret=self.get_current_user()
        if not ret:
            ret_data={
                "ret":"0",
                "msg":"请登录!",
            }
        else:
            user_id=ret.get('user_id')
            user_phone=ret.get('user_phone')
            house_list=[]
            
            try:
                sql="select house_info.house_id as house_id,house_image.image_path as imgsrc,house_info.house_address as house_address,house_info.house_price as house_price,house_info.create_time as create_time from house_info left join house_image on house_info.house_id=house_image.house_id where house_info.house_owner=%(user_id)s"                
                ret_list=self.db.query(sql,user_id=user_id)
                for each in ret_list:
                    house_list.append({
                        "house_id":each.house_id,
                        "imgsrc":each.imgsrc,
                        "house_address":each.house_address,
                        "house_price":each.house_price,
                        "create_time":str(each.create_time),
                        })
            except Exception as e:
                logging.error(e.message)
                ret_data={
                    "ret":"2",
                    "msg":"系统错误!",
                }
            else:
                ret_data={
                    "ret":"1",
                    "house_data":house_list
                }

        self.write(ret_data)


class PubNewHouse(BaseHandler):
    def post(self):
        #检验用户是否在线
        ret=self.get_current_user()
        if not ret:
            return self.write({"ret":"0","msg":"请先登录!"})
        user_id=ret.get("user_id")


        # 获取传递的参数
        from column_map import house_info_map,house_facility_map
        house_args={}
        for key in house_info_map.keys():
            val=self.get_argument(key,'')
            if val != '':
                house_args[house_info_map[key]]=val.encode('utf-8')
                print(house_args[house_info_map[key]])

        house_args['house_owner']=user_id
        house_info_insert=self.sql_combain(house_args,'house_info')

        
        #拼接sql
        print(house_info_insert)
        try:
            # 提交事务
            self.db.execute("begin;")
            #执行sql        
            try:
                house_id=self.db.execute(house_info_insert)
                print('house_id'+str(house_id))
                if not house_id:
                    # raise 'execute error' 
                    logging.error("house_id:"+str(house_id)) 
                    raise Exception

                facility_args={}
                for key in house_facility_map.keys():
                    val=self.get_argument(key,'')
                    if val != '':
                        facility_args[house_facility_map[key]]=val

                facility_args['house_id']=str(house_id)
                house_facility_insert=self.sql_combain(facility_args,'house_facility')

                print(house_facility_insert)
                try:
                    ret=self.db.execute_rowcount(house_facility_insert)
                except Exception as e:
                    logging.error(e.message)
                else:
                    if ret != 1:            
                        logging.error("facility sql ret not equal 1")
                        raise Exception

            except Exception as e:
                logging.error(e.message)
        except Exception as e:
            logging.error(e.message)
            #异常回滚
            self.db.execute('rollback;')
        else:
            #正常提交
            self.db.execute("commit;")
        self.write({"ret":"1"})

    def sql_combain(self,sql_dic,table_name):
        """拼接insert语句"""
        colums=','.join(sql_dic.keys())
        value_list=[]        
        for each_val in sql_dic.values():
            value_list.append("'"+each_val+"'")
        values=','.join(value_list)
        sql='insert into '+table_name+' ('+colums+') values ('+values+');'
        return sql



class GetHouseList(BaseHandler):
    '''获取房屋列表'''
    @require_logined
    def get(self):
        ret_data=self.get_current_user()
        if not ret_data:
            return self.write({"ret":"0","meg":"请先登录!"})
        user_id=ret_data.get('user_id','')
        user_phone=ret_data.get('user_phone','')
        #查询房屋及其拥有者信息
        sql_sel_house="select house_id,house_owner,house_address,house_price,rent_house_num,user_name,user_photo from house_info left join user_info on house_owner=user_id where is_hire=0 order by house_info.upd_time desc;"
        sel_data=None;
        result_data=[]
        try:
            sel_data=self.db.query(sql_sel_house);
        except Exception as e:
            logging.log(e.message)
            return self.write({"ret":"2","msg":"获取房屋列表信息失败!"})

        #查询房屋图片
        sel_house_img="select image_path from house_image inner join house_info on house_image.house_id=house_info.house_id where house_image.house_id=%(house_id)s;"
        #统计房屋下单次数
        sel_house_order_count="select count(*) as count from order_info where houseo_id=%(house_id)s"
        for each in sel_data:
            try:
                ID=each['house_id']
                image_list=self.db.query(sel_house_img,house_id=ID)
                print(image_list)

                count=self.db.get(sel_house_order_count,house_id=ID)
                result_data.append({
                        "house_id":ID,
                        "house_owner":each['house_owner'],
                        "house_address":each["house_address"],
                        "house_price":each["house_price"]/100,
                        "rent_house_num":each["rent_house_num"],
                        "user_name":each["user_name"],
                        "user_photo":each["user_photo"],
                        "images":[img.image_path for img in image_list],
                        "order_count":count['count'],
                    })
            except Exception as e:
                logging.error(e.message)
                continue;
        result={"ret":"1","result_data":result_data}
        return self.write(result)

class GetHouseDetail(BaseHandler):
    def get(self):
        house_id=self.get_argument('house_id',default='')
        if house_id == "":
            return self.write({"ret":0,"msg":"请求错误!"})           
        
        print("GetHouseDetail:"+house_id)
        sel_house_info='select house_info.house_id as house_id,house_info.house_owner as house_owner,house_info.house_address as house_address,house_info.house_area as house_area, house_info.house_price as house_price,house_info.rent_house_num as rent_house_num,house_info.house_type as house_type,house_info.suit_persons as suit_persons,house_info.bed_cond as bed_cond,house_info.deposite as deposite,house_info.least_days as least_days,house_info.most_days as most_days,user_info.user_name as owner_name,user_info.user_photo as user_photo from house_info left join user_info  on house_info.house_owner=user_info.user_id where house_info.house_id=%(house_id)s and house_info.is_hire=0;'
        sel_house_facility='select wifi,hot_water,air_condition,air_warmer,allow_smoke,water_facility,toothbrush,soap,slippers,toilte_paper,towel,bath_liquid,icebox,washing_machine,lift,allow_cook,allow_party,guard_sys,parking_pos,wired_network,tv,bathtub from house_facility where house_id=%(house_id)s';

        house_data={}
        house_facility={}
        try:
            ret_data=self.db.get(sel_house_info,house_id=house_id)
            print(ret_data)
            house_faci=self.db.get(sel_house_facility,house_id=house_id)
            print(house_faci)

        except Exception as e:
            logging.log(e.message)
        else:
            for key,value in ret_data.items():
                if value is None:
                    value = ''
                house_data[key]=value
            from column_map import facility_comment_map
            for key,value in house_faci.items():
                if value is None:
                    value = "0"
                faci_key=facility_comment_map[key]
                house_facility[faci_key]=value

            json_data=json.dumps(house_data)
            self.write({"ret":"1","house_data":json_data,"house_facility":house_facility})


class GetHouseImages(BaseHandler):
    def initialize(self):
        super(GetHouseImages,self).initialize()
        """处理函数映射"""
        self.map={
            "insert":self.getimages,
            "remove":self.removeFromDb,
        }


    def get(self):
        house_id=self.get_argument('house_id',default='')
        operator=self.get_argument('operator',default='')
        if not (house_id and operator) :
            return self.write({"ret":"0","msg":"请求错误！"})

        self.map[operator](house_id)

    def getimages(self,house_id):
        """获取图片"""
        sql='select image_id,image_path,upd_time from house_image where house_id=%(house_id)s;'
        result=[]
        try:
            result=self.db.query(sql,house_id=house_id)
        except Exception as e:
            logging.error(e.message)
            return self.write({"ret":"2","msg":"系统错误"})
        else:
            img_list=[]
            for each in result:
                img_list.append({
                    "image_id":each['image_id'],
                    "image_path":each['image_path'],
                    "upd_time":str(each['upd_time']),
                })
            ret_data={
                "ret":"1",
                "img_list":img_list,
            }
            self.write(ret_data)

    def removeFromDb(self,house_id):
        """删除图片"""
        image_id=self.get_argument('image_id',default='')
        if not (image_id) :
            return self.write({"ret":"0","msg":"请求错误！"})
        sql='delete from house_image where house_id=%(house_id)s and image_id=%(image_id)s;'
        try:
            c=self.db.execute_rowcount(sql,house_id=house_id,image_id=image_id)
            if c != 1:
                return self.write({"ret":"2","msg":"系统错误"})
        except Exception as e:
            logging.error(e.message)
            return self.write({"ret":"2","msg":"系统错误！"})
        else:
            self.write({"ret":"0"})

class GetHouseBreif(BaseHandler):
    def get(self):
        self.house_id=self.get_argument('house_id',default='')
        if not self.house_id:
            return self.write({"ret":"0","msg":"请求错误！"})

        sel_house_breif='select house_price,house_address,deposite,image_path from house_info left join house_image on house_image.house_id=house_info.house_id where house_info.house_id=%(house_id)s limit 1;'
        try:
            result=self.db.get(sel_house_breif,house_id=self.house_id)
            if not result:
                self.write({"ret":"2","msg":"查询房屋信息失败!"})
        except Exception as e:
            logging.error(e.message)
            self.write({"ret":"3","msg":"系统错误!"})
        else:
            ret_data={
                "ret":"1",
                "house_price":str(result['house_price'])[:-2],
                "deposite":str(result['deposite'])[:-2],
                "house_address":result['house_address'],
                "image_path":result['image_path'],
            }
            self.write(ret_data)

class PlaceOrder(BaseHandler):
    def post(self):
        args=self.check_args(house_id=False,house_owner=True)
        if not args:
            self.write("ret":"0","msg":"请求错误！")
        insert_order_sql='insert into order_info(houseo_id,house_owner,house_renter,house_tent) values(%(houseo_id)s,%(house_owner)s,%(house_renter)s,%(house_tent)s);'



