-- creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMETER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	ALTER TABLE users ADD COLUMN IF NOT EXISTS total_weighted_score INT NOT NULL;
	ALTER TABLE users ADD COLUMN IF NOT EXISTS total_weight_score INT NOT NULL;

	UPDATE users
		SET total_weighted_score = (
			SELECT SUM(corrections.score * projects.weight)
			FROM corrections
				INNER JOIN projects
					ON corrections.project_id = projects.id
			WHERE corrections.user_id = users.id
		);
	UPDATE USERS
		SET total_weight = (
			SELECT SUM(projects.weigh)
				FROM corrections
					INNER JOIN projects
						ON corrections.project_id = products.id
				WHERE corrections.user_id = users.id
		);
	UPDATE users
		SET users.average_score = IF(
			users.total_weight = 0, 0, users.total_weighted_score / users.total_weight
		);
	ALTER TABLE users
		DROP COLUMN total_weighted_score;
	ALTER TABLE users
		DROP COLUMN total_weigh;
END;
$$
DELIMETER ;
