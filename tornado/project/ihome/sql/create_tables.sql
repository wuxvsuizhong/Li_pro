create table user_info(
    user_id bigint unsigned not null auto_increment comment '用户id',
    user_name varchar(128) not null comment '用户名',
    user_phone char(11) not null comment '手机号码',
    user_password varchar(128) not null comment '密码',
    user_age int unsigned null comment '年龄',
    user_gender char(1) null comment '性别',
    is_house_hodler char(1) not null default 0 comment '是否房东(1:是 0:否)',
    user_photo varchar(128) null comment '用户头像',
    create_time datetime not null default current_timestamp comment '创建时间',
    upd_time datetime null default current_timestamp comment '更新时间',
    primary key(user_id),
    unique(user_phone)
)comment'用户信息表';

create table house_info(
    house_id bigint unsigned not null auto_increment comment '房屋id',
    house_owner bigint unsigned not null comment '房+主',
    house_address varchar(128) not null comment '房屋地址',
    house_area int unsigned not null comment '房屋面积',
    house_price int unsigned not null comment '租金',
    is_hire char(1) not null default 0 comment '1.已出租 0.未出租',
    rent_house_num int unsigned null comment'出租房间数目',
    house_type varchar(128) null comment'户型描述',
    suit_persons int unsigned null comment'宜住人数',
    bed_cond varchar(64) null comment'卧床配置',
    deposite int unsigned null comment'押金数额',
    least_days int unsigned null comment'最少入住天数',
    most_days int unsigned null comment'最多入住天数',
    brief varchar(256) null comment'房屋标题',
    house_on varchar(64) null comment'所在地区',
    create_time datetime not null default current_timestamp comment '创建时间',
    upd_time datetime null default current_timestamp comment '更新时间',
    primary key(house_id)
)comment'房屋信息表';

create table house_facility(
    facility_id bigint unsigned not null auto_increment  comment'房屋设施条目id',
    house_id bigint unsigned not null comment'房屋id',
    wifi char(1) null comment'无线网络 0.未配备 1.已配备,其余类似条目同此',
    hot_water char(1) null comment'热水淋浴',
    air_condition char(1) null comment'空调',
    air_warmer char(1) null comment'暖气',
    allow_smoke char(1) null comment'允许吸烟',
    water_facility char(1) null comment'饮水设备',
    toothbrush char(1) null comment'牙具',
    soap char(1) null comment'香皂',
    slippers char(1) null comment'拖鞋',
    toilte_paper char(1) null comment'手纸',
    towel char(1) null comment'毛巾',
    bath_liquid char(1) null comment'沐浴露、洗发露',
    icebox char(1) null comment'冰箱',    
    washing_machine char(1) null comment'洗衣机',    
    lift char(1) null comment'电梯',
    allow_cook char(1) null comment'允许做饭',
    allow_party char(1) null comment'允许聚会',
    guard_sys char(1) null comment'门禁系统',
    parking_pos char(1) null comment'停车位',
    wired_network char(1) null comment'有线网络',
    tv char(1) null comment'电视',
    bathtub char(1) null comment'浴缸',
    primary key(facility_id),
    unique(house_id)
)comment'房屋配置表';

create table order_info(
    order_id bigint unsigned not null auto_increment comment '订单id',
    order_time datetime not null default current_timestamp comment '下单时间',
    houseo_id bigint unsigned not null comment '房屋id',
    house_owner bigint unsigned not null comment '房主',
    house_renter bigint unsigned not null comment '租客(户名)',
    start_date datetime not null default current_timestamp comment '入住时间',
    end_date datetime null comment '结束时间',
    hire_duration int unsigned null comment '居住时长',
    house_tent int unsigned not null comment '租金(分)',
    create_time datetime not null default current_timestamp comment '创建时间',
    upd_time datetime not null default current_timestamp comment '更新时间', 
    tenter_comment varchar(1024) null comment '租客评价',
    primary key(order_id)
)comment'订单表';

create table house_image (
    image_id bigint unsigned not null auto_increment comment'图片id',
    house_id bigint unsigned not null comment '房屋id',
    image_path varchar(128) not null comment '图片保存路径',
    create_time datetime not null default current_timestamp comment '图片上传时间',
    upd_time datetime not null default current_timestamp comment'图片更新时间',
    primary key(image_id)
)comment'房屋图片信息';


create table area_info(
    area_num int unsigned not null comment'区域代码',
    area_name varchar(128) not null comment'区域名称',
    parent_area int unsigned null comment'上级区域',
    primary key(area_num)
)comment'区域信息表';


alter table house_info add constraint house_owner foreign key(house_owner) references user_info(user_id);
alter table house_facility add constraint house_id foreign key(house_id) references house_info(house_id);
alter table order_info add constraint houseo_id foreign key(houseo_id) references house_info(house_id);
alter table order_info add constraint house_renter foreign key(house_renter) references user_info(user_id);
alter table order_info add constraint houseo_owner foreign key(house_owner) references user_info(user_id);
alter table house_image add constraint housei_id foreign key(house_id) references house_info(house_id);
alter table area_info add constraint parent_area foreign key(parent_area) references area_info(area_num);
alter table house_image add unique key(image_path);