insert into user_info(user_name,user_passwd,user_age,user_phone) values ('a','a',20,"12345678901"),('b','b',21,'12345678902'),('c','c',21,'12345678903');

insert into houses(owner_id,house_name,house_address,price) values('1','a的房子','aaaaa',30000),('1','a的房子2','bbbbbb',50000),('2','b的房子','aaaaaaaa',60000);


select houses.house_name,houses.house_address,houses.price,house_image.img_url,user_info.user_name from houses inner join user_info on houses.owner_id=user_info.user_id left join house_image on houses.house_id=house_image.house_id;

