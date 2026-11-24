CREATE TABLE question(
    id INT AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    first_option VARCHAR(100) NOT NULL,
    second_option VARCHAR(100) NOT NULL,
    third_option VARCHAR(100) NOT NULL,
    fourth_option VARCHAR(100) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE answer(
    id INT AUTO_INCREMENT,
    question_id INT NOT NULL,
    user_id INT NOT NULL,
    selected_option VARCHAR(20) NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(question_id) REFERENCES question(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_question (user_id, question_id)
);

INSERT INTO question (title, first_option, second_option, third_option, fourth_option) VALUES
('Between the following, what do you most love to do?', 'Watch TV', 'Play the computer', 'Hanging out with friends', 'Travel the world'),
('Where is your preferred place to travel?', 'USA', 'France', 'South America', 'Thailand');