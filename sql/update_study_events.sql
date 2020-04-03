CREATE OR REPLACE PROCEDURE update_study_events(p_exam_id INTEGER)
LANGUAGE plpgsql    
AS $$
BEGIN
    -- PREP

	-- Temp table that contains all events ids that will be deleted
	CREATE TEMP TABLE event_ids
    AS
	SELECT 
		event_id
	FROM 
		examstudy_examstudy AS examstudy
	WHERE 
		examstudy.exam_id = p_exam_id;
		
	-- START
		
	-- Delete ExamStudy records
	DELETE FROM 
		examstudy_examstudy AS examstudy 
	WHERE 
		examstudy.exam_id = p_exam_id;
	
	-- Delete Event records
	DELETE FROM 
		events_event AS event 
	WHERE 
		event.id IN (
					SELECT 
						event_id 
					FROM 
						event_ids
					);
		
	-- END
	
	-- Drop temp table
	DROP TABLE event_ids;
	
END;
$$;

----------------------

CALL update_study_events(26)

select * from events_event
select * from examstudy_examstudy