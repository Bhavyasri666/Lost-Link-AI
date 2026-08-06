from flask import Flask,render_template,request,redirect,url_for,flash
from database import driver

app=Flask(__name__)
app.secret_key="lostlink123"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search",methods=["POST"])
def search():
    item=request.form["item"].strip()
    with driver.session() as session:
        result=session.run("""
        MATCH(l:LostItem)
       WHERE toLower(l.name)=toLower($item)

       OPTIONAL MATCH(l)-[r:POSSIBLE_MATCH]->(f:FoundItem)

       OPTIONAL MATCH(owner:Person)-[:REPORTED_LOST]->(l)

       RETURN DISTINCT
       l.name AS lost_item,
       f.name AS found_item,
       owner.name AS owner,
       owner.phone AS owner_phone,
       max(r.score) AS score,
       head(collect(r.status)) AS status

       ORDER BY score DESC
       """,item=item)

        matches=[]
        for row in result:
            matches.append({
                "lost_item":row["lost_item"],
                "found_item":row["found_item"],
                "owner":row["owner"],
                "owner_phone":row["owner_phone"],
                "score":row["score"],
                "status":row["status"]
            })

    return render_template("index.html",matches=matches)
@app.route("/report-lost",methods=["GET","POST"])
def report_lost():
    if request.method=="POST":
        owner_name=request.form["owner_name"]
        phone=request.form["phone"]
        email=request.form["email"]
        item_name=request.form["item_name"].strip().title()
        category=request.form["category"]
        brand=request.form.get("brand","").strip()
        color=request.form["color"]
        location=request.form["location"]
        lost_date=request.form["lost_date"]
        description=request.form["description"]

        with driver.session() as session:
            session.run("""
            MERGE(p:Person{phone:$phone})
            SET p.name=$owner_name,p.email=$email
            CREATE(i:LostItem{
            name:$item_name,
            brand:$brand,
            color:$color,
            lost_date:$lost_date,
            description:$description,
            status:"Lost"
            })
            CREATE(p)-[:REPORTED_LOST]->(i)
            MERGE(c:Category{name:$category})
            MERGE(l:Location{name:$location})
            CREATE(i)-[:BELONGS_TO]->(c)
            CREATE(i)-[:LAST_SEEN_AT]->(l)
            """,
            owner_name=owner_name,
            phone=phone,
            email=email,
            item_name=item_name,
            brand=brand,
            color=color,
            lost_date=lost_date,
            description=description,
            category=category,
            location=location)

        flash("✅ Lost Item Report Submitted Successfully!")
        return redirect(url_for("home"))

    return render_template("report_lost.html")


@app.route("/report-found",methods=["GET","POST"])
def report_found():
    if request.method=="POST":
        finder_name=request.form["finder_name"]
        phone=request.form["phone"]
        email=request.form["email"]
        item_name=request.form["item_name"].strip().title()
        category=request.form["category"]
        brand=request.form.get("brand","").strip()
        color=request.form["color"]
        location=request.form["location"]
        found_date=request.form["found_date"]
        description=request.form["description"]

        with driver.session() as session:
            session.run("""
            MERGE(p:Person{phone:$phone})
            SET p.name=$finder_name,p.email=$email
            CREATE(f:FoundItem{
            name:$item_name,
            brand:$brand,
            color:$color,
            found_date:$found_date,
            description:$description,
            status:"Found"
            })
            CREATE(p)-[:REPORTED_FOUND]->(f)
            MERGE(c:Category{name:$category})
            MERGE(l:Location{name:$location})
            CREATE(f)-[:BELONGS_TO]->(c)
            CREATE(f)-[:FOUND_AT]->(l)
            """,
            finder_name=finder_name,
            phone=phone,
            email=email,
            item_name=item_name,
            brand=brand,
            color=color,
            found_date=found_date,
            description=description,
            category=category,
            location=location)

            session.run("""
            MATCH(l:LostItem)
            MATCH(f:FoundItem)
            WHERE toLower(l.name)=toLower(f.name)
            MERGE(l)-[r:POSSIBLE_MATCH]->(f)
            SET r.score=100,
            r.status="High Confidence"
            """)

        flash("✅ Found Item Report Submitted Successfully!")
        return redirect(url_for("home"))

    return render_template("report_found.html")
@app.route("/dashboard")
def dashboard():
    with driver.session() as session:
        lost=session.run("MATCH(n:LostItem) RETURN count(n) AS c").single()["c"]
        found=session.run("MATCH(n:FoundItem) RETURN count(n) AS c").single()["c"]
        people=session.run("MATCH(n:Person) RETURN count(n) AS c").single()["c"]
        matches=session.run("MATCH()-[r:POSSIBLE_MATCH]->() RETURN count(r) AS c").single()["c"]

    return render_template("dashboard.html",
    lost=lost,
    found=found,
    people=people,
    matches=matches)


if __name__=="__main__":
    app.run(debug=True)