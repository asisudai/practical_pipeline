#!/usr/bin/env python
# https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes
# http://docs.sqlalchemy.org/en/latest/orm/examples.html
from contextlib import contextmanager
from sqlalchemy import (create_engine, Table, MetaData, Column, Integer, String, Enum,
                        ForeignKey, Index, UniqueConstraint)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# define engine/database (as an sqlite file)
engine = create_engine('sqlite:////tmp/sqlite.db')
Base = declarative_base(metadata=MetaData())

# Use scoped_session (session object is maintained across multiple call)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

class BaseMixin(object):

    @classmethod
    def create(cls, **kw):
        try:
            # Create a session
            session = Session()

            # add new instance
            new = cls(**kw)
            session.add(new)
            session.commit()
            return new

        except Exception:
            session.rollback()
            raise

    @classmethod
    def find_one(cls, **kwargs):
        result = cls.find(**kwargs)

        if not result:
            raise NoResultFound("No {} found for query:{}".format(cls.__name__, kwargs))
        elif len(result) > 1:
            raise MultipleResultsFound("More than one {} found for query:{}".format(cls.__name__, kwargs))
        else:
            return result[0]

    @staticmethod
    @contextmanager
    def session_context():
        session = Session()
        session.begin(subtransactions=True)
        try:
            yield session
        except Exception:
            if session.transaction or session.transaction.is_active:
                session.rollback()
            raise
        else:
            session.commit()

class Project(Base, BaseMixin):

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

    # define a relationship attribute between Project <--> Assets
    assets    = relationship('Asset', backref='project', lazy='dynamic', order_by='Asset.name')

    def __repr__(self):
        return "{0.__class__.__name__}(name='{0.name}', id={0.id}, format='{0.format}')".format(self)

    @classmethod
    def create(cls, name, root, format='tv', description='', status=None):
        data = dict(name        = name,
                    format      = format,
                    root        = root,
                    status      = status,
                    description = description)
        return super(Project, cls).create(**data)

    @classmethod
    def find(cls, name=None, format=None, status=None, root=None, id=None):
        query = Session().query(cls)

        if name:
            query = query.filter(cls.name == name)

        if format:
            query = query.filter(cls.format == format)

        if root:
            query = query.filter(cls.root == root)

        # allow status arg to be a list of status or a single status-string
        if status is None:
            pass
        elif isinstance(status, (list, tuple)):
            query = query.filter(cls.status.in_(status))
        elif status:
            query = query.filter(cls.status == status)

        # allow id arg to be a list of status or a single id-int
        if id:
            if isinstance(id, (int, long)):
                query = query.filter(cls.id == id)
            elif isinstance(id, (list, tuple)):
                query = query.filter(cls.id.in_(id))

        query = query.order_by(cls.name)
        return query.all()

class Asset(Base, BaseMixin):

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

    @classmethod
    def create(cls, project_id, name, status=None, type=None, description=''):
        data = dict(project_id  = project_id,
                    name        = name,
                    status      = status,
                    type        = type,
                    description = description)
        return super(Asset, cls).create(**data)

    @classmethod
    def find(cls, name=None, project_id=None, status=None, type=None, id=None):
        query = Session().query(cls)

        if name:
            query = query.filter(cls.name == name)

        if project_id:
            query = query.filter(cls.project_id == project_id)

        # allow type arg to be a list of status or a single type-string
        if type is None:
            pass
        elif isinstance(type, (list, tuple)):
            query = query.filter(cls.status.in_(type))
        elif type:
            query = query.filter(cls.status == type)

        # allow status arg to be a list of status or a single status-string
        if status is None:
            pass
        elif isinstance(status, (list, tuple)):
            query = query.filter(cls.status.in_(status))
        elif status:
            query = query.filter(cls.status == status)

        # allow id arg to be a list of status or a single id-int
        if id:
            if isinstance(id, (int, long)):
                query = query.filter(cls.id == id)
            elif isinstance(id, (list, tuple)):
                query = query.filter(cls.id.in_(id))

        query = query.order_by(cls.name)
        return query.all()

if __name__ == '__main__':

    # # DROP ALL TABLES (WILL REMOVE ALL DATA)
    # # Adding this to allow re-running this code.
    Base.metadata.drop_all(engine)
    #
    # # create tables
    Base.metadata.create_all(engine)

    # Create project and assets within a transaction. if transaction failed at any point,
    # the enter commit will rollback. Ensuring data integrity vs partial commits.
    with BaseMixin.session_context() as session:

        # create project
        project = Project.create(name='Who Framed Roger Rabbit', root='/jobs/roger')

        # create assets
        asset1 = Asset.create(name='Roger', type='char', project_id=project.id)
        asset2 = Asset.create(name='Jessica', type='char', project_id=project.id)
        asset3 = Asset.create(name='Benny', type='vhcl', project_id=project.id)
        asset4 = Asset.create(name='Bullet', type='prop', project_id=project.id)

    # query back project
    project = Project.find_one(name='Who Framed Roger Rabbit')

    # query back assets
    result = Asset.find(project_id=project.id)

    for asset in result:
        print(asset)
    # >>> Asset(name='Roger', id=1, type='char')
    # >>> Asset(name='Jessica', id=2, type='char')
    # >>> Asset(name='Bullet', id=4, type='prop')
    # >>> Asset(name='Benny', id=3, type='vhcl')
