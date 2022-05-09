from flask import Blueprint, redirect, render_template, flash, session, url_for
from flask_login import login_required, current_user
from .models import BlogPost
from .forms import NewPost
from datetime import date, datetime
from . import db
from .auth import admin_only


views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template ("home.html")

@views.route("/blog")
@login_required
def blog():
    all_posts = BlogPost.query.all()
    return render_template ("blog.html", all_posts=all_posts)

@views.route("/add_new_post", methods=['GET','POST'])
@login_required
def add_new_post():
    form = NewPost()
    if form.validate_on_submit():
        title = form.title.data
        subtitle = form.subtitle.data
        img_url = form.img_url.data
        body = form.body.data
        author = current_user.id

        new_post =  BlogPost(
            title = title,
            subtitle = subtitle,
            img_url = img_url,
            body = body,
            date = datetime.now().strftime('%d/%m/%Y'),
            author_id = author
        )
        db.session.add(new_post)
        db.session.commit()

        flash('Post wprowadzony pomyślnie :)', category='success')
        return redirect(url_for('views.blog'))

    return render_template ("new_post.html", form=form)


@views.route("/post/<int:post_id>")
@login_required
def show_post(post_id):
    the_post = BlogPost.query.get(post_id)
    return render_template ("post.html", post=the_post)


@views.route("/edit-post/<int:post_id>", methods=['GET','POST'])
@admin_only
def edit_post(post_id):
    edited_post = BlogPost.query.get(post_id)
    edit_form = NewPost(obj=edited_post)

    if edit_form.validate_on_submit():
        edited_post.title = edit_form.title.data
        edited_post.subtitle = edit_form.subtitle.data
        edited_post.img_url = edit_form.img_url.data
        edited_post.date = datetime.now().strftime('%d/%m/%Y')
        edited_post.author_id = current_user.id

        db.session.commit()
        return redirect(url_for('views.blog'))

    return render_template("new_post.html", form=edit_form)