from database import driver

try:
    with driver.session() as session:
        result = session.run("RETURN 'Connected Successfully!' AS message")
        print(result.single()["message"])
except Exception as e:
    print("Connection failed!")
    print(e)
finally:
    driver.close()