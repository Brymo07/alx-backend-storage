-- Create the stored procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUser
(
    IN user_id INT
)
BEGIN
    -- Declare variables
    DECLARE total_score FLOAT;
    DECLARE total_weight FLOAT;
    DECLARE average_score FLOAT;

    -- Calculate the weighted average score
    SELECT SUM(score * weight) INTO total_score, SUM(weight) INTO total_weight
    FROM scores
    WHERE user_id = user_id;

    -- Compute the average weighted score
    IF total_weight > 0 THEN
        SET average_score = total_score / total_weight;
    ELSE
        SET average_score = 0;
    END IF;

    -- Store the average weighted score for the user
    UPDATE users
    SET average_weighted_score = average_score
    WHERE id = user_id;
END;
