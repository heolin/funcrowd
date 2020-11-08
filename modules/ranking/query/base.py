
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
where
    profile > 0 and
    id > 2570
"""


'''
Base ranking query for mission package statistics

Params:
0 - mission id
'''
MISSION_PACKAGE_RANKING_BASE_QUERY = """

select
    *, row_number() over (order by value desc)
from (
    select
        ums.user_id,
        u.username,
        ums.annotated_documents,
        coalesce(ums.high_agreement_percentage, 0) high_agreement_percentage,
        ump.bonus_exp bonus_exp,
        ceil(
            (ums.annotated_documents * coalesce(ums.high_agreement_percentage, 0) * 10) + 
            ump.bonus_exp
        ) as value
    from
        statistics_usermissionstats ums 
    join
        users_endworker u on u.id = ums.user_id
    join
        tasks_usermissionprogress ump
            on ump.mission_id = {0} and ump.user_id = ums.user_id
    where
        ums.mission_id = {0}
) acu
"""
