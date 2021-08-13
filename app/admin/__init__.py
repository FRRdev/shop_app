from app import app, db
from flask import url_for, redirect, request, abort
from app.models import Users, Role, Category, Product, Cart, Comment
from wtforms import FileField
from flask_login import current_user
import flask_login as login
# flask-security
from flask_security import SQLAlchemyUserDatastore, Security
# flask-admin
import flask_admin
from flask_admin import helpers, expose, form
from flask_admin.contrib import sqla

user_datastore = SQLAlchemyUserDatastore(db, Users, Role)
security = Security(app, user_datastore)


class MyImageView(sqla.ModelView):
    form_extra_fields = {
        'image': form.ImageUploadField('Image',
                                       base_path='app/static/img/',
                                       thumbnail_size=(200, 200, False))
    }


class MyAdminIndexView(flask_admin.AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_page'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_page(self):
        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_page(self):
        login.logout_user()
        return redirect(url_for('.index'))

    @expose('/reset/')
    def reset_page(self):
        return redirect(url_for('.index'))


# Create admin
admin = flask_admin.Admin(app, index_view=MyAdminIndexView(), base_template='admin/master-extended.html')

admin.add_view(sqla.ModelView(Users, db.session))
admin.add_view(MyImageView(Product, db.session))
admin.add_view(sqla.ModelView(Cart, db.session))
admin.add_view(sqla.ModelView(Comment, db.session))
admin.add_view(sqla.ModelView(Category, db.session))


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=helpers,
        get_url=url_for
    )
