from django.db import connections


class QueryUtility:
    '''
    query = raw query to be executed
    params = params to be passed to query
    db = database connection name
    '''

    @staticmethod
    def execute_query(
        query,
        params,
        db='default',
    ):
        with connections[db].cursor() as cursor:
            cursor.execute(query, params)
            query_response = QueryUtility.dict_fetch_all(cursor)
            return query_response

    @staticmethod
    def dict_fetch_all(cursor):
        desc = list(cursor.description)
        response_list = []
        for result in QueryUtility.result_iterator(cursor, 1000):
            response_list.append(dict(zip([col[0] for col in desc], result)))
        return response_list

    # using generator to fetch records in chunks
    @staticmethod
    def result_iterator(cursor, chunk_size):
        while True:
            results = cursor.fetchmany(chunk_size)
            if not results:
                break
            for result in results:
                yield result