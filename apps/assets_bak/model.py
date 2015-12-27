#!/usr/bin/env python 
#-*-coding:utf8-*-

from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

#engine = create_engine('mysql+mysqldb://root:root@127.0.0.1:3306/mytest',encoding='utf8', echo=True)

BaseModel = declarative_base()
'''
class User_Group_Relation(BaseModel):
    __tablename__ = 'user_group'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'), primary_key=True)
    #users = relationship("User", backref="user_assocs")
'''
class BaseInfo(BaseModel):
    __tablename__ = 'baseinfo'

    id = Column(Integer,primary_key=True,autoincrement=True)  
    _id = Column(Integer,primary_key=True,autoincrement=True,doc='资产编号')
    sn = Column(String(100),nullable=False,doc=u'设备SN号')                                    
    type = Column(String(100),nullable=False,doc=u'设备类型')                                    
    brand = Column(String(100),nullable=False,doc=u'设备品牌')
    unit_type = Column(String(100),nullable=False,doc=u'设备型号')
    unit = Column(String(100),nullable=False,doc=u'设备规格')
    price = Column(String(100),nullable=False,doc=u'购买单价')
    buy_time = Column(String(100),nullable=False,doc=u'购买日期')
    expired_time = Column(String(100),nullable=False,doc=u'过保日期')
    state = Column(String(100),nullable=False,doc=u'使用状态')
    idcinfo = relationship("IdcInfo",uselist=False,backref="idcinfo_assocs")

class IdcInfo(BaseModel):
    __tablename__ = 'idcinfo'
    id = Column(Integer,primary_key=True,autoincrement=True)  
    base_id = Column(Integer,ForeignKey('baseinfo.id'))
    idc = Column(String(100),nullable=False,doc=u'IDC')                                    
    brand = Column(String(100),nullable=False,doc=u'机柜位置')
    unit_type = Column(String(100),nullable=False,doc=u'托盘位置')
    unit = Column(String(100),nullable=False,doc=u'机房联系人')
    phone = Column(String(100),nullable=False,doc=u'机房联系人电话')
    
class DevInfo(BaseModel):
    __tablename__ = 'devinfo'
    id = Column(Integer,primary_key=True,autoincrement=True)  
    base_id = Column(Integer,ForeignKey('baseinfo.id'))
    cpu_type = Column(String(100),nullable=False,doc=u'CPU类型')
    cpu_core = Column(String(100),nullable=False,doc=u'CPU物理核数')
    cpu_num = Column(String(100),nullable=False,doc=u'CPU颗数')
    mem_total = Column(String(100),nullable=False,doc=u'内存总容量')
    mem_num = Column(String(100),nullable=False,doc=u'内存插槽数')
    mem_info = Column(String(100),nullable=False,doc=u'内存信息[内存型号,内存容量]')
    

class DiskInfo(BaseModel):
    __tablename__ = 'diskinfo'
    id = Column(Integer,primary_key=True,autoincrement=True)  
    base_id = Column(Integer,ForeignKey('baseinfo.id'))
    disk_num = Column(String(100),nullable=False,doc=u'磁盘数量')
    disk_total = Column(String(100),nullable=False,doc=u'磁盘总容量')
    ssd_total = Column(String(100),nullable=False,doc=u'SSD容量')
    disk_info = Column(String(100),nullable=False,doc=u'磁盘信息[SN,类型,型号,转速,容量]')
    raid_info = Column(String(100),nullable=False,doc=u'RAID信息[类型,SN]')
    
    raid_type = Column(String(100),nullable=False,doc=u'RAID型号')
    raid_cache = Column(String(100),nullable=False,doc=u'RAID缓存')
    raid_num = Column(String(100),nullable=False,doc=u'RAID数量')
    raid_conf = Column(String(100),nullable=False,doc=u'RADID配置')
    raid_cache = Column(String(100),nullable=False,doc=u'RAID缓存')
    raid_state = Column(String(100),nullable=False,doc=u'RAID状态')

class NetInfo(BaseModel):
    __tablename__ = 'netinfo'
    id = Column(Integer,primary_key=True,autoincrement=True)  
    base_id = Column(Integer,ForeignKey('baseinfo.id'))
    net_num = Column(String(100),nullable=False,doc=u'网卡总数量')
    net_speed = Column(String(100),nullable=False,doc=u'网卡总速率')
    net_info = Column(String(100),nullable=False,doc=u'网卡信息[品牌,型号,速率,MAC,交换机端口]')

class SystemInfo(BaseModel):
    __tablename__ = 'systeminfo'
    id = Column(Integer,primary_key=True,autoincrement=True)  
    base_id = Column(Integer,ForeignKey('baseinfo.id'))
    n_ip = Column(String(100),nullable=False,doc=u'内网IP')
    w_ip = Column(String(100),nullable=False,doc=u'外网IP')
    v_ip = Column(String(100),nullable=False,doc=u'虚拟IP')
    y_ip = Column(String(100),nullable=False,doc=u'远控IP')
    account = Column(String(100),nullable=False,doc=u'远控帐号')
    password = Column(String(100),nullable=False,doc=u'远控密码')

class UseInfo(BaseModel):
    __tablename__ = 'useinfo'
    id = Column(Integer,primary_key=True,autoincrement=True)  
    base_id = Column(Integer,ForeignKey('baseinfo.id'))
    leader = Column(String(100),nullable=False,doc=u'负责人')
    users = Column(String(100),nullable=False,doc=u'使用人')
    use = Column(String(100),nullable=False,doc=u'业务用途')

    

class Zone(BaseModel):
    __tablename__ = 'zone'
    id = Column(Integer,primary_key=True,autoincrement=True)  
    gname = Column(String(100),nullable=False,doc=u'组名称')
    user_id = Column(String(100),ForeignKey('user.id'))
    #user = relationship("User",backref="user_assocs")

class User(BaseModel):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,autoincrement=True)  
    zone_id = Column(Integer,ForeignKey('zone.id'))
    uname = Column(String(100),nullable=False,doc=u'用户名')
    mail = Column(String(100),nullable=False,doc=u'邮箱')
    role = Column(String(100),nullable=False,doc=u'权限')
    #zone = relationship("Zone",backref="zone_assocs")

    


'''
    def __repr__(self):
        return "<User(id='%s', uname='%s', dept='%s', phone='%s', mail='%s')>" % (self.id, self.uname, self.dept, self.phone, self.mail)
'''

engine = create_engine('mysql+mysqldb://root:root@127.0.0.1:3306/mytest',encoding='utf8', echo=True)
BaseModel.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)  # once engine is available
session = Session()



if __name__ == '__main__':
    z=Zone(gname='aws')
    u = User(uname='luopeng',mail='xxx',role='001')
    session.add(z)
    session.flush()
    session.add(u)
    session.flush()
    u.zone_id = z.id
    z.user_id = u.id
    session.commit()
    #our_user = session.query(User).filter_by(uname='ed').first() 
    #print session.query(Zone).filter_by(gname='aws').first().__dict__
    pass










