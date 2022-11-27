from flask import render_template, redirect, url_for, flash
from app import app
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import Contact, SignupForm, LogInForm
from app.models import Contact, User


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contacts')
@login_required
def contacts():
    contact = Contact.query.all()
    return render_template("contacts.html", contact=contact)


@app.route('/contacts/<contact_id>')
@login_required
def contact(contact_id):
    contact = Contact.query.get(contact_id)
    return render_template("contacts.html", contact=contact)


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = Contact()
    if form.validate_on_submit():
        first_name = form.first.data
        last_name = form.last.data
        phone_num = form.phone.data
        home = form.home.data
        print(first_name, last_name, phone_num, home)

        check_contact = Contact.query.filter(
            (Contact.first_name == first_name) and (Contact.last_name == last_name)).first()
        if check_contact is not None:
            flash("This person is already in your addressbook.", 'danger')
            return redirect(url_for('contacts'))
        new_contact = Contact(
            first_name=first_name, last_name=last_name, phone_num=phone_num, home=home)
        flash(f"{new_contact} was uploaded to your contacts.", "success")
        return redirect(url_for('index'))

    return render_template('create_contacts.html', form=form)


app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.user_name.data
        password = form.password.data
        print(email, name, password)

        checks = User.query.filter(
            (User.email == email) | (User.user_name == name))
        if checks is not None:
            flash('Congrats on your new account', 'success')
            return redirect(url_for('index'))
        # else:
        #     flash('There is already an account with that Username or Email', 'warning')
        #     return redirect(url_for('login'))
        

    return render_template('sign_up.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter(email=email).first()

        if email is not None and User.pass_check(password):
            login_user(user)
            flash(f"{User.user_name} has successfully logged in.", 'success')
            return redirect(url_for(index))
        else:
            flash(f"Something went wrong please check your email or password", 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('comeback soon', 'primary')
    return redirect(url_for('index'))


@app.route('/contacts/<contact_id>/delete')
@login_required
def delete(contacts_id):
    contact = Contact.query.get(contacts_id)

    if contact.author != current_user:
        flash("You do not have permission for this", "danger")
        return render_template(url_for('index'))

    contact.delete()
    flash(f" {contact.first_name} has been deleted from your contacts?")
    return render_template(url_for('index'))


@app.route('/contacts/<contact_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(contact_id):
    contact = Contact.query.get(contact_id)

    form = Contact()
    if form.validate_on_submit():
        new_first_name = form.first.data
        new_last_name = form.last.data
        new_phone_num = form.phone.data
        new_home = form.home.data
        contact.update(new_first_name, new_last_name, new_phone_num, new_home)
        flash("This contact has been updated", 'success')
        return render_template(url_for('get_post', contact_id))

    if contact.author != current_user:
        flash("You do not have permission for this", "danger")
        return render_template(url_for('index'))

    return render_template(url_for('edit_contact.html', form=form, contact=contact))
