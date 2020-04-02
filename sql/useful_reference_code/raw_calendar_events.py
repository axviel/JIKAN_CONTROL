
# Get events of an entire year
current_date = datetime.date.today()
start_date = current_date.replace(day=1) - relativedelta.relativedelta(months=6)
month_days = monthrange(start_date.year + 1, start_date.month)[1]
end_date = start_date.replace(day=month_days, month=start_date.month, year=(start_date.year + 1))

db_result = query_result_as_dict("select * from get_events_in_range(%s, %s, %s)", (start_date, end_date,request.user.id))
# db_events = json.dumps(db_events, indent=4, sort_keys=True, default=str)
db_events = {}

for event in db_result:
  # key = event.start_date.strftime("%d/%m/%Y")
  key = event['start_date'].strftime("%m/%d/%Y")

  end_date = event['end_date']
  if end_date != None:
    end_date = end_date.strftime("%m/%d/%Y")

  event_data = {
      'event_id': event['id'],
      'title': event['title'],
      'event_type': event['event_type_id'],
      'repeat_type': event['repeat_type_id'],
      'start_date': key,
      'end_date': end_date,
      'start_time': event['start_time'].strftime("%H:%M"), # Keep only hour and minutes
      'end_time': event['end_time'].strftime("%H:%M"),
      'is_completed': event['is_completed']
    }

  if key in db_events:
    db_events[key].append(event_data)
  else:
    db_events[key] = [event_data]
