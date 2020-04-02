CREATE OR REPLACE FUNCTION generate_study_events(p_start_date DATE, p_end_date DATE, p_first_hour TIME, p_last_hour TIME, p_remaining_hours INTEGER, p_exam_id INTEGER, p_exam_title VARCHAR(50), p_user_id INTEGER)
 RETURNS INTEGER
AS $$
DECLARE
	previous_remaining_hours INTEGER = 0;
	curr_date DATE = p_start_date;
	curr_hour TIME = p_first_hour;
	is_hour_added BOOLEAN = false;
	new_event_id INTEGER;
	cursor_study_events refcursor;
	rec_event RECORD;
BEGIN
    
	-- PREP
	
	CREATE TEMP TABLE events_in_between
    AS
	SELECT 
		events.*,
		false as is_study_event
	FROM
		get_event_range(p_start_date, p_end_date, p_user_id) as events;
		
	-- START	
		
	-- Loops until every study hour has been asigned or if there are no more available hours to use
	WHILE p_remaining_hours <> 0 AND p_remaining_hours <> previous_remaining_hours LOOP
      
	  -- Update previous remaining hours
	  previous_remaining_hours = p_remaining_hours;
	  -- Reset current hour
	  curr_hour = p_first_hour;
	  
	  -- Find available hours
	  WHILE curr_hour <> p_last_hour AND NOT is_hour_added LOOP
	  
	  -- If no event with conflicting hour was found, add new study event
	  IF NOT EXISTS (
	  					SELECT 
		  					events.id
		  				FROM
		  					events_in_between as events
		  				WHERE 
		  					curr_hour BETWEEN events.start_time AND (events.end_time - (1 * interval '1 minute'))
		  					AND curr_date = events.start_date
	  				)
	  THEN
	  	-- Mark as true
	  	is_hour_added = true; 
		
		-- If previous event is study event exists, update its end_time
		IF EXISTS (
	  					SELECT 
		  					events.id
		  				FROM
		  					events_in_between as events
		  				WHERE 
		  					events.start_date = curr_date
							AND events.end_time = curr_hour
							AND events.is_study_event = true
	  			  )
		THEN
			UPDATE 
				events_in_between as events
			SET
				end_time = curr_hour + (1 * interval '1 hour')
			WHERE 
				events.start_date = curr_date
				AND events.end_time = curr_hour
				AND events.is_study_event = true;
				
		-- Add new study event
		ELSE
		
			INSERT INTO 
				events_in_between (id, event_type_id, repeat_type_id, title, description, start_time, end_time, start_date, end_date, user_id, is_completed, is_hidden, is_study_event)
			VALUES
				(NULL, 
				 3, 
				 1, 
				 CONCAT('Study event for: ', p_exam_title), 
				 CONCAT('Autogenerated study event for exam: ', p_exam_title), 
				 curr_hour, 
				 curr_hour + (1 * interval '1 hour'), 
				 curr_date, 
				 NULL, 
				 p_user_id, 
				 false, 
				 false,
				 true
				);
		
		END IF;
		
	  ELSE
	  
	  	-- Next hour
	  	curr_hour = curr_hour + (1 * interval '1 hour');
		
	  END IF;
	  
	  END LOOP ;
	  
	  
	  -- Decrease remaining hours
	  IF is_hour_added
	  THEN
	  	p_remaining_hours = p_remaining_hours - 1;
		is_hour_added = false;
	  END IF;
	  
	  -- Increase date or reset to start date
	  IF curr_date = p_end_date
	  THEN
	  	curr_date = p_start_date;
	  ELSE
	  	curr_date = date(curr_date + interval '1 day');
	  END IF;
	  
   	END LOOP ;
	
	-- Open cursor
	OPEN cursor_study_events FOR SELECT * FROM events_in_between as events WHERE events.is_study_event = true;
	LOOP
		FETCH cursor_study_events INTO rec_event;
		EXIT WHEN NOT FOUND;
		
		-- Insert new study events in Events table
		INSERT INTO 
			events_event (event_type_id, repeat_type_id, title, description, start_time, end_time, start_date, end_date, user_id, is_completed, is_hidden)
		VALUES
			(rec_event.event_type_id, rec_event.repeat_type_id, rec_event.title, rec_event.description, rec_event.start_time, rec_event.end_time, rec_event.start_date, rec_event.end_date, rec_event.user_id, rec_event.is_completed, rec_event.is_hidden) 
		RETURNING events_event.id INTO new_event_id;
		
		-- Insert ExamStudy table entries
		INSERT INTO
			examstudy_examstudy (exam_id, event_id, created_date, is_hidden)
		VALUES
			(p_exam_id, new_event_id, NOW(), false);
		
		RAISE NOTICE 'New id: %', new_event_id;
		
	END LOOP;
	CLOSE cursor_study_events;
	
	-- END

	-- Return how many hoursdidn't have an event created
	RETURN p_remaining_hours;
	
	-- Drop temp tables
	DROP TABLE events_in_between;

END;
$$
LANGUAGE plpgsql;

---------------- TEST
select * from  generate_study_events(date('2020-03-31'), date('2020-04-29'), '07:00:00'::time, '00:00:00'::time, 48, 26, 'Test Title', 1);

delete from events_event where event_type_id = 3
delete from examstudy_examstudy;
select * from examstudy_examstudy;

