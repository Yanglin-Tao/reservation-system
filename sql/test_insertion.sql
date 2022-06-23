/*insert Airline*/
insert into Airline values('Jet Blue');
insert into Airline values('United Airlines');

/*insert Airport*/
insert into Airport values('JFK', 'New York', 'United States', 'both');
insert into Airport values('PVG', 'Shanghai', 'China', 'both');
insert into Airport values('LAX', 'Los Angeles', 'United States', 'both');

/*insert Customer*/
insert into Customer values('Yanglin Tao', 'yt2061@nyu.edu', 'p@ssword', 110, 'Livingston St', 'New York', 'NY', 3472003837, 'YT1234567', '2031-02-18', 'China Mainland', '2001-12-27');

insert into Customer values('Tianzuo Liu', 'tl3119@nyu.edu', 'logmein123', 370, 'Jay St', 'New York', 'NY', 8632473460, 'TL7654321', '2031-01-01', 'China Mainland', '2002-01-01');

insert into Customer values('Yuting Li', 'yl7685@nyu.edu', 'imjustin456', 370, 'Jay St', 'New York', 'NY', 8335482809, 'YL432561', '2031-06-13', 'China Mainland', '2002-01-01');

/*insert Airplane*/
insert into Airplane values(777330, 368, 'Boeing', 10, 'Jet Blue');
insert into Airplane values(737009, 159, 'Boeing', 3, 'United Airlines');
insert into Airplane values(787010, 276, 'Boeing', 2, 'Jet Blue');

/*insert Airline_Staff*/
insert into Airline_Staff values('worker01',  '12345', 'Jack', 'Green',  '1990-12-03', 'Jet Blue');
insert into staff_phone values('worker01', 3203645377);
insert into staff_email values('worker01', 'jackgreen@gmail.com');

insert into Airline_Staff values('worker02',  '67890', 'Jane', 'Doe',  '1992-05-03', 'United Airlines');
insert into staff_phone values('worker02',5169902432);
insert into staff_email values('worker02', 'janedoe@gmail.com');

INSERT INTO Airline_Staff VALUES ('worker03', '12345', 'James', 'Wayne', '1991-12-02', 'Jet Blue');
INSERT INTO staff_phone VALUES ('worker03', 3472883737);
INSERT INTO staff_email VALUES ('worker03', 'jameswayne@gmail.com');



/*insert Flight*/
insert into Flight values(350204, 'JFK', '2022-03-20', '22:15:00', 'LAX', '2022-03-21', '03:30:00', 777330, 199,'Jet Blue', 'delayed'); 

insert into Flight values (350206, 'JFK', '2022-07-25', '16:00:00' , 'PVG', '2022-07-26', '09:20:00', 737009, 1000, 'United Airlines', 'on time');

insert into Flight values (350220, 'LAX', '2022-05-20', '08:00:00' , 'JFK', '2022-05-20', '14:30:00' ,787010, 199, 'Jet Blue', 'on time');

insert into Flight values (350222, 'LAX', '2022-07-01', '22:00:00' , 'PVG', '2022-07-02', '13:30:00' ,787010, 1100, 'Jet Blue', 'on time');

/*insert Ticket and Purchase records*/
insert into Ticket values(177602,'yl7685@nyu.edu', 180, 'credit', 82222222232, 'Yuting Li', '2022-12-03', '2022-03-12', '15:00:02', '2022-03-20', '22:15:00',350204, 'Jet Blue');

insert into Ticket values(177688,'tl3119@nyu.edu', 1100, 'debit', 82222228523, 'Tianzuo Liu', '2022-10-12', '2021-12-30', '18:44:02', '2022-07-25', '16:00:00', 350206, 'United Airlines');

insert into Ticket values(195602,'yt2061@nyu.edu', 210, 'credit', 82923622232, 'Yanglin Tao', '2022-12-03', '2022-05-15', '18:00:00', '2022-05-20', '08:00:00', 350220, 'Jet Blue');

insert into Ticket values(195660,'yt2061@nyu.edu', 1100, 'credit', 82923622232, 'Yanglin Tao', '2022-12-03', '2022-06-25', '17:00:00', '2022-07-01', '22:00:00', 350222, 'Jet Blue');

insert into Purchase values('yl7685@nyu.edu', 177602);
insert into Purchase values('tl3119@nyu.edu', 177688);
insert into Purchase values('yt2061@nyu.edu', 195602);
insert into Purchase values('yt2061@nyu.edu', 195660);