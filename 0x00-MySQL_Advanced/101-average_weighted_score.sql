-- Create the stored procedure
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id INT;
    DECLARE total_score FLOAT;
    DECLARE total_weight FLOAT;
    DECLARE average_score FLOAT;

    -- Cursor to fetch user IDs
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;

    -- Declare handlers
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET @done = TRUE;

    OPEN user_cursor;

    -- Loop through each user
    user_loop: LOOP
        FETCH user_cursor INTO user_id;
        IF @done THEN
            LEAVE user_loop;
        END IF;

        -- Calculate the total weighted score
        SELECT SUM(c.score * p.weight) INTO total_score
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

        -- Calculate the total weight
        SELECT SUM(p.weight) INTO total_weight
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

        -- Calculate the average weighted score
        IF total_weight > 0 THEN
            SET average_score = total_score / total_weight;
        ELSE
            SET average_score = 0;
        END IF;

        -- Update the average weighted score for the user
        UPDATE users
        SET average_score = average_score
        WHERE id = user_id;
    END LOOP;

    CLOSE user_cursor;
END //

DELIMITER ;
