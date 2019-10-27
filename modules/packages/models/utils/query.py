
UNFINISHED_PACKAGES_QUERY = """
select 
    A.id
from (
    select 
        A.id,
        sum(full_annotations) as annotations_done
    from (
        select
            pp.id,
            a.user_id,
            (count(a.id) / %s) as full_annotations
        from
            packages_missionpackages mp
            left outer join packages_package pp on mp.id = pp.parent_id
            left outer join tasks_item i on pp.id = i.package_id
            left outer join tasks_annotation a on i.id = a.item_id
        where
            mp.id = %s
        group by
            pp.id, a.user_id) as A
    group by
        1) as A
where
    A.annotations_done < %s
"""
