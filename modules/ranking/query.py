
'''
Base ranking query used to create annotations count ranking
'''
ANNOTATIONS_COUNT_RANKING_BASE_QUERY = """
select
    *, row_number() over (order by value desc)
from (
    select
        id as user_id, username, coalesce(annotations_count, 0) as value
    from 
        users_endworker
    left outer join (
        select
            user_id, count(user_id) annotations_count
        from
            tasks_annotation a
        where
            annotated = true and
            skipped = false
        group by 1
    ) ac on ac.user_id = id
    where
        profile >= 0
) acu
"""

'''
Base ranking query used to create exp ranking
'''
EXP_RANKING_BASE_QUERY = """
select
    id as user_id, username, exp as value, row_number() over (order by exp desc)
from
    users_endworker
"""


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
