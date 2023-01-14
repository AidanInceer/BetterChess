def get_sql_file(sqlfilepath, **kwargs):
    with open(sqlfilepath) as file:
        sql = file.read()
    return sql
