#!/usr/bin/env python 
#-*-coding:utf8-*-

from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

#engine = create_engine('mysql+mysqldb://root:root@127.0.0.1:3306/mytest',encoding='utf8', echo=True)

Base = declarative_base()

class User_Group_Relation(Base):
    __tablename__ = 'user_group'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'), primary_key=True)
    #users = relationship("User", backref="user_assocs")

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer,primary_key=True,autoincrement=True)
    uname = Column(String(10))
    dept = Column(String(10))
    phone = Column(String(10))
    mail = Column(String(10))

    def __repr__(self):
        return "<User(id='%s', uname='%s', dept='%s', phone='%s', mail='%s')>" % (self.id, self.uname, self.dept, self.phone, self.mail)

class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    gname = Column(String(10))
    desc = Column(String(10))
    users = relationship("User_Group_Relation", backref="Group")
    
    def __repr__(self):
        return "<Group(id='%s', gname='%s', desc='%s')>" % (self.id, self.gname, self.desc)


engine = create_engine('mysql+mysqldb://root:root@127.0.0.1:3306/mytest',encoding='utf8', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)  # once engine is available
session = Session()



if __name__ == '__main__':
    u = User(uname='ed', phone='Ed Jones', dept='edspassword')
    session.add(u)
    our_user = session.query(User).filter_by(uname='ed').first() 



