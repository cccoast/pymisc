import pandas as pd
import numpy as np
# import MySQLdb as mdb
import pandas.io.sql as psql
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.schema import *
from sqlalchemy.ext.declarative import declarative_base
import collections
import pyodbc

class DBbase(object):

    Base = declarative_base()

    class Price(Base):
        
        __tablename__ = 'price'
        time = Column(Integer,primary_key = True)
        id = Column(String(10),primary_key = True)
        open = Column(Float)
        high = Column(Float)
        low  = Column(Float)
        close = Column(Float)
        volume = Column(Float)
        float_a_shares = Column(Float)
        
    class TradingDays(Base):
        
        __tablename__ = 'trading_days'
        trading_day = Column(Integer,primary_key = True)
        
    class Tickers(Base):
        
        __tablename__ = 'tickers'
        ticker = Column(String(20))
        id   = Column(String(20),primary_key = True)
        
    class Indicators(Base):
        
        __tablename__ = 'indicators'
        indicator_names = Column(String(20))
        id   = Column(String(20),primary_key = True)
        
    def __init__(self,db,user,pwd):
        self.engine = None
        self.Session = None 
        self.transaction = None
        self.user = user
        self.pwd  = pwd
        self.db   = db
        
    def CreateEngine(self,echo = False):
#         self.engine = create_engine(r'mssql+pyodbc://wdzhangyuxiang:wdzhangyuxiang@wind',encoding = 'utf8',echo = echo)
        self.engine = create_engine('mysql+mysqldb://{0}:{1}@localhost:3306/{2}?use_unicode=0&charset=utf8'.format(self.user,self.pwd,self.db),echo = echo)
        return self.engine
        
    def CreateSession(self):
        if not self.engine:
            self.Session = sessionmaker(self.engine)
        else:
            self.Session = sessionmaker(self.CreateEngine())    
        return self.Session
    
    def GetEngine(self):
        if self.engine:
            return self.engine
        else:
            self.CreateEngine()
            return self.engine
    
    def StartTransaction(self,_session):
        transaction=_session.create_transaction()
        return transaction
        
    def GetSession(self):
        if self.Session:
            return self.Session()
        else:
            self.CreateSession()
            return self.Session()

    def InitTable(self):
        if self.engine:
            self.Base.metadata.create_all(self.engine)
        else:
            self.Base.metadata.create_all(self.CreateEngine())
        
    def SetEngineEcho(self,val):
        self.engine.echo = val 
    
    def execute_sqls(self,sqls):
        session = self.GetSession()
        for isql in sqls:
            session.execute(isql)
        session.commit()
        session.close()
        
    def execute_sql(self,sql):
        session = self.GetSession()
        re = session.execute(sql)
        session.commit()
        return re    
    
    def drop_table(self,table_name):
        self.execute_sql('Drop Table {0}.{1}'.format(self.db,table_name))
        
    def insert_data_frame(self,_class,df,merge = False):
        self.insert_dicts(_class,df.to_dict('records'),merge)
        
    def insert_dicts(self,_class,_dicts,merge = False):
        session = self.GetSession()
        if not merge:
            session.execute(_class.__table__.insert(),_dicts)
        else:
#             keys = _class.__table__.primary_key.columns.keys()
#             qry_keys = [idict[keys] for idict in _dicts]
#             re = session.execute(_class.__table__.select(),qry_keys)
#             if re == None:
#                 session.execute(_class.__table__.insert().prefix_with("IGNORE"),_dicts)
#             session.execute(_class.__table__.insert.prefix_with("IGNORE"),_dicts)
            for idict in _dicts:
                session.merge(_class(**idict))
        session.commit()
        session.close()
    
    def insert_dictlike(self,_class,_dict,merge = False):
        session = self.GetSession()
        if not merge:
            session.add(_class(**_dict))
        else:
            session.merge(_class(**_dict))
        session.commit()
        session.close()
    
    def insert_lists(self,_class,_lists,merge = False):
        cols = _class.__table__.c.keys()
        if isinstance(_lists[0],collections.Iterable):
            _dicts = [dict(zip(cols,val)) for val in _lists]
        else:
            _dicts = [{cols[0]:val} for val in _lists]
        self.insert_dicts(_class,_dicts,merge)
    
    def insert_listlike(self,_class,val,merge = False):
        _dict = dict(zip(_class.__table__.c.keys(),val))
        self.insert_dictlike(_class,_dict,merge)

    def delete_lists_obj(self,obj_lists):
        session = self.GetSession();
        for i in obj_lists:
            session.delete(i)
        session.commit()
        session.close()
            
    def delete_lists(self,_class,_values):
        session = self.GetSession()
        table = _class.__table__
        _key = table.primary_key.columns.keys()
        _lists = None
        if isinstance(_values,list):
            if isinstance(_values[0],collections.Iterable):
                _lists = [dict(zip(_key,iv)) for iv in _values]
            else:
                _lists = [{_key[0]:val} for val in _values]
        else:
            return False
            
        session.execute(table.delete(),_lists)
        session.commit()
    
    def show_dir(self,_class):
        return filter(lambda x:not x.startswith('_'),dir(_class))
    
    def get_column_names(self,_class):
        return _class.__table__.c.keys()
    
    def get_column_obj(self,_class,key):
        return _class.__table__.columns[key]
    
    def get_columns_obj(self,_class):
#         return [ _class.__dict__[i] for i in dbbase.get_column_names(_class)]
        return _class.__table__.columns
    
    def get_primary_key(self,_class):
        return _class.__table__.primary_key.columns.keys()
    
    def get_primary_key_obj(self,_class):
        return _class.__table__.primary_key.columns
        
class DBapi(DBbase):
    
    def __init__(self,user,pwd,db):
        DBbase.__init__(user,pwd,db)
        self.CreateEngine()
        self.InitTable()
        self.CreateSession()

if __name__ == '__main__':
    dbbase = DBbase('stock_day','root', '123456')
    dbbase.CreateEngine() 
    dbbase.SetEngineEcho(False)
    dbbase.InitTable()
    exit()
    _d = {'trading_day':19890219}
    vals = [19890119,19890120,19890121,19890319,19890320]
    prices =(201601010,'399300',1000.0,1001.0,999.0,1000.0,10000,20000)
    prices2 =(201601011,'399500',1000.0,1001.0,999.0,1000.0,10000,20000)
    prices3 =(201601012,'399300',1000.0,1001.0,999.0,1000.0,10000,20000)
    
    '''Test class function and attribute'''
#     print filter(lambda x:not x.startswith('_'),dir(dbbase.Price.__table__))
#     print filter(lambda x:not x.startswith('_'),dir(dbbase.Price.__table__.c))  
#     print dbbase.Price.__table__.c.values()  
#     print dbbase.Price.__table__.primary_key.columns.keys()
    
#     dprices = dict(zip(dbbase.Price.__table__.c.keys(),prices2))
#     print dprices

    ''' Test Drop Table '''
#     dbbase.drop_table(dbbase.Tickers.__tablename__)
#     exit()
    
    ''' Tets insert list & dict, lists & dicts '''
#     dbbase.insert_listlike(dbbase.TradingDays,vals,merge = True)
#     dbbase.insert_dictlike(dbbase.TradingDays,_d,merge = True)
#     
#     dbbase.insert_listlike(dbbase.Price,prices3,merge = True)
#     dbbase.insert_lists(dbbase.Price,(prices,prices2),merge = True)

    ''' Test Insert DataFrame '''
    df = pd.DataFrame(columns = dbbase.Price.__table__.c.keys())
    df = df.append(pd.Series(prices,index = dbbase.Price.__table__.c.keys()),ignore_index = True)
    df = df.append(pd.Series(prices2,index = dbbase.Price.__table__.c.keys()),ignore_index = True)
    df = df.append(pd.Series(prices3,index = dbbase.Price.__table__.c.keys()),ignore_index = True)
    
    dbbase.insert_lists(dbbase.Price,[prices2,prices3],True)
    dbbase.insert_lists(dbbase.TradingDays,vals, True)
    dbbase.insert_data_frame(dbbase.Price, df, merge = True)
      
    ''' Test Delete '''
#     session = dbbase.GetSession()
#     r = session.query(dbbase.TradingDays).all()
#     session.close()
#      
#     dbbase.delete_lists_obj(r)

#     dbbase.delete_lists(dbbase.Price, [(201601010,'399300'),])
#     dbbase.delete_lists(dbbase.Price, [(201601010,'399300'),(201601011,'399500')])
#     dbbase.delete_lists(dbbase.TradingDays,vals)
#     exit()
     
    ''' Test Query '''
    
    session = dbbase.GetSession()
    cols = dbbase.get_columns_obj(dbbase.Price)
    print cols
    re = session.query(cols['id'])
    for i in re.all():
        print i
    session.commit()
    session.close()
    exit()
    
    session = dbbase.GetSession()
    i = select([dbbase.TradingDays]).where(dbbase.TradingDays.trading_day == 19890319L)
    re = session.execute(i)
    print re.fetchall()
    print session.execute('selfect * from trading_days')
    
    r = session.query(dbbase.TradingDays)
    r.delete()
    session.commit()
    exit()
    
    i = session.execute(dbbase.TradingDays.__table__.insert(),[{'tarding_day':i} for i in range(10)])
    session.commit()
    i = insert(dbbase.TradingDays).values(trading_day = 19890111)
    session.execute(i)
    session.commit()
    
    session.add(dbbase.TradingDays(trading_day = 19890319))
    session.commit()