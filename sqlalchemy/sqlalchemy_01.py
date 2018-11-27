#!/usr/bin/env python
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, Enum, \
                       ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

# define mysql engine/database (replace user, password, hostname, database)
# engine = create_engine('mysql://user:password@hostname/database')

# define engine/database (as an sqlite file)
engine = create_engine('sqlite:////tmp/sqlite.db')
Base = declarative_base(metadata=MetaData())

class Project(Base):

    __table__ = Table('project', Base.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String(32), nullable=False),
                      )

    def __repr__(self):
        return "{0.__class__.__name__}(name='{0.name}', id={0.id}, type='{0.type}')".format(self)

class Asset(Base):

    __table__ = Table('asset', Base.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('project_id', Integer, ForeignKey('project.id'), nullable=False),
                      Column('name', String(32), nullable=False),
                      Column('type', Enum('char', 'prop', 'vhcl', 'env', 'fx'), nullable=False),
                      )

    def __repr__(self):
        return "{0.__class__.__name__}(name='{0.name}', id={0.id}, type='{0.type}')".format(self)


if __name__ == '__main__':

    # DROP ALL TABLES (WILL REMOVE ALL DATA!)
    # Adding this to allow re-running this code.
    Base.metadata.drop_all(engine)

    # create tables
    Base.metadata.create_all(engine)

    # create connection/session
    session = Session(engine)

    # create project
    project = Project(name='Who Framed Roger Rabbit')

    # add project to session
    session.add(project)

    # commit changes
    session.commit()

    # create asset
    asset1 = Asset(name='Roger', type='char', project_id=project.id)
    asset2 = Asset(name='Jessica', type='char', project_id=project.id)
    asset3 = Asset(name='Benny', type='vhcl', project_id=project.id)
    asset4 = Asset(name='Bullet', type='prop', project_id=project.id)
    session.add(asset1)
    session.add(asset2)
    session.add(asset3)
    session.add(asset4)

    # commit changes
    session.commit()


    # query back project
    query   = session.query(Project)
    project = query.one()

    # query back assets
    query  = session.query(Asset)
    query  = query.filter(Asset.project_id == project.id)
    result = query.all()

    for asset in result:
        print(asset)

    #>>> Asset(name='Roger', id=1, type='char')
    #>>> Asset(name='Jessica', id=2, type='char')
    #>>> Asset(name='Bullet', id=4, type='prop')
    #>>> Asset(name='Benny', id=3, type='vhcl')
