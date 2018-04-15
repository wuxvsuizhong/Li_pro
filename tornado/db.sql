create database TestDB3 default character set utf8;

use TestDB3;
create table user_info(
    user_id bigint unsigned auto_increment comment '用户id',
    user_name varchar(64) not null comment '用户名',
    user_passwd varchar(128) not null comment '密码',
    user_age int unsigned null comment '年龄',
    user_avatar varchar(128) null comment '头像',
    user_phone char(11) not null comment '手机号码',
    creat_time datetime not null default current_timestamp comment '创建时间',
    upd_time datetime not null default current_timestamp comment '更新时间',
    primary key(user_id),
    unique (user_phone)
)engine=InnoDB default charset=utf8 comment'用户信息表';

create table houses(
    house_id bigint unsigned auto_increment comment '房屋id',
    owner_id bigint unsigned not null comment '用户ID',
    house_name varchar(64) not null comment '房屋名',
    house_address varchar(128) not null comment '房屋地址',
    price int unsigned not null comment '价格(单位:分)',
    creat_time datetime not null default current_timestamp comment '创建时间',
    upd_time datetime not null default current_timestamp comment '更新时间',
    primary key(house_id),
    constraint foreign key(owner_id) references user_info(user_id) 
)engine=InnoDB default charset=utf8 comment '房屋信息表';


create table house_image(
    image_id bigint unsigned auto_increment comment '图片id',
    house_id bigint unsigned comment '房屋id',
    img_url varchar(128) not null comment '图片url',
    creat_time datetime not null default current_timestamp comment '创建时间',
    upd_time datetime null default current_timestamp comment '更新时间',
    primary key(image_id),
    constraint foreign key(house_id) references houses(house_id)
)engine=InnoDB default charset=utf8 comment'房屋图片信息表';
