from flask_httpauth import HTTPBasicAuth
from app.models import User, Data, Alert
from flask import g
from flask import jsonify
from . import api
from flask import request
from app import db


auth = HTTPBasicAuth()


@auth.verify_password
def verify_user(email_token, password):
    if len(email_token) == 0:
        return False
    if len(password) == 0:
        user = User.check_api_token(email_token)
        if user is None:
            return False
        g.current_user = user
        return True
    user = User.query.filter_by(email=email_token).first()
    if user is None:
        return False
    if user.check_password(password):
        g.current_user = user
        return True
    return False


@auth.error_handler
def error():
    return jsonify({'status': 123, 'info': 'auth error'})


@api.route('/')
@auth.login_required
def test():
    return jsonify({'status': 200, 'info': 'welcome'})


@api.route('/token')
@auth.login_required
def token():
    return jsonify({'status': 200, 'token': g.current_user.API_KEY})


# 获取自己所有设备
@api.route('/devices')
@auth.login_required
def devices():
    ds = g.current_user.devices.all()
    dlist = []
    for d in ds:
        dlist.append(d.to_json())
        print(dlist)
    return jsonify({'status': 200, 'devices': dlist})


# 上传数据
@api.route('/device/<int:did>/sensor/<int:sid>/data', methods=['POST'])
@auth.login_required
def data(did, sid):
    print(type(request.json), request.json)
    device = g.current_user.devices.filter_by(id=did).first()
    if device is None:
        return jsonify({'status': 404, 'info': '找不到你的设备'})

    sensor = device.sensors.filter_by(id=sid).first()
    if sensor is None:
        return jsonify({'status': 404, 'info': '找不到你的传感器'})
    print(request.json)
    if request.json is None:
        return jsonify({'status': 404, 'info': '找不到你的数据'})

    if 'data' not in request.json.keys():
        return jsonify({'status': 404, 'info': '找不到你的数据'})

    # 判断报警

    data = Data()
    data.data = request.json.get('data')
    data.sensor_id = sid
    db.session.add(data)
    db.session.commit()
    if data.data > sensor.max:
        alert = Alert()
        alert.sensor_id = sensor.id
        alert.reason = '超出最大值'
        alert.data_id = data.id
        alert.current_max =sensor.max
        alert.current_min=sensor.min
        db.session.add(alert)
        db.session.commit()
    if data.data < sensor.max:
        alert = Alert()
        alert.sensor_id = sensor.id
        alert.reason = '低于最小值'
        alert.data_id = data.id
        alert.current_max = sensor.max
        alert.current_min = sensor.min
        db.session.add(alert)
        db.session.commit()
    return jsonify({'status': 200})


# 下载数据
@api.route('/device/<int:did>/sensor/<int:sid>/data', methods=['GET'])
@auth.login_required
def get_data(did, sid):
    device = g.current_user.devices.filter_by(id=did).first()
    print(device)
    if device is None:
        return jsonify({'status': 404, 'info': '找不到你的设备'})
    sensor = device.sensors.filter_by(id=sid).first()
    if sensor is None:
        return jsonify({'status': 404, 'info': '找不到你的传感器'})
    data = sensor.datas.order_by(Data.timestamp.desc()).first()
    # print(data.data)
    if data is None:
        return jsonify({'status': 404, 'info': '找不到你的数据'})
    return jsonify({'status': 200, 'data': data.data})


# 下载传感器
@api.route('/device/<int:did>/sensor', methods=['GET'])
@auth.login_required
def all_sensors(did):
    slist = []
    device = g.current_user.devices.filter_by(id=did).first()
    print(device)
    if device is None:
        return jsonify({'status': 404, 'info': '你的传感器没有找到'})
    sensors = device.sensors.all()
    print(sensors)
    if sensors is None:
        return jsonify({'status': 404, 'info': '你的传感器没有找到'})
    for sensor in sensors:
        s = sensor.to_json()
        slist.append(s)
        print(slist)
    return jsonify({'status': 200, 'sensors': slist})


# 下载所有数据
@api.route('/device/<int:did>/sensor/<int:sid>/datas/<int:page>', methods=['GET'])
@auth.login_required
def datas(did, sid, page):
    # page = request.args.get('page', type=int, default=1)
    device = g.current_user.devices.filter_by(id=did).first()
    if device is None:
        return jsonify({'status': 404, 'info': '找不到你的设备'})
        print('1')
    sensor = device.sensors.filter_by(id=sid).first()
    if sensor is None:
        return jsonify({'status': 404, 'info': '找不到你的传感器'})
        print('2')
    datas = sensor.datas.order_by(Data.timestamp.desc()).paginate(page=page, per_page=2, error_out=False)
    if not datas:
        return jsonify({'status': 404})
        print('3')
    dlist = []
    for data in datas.items:
        dlist.append(data.to_json())
    print(dlist)
    #print(type(datas), datas)
    # if datas is None:
    #     return jsonify({'status': 404, 'info': '找不到你的数据'})
    return jsonify({'status': 200, 'datas': dlist})




