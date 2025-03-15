CREATE TABLE public.sex (
	id serial NOT NULL,
	name varchar(20),
	CONSTRAINT sex_unique_constraint UNIQUE (name),
	CONSTRAINT sex_pk PRIMARY KEY (id)
);

INSERT INTO public.sex (id, name) VALUES (E'1', E'male');
INSERT INTO public.sex (id, name) VALUES (E'2', E'female');

CREATE TABLE public.person (
	id serial NOT NULL,
	name varchar(255) NOT NULL,
	birth_date date NOT NULL,
	sex_id integer NOT NULL,
	CONSTRAINT person_pk PRIMARY KEY (id)
);

ALTER TABLE public.person ADD CONSTRAINT fk_person_sex FOREIGN KEY (sex_id)
REFERENCES public.sex (id);

INSERT INTO public.person (id, name, birth_date, sex_id) VALUES (1, 'John Dow', '2000-01-01', 1);
INSERT INTO public.person (id, name, birth_date, sex_id) VALUES (2, 'Jane Dow', '2001-06-15', 2);


CREATE TABLE public.student_group (
	id serial NOT NULL,
	name varchar(255) NOT NULL,
	CONSTRAINT student_group_unique_constraint UNIQUE (name),
	CONSTRAINT student_group_pk PRIMARY KEY (id)
);

INSERT INTO public.student_group (id, name) VALUES (1, 'test-25-1');
INSERT INTO public.student_group (id, name) VALUES (2, 'test-25-2');


CREATE TABLE public.student (
	id serial NOT NULL,
	person_id INTEGER NOT NULL,
	student_group_id INTEGER NOT NULL,
	CONSTRAINT student_pk PRIMARY KEY (id)
);
ALTER TABLE public.student ADD CONSTRAINT fk_student_person FOREIGN KEY (person_id)
REFERENCES public.person (id);
ALTER TABLE public.student ADD CONSTRAINT fk_student_student_group FOREIGN KEY (student_group_id)
REFERENCES public.student_group (id);

INSERT INTO public.student (id, person_id, student_group_id) VALUES (1, 1, 1);
INSERT INTO public.student (id, person_id, student_group_id) VALUES (2, 2, 2);