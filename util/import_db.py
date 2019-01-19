import csv
from products.models import Product
import django.db.utils as dbutil
from django.contrib.auth.models import User

def import_into_Product_db(csv_path):
    with open(csv_path) as f:
        next(f)  # skip the first line in csv
        reader = csv.reader(f)
        for row in reader:
            try:
                created = Product.objects.create(
                    title=row[0].strip().lower(),
                    price=float(row[1]),
                    inventory_count=int(row[2])
                )
                print(created)

            except dbutil.IntegrityError:
                print("product %s existed, skip" % row[0])


# csv_path = 'util/data.csv'
# import_into_Product_db(csv_path)

def fake_user():
    try:
        authuser = User.objects.create_user(username='test_user', email='fake@email.com', password='temp_password')
        print(authuser)

    except Exception as e:
        print(str(e))