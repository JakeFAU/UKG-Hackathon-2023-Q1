import json
import mysql.connector
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    """Handle a Check Out"""

    body = json.loads(event.get("body", {}))
    print("Message Recieved")

    user: str = body.get("employee")
    if not user:
        return {
            "statusCode": 403,
            "body": json.dumps({"message": "User is Missing"}),
        }
    item: str = body.get("object")
    if not item:
        return {
            "statusCode": 403,
            "body": json.dumps({"message": "Item is Missing"}),
        }
    location: str = body.get("location")
    if not location:
        return {
            "statusCode": 403,
            "body": json.dumps({"message": "Location is Missing"}),
        }
    print(f"Item {item} was checked out by {user} at {location}")
    cnx = mysql.connector.connect(
        user="admin",
        passwd="ukg#JacobMariaCorey",
        host="ukghackathondev.czbh3aap8czw.us-east-1.rds.amazonaws.com",
        database="ukgHackathonDev",
        port=4020,
    )

    try:
        cursor = cnx.cursor()
        now = datetime.now()
        sql = f'INSERT INTO ukgHackathonDev.Object_Trx (EmployeeID, ObjectID, DateTime, Location, Type) values ({user}, {item}, "{now}", "{location}", "RETURNED")'
        print(f"SQL={sql}")
        cursor.execute(sql)
        cnx.commit()
        print("Item Registered")
    except Exception as ex:
        print(ex)
        return {"statusCode": 500, "body": json.dumps({"message": "Database Error"})}
    finally:
        cnx.close()
        return {
            "statusCode": 201,
            "body": json.dumps(
                {
                    "message": "TX Recorded",
                    "user": user,
                    "item": item,
                    "location": location,
                }
            ),
        }
