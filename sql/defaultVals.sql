INSERT INTO eventtypes_eventtype(id, title, description, is_hidden)
VALUES
	(1, 'Task', 'Task', false),
    (2, 'Reminder', 'Reminder', false),
    (3, 'Study Time', 'Study Time', false),
    (4,'Exam','Exam',false);

INSERT INTO repeattypes_repeattype(id, title, description, is_hidden)
VALUES
    (1,'Does not repeat','no repeat',false),
    (2,'Daily','Daily',false),
    (3,'Weekly','Weekly',false),
    (4,'Monthly','Monthly',false),
    (5,'Yearly','Yearly',false);