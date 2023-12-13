#!/usr/bin/env python3

from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Restaurant, Review, Customer

if __name__ == '__main__':
    engine = create_engine('sqlite:///restaurants.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Restaurant).delete()
    session.query(Review).delete()
    session.query(Customer).delete()

    fake = Faker()

    restaurants = []
    for i in range(50):
        restaurant = Restaurant(
            name=fake.company(),
            price=random.randint(5, 60)
        )

        # add and commit individually to get IDs back
        session.add(restaurant)
        session.commit()

        restaurants.append(restaurant)


    customers = []
    for i in range(25):
        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )

        session.add(customer)
        session.commit()

        customers.append(customer)


    reviews = []
    for restaurant in restaurants:
        for i in range(random.randint(1,5)):
            customer = random.choice(restaurants)
            if restaurant not in customer.restaurants:
                customer.restaurants.append(restaurant)
                session.add(customer)
                session.commit()
            
            review = Review(
                rating=random.randint(0, 10),
                restaurant_id=restaurant.id,
                customer_id=customer.id,
            )

            reviews.append(review)

    session.bulk_save_objects(reviews)
    session.commit()
    session.close()
