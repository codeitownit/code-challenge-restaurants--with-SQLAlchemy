from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)
engine = create_engine('sqlite:///restaurant_reviews.db')
Base = declarative_base()

restaurant_customer = Table(
    'restaurant_customers',
    Base.metadata,
    Column('restaurant_id', ForeignKey('restaurants.id'), primary_key=True),
    Column('customer_id', ForeignKey('customers.id'), primary_key=True),
    extend_existing=True,
)

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    price = Column(Integer())

    reviews = relationship('Review', backref=backref('restaurant'))
    customers = relationship('Customer', secondary=restaurant_customer, back_populates='restaurants')

    def __repr__(self):
        return f'Restaurant(id={self.id}, ' + \
            f'name={self.name}, ' + \
            f'price={self.price})'

    def reviews(self):
        return self.reviews

    def customers(self):
        return [review.customer for review in self.reviews]

    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

    def all_reviews(self):
        return [review.full_review() for review in self.reviews]
        

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)
    rating = Column(Integer())
    
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    
    

    def __repr__(self):
        return f'Review(id={self.id}, ' + \
            f'rating={self.rating}, ' + \
            f'restaurant_id={self.restaurant_id})'
    
    def customer(self):
        return self.customer

    def restaurant(self):
        return self.restaurant
    


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())

    reviews = relationship('Review', backref=backref('customer'))
    restaurants = relationship('Restaurant', secondary=restaurant_customer, back_populates='restaurants')

   
    def __repr__(self):
        return f'Customer(id={self.id}, ' + \
            f'first_name={self.first_name}), ' + \
            f'last_name={self.last_name}'
    
    def reviews(self):
        return self.reviews

    def restaurants(self):
        return [review.restaurant for review in self.reviews]

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        if self.reviews:
            max_rating = max(self.reviews, key=lambda review: review.star_rating)
            return max_rating.restaurant
        return None

    def add_review(self, restaurant, rating):
        new_review = Review(restaurant=restaurant, customer=self, star_rating=rating)
        self.reviews.append(new_review)
        return new_review

    def delete_reviews(self, restaurant):
        self.reviews = [review for review in self.reviews if review.restaurant != restaurant]

# Create tables
Base.metadata.create_all(engine)

# Create session
Session = sessionmaker(bind=engine)
session = Session()

def main():
    # Display all customers
    all_customers = session.query(Customer).all()
    print("All Customers:")
    for customer in all_customers:
        print(f"{customer.first_name} {customer.last_name}")

    # Display all restaurants
    all_restaurants = session.query(Restaurant).all()
    print("\nAll Restaurants:")
    for restaurant in all_restaurants:
        print(f"{restaurant.name} - Price: {restaurant.price}")

    # Display all reviews
    all_reviews = session.query(Review).all()
    print("\nAll Reviews:")
    for review in all_reviews:
        print(f"Review for {review.restaurant.name} by {review.customer.full_name()}: {review.rating} stars")

if __name__ == "__main__":
    main()