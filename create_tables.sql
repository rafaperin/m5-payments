create table if not exists payments (
	order_id uuid primary key,
    creation_date timestamp default now(),
    payment_status varchar(30) not null
);
