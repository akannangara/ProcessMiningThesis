import sqlalchemy as sql

from DbProjects import DbProjects
from Base import Base


class SqlDbRepository:
    __engine = None #sql db engine
    __sessionMaker = None

    def __init__(self, settings):
        connectionString = settings.SqlDb["ConnectionString"]
        SqlDbRepository.__engine = sql.create_engine(connectionString, echo=True)
        Base.metadata.create_all(SqlDbRepository.__engine)
        SqlDbRepository.__sessionMaker = sql.orm.sessionmaker(bind=SqlDbRepository.__engine)

    def AddMultipleToDb(self, entitiesList):
        session = SqlDbRepository.__sessionMaker()
        session.add_all(entitiesList)
        session.commit()

    def AddToDb(self, entity):
        session = SqlDbRepository.__sessionMaker()
        session.add(entity)
        session.commit()


    def GetDatabase(self):
        x = DbProjects.__table__

        newProject = DbProjects(Id=1, Key='projectKey', Name='projectName', ProjectTypeKey='project type key')
        session = SqlDbRepository.__sessionMaker()
        session.add(newProject)
        session.commit()

        y = 0