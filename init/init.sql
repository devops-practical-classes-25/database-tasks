DROP TABLE IF EXISTS grades CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS students CASCADE;

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    group_name VARCHAR(50) NOT NULL
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE grades (
    id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(id),
    course_id INT NOT NULL REFERENCES courses(id),
    grade INT NOT NULL CHECK (grade BETWEEN 1 AND 10),
    date DATE NOT NULL DEFAULT CURRENT_DATE
);

INSERT INTO students (name, group_name) VALUES
('Иван Петров', 'РИС'),
('Анна Иванова', 'Юриспруденция'),
('Сергей Смирнов', 'РИС'),
('Мария Кузнецова', 'Дизайн'),
('Алексей Васильев', 'Юриспруденция');

INSERT INTO courses (name) VALUES
('Математика'),
('Физика'),
('История');

INSERT INTO grades (student_id, course_id, grade, date) VALUES
(1, 1, 10, '2024-03-01'),
(1, 2, 8, '2024-03-02'),
(2, 1, 9, '2024-03-03'),
(2, 3, 10, '2024-03-04'),
(3, 2, 7, '2024-03-05'),
(3, 3, 9, '2024-03-06'),
(4, 1, 10, '2024-03-07'),
(4, 2, 10, '2024-03-08'),
(5, 3, 6, '2024-03-09'),
(5, 1, 8, '2024-03-10'),
(1, 1, 10, '2024-03-11'),
(2, 1, 9, '2024-03-12'),
(3, 2, 10, '2024-03-13'),
(4, 3, 7, '2024-03-14'),
(5, 2, 8, '2024-03-15');

-- 1. Средний балл каждого студента
SELECT 
    s.id,
    s.name,
    s.group_name,
    ROUND(AVG(g.grade)::NUMERIC, 2)::FLOAT AS average_grade
FROM students s
LEFT JOIN grades g ON s.id = g.student_id
GROUP BY s.id
ORDER BY average_grade DESC;

-- 2. Средний балл по каждому курсу
SELECT 
    c.id,
    c.name,
    ROUND(AVG(g.grade)::NUMERIC, 2)::FLOAT AS course_avg
FROM courses c
LEFT JOIN grades g ON c.id = g.course_id
GROUP BY c.id
ORDER BY course_avg DESC;

-- 3. Количество студентов в группах
SELECT 
    group_name,
    COUNT(*) AS students_count
FROM students
GROUP BY group_name
ORDER BY students_count DESC;

-- 4. Студент с максимальным средним баллом
SELECT 
    s.name,
    ROUND(AVG(g.grade), 2) AS max_avg
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id
ORDER BY max_avg DESC
LIMIT 1;

-- 5. Студенты без оценок по курсу "История"
SELECT 
    s.id,
    s.name,
    s.group_name
FROM students s
WHERE NOT EXISTS (
    SELECT 1
    FROM grades g
    JOIN courses c ON g.course_id = c.id
    WHERE g.student_id = s.id 
    AND c.name = 'История'
);

-- 6. Курс с наибольшим количеством оценок "10"
SELECT 
    c.name,
    COUNT(*) AS tens_count
FROM courses c
JOIN grades g ON c.id = g.course_id
WHERE g.grade = 10
GROUP BY c.id
ORDER BY tens_count DESC
LIMIT 1;