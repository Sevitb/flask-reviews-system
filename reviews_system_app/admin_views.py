import json
import os
import time
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import cm, inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, TableStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from datetime import datetime
from reviews_system_app import app, db
from flask import Flask, flash, url_for, render_template, request, redirect, send_from_directory, current_app
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from .models import Materials, Reviews, User
from .forms import LoginForm

prefix='/adm'

@app.route(prefix, methods=['POST','GET'])
@login_required
def admin():
    return render_template('admin/dashboard/dashboard.html', title="Админ-панель")

# Material

@app.route(prefix + '/materials', methods=['POST','GET'])
@login_required
def adminMaterials():

    materials = Materials.query.order_by(Materials.title).all()

    if request.method == 'POST':

        materialTitle = str(request.form.get('materialTitle'))

        material = Materials(title = materialTitle)

        try:
            db.session.add(material)
            db.session.commit()
            flash('Материал успешно создан!')
            return redirect(request.url)
        except:
            flash('Ошибка при добавлении материала!')
            return redirect(request.url)
    else:
        return render_template('admin/pages/materials/materials.html', title="Материалы", materials=materials)

@app.route(prefix + '/material/edit', methods=['GET','POST'])
@login_required
def adminMaterialEdit():

    material_id = int(request.args.get('material_id'))

    if request.method == 'POST':
        new_title = str(request.form.get('newMaterialTitle'))

        material = Materials.query.filter(Materials.id == material_id).first()

        material.title = new_title

        try:
            db.session.commit()
            flash('Материал успешно изменен!')
            return redirect(url_for('adminMaterials'))
        except:
            flash('Ошибка при изменении материала!')
            return redirect(url_for('adminMaterials'))
    return render_template('admin/pages/materials/edit.html')

# Reviews

@app.route(prefix + '/reviews', methods=['POST','GET'])
@login_required
def adminReviews():
    material_id = int(request.args.get('material_id'))

    all_chapters_filters = []

    if (material_id):
        all_chapters_filters.append(Reviews.material_id == material_id)

    # chapters = Chapters.query.order_by(Chapters.chapterTitle).filter(*all_chapters_filters).all()
    reviews = Reviews.query.order_by(Reviews.id).filter(Reviews.material_id == material_id).all()
    material = Materials.query.filter(Materials.id == material_id).first()
    return render_template('admin/pages/reviews/reviews.html', title="Список рецензий", reviews=reviews, material=material)

@app.route(prefix + '/reviews/create-report', methods=['POST'])
@login_required
def createReport():

    review_id = str(request.form.get('review_id'))
    material_id = str(request.form.get('material_id'))

    material = Materials.query.filter(Materials.id == material_id).first()
    review = Reviews.query.filter(Reviews.id == review_id).first()

    pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))

    doc = SimpleDocTemplate(os.path.join(app.root_path, 'reports') + '/report_'+review_id+'.pdf',
                        rightMargin=60,leftMargin=60,
                        topMargin=60,bottomMargin=18)
    

    Story=[]
    formatted_time = time.ctime()

    paragraphStyleJsutify = ParagraphStyle('Russian_text_justify', alignment=TA_JUSTIFY)
    paragraphStyleJsutify.fontName = 'DejaVuSerif'
    paragraphStyleJsutify.leading = 0.5*cm

    paragraphStyleCenter = ParagraphStyle('Russian_text_center', alignment=TA_CENTER)
    paragraphStyleCenter.fontName = 'DejaVuSerif'
    paragraphStyleCenter.leading = 0.5*cm

    styles=getSampleStyleSheet()
    styles.add(paragraphStyleJsutify)
    styles.add(paragraphStyleCenter)

    tableData = [['Критерий','Комментарий'],
                 [Paragraph('Соответствие работы тематике', styles["Russian_text_justify"]), Paragraph(review.fits_theme, styles["Russian_text_justify"])],
                 [Paragraph('Обоснование целей исследования', styles["Russian_text_justify"]), Paragraph(review.justified, styles["Russian_text_justify"])],
                 [Paragraph('Достигнуты ли цели, поставленные в исследовании', styles["Russian_text_justify"]), Paragraph(review.goal_reached, styles["Russian_text_justify"])],
                 [Paragraph('Вносит ли работа значительный вклад в развитие дисциплины', styles["Russian_text_justify"]), Paragraph(review.contribution_was_made, styles["Russian_text_justify"])],
                 [Paragraph('Актуальность источников', styles["Russian_text_justify"]), Paragraph(review.relevance_of_sources, styles["Russian_text_justify"])],
                 [Paragraph('Соответствие методологии/объяснение методологии: использовал ли автор подходящую методологию? Обоснована ли методология', styles["Russian_text_justify"]), Paragraph(review.into_methodology, styles["Russian_text_justify"])],
                 [Paragraph('Интерпритация результатов: насколько ясно представлены результаты и выводы?', styles["Russian_text_justify"]), Paragraph(review.results_are_interpreted, styles["Russian_text_justify"])],
                 [Paragraph('Изложение текста: Есть ли замечания по стилистике текста?', styles["Russian_text_justify"]), Paragraph(review.presentation_of_text, styles["Russian_text_justify"])],
                 [Paragraph('Графика, рисунки, иллюстрации: Были ли использованы рисунки, таблицы, графики и иллючтрации там, где это необходимо?', styles["Russian_text_justify"]), Paragraph(review.presence_of_graphics, styles["Russian_text_justify"])],
                 
                 ]

    tableStyle = TableStyle([
        ('GRID', (0,0), (-1,-1), 0.25, colors.black),
        ('FONTNAME', (0,0), (-1,-1), 'DejaVuSerif')
        ])

    table = Table(tableData, style=tableStyle, colWidths=[200,200])
    table.wrapOn(Story, 10, 20) 


    Story.append(Paragraph('Рецензия к материалу: ' + material.title, styles["Russian_text_center"]))
    Story.append(Spacer(1, 20))

    Story.append(Paragraph('Данные рецензента:', styles["Russian_text_justify"]))
    Story.append(Spacer(1, 1))
    Story.append(Paragraph(review.reviewer_information, styles["Russian_text_justify"]))
    Story.append(Spacer(1, 1))
    Story.append(Paragraph('Электронная почта: ' + review.email, styles["Russian_text_justify"]))
    Story.append(Spacer(1, 12))

    Story.append(Paragraph('Оценка научного материала по критериям', styles["Russian_text_center"]))
    Story.append(Spacer(1, 20))

    Story.append(table)
    Story.append(Spacer(1, 20))

    Story.append(Paragraph('Комментарии и предложения', styles["Russian_text_center"]))
    Story.append(Spacer(1, 20))

    Story.append(Paragraph('Комментарии автору:', styles["Russian_text_justify"]))
    Story.append(Spacer(1, 1))
    Story.append(Paragraph(review.comment_for_author, styles["Russian_text_justify"]))
    Story.append(Spacer(1, 1))
    Story.append(Paragraph('Комментарии редактору:', styles["Russian_text_justify"]))
    Story.append(Spacer(1, 1))
    Story.append(Paragraph(review.comment_for_editor, styles["Russian_text_justify"]))
    Story.append(Spacer(1, 1))


    Story.append(Paragraph('Заключение и общие рекомендации', styles["Russian_text_center"]))
    Story.append(Spacer(1, 20))

    Story.append(Paragraph('Общие рекомендации:', styles["Russian_text_justify"]))
    Story.append(Spacer(1, 1))
    Story.append(Paragraph(review.general_recommendations, styles["Russian_text_justify"]))
    Story.append(Spacer(1, 1))
    Story.append(Paragraph('Заключение:'+review.result, styles["Russian_text_justify"]))
    Story.append(Spacer(1, 20))


    Story.append(Paragraph('Дата написания рецензии: '+review.created_at, styles["Russian_text_justify"]))

    doc.build(Story)

    return redirect(url_for('download', filename='report_'+review_id+'.pdf'))

@app.route(prefix + '/reviews/table', methods=['POST','GET'])
@login_required
def adminReviewsTable():
    material_id = int(request.args.get('material_id'))

    reviews = Reviews.query.order_by(Reviews.id).filter(Reviews.material_id == material_id).all()
    material = Materials.query.filter(Materials.id == material_id).first()
    return render_template('admin/pages/reviews/reviews-full-table.html', title="Список глав", reviews=reviews, material=material)

@app.route(prefix + '/review/edit', methods=['POST','GET'])
@login_required
def adminChapterEdit():

    chapter_id = int(request.args.get('chapter_id'))

    if request.method == 'POST':
        new_title = str(request.form.get('new'))
        new_authors_count = int(str(request.form.get('count')))

        chapter = Chapters.query.filter(Chapters.id == chapter_id).first()

        chapter.chapterTitle = new_title
        chapter.authorsCountMax = new_authors_count

        try:
            db.session.commit()
            return redirect(url_for('adminChapters'))
        except:
            return "Ошибка при изменении!"
    else:
        chapter = Chapters.query.get(chapter_id)
        return render_template('admin/chapter/edit.html', title="Редактировать главу", chapter=chapter)


@app.route(prefix + "/material/delete", methods=['GET'])
@login_required
def adminMaterialDelete():
    material_id = int(request.args.get('material_id'))

    Materials.query.filter(Materials.id == material_id).delete()
    Reviews.query.filter(Reviews.material_id == material_id).all().delete()

    try:
        db.session.commit()
        flash('Материал успешно удален!')
        return redirect(url_for('adminMaterials'))

    except:
        flash('Ошибка при удалении материала!')
        return redirect(url_for('adminMaterials'))

# Utils

@app.route('/reports/<path:filename>', methods=['GET', 'POST'])
@login_required
def download(filename):
    reports = os.path.join(app.root_path, 'reports')
    return send_from_directory(directory=reports, path=filename)

@app.route(prefix + '/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('admin'))

        flash("Неправильное имя пользователя/пароль", 'error')
        return redirect(url_for('login'))
    return render_template('admin/auth/login/login.html', title="Вход",form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли.")
    return redirect(url_for('login'))