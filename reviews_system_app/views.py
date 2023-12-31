import json 
from datetime import datetime
from reviews_system_app import app, db, babel
from flask import render_template, request, redirect, url_for, flash
from flask_babel import gettext
from .forms import ReviewForm
from .models import Materials, Reviews, User
from .utils import send_mail


def get_locale():
    if (request.args.get('lang')):
        return request.args.get('lang')
    else:
        return 'ru'

babel.init_app(app, locale_selector=get_locale)

@app.route('/')
def materials():
    materials = Materials.query.order_by(Materials.title).all()
    return render_template('pages/materials/materials.html', title='Материалы', materials=materials)

@app.route('/choose-review-language')
def choose_review_language():
    return render_template('pages/choose-review-language/choose-review-language.html', title='Выбор языка', material_id=request.args.get('material_id'))

@app.route('/review/send', methods = ['GET', 'POST'])
def review():
    reviewForm = ReviewForm()

    if request.method == 'POST':

        review = Reviews(
            material_id = request.args.get('material_id'),
            email = str(request.form.get('email')),
            reviewer_information = str(request.form.get('reviewer_information')),
            fits_theme = json.dumps({
                'answer': str(request.form.get('fits_theme')),
                'comment': str(request.form.get('fits_theme-comment'))
                }),
            justified = json.dumps({
                'answer': str(request.form.get('justified')),
                'comment': str(request.form.get('justified-comment'))
                }),
            goal_reached = json.dumps({
                'answer': str(request.form.get('goal_reached')),
                'comment': str(request.form.get('goal_reached-comment'))
                }),
            contribution_was_made = json.dumps({
                'answer': str(request.form.get('contribution_was_made')),
                'comment': str(request.form.get('contribution_was_made-comment'))
                }), 
            relevance_of_sources = json.dumps({
                'answer': str(request.form.get('relevance_of_sources')),
                'comment': str(request.form.get('relevance_of_sources-comment'))
                }), 
            into_methodology = json.dumps({
                'answer': str(request.form.get('into_methodology')),
                'comment': str(request.form.get('into_methodology-comment'))
                }), 
            results_are_interpreted = json.dumps({
                'answer': str(request.form.get('results_are_interpreted')),
                'comment': str(request.form.get('results_are_interpreted-comment'))
                }), 
            presentation_of_text = json.dumps({
                'answer': str(request.form.get('presentation_of_text')),
                'comment': str(request.form.get('presentation_of_text-comment'))
                }), 
            presence_of_graphics = json.dumps({
                'answer': str(request.form.get('presence_of_graphics')),
                'comment': str(request.form.get('presence_of_graphics-comment'))
                }), 
            comment_for_author = str(request.form.get('comment_for_author')),
            comment_for_editor = str(request.form.get(' comment_for_editor')),
            result = str(request.form.get('result')),
            general_recommendations = str(request.form.get('general_recommendations')),
            created_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            )
        
        try:
            db.session.add(review)
            db.session.commit()

            flash(gettext('Great! Your review has been sent!'), 'message')
                
            # send_mail("Спасибо за заявку!",emailAdress,"mail/author-letter.html",author=authorData)
            # send_mail("Заявка к книге (authorsdatasend.ru)!",['iscvolga@yandex.ru],["mail/isc-letter.html"],"isc-letter.html")

            return redirect(url_for('materials'))
        except:
            flash(gettext('Sorry, it looks like something went wrong. Please try again later.'), 'danger')
            return redirect(url_for('materials'))

    return render_template('pages/review/review-form.html', title='Рецензия', reviewForm=reviewForm)

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

@app.errorhandler(500)
def not_found(error):
    return render_template('error.html'), 500