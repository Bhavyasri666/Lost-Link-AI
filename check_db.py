from database import URI
print("CONNECTED TO:", URI)
from database import driver

with driver.session() as session:

    result = session.run("""
    MATCH (n)
    RETURN labels(n), count(n) AS count
    """)

    for r in result:
        print(r)

driver.close()