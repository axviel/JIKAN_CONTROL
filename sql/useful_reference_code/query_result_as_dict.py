from django.db import connection

def query_result_as_dict(query, args=(), one=False):
  with connection.cursor() as cursor:
    cursor.execute(query, args)
    r = [dict((cursor.description[i][0], value) \
                for i, value in enumerate(row)) for row in cursor.fetchall()]
    return (r[0] if r else None) if one else r