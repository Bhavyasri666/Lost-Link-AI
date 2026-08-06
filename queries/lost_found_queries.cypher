MATCH 
(l:LostItem),
(f:FoundItem)

WHERE 
l.name = f.name
AND
l.brand = f.brand

RETURN
l,
f;