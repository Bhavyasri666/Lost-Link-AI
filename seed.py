from database import driver
import random

def seed():
    with driver.session() as session:
        session.run("MATCH(n) DETACH DELETE n")
        print("Database Cleared")

        categories=[
            "Mobile","Laptop","Wallet","Documents","Keys",
            "Bag","Watch","Jewellery","Electronics",
            "Books","ID Cards","Accessories"
        ]

        brands=[
            "Apple","Samsung","Dell","HP","Lenovo",
            "OnePlus","Boat","Sony","Casio","Nike"
        ]

        locations=[
            "Railway Station","Bus Stand","College Campus",
            "Shopping Mall","Airport","Office Building",
            "Metro Station","Hospital","Library","Restaurant"
        ]

        for c in categories:
            session.run(
            "CREATE(:Category{name:$name})",
            name=c
            )

        for b in brands:
            session.run(
            "CREATE(:Brand{name:$name})",
            name=b
            )

        for l in locations:
            session.run(
            "CREATE(:Location{name:$name})",
            name=l
            )

        print("Master Data Added")

        people=[
            "Rahul","Priya","Arjun","Sneha","Kiran",
            "Anjali","Ravi","Pooja","Vikram","Neha",
            "Sai","Vijay","Kavya","Manoj","Asha",
            "Rohan","Divya","Nikhil","Swathi","Tarun",
            "Meena","Harsha","Deepika","Varun",
            "Keerthi","Akash","Sanjay","Teja",
            "Lavanya","Surya"
        ]

        for i,name in enumerate(people):
            session.run(
            """
            CREATE(:Person{
            name:$name,
            phone:$phone,
            email:$email
            })
            """,
            name=name,
            phone=f"987650{i:03}",
            email=f"{name.lower()}@lostlink.com"
            )

        print("Users Added")
        items=[
        {"name":"iPhone 15","category":"Mobile","brand":"Apple","color":"Black","location":"Railway Station"},
        {"name":"Samsung Galaxy S24","category":"Mobile","brand":"Samsung","color":"Blue","location":"Bus Stand"},
        {"name":"OnePlus 12","category":"Mobile","brand":"OnePlus","color":"White","location":"Airport"},
        {"name":"Dell Laptop","category":"Laptop","brand":"Dell","color":"Grey","location":"College Campus"},
        {"name":"HP Pavilion Laptop","category":"Laptop","brand":"HP","color":"Silver","location":"Library"},
        {"name":"Lenovo ThinkPad","category":"Laptop","brand":"Lenovo","color":"Black","location":"Office Building"},
        {"name":"Gold Ring","category":"Jewellery","brand":"","color":"Golden","location":"Shopping Mall"},
        {"name":"Silver Chain","category":"Jewellery","brand":"","color":"Silver","location":"Hospital"},
        {"name":"Diamond Bracelet","category":"Jewellery","brand":"","color":"Silver","location":"Restaurant"},
        {"name":"Boat Earbuds","category":"Electronics","brand":"Boat","color":"White","location":"Bus Stand"},
        {"name":"Sony Headphones","category":"Electronics","brand":"Sony","color":"Black","location":"Airport"},
        {"name":"Smart Watch","category":"Watch","brand":"Boat","color":"Black","location":"Metro Station"},
        {"name":"Casio Watch","category":"Watch","brand":"Casio","color":"Silver","location":"Office Building"},
        {"name":"College ID Card","category":"ID Cards","brand":"","color":"Blue","location":"College Campus"},
        {"name":"Passport","category":"Documents","brand":"","color":"White","location":"Airport"},
        {"name":"PAN Card","category":"Documents","brand":"","color":"White","location":"Railway Station"},
        {"name":"Laptop Bag","category":"Bag","brand":"Dell","color":"Black","location":"Library"},
        {"name":"Nike Backpack","category":"Bag","brand":"Nike","color":"Blue","location":"College Campus"},
        {"name":"Leather Wallet","category":"Wallet","brand":"","color":"Brown","location":"Restaurant"},
        {"name":"Nike Wallet","category":"Wallet","brand":"Nike","color":"Black","location":"Shopping Mall"}
        ]

        lost_id=1
        found_id=1

        for item in items:
            person=random.choice(people)
            session.run("""
            MATCH(p:Person{name:$person})
            MATCH(c:Category{name:$category})
            MATCH(b:Brand{name:$brand})
            MATCH(l:Location{name:$location})
            CREATE(i:LostItem{
            itemId:$id,
            name:$name,
            color:$color,
            status:"Lost",
            description:"Lost item reported"
            })
            CREATE(p)-[:REPORTED_LOST]->(i)
            CREATE(i)-[:BELONGS_TO]->(c)
            CREATE(i)-[:HAS_BRAND]->(b)
            CREATE(i)-[:LAST_SEEN_AT]->(l)
            """,
            person=person,
            category=item["category"],
            brand=item["brand"],
            location=item["location"],
            id=f"LOST-{lost_id}",
            name=item["name"],
            color=item["color"])
            lost_id+=1

        for item in items:
            person=random.choice(people)
            session.run("""
            MATCH(p:Person{name:$person})
            MATCH(c:Category{name:$category})
            MATCH(b:Brand{name:$brand})
            MATCH(l:Location{name:$location})
            CREATE(i:FoundItem{
            itemId:$id,
            name:$name,
            color:$color,
            status:"Found",
            description:"Found item reported"
            })
            CREATE(p)-[:REPORTED_FOUND]->(i)
            CREATE(i)-[:BELONGS_TO]->(c)
            CREATE(i)-[:HAS_BRAND]->(b)
            CREATE(i)-[:FOUND_AT]->(l)
            """,
            person=person,
            category=item["category"],
            brand=item["brand"],
            location=item["location"],
            id=f"FOUND-{found_id}",
            name=item["name"],
            color=item["color"])
            found_id+=1

        print("Lost and Found Items Added")
        session.run("""
        MATCH(l:LostItem)
        MATCH(f:FoundItem)
        WITH l,f,
        CASE
        WHEN toLower(l.name)=toLower(f.name)
        THEN 100
        ELSE 0
        END
        +
        CASE
        WHEN toLower(l.color)=toLower(f.color)
        THEN 20
        ELSE 0
        END AS score
        WHERE score>=60
        MERGE(l)-[r:POSSIBLE_MATCH]->(f)
        SET r.score=score,
        r.status=
        CASE
        WHEN score>=90 THEN "High Confidence"
        WHEN score>=70 THEN "Medium Confidence"
        ELSE "Low Confidence"
        END
        """)

        print("AI Matches Created")

        nodes=session.run("""
        MATCH(n)
        RETURN count(n) AS total
        """).single()["total"]

        relations=session.run("""
        MATCH()-[r]->()
        RETURN count(r) AS total
        """).single()["total"]

        matches=session.run("""
        MATCH()-[r:POSSIBLE_MATCH]->()
        RETURN count(r) AS total
        """).single()["total"]

        print("----------------------")
        print("DATABASE SEEDED SUCCESSFULLY")
        print("----------------------")
        print("Total Nodes :",nodes)
        print("Total Relationships :",relations)
        print("AI Possible Matches :",matches)
        print("----------------------")


seed()
driver.close()