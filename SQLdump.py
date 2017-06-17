# -*- coding: cp936 -*- 

import getopt

import sys
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,DateTime,Numeric,Index

type_dict = dict([('String',String),('Integer',Integer),('DateTime',DateTime)])
trans = lambda x: x.decode('cp936').encode('utf8') if isinstance(x,unicode) else x

def parse_primary_key(x):
    keys = []
    for i in range(0,len(x),3):
        col_name,col_type,type_len = x[i],x[i+1],int(x[i+2])
        if col_type == 'String':
            keys.append( Column("%s" %col_name,type_dict[col_type](type_len), primary_key=True) )
        elif col_type == 'Integer':
            keys.append( Column("%s" %col_name,type_dict[col_type], primary_key=True) )
        elif col_type == 'DateTime':
            keys.append( Column("%s" %col_name,type_dict[col_type], primary_key=True) )
    return keys

def trans2(x):
    return trans(x)

def make_session(connection_string,src = False):
    if src == True:
        engine = create_engine(connection_string, echo=False, coerce_to_unicode=True)
    else:
        engine = create_engine(connection_string, echo=False, convert_unicode=True, encoding = "utf8")
    Session = sessionmaker(bind=engine)
    return Session(), engine

def Init(from_db, to_db):
    global source,sengine,smeta,destination,dengine
    source, sengine = make_session(from_db,True)
    smeta = MetaData(bind=sengine,schema = 'das')
    destination, dengine = make_session(to_db)

def pull_data(tables,tables_type):
    table = None
    for table_item in tables:
        if tables_type == 'tuple':
            table_name,para_array = table_item.split(',')[0],table_item.split(',')[1:]
            columns = parse_primary_key(para_array)
            print 'Processing', table_name 
            print 'Pulling schema from source server'
            table = Table(table_name, smeta, \
                          *columns,
                          autoload=True)
        elif tables_type == 'struct':
            table = table_item
        else:
            print 'wrong table type'
            exit()
        print 'Creating table on destination server'
        table.metadata.create_all(dengine,)
        NewRecord = quick_mapper(table)
        columns = table.columns.keys()
        print 'Transferring records'
        for record in source.query(table).all():
            data = dict(
                [(str(column), trans( getattr(record, column) ) ) for column in columns]
            )
            print data
            destination.merge(NewRecord(**data))
    print 'Committing changes'
    destination.commit()

def quick_mapper(table):
    Base = declarative_base()
    class GenericMapper(Base):
        __table__ = table
    return GenericMapper

if __name__ == '__main__':

    fromd = 'oracle+cx_oracle://queryuser:hhjszHXWYX_$863$@172.17.80.6:1521/bgrac'
    tod   = 'mysql+mysqldb://root:123456@localhost:3306/das?charset=utf8'
    Init(fromd,tod)

    t_b_stock_reprice = Table(
        'b_stock_reprice', smeta,
        Column('stock_code', String(100),primary_key = True),
        Column('effective_date', Numeric(asdecimal=False),primary_key = True),
        Column('price_type_code', String(100)),
        Column('high_price', Numeric(asdecimal=False)),
        Column('open_price', Numeric(asdecimal=False)),
        Column('low_price', Numeric(asdecimal=False)),
        Column('close_price', Numeric(asdecimal=False)),
        Column('volume', Numeric(asdecimal=False)),
        Column('turnover', Numeric(asdecimal=False)),
        Column('last_close_price', Numeric(asdecimal=False)),
        Column('factor', Numeric(asdecimal=False)),
        Column('first_created_date', DateTime),
        Column('last_updated_date', DateTime),
        Index('b_stock_reprice_u1', 'effective_date', 'stock_code'),
        schema='das'
    )
    
    t_b_stock = Table(
        'b_stock', smeta,
        Column('stock_code', String(100), primary_key=True),
        Column('stock_name', String(100)),
        Column('first_created_date', DateTime),
        Column('last_updated_date', DateTime),
        schema='das'
    )
#     table_para = ('b_stock_reprice,stock_code,String,20,effective_date,Integer,10',)
    table_para = (t_b_stock_reprice,)
    pull_data(
        table_para,
        'struct'
    )