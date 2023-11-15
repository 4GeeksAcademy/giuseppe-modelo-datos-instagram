from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from eralchemy2 import render_er

Base = declarative_base()

# Tabla de muchos a muchos para la relación followers
followers_association = Table(
    'followers', Base.metadata,
    Column('follower_id', Integer, ForeignKey('user.id')),
    Column('followed_id', Integer, ForeignKey('user.id'))
)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    bio = Column(String(255), nullable=True)
    profile_image_url = Column(String(255), nullable=True)

    posts = relationship('Post', back_populates='user')
    likes = relationship('Like', back_populates='user')
    followers = relationship('User',
                             secondary=followers_association,
                             primaryjoin=id == followers_association.c.followed_id,
                             secondaryjoin=id == followers_association.c.follower_id,
                             back_populates='following')
    following = relationship('User',
                             secondary=followers_association,
                             primaryjoin=id == followers_association.c.follower_id,
                             secondaryjoin=id == followers_association.c.followed_id,
                             back_populates='followers')

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    caption = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='posts')

    likes = relationship('Like', back_populates='post')
    comments = relationship('Comment', back_populates='post')

class Like(Base):
    __tablename__ = 'like'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='likes')

    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship('Post', back_populates='likes')

class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    text = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='comments')

    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship('Post', back_populates='comments')

# Configura el motor de la base de datos
engine = create_engine('sqlite:///instagram.db')
Base.metadata.create_all(engine)

# Intenta generar el diagrama
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
