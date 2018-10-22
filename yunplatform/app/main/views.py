from flask_login import login_required, logout_user, login_user
from . import main
from flask import abort, redirect, render_template, request, url_for
from app.models import User, News, Device, Sensor, Data, Alert
from .forms import EditUserForm, PostNewsForm, DeviceForm, SensorForm, EditSensorForm, SearchForm, HeadImageForm
from flask_login import current_user
from app import db
# from app import uploadset
from flask import session

@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/user_info')
@login_required
def user_info():
    id = request.args.get('id')
    if id is None:
        abort(404)
        print('1')
    news = News.query.filter_by(user_id=id).all()
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    return render_template('main/user_info.html', user=user, news=news)


@main.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    form = EditUserForm()
    if form.validate_on_submit():
        print('3')
        user = User.query.filter_by(id=current_user.id).first()
        user.name = form.name.data
        user.about_me = form.about_me.data
        user.location = form.location.data
        if len(form.password.data) != 0:
            user.password.data = form.password.data
        print('2')
        db.session.add(user)
        db.session.commit()
        print('1')
        return redirect(url_for('main.user_info', id=user.id))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('main/edit_user.html', form=form)


@main.route('/post_news', methods=['GET', 'POST'])
@login_required
def post_news():
    form = PostNewsForm()
    if form.validate_on_submit():
        print('1')
        new = News()
        new.body = form.body.data
        new.private = form.private.data
        new.title = form.title.data
        new.user_id = current_user.id
        db.session.add(new)
        db.session.commit()
        print('2')
        return redirect(url_for('main.user_info', id=current_user.id))
    return render_template('main/post_news.html', form=form)


@main.route('/news')
@login_required
def news():

    nid = request.args.get('nid')
    print(nid)
    if nid is None:
        abort(404)
        print('1')
    news = News.query.filter_by(user_id=nid).first()
    if news is None:
        abort(404)
        print('3')
    print('2')
    return render_template('main/news.html', news=news)


@main.route('/delete_news')
@login_required
def delete_news():
    nid = request.args.get('nid')
    if nid is None:
        abort(404)
    news = News.query.filter_by(id=nid).first()
    if news is None:
        abort(404)
    if current_user == news.user or current_user.is_admin():
        db.session.delete(news)
        db.session.commit()
    return redirect(url_for('main.user_info', id=current_user.id))


@main.route('/edit_news', methods=['GET', 'POST'])
def edit_news():
    nid = request.args.get('nid')
    if nid is None:
        abort(404)
    news = News.query.filter_by(id=nid).first()
    if news is None:
        abort(404)
    form = PostNewsForm()
    if form.validate_on_submit():
        news.title = form.title.data
        news.body = form.body.data
        news.private = form.private.data
        db.session.add(news)
        db.session.commit()
        return redirect(url_for('main.news', nid=nid))
    form.title.data = news.title
    form.body.data = news.body
    return render_template('main/post_news.html', form=form)


@main.route('/all_devices')
@login_required
def all_devices():
    id = request.args.get('id')
    if id is None:
        abort(404)
    page = request.args.get('page', type=int, default=1)
    devices = Device.query.filter_by(user_id=id).paginate(page=page, per_page=5, error_out=False)
    if devices is None:
        abort(404)
    return render_template('main/all_devices.html', devices=devices,id=id)


@main.route('/add_device', methods=['GET', 'POST'])
@login_required
def add_device():
    id = request.args.get('id')
    form = DeviceForm()
    if form.validate_on_submit():
        device = Device()
        device.name = form.name.data
        device.describe = form.describe.data
        device.location = form.location.data
        device.user_id = id
        db.session.add(device)
        db.session.commit()
        return redirect(url_for('main.all_devices', id=id))
    return render_template('main/add_device.html', form=form)


@main.route('/delete_device')
@login_required
def delete_device():
    did = request.args.get('did')
    if did is None:
        abort(404)
    device = Device.query.filter_by(id=did).first()
    if device is None:
        abort(404)
    if current_user.is_admin or current_user.is_common_user :
        db.session.delete(device)
        db.session.commit()
    return redirect(url_for('main.all_devices', id=current_user.id))


@main.route('/edit_device', methods=['GET', 'POST'])
@login_required
def edit_device():
    did = request.args.get('did')
    if did is None:
        abort(404)
    device = Device.query.filter_by(id=did).first()
    if device is None:
        abort(404)
    form = DeviceForm()
    if form.validate_on_submit():
        device.name = form.name.data
        device.describe = form.describe.data
        device.location = form.location.data
        db.session.add(device)
        db.session.commit()
        return redirect(url_for('main.all_devices', id=current_user.id))
    form.name.data = device.name
    form.describe.data = device.describe
    form.location.data = device.location
    return render_template('main/edit_device.html', form=form)


@main.route('/device')
def device():
    did = request.args.get('did')
    if did is None:
        abort(404)
    sensors = Sensor.query.filter_by(device_id=did).all()
    device = Device.query.filter_by(id=did).first()
    if device is None:
        abort(404)
    return render_template('main/device.html', device=device, sensors=sensors)


@main.route('/add_sensor', methods=['GET', 'POST'])
def add_sensor():
    did = request.args.get('did')
    form = SensorForm()
    if form.validate_on_submit():
        sensor = Sensor()
        sensor.name = form.name.data
        sensor.describe = form.describe.data
        sensor.unit = form.unit.data
        sensor.device_id = did
        db.session.add(sensor)
        db.session.commit()
        return redirect(url_for('main.device', did=did))
    return render_template('main/add_sensor.html', form=form)


@main.route('/delete_sensor')
def delete_sensor():
    did = request.args.get('did')
    sid = request.args.get('sid')
    if sid is None:
        abort(sid)
    sensor = Sensor.query.filter_by(id=sid).first()
    if sensor is None:
        abort(404)
    if current_user.is_admin() or current_user.is_common_user():
        db.session.delete(sensor)
        db.session.commit()
    return redirect(url_for('main.device', did=did))


@main.route('/edit_sensor', methods=['GET', 'POST'])
def edit_sensor():
    did = request.args.get('did')
    sid = request.args.get('sid')
    if sid is None:
        abort(404)
    sensor = Sensor.query.filter_by(id=sid).first()
    if sensor is None:
        abort(404)
    form = EditSensorForm()
    if form.validate_on_submit():
        sensor.name = form.name.data
        sensor.describe = form.describe.data
        sensor.unit = form.unit.data
        sensor.max = form.max.data
        sensor.min = form.min.data
        db.session.add(sensor)
        db.session.commit()
        return redirect(url_for('main.device', did=did))
    form.name.data = sensor.name
    form.describe.data = sensor.describe
    form.unit.data = sensor.unit
    form.max.data = sensor.max
    form.min.data = sensor.min
    return render_template('main/edit_sensor.html', form=form)


@main.route('/data')
@login_required
def data_info():
    page = request.args.get('page', type=int, default=1)
    sid = request.args.get('sid')
    datas = Data.query.filter_by(sensor_id=sid).paginate(page=page, per_page=9, error_out=False)
    #print(datas)
    datacount = int(len(datas.items)/3)
    data1 = datas.items[0:datacount]
    #print(data1)
    data2 = datas.items[datacount:datacount*2]
    data3 = datas.items[datacount*2:]
    xlist = []
    ylist = []
    for data in datas.items:
        xlist.append(data.timestamp)
        ylist.append(data.data)
        #print(xlist)
        #print(ylist)
    # print(datas)
    return render_template('main/data_info.html', data1=data1, data2=data2, data3=data3,datas=datas, xDataArray=xlist, yDataArray=ylist, sid=sid)


@main.route('/alert',methods=['GET', 'POST'])
@login_required
def alert():
    page = request.args.get('page', type=int, default=1)
    alerts = Alert.query.order_by(Alert.timestamp.desc()).paginate(page=page, per_page=10, error_out=False)
    form = SearchForm()
    if form.validate_on_submit():
        page = request.args.get('page', type=int, default=1)
        sensor_id = form.data.data
        # alerts = Alert.query.filter(Alert.sensor_id.like('%'+sensor_id+'%')).paginate(page=page, per_page=10, error_out=False)
        return redirect(url_for('main.alerts', sensor_id=sensor_id))
        #print(sensor)
        # if len(alerts) == 0:
        #     abort(404)

    # alerts1 = Alert.query.all()
    # for alert in alerts1:
    #     alert.data_id
        # print(alert.data_id)
    return render_template('main/alert.html', alerts=alerts, form=form)


# 显示图片路由
@main.route('/show_image')
def show_image():
    pic_name = request.args.get('pic_name')
    if not pic_name:
        abort(404)
    return render_template('main/show_image.html', image_url=url_for('static', filename='images'+pic_name))


@main.route('/image', methods=['GET', 'POST'])
def image():
    form = HeadImageForm()
    if form.validate_on_submit():
        # 获得文件对象
        file = request.files['file']
        print(file)
        if file:
        # 保存文件
            file.save('D:/PyCharm2017.3/yunplatform/app/static/images' +form.pic_name.data)
        return redirect(url_for('.show_image', pic_name=form.pic_name.data))
    return render_template('main/image.html', form=form)


# 上传图片路由
# @main.route('/image', methods=['GET', 'POST'])
# def uploadHeadImage():
#     form = HeadImageForm()
#     if form.validate_on_submit():
#         fileName = uploadset.save(form.file.data, folder='abc', name=form.fileName.data)
#         session['headImage'] = fileName
#         return redirect(url_for('.uploadHeadImage'))
#     fileName = session['headImage']
#     if fileName:
#         url = uploadset.url(fileName)
#     else:
#         url = None
#     session['headImage'] = None
#     return render_template('main/uploadHeadImage.html', form=form,url=url)


@main.route('/alerts')
def alerts():
    sensor_id = request.args.get('sensor_id')
    page = request.args.get('page', type=int, default=1)
    alerts = Alert.query.filter(Alert.sensor_id.like('%' + sensor_id + '%')).paginate(page=page, per_page=10,
                                                                                      error_out=False)

    return render_template('main/alerts.html', alerts=alerts, sensor_id=sensor_id)


