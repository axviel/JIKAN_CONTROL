CREATE OR REPLACE FUNCTION get_events_in_range(p_start_date date, p_end_date date, p_user_id integer)
 RETURNS TABLE (
	id integer,
	event_type_id integer,
	repeat_type_id integer,
	title VARCHAR,
	description text,
	start_time time,
	end_time time,
	start_date date,
	end_date date,
	user_id integer ,
	is_completed boolean,
	is_hidden boolean
) 
AS $$
DECLARE
   date_record RECORD; 
   event_record RECORD; 
   no_repeat INTEGER = 1;
   daily_repeat INTEGER = 2;
   weekly_repeat INTEGER = 3;
   monthly_repeat INTEGER = 4;
   yearly_repeat INTEGER = 5;
BEGIN

	-- PREP

	-- Temp table that contains all events that could appear in the given time period
	CREATE TEMP TABLE event_collection 
    AS
	SELECT 
		*
	FROM 
		events_event as event
	WHERE 
		--The user's events
		event.is_hidden = false
		AND event.user_id = p_user_id
		AND(
			(
				event.repeat_type_id <> 1
				AND
				event.start_date <= p_end_date
				AND ( 
					event.end_date is null 
					OR 
					event.end_date >= p_start_date 
				)
			)
			OR
			(
				event.repeat_type_id = 1
				AND
				event.start_date BETWEEN p_start_date AND p_end_date
			)
		);
		
	-- Temp table contains the dates that belong to the period
	CREATE TEMP TABLE date_collection 
    AS
	SELECT 
		date(dd)
	FROM 
		generate_series( p_start_date, p_end_date, '1 day'::interval) dd;
	
	-- Temp table that will be the result containing all the instances of the events in the period
	CREATE TEMP TABLE result_events 
	AS 
	SELECT 
		* 
	FROM 
		events_event 
	LIMIT 0;
	
	-- START
		
	-- Insert into result_events all the instances of the events that will be visible during the period
	FOR date_record IN SELECT * FROM date_collection
	LOOP 
		
		-- Loop through all of the events
		FOR event_record IN SELECT * FROM event_collection
		LOOP 
		
			-- If the event is not active, continue with the next iteration
			IF	NOT (
					event_record.start_date <= date_record.date 
					AND (event_record.end_date >= date_record.date OR event_record.end_date IS NULL)
					)
			THEN
				CONTINUE;

			-- If event repeats daily, add it start_date is gte date_record and end_date is lte daterecord or is null
			ELSIF 	event_record.repeat_type_id = daily_repeat
			THEN		

				INSERT INTO 
					result_events (id, event_type_id, repeat_type_id, title, description, start_time, end_time, start_date, end_date, user_id, is_completed, is_hidden)
				VALUES
					(event_record.id, event_record.event_type_id, event_record.repeat_type_id, event_record.title, event_record.description, event_record.start_time, event_record.end_time, date_record.date, event_record.end_date, event_record.user_id, event_record.is_completed, event_record.is_hidden);
				
			-- If event repats weekly, add it if week day matches daterecord weekday
			ELSIF 	event_record.repeat_type_id = weekly_repeat
					AND EXTRACT(DOW FROM event_record.start_date) = EXTRACT(DOW FROM date_record.date)
			THEN	
			
				INSERT INTO 
					result_events (id, event_type_id, repeat_type_id, title, description, start_time, end_time, start_date, end_date, user_id, is_completed, is_hidden)
				VALUES
					(event_record.id, event_record.event_type_id, event_record.repeat_type_id, event_record.title, event_record.description, event_record.start_time, event_record.end_time, date_record.date, event_record.end_date, event_record.user_id, event_record.is_completed, event_record.is_hidden);
				
			-- If event repeats monthly, yearly or does not repeat at all, add when conditions match
			ELSE
				-- If repeats monthly, add if day number is the same
				IF  event_record.repeat_type_id = monthly_repeat
					AND EXTRACT(DAY FROM event_record.start_date) = EXTRACT(DAY FROM date_record.date)
				THEN
				
					INSERT INTO 
					result_events (id, event_type_id, repeat_type_id, title, description, start_time, end_time, start_date, end_date, user_id, is_completed, is_hidden)
				VALUES
					(event_record.id, event_record.event_type_id, event_record.repeat_type_id, event_record.title, event_record.description, event_record.start_time, event_record.end_time, date_record.date, event_record.end_date, event_record.user_id, event_record.is_completed, event_record.is_hidden);
					 
				ELSIF 	event_record.repeat_type_id = yearly_repeat
						AND EXTRACT(DAY FROM event_record.start_date) = EXTRACT(DAY FROM date_record.date )
						AND EXTRACT(MONTH FROM event_record.start_date) = EXTRACT(MONTH FROM date_record.date )
				THEN
				
					INSERT INTO 
					result_events (id, event_type_id, repeat_type_id, title, description, start_time, end_time, start_date, end_date, user_id, is_completed, is_hidden)
				VALUES
					(event_record.id, event_record.event_type_id, event_record.repeat_type_id, event_record.title, event_record.description, event_record.start_time, event_record.end_time, date_record.date, event_record.end_date, event_record.user_id, event_record.is_completed, event_record.is_hidden);
					
				ELSIF 	event_record.repeat_type_id = no_repeat
						AND EXTRACT(DAY FROM event_record.start_date) = EXTRACT(DAY FROM date_record.date )
						AND EXTRACT(MONTH FROM event_record.start_date) = EXTRACT(MONTH FROM date_record.date )
						AND EXTRACT(YEAR FROM event_record.start_date) = EXTRACT(YEAR FROM date_record.date )
				THEN
				
					INSERT INTO 
					result_events (id, event_type_id, repeat_type_id, title, description, start_time, end_time, start_date, end_date, user_id, is_completed, is_hidden)
				VALUES
					(event_record.id, event_record.event_type_id, event_record.repeat_type_id, event_record.title, event_record.description, event_record.start_time, event_record.end_time, date_record.date, event_record.end_date, event_record.user_id, event_record.is_completed, event_record.is_hidden);
					
				END IF;
				
			END IF;
		
			-- If event end date is equal to the date_record then remove it from the table
			IF 	event_record.end_date = date_record.date 
			THEN
				DELETE
				FROM
					event_collection
				WHERE
					event_collection.id = event_record.id;				
			END IF;
		

		END LOOP;
	
	END LOOP;
	
	-- END
		
	-- Return the result
	RETURN QUERY
	SELECT 
		*
	FROM
		result_events
	ORDER BY
		start_date,
		start_time;

	-- Drop the temp tables
	DROP TABLE event_collection;
	DROP TABLE date_collection;
	DROP TABLE result_events;

END;
$$
LANGUAGE 'plpgsql';  

-----------------------------------------------
-- TEST
--select * from get_events_in_range(date('2020-03-30'), date('2020-04-30'), 1);
