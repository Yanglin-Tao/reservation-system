create table Customer(
  customer_name varchar(200),
  customer_email varchar(200),
  customer_password varchar(200),
  building_number numeric(5,0),
  street varchar(200),
  city varchar(200),
  state_name varchar(200),
  phone_number numeric(10,0),
  passport_number varchar(200),
  passport_expiration date,
  passport_country varchar(200),
  date_of_birth date,
  primary key(customer_email)
);

create table Airline(
  airline_name varchar(200),
  primary key(airline_name)
);
 
create table Airplane(
  airplane_identification_number numeric(50,0),
  number_seats numeric(3,0),
  manufacture_company varchar(200),
  age numeric(3,0),
  airline_name varchar(200),
  primary key(airplane_identification_number),
  foreign key(airline_name) references Airline(airline_name)
);
 
create table Airport(
  airport_name varchar(200),
  airport_city varchar(200),
  airport_country varchar(200),
  airport_type varchar(200),
  primary key(airport_name)
);

create table Flight(
  flight_number numeric(50,0),
  departure_airport varchar(200),
  departure_date date,
  departure_time time,
  arrival_airport varchar(200),
  arrival_date date,
  arrival_time time,
  airplane_identification_number numeric(50,0),
  base_price numeric(50,0),
  airline_name varchar(200),
  flight_status varchar(200),
  primary key(flight_number, departure_date, departure_time, airline_name),
  foreign key(airline_name) references Airline(airline_name),
  foreign key(arrival_airport) references Airport(airport_name),
  foreign key(departure_airport) references Airport(airport_name),
  foreign key(airplane_identification_number) references Airplane(airplane_identification_number)
);
 
create table Ticket(
  ticket_ID numeric(50,0),
  customer_email varchar(200),
  sold_price numeric(6,0),
  card_type varchar(200),
  card_number numeric(50,0),
  name_on_card varchar(200),
  expiration_date date,
  purchase_date date,
  purchase_time time,
  departure_date date,
  departure_time time,
  flight_number numeric(50,0),
  airline_name varchar(200),
  primary key(ticket_ID),
  foreign key(customer_email) references Customer(customer_email),
  foreign key(flight_number, departure_date, departure_time, airline_name) references Flight(flight_number, departure_date, departure_time, airline_name)
);

create table Purchase(
  customer_email varchar(200),
  ticket_ID numeric(50,0),
  foreign key(customer_email) references Customer(customer_email),
  foreign key(ticket_ID) references Ticket(ticket_ID)
);

create table Airline_Staff(
  user_name varchar(200),
  staff_password varchar(200),
  first_name varchar(200),
  last_name varchar(200),
  date_of_birth date,
  airline_name varchar(200),
  primary key(user_name),
  foreign key(airline_name) references Airline(airline_name)
);

create table staff_phone(
  user_name varchar(200),
  staff_phone numeric(10,0),
  primary key(user_name, staff_phone),
  foreign key(user_name) references Airline_Staff(user_name)
);

create table staff_email(
  user_name varchar(200),
  staff_email varchar(200),
  primary key(user_name, staff_email),
  foreign key(user_name) references Airline_Staff(user_name)
);

create table Taken(
  customer_email varchar(200),
  airline_name varchar(200),
  rating numeric(1,0),
  comment varchar(1000),
  flight_number numeric(50,0),
  departure_date date,
  departure_time time,
  foreign key(customer_email) references Customer(customer_email),
  foreign key(airline_name) references Airline(airline_name),
  foreign key(flight_number, departure_date, departure_time, airline_name) references Ticket(flight_number, departure_date, departure_time, airline_name)
  );
