create table Customer(
   customer_name varchar(20),
   customer_email varchar(20),
   customer_password varchar(20),
   building_number numeric(5,0),
   street varchar(20),
   city varchar(20),
   state_name varchar(20),
   phone_number numeric(10,0),
   passport_number varchar(20),
   passport_expiration date,
   passport_country varchar(20),
   date_of_birth date,
   primary key(customer_email)
);
 
create table Airline(
   airline_name varchar(20),
   primary key(airline_name)
);

create table Airplane(
   airplane_identification_number numeric(20,0),
   number_seats numeric(3,0),
   manufacture_company varchar(20),
   age numeric(3,0),
   airline_name varchar(20),
   primary key(airplane_identification_number),
   foreign key(airline_name) references Airline(airline_name)
);

create table Airport(
   airport_name varchar(20),
   airport_city varchar(20),
   airport_country varchar(20),
   airport_type varchar(20),
   primary key(airport_name)
);
 
create table Flight(
   flight_number numeric(20,0),
   departure_airport varchar(20),
   departure_date_time timestamp,
   arrival_airport varchar(20),
   arrival_date_time timestamp,
   airplane_identification_number numeric(20,0),
   base_price numeric(20,0),
   airline_name varchar(20),
   primary key(flight_number, departure_date_time, airline_name),
   foreign key(airline_name) references Airline(airline_name),
   foreign key(arrival_airport) references Airport(airport_name),
   foreign key(departure_airport) references Airport(airport_name),
   foreign key(airplane_identification_number) references Airplane(airplane_identification_number)
);

create table Ticket(
   ticket_ID numeric(20,0),
   customer_email varchar(20),
   sold_price numeric(6,0),
   card_type varchar(20),
   card_number numeric(20,0),
   name_on_card varchar(20),
   expiration_date date,
   purchase_date_time timestamp,
   departure_date_time timestamp,
   flight_number numeric(20,0),
   airline_name varchar(20),
   primary key(ticket_ID),
   foreign key(customer_email) references Customer(customer_email),
   foreign key(flight_number, departure_date_time, airline_name) references Flight(flight_number, departure_date_time, airline_name)
);
 
create table Purchase(
   customer_email varchar(20),
   ticket_ID numeric(20,0),
   foreign key(customer_email) references Customer(customer_email),
   foreign key(ticket_ID) references Ticket(ticket_ID)
);
 
create table Airline_Staff(
   user_name varchar(20),
   staff_password varchar(20),
   first_name varchar(20),
   last_name varchar(20),
   date_of_birth date,
   airline_name varchar(20),
   primary key(user_name),
   foreign key(airline_name) references Airline(airline_name)
);
 
create table staff_phone(
   user_name varchar(20),
   staff_phone numeric(10,0),
   primary key(user_name, staff_phone),
   foreign key(user_name) references Airline_Staff(user_name)
);
 
create table staff_email(
   user_name varchar(20),
   staff_email varchar(20),
   primary key(user_name, staff_email),
   foreign key(user_name) references Airline_Staff(user_name)
);
 
create table Taken(
   customer_email varchar(20),
   airline_name varchar(20),
   rating numeric(1,0),
   comment varchar(1000),
   foreign key(customer_email) references Customer(customer_email),
   foreign key(airline_name) references Airline(airline_name)
);