use store;
drop table categories;
drop table products;
CREATE TABLE categories (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL unique,
    PRIMARY KEY (id)
);

create table products(
    id INT NOT NULL AUTO_INCREMENT,
	title varchar(30) not null,
    description varchar(30) not null,
    price float not null,
    img_url varchar(200) not null,
    favorite ENUM("0","1"),
    category_id int not null,
    primary key(id),
     FOREIGN KEY (category_id)
        REFERENCES categories (id)
        ON DELETE cascade
);

insert into categories (name) values('romance'),('fantasy');
insert into products (title,description,price,img_url,favorite,category_id) values('Soul of the Witch','nice book',10.22,'https://ca.ctrinstitute.com/wp-content/uploads/2017/12/Counselling-Insights-Softcover-final.png','1',1),('How to Date Your Dragon','good book',23.99,'https://images-na.ssl-images-amazon.com/images/I/51GU5a3WPHL._SX342_.jpg','1',2);
select * from categories;
select * from products;
-- 'INSERT INTO products (title,description,price,img_url,favorite,category_id) VALUES(%(title)s,%(description)s,%(price)s,%(img_url)s,%(category_id)s)'

-- insert into products (title,description,price,img_url,favorite,category_id) values('The Wolfs Call','best book',22.5,'https://images-na.ssl-images-amazon.com/images/I/51dR4sLUlEL._SX329_BO1,204,203,200_.jpg','1',2);
    
