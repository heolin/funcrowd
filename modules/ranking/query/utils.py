'''
Query used to get neighbour values for selected user
Params:
0 - ranking base query
1 - user id
2 - neighbourhood size
'''
RANKING_NEIGHBOURHOOD_QUERY = """
with cte as (
    {0}
), current as (
    select
        row_number
    from
        cte
    where
        user_id = {1}
)
select 
    cte.*
from
    cte, current
where 
    abs(cte.row_number - current.row_number) <= {2}
order by cte.row_number;
"""


'''
Query used to create a ranking pagination query
Params:
0 - ranking base query
1 - page size
2 - page offset = page number * page size
'''
RANKING_PAGINATION_QUERY = """
{0}
limit {1} offset {2}
"""
