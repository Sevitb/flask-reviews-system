from flask_wtf import FlaskForm
from wtforms import Form, ValidationError
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField, RadioField
from wtforms.validators import DataRequired, Email
from .fields import RadioPlusField
from flask_babel import lazy_gettext

class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember = BooleanField("Запомнить меня")
    submit = SubmitField("Отправить")

class ReviewForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])

    reviewer_information = TextAreaField(
        lazy_gettext(u'Reviewer information'), 
        validators=[DataRequired()], 
        description=lazy_gettext(u'Provide your information (in English if possible): full name, degree, title, affiliation, e-mail and address.'))

    fits_theme = RadioField(
        lazy_gettext(u'Relevance of the work to the book’s topic'), 
        validators=[DataRequired()], 
        choices=[
            (lazy_gettext('Corresponds'),lazy_gettext('Corresponds')),
            (lazy_gettext('Revision is required'),lazy_gettext('Revision is required'))],
        description=lazy_gettext(u'Check option 1 or 2; provide a brief comment on your answer in the section “other.”'))

    justified = RadioField(
        lazy_gettext(u'Rationale for the research goals'), 
        validators=[DataRequired()], 
        choices=[
            (lazy_gettext('Substantiated'),lazy_gettext('Substantiated')),
            (lazy_gettext('Revision is required'),lazy_gettext('Revision is required'))],
        description=lazy_gettext(u'Check option 1 or 2; provide a brief comment on your answer in the section “other.”'))

    goal_reached = RadioField(
        lazy_gettext(u'Are the research goals achieved'), 
        validators=[DataRequired()], 
        choices=[
            (lazy_gettext('Achieved'),lazy_gettext('Achieved')),
            (lazy_gettext('Revision is required'),lazy_gettext('Revision is required'))],
        description=lazy_gettext(u'Check option 1 or 2; provide a brief comment on your answer in the section “other.”'))

    contribution_was_made = RadioField(
        lazy_gettext(u'Does this work make a significant contribution to the development of the discipline?'), 
        validators=[DataRequired()], 
        choices=[
            (lazy_gettext('Yes'),lazy_gettext('Yes')),
            (lazy_gettext('No'),lazy_gettext('No'))],
        description=lazy_gettext(u'Check option 1 or 2; provide a brief comment on your answer in the section “other.”'))

    relevance_of_sources = RadioField(
        lazy_gettext(u'Relevance of references'), 
        validators=[DataRequired()], 
        choices=[
            (lazy_gettext('Yes'),lazy_gettext('Yes')),
            (lazy_gettext('No'),lazy_gettext('No'))],
        description=lazy_gettext(u'Check option 1 or 2; provide a brief comment on your answer in the section “other.”'))

    into_methodology = RadioField(
        lazy_gettext(u'Appropriateness of the methodology / explanation of the methodology: Did the author use an appropriate methodology? Is the methodology justified?'), 
        validators=[DataRequired()], 
        choices=[
            (lazy_gettext('The methodology is consistent'),lazy_gettext('The methodology is consistent')),
            (lazy_gettext('Revision is required'),lazy_gettext('Revision is required'))],
        description=lazy_gettext(u'Check option 1 or 2; provide a brief comment on your answer in the section “other.”'))

    results_are_interpreted = RadioField(
        lazy_gettext(u'Interpretation of the results: How clearly the results and conclusions are presented?'), 
        validators=[DataRequired()], 
        choices=[
            (lazy_gettext('The results and conclusions are clear'),lazy_gettext('The results and conclusions are clear')),
            (lazy_gettext('Revision is required'),lazy_gettext('Revision is required'))],
        description=lazy_gettext(u'Check option 1 or 2; provide a brief comment on your answer in the section “other.”'))

    presentation_of_text = RadioField(
        lazy_gettext(u'A presentation of the text of the article: Are there any comments on the style of the text?'), 
        validators=[DataRequired()], 
        choices=[
            (lazy_gettext('No comments'),lazy_gettext('No comments')),
            (lazy_gettext('Revision is required'),lazy_gettext('Revision is required'))],
        description=lazy_gettext(u'Check option 1 or 2; provide a brief comment on your answer in the section “other.”'))

    presence_of_graphics = RadioField(
        lazy_gettext(u'Diagrams, Figures, Illustrations: Were figures, tables, graphs, and illustrations used where appropriate?'), 
        validators=[DataRequired()], 
        choices=[
            (lazy_gettext('The use is appropriate'),lazy_gettext('The use is appropriate')),
            (lazy_gettext('The use is not appropriate'),lazy_gettext('The use is not appropriate'))],
        description=lazy_gettext(u'Check option 1 or 2; provide a brief comment on your answer in the section “other.”'))

    comment_for_author = TextAreaField(
        lazy_gettext(u'Comments and suggestions to the book author'), 
        validators=[DataRequired()])

    comment_for_editor = TextAreaField(
        lazy_gettext(u'Comments and suggestions to the book editor'), 
        validators=[DataRequired()])

    result = RadioField(
        lazy_gettext(u'Conclusion'),
        choices=[
            (lazy_gettext('Accept the text as it is'),lazy_gettext('Accept the text as it is')),
            (lazy_gettext('Accept the text after minor revisions'),lazy_gettext('Accept the text after minor revisions')),
            (lazy_gettext('Revise the text and resubmit it for further review'),lazy_gettext('Revise the text and resubmit it for further review')),
            (lazy_gettext('Reject'),lazy_gettext('Reject'))
            ],
        validators=[DataRequired()])

    general_recommendations = TextAreaField(
        lazy_gettext(u'General recommendations'), 
        validators=[DataRequired()])
    
    submit = SubmitField('POST')