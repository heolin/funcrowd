

UNFINISHED_PACKAGES_QUERY = """
select 
    A.id
from (
    select 
        A.id,
        SUM(full_annotations) as annotations_done
    from
        (select
            "packages_package"."id",
            "tasks_annotation"."user_id",
            (COUNT("tasks_annotation"."id") / %s) AS "full_annotations"
        from
            "packages_missionpackages"
            LEFT OUTER JOIN "packages_package" ON ("packages_missionpackages"."id" = "packages_package"."parent_id")
            LEFT OUTER JOIN "tasks_item" ON ("packages_package"."id" = "tasks_item"."package_id")
            LEFT OUTER JOIN "tasks_annotation" ON ("tasks_item"."id" = "tasks_annotation"."item_id")
        where
            "packages_missionpackages"."id" = %s
        group by
            "packages_package"."id", "tasks_annotation"."user_id") as A
    group by
        A.id) as A
where
    A.annotations_done < %s"""