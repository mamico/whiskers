from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import ForeignKey
from sqlalchemy import Table

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

from zope.sqlalchemy import ZopeTransactionExtension
from zope.interface import implements
from whiskers import interfaces

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


bp_association_table = Table('buildout_package_association', Base.metadata,
    Column('buildout_id', Integer, ForeignKey('buildout.id')),
    Column('package_id', Integer, ForeignKey('package.id'))
)

class Buildout(Base):
    implements(interfaces.IBuildout)
    __tablename__ = 'buildout'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255))
    packages = relationship("Package", secondary=bp_association_table,
                            backref="buildouts")

    def __init__(self, name, packages):
        self.name = name
        self.packages = packages


class Package(Base):
    implements(interfaces.IPackage)

    __tablename__ = 'package'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255))
    version = Column(Unicode(20))
    #buildouts = relationship("Buildout", secondary=bp_association_table,
    #                         backref="packages")

    def __init__(self, name, version):
        self.name = name
        self.version = version


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
