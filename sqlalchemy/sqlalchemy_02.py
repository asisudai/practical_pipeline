#!/usr/bin/env python
from sqlalchemy import (create_engine, Table, MetaData, Column, Integer, String, Enum,
                        ForeignKey, Index, UniqueConstraint)
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

# define engine/database (as an sqlite file)
engine = create_engine('sqlite:////tmp/sqlite.db')
Base = declarative_base(metadata=MetaData())

class Project(Base):

    __table__ = Table('project', Base.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String(32), nullable=False),
                      Column('status', Enum('act', 'dis'), default='act', nullable=False),
                      Column('format', Enum('tv', 'film'), default='film', nullable=False),
                      Column('root', String(128), nullable=False),
                      Column('description', String(255)),

                      # index project.name
                      Index('ix_name', 'name'),

                      # unique constraint project name and root
                      UniqueConstraint('name', name='uc_name'),
                      UniqueConstraint('root', name='uc_root'),
                      )

    def __repr__(self):
        return "{0.__class__.__name__}(name='{0.name}', id={0.id}, format='{0.format}')".format(self)

class Asset(Base):

    __table__ = Table('asset', Base.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('project_id', Integer, ForeignKey('project.id'), nullable=False),
                      Column('name', String(32), nullable=False),
                      Column('status', Enum('act', 'dis'), default='act', nullable=False),
                      Column('type', Enum('char', 'prop', 'vhcl', 'env', 'fx'), nullable=False),
                      Column('description', String(255)),

                      # add indexes for common asset queries
                      Index('ix_proj_stat_name', 'project_id', 'status', 'name'),
                      Index('ix_proj_stat_typ', 'project_id', 'status', 'type'),

                      # unique constraint asset name within the project
                      UniqueConstraint('project_id', 'name', name='uc_prj_name'),
                      )

    def __repr__(self):
        return "{0.__class__.__name__}(name='{0.name}', id={0.id}, type='{0.type}')".format(self)


if __name__ == '__main__':

    # DROP ALL TABLES (WILL REMOVE ALL DATA)
    # Adding this to allow re-running this code.
    Base.metadata.drop_all(engine)

    # create tables
    Base.metadata.create_all(engine)

    # create connection/session
    session = Session(engine)

    # create project
    project = Project(name='Who Framed Roger Rabbit', root='/jobs/roger')

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
