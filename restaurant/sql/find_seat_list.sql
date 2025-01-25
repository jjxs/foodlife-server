
SELECT
seat.id
, seat_no
, seat.name
, seat.start
, usable
, seat.number
, master1.display_name as seat_type
, master2.display_name as seat_smoke_type
, seat_group.no as group_no
, seat_group.name as group_name
, case when seat_status.number is null then 0 else seat_status.number end as guest_number
, seat_status.utype as guest_utype
, seat_status.start as use_start
FROM seat
    left join seat_group on seat_group.id = seat.group_id
    left join master_data master1 on master1.id = seat_type_id
    left join master_data master2 on master2.id = seat_smoke_type_id
    left join seat_status on seat_status.seat_id = seat.id
WHERE seat.usable = true 
    AND (seat.seat_type_id in %(seat_type)s OR %(seat_type_str)s)
    AND (seat.seat_smoke_type_id in %(seat_smoke_type)s OR %(seat_smoke_type_str)s)
    AND (seat_group.id in %(seat_group)s OR %(seat_group_str)s)
    {0} 
    {1}
ORDER BY lpad(seat_no, 8, '0')
