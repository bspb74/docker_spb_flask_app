import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host="bspb-srv",
    user="bspb74",
    password="b$pB742980",
    database="spb_db"
)

cursor = mydb.cursor()

filepath = "./website/static/products/products.xlsx"

df = pd.read_excel(filepath)

list_of_dictionaries = df.to_dict(orient='records')

print(list_of_dictionaries)

sql = 'INSERT IGNORE INTO product (model, prodName, prodType, imgName, price, prodDesc, stockQty) VALUES (%(model)s, %(prodName)s, %(prodType)s, %(imgName)s, %(price)s, %(prodDesc)s, %(stockQty)s);'
# sql = 'UPDATE IGNORE product SET stockQty=%s WHERE prodName=%s;'
for d in list_of_dictionaries:
    print(d.get('stockQty'))
    # values = (d.get('stockQty'), d.get('prodName'))
    cursor.execute(sql, d)
    # cursor.execute(sql, values)

mydb.commit()
cursor.close()
mydb.close()