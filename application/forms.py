from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField, BooleanField, TextAreaField, SubmitField
from wtforms.validators  import ValidationError, DataRequired, Email, EqualTo, Length
from application.models import Users

class LoginForm (FlaskForm):
    username = StringField(lazy_gettext('Username'), validators=[DataRequired()])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired()])
    remember_me = BooleanField(lazy_gettext('Remember me'))
    btn_submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email')

class EditProfileForm (FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=200)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs) :
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data !=self.original_username:
            user = User.query.filter_by(username=self.username.data).first()

            if user is not None:
                raise ValidationError('Please use a different username.')

class SampleForm (FlaskForm):
    description = StringField ('Description of Sample', validators=[Length(min=1, max=255)])
    species = StringField ('Type of Species', validators=[Length(min=1, max=85)])
    location_collected = StringField ('Area, County, Country', validators=[Length(min=1, max=85)])
    project = StringField ('Project it belongs', validators=[DataRequired(), Length(min=1, max=85)])
    owner = StringField ('The owner of the project', validators=[Length(min=1, max=85)])
    retension_period = IntegerField ('Retension of the sample in months', validators=[DataRequired()])
    barcode = StringField ('Barcode Number', validators=[Length(min=1, max=85)])
    analysis = StringField ('Type analysis carried out', validators=[Length(min=1, max=85)])
    amount = IntegerField ('Amount of Sample', validators=[DataRequired()])

    submit = SubmitField('Submit')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired()])
    password2 = PasswordField(
                lazy_gettext('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')
