from sqlalchemy import Column, Integer, String, DECIMAL, create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select, desc, distinct

Base = declarative_base()
engine = create_engine('sqlite:///azbykamebeli.db')
Session = sessionmaker(bind=engine)


class Couch(Base):
    __tablename__ = 'couch'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    vendor_code = Column(String)
    discount_price = Column(DECIMAL, nullable=True)
    full_price = Column(DECIMAL)
    status = Column(String)
    scraped_id = Column(Integer)

    def __str__(self) -> str:
        return f'{self.name} ({self.id},{self.status})'

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def bulk_save(couch_list):
        with Session() as session:
            session.add_all(couch_list)
            session.commit()

    @staticmethod
    def get_prices_by_status(status):
        """Returns full prices for couches with a given status"""
        stmt = select(Couch.full_price).where(Couch.status == status)
        with Session() as session:
            return [row.full_price for row in session.execute(stmt)]

    @staticmethod
    def get_top_10():
        """Returns 10 vendor codes with the biggest average price"""
        stmt = select(Couch.vendor_code, func.avg(Couch.full_price).label('average')).\
            group_by(Couch.vendor_code).\
            order_by(desc('average')).\
            limit(10)
        with Session() as session:
            return [{'vendor_code': row.vendor_code, 'average': row.average} for row in session.execute(stmt)]

    @staticmethod
    def get_count_by_status():
        """Returns statuses and the amount of couches with this status"""
        stmt = select(Couch.status, func.count(distinct(Couch.scraped_id))).group_by(Couch.status)
        with Session() as session:
            return [{'status': row.status, 'count': row.count} for row in session.execute(stmt)]


# Creates initial table structure
Base.metadata.create_all(bind=engine)
