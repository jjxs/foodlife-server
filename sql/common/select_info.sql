select title, message
from mst_info
where
seq = 1 and release_flag = 'Y'
and release_period_from < sysdate 
and ( release_period_to >= sysdate or release_period_to is null)
and language = %(language)s
