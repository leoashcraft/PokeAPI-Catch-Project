from flask import g, render_template, request, redirect, url_for, flash
import requests
from app import app
from .forms import SearchForm, LoginForm, RegisterForm
from .models import User, Pokemon, db
from flask_login import login_user, logout_user, current_user, login_required

#Routes
@app.route('/', methods=['GET'])
def index():
    form = SearchForm()
    g.form=form
    return render_template('index.html.j2')

@app.route('/register', methods=['GET','POST'])
def register():
    form = SearchForm()
    g.form=form
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "password": form.password.data
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
        except:
            error_string="There was a problem creating your account. Please try again"
            return render_template('register.html.j2',form=form, error=error_string)
        # Give the user some feedback that says registered successfully 
        return redirect(url_for('login'))

    return render_template('register.html.j2',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = SearchForm()
    g.form=form
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Do login Stuff
        email = form.email.data.lower()
        password = form.password.data
        u = User.query.filter_by(email=email).first()
        print(u)
        if u is not None and u.check_hashed_password(password):
            login_user(u)
            # Give User feeedback of success
            return redirect(url_for('index'))
        else:
            # Give user Invalid Password Combo error
            return redirect(url_for('login'))
    return render_template("login.html.j2", form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user is not None:
        logout_user()
        return redirect(url_for('index'))

@app.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    form = SearchForm()
    g.form=form
    if request.method == 'POST' and g.form.validate_on_submit():
        pokemon = form.search.data.lower()
        print("Pokemon is", pokemon)
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
        response = requests.get(url)
        if response.ok:
            try:
                data = response.json().get("stats")
                spritedata = response.json()["sprites"]['other']['dream_world'].get("front_default")
                print("Sprit data is", spritedata)
            except:
                error_string=f'There is no info for {pokemon}'
                return render_template("pokemon.html.j2", form=form, error=error_string)

            # Check if pokemon exists
            check_pokemon = bool(Pokemon.query.filter_by(name = pokemon).first())

            if check_pokemon == True:
                user = current_user

                # Check is user has the pokemon
                user_pokemon_object = db.session.query(User).join(User.pokemons).filter(Pokemon.name==pokemon).all()

                # Send message to frontend if user has pokemon
                if user in user_pokemon_object:
                    flash(f'{pokemon.capitalize()} already exists in your database', 'success')
                else:
                    # Add pokemon to user's pokemon list
                    p = Pokemon.query.filter_by(name = pokemon).first()
                    user.pokemons.append(p)
                    db.session.add(user)
                    db.session.commit()
                    flash(f'{pokemon.capitalize()} has been added to your pokemon collections', 'success')
                
            # If pokemon has never been searched before then add to database
            else:
                new_pokemon_data={
                    "name": pokemon,
                    "spritedata": spritedata
                }
                
                # Create a dictionary with each attribute as a key
                for attribute in data:
                    attribute_name = attribute['stat']['name']
                    if attribute_name == 'special-attack':
                        new_pokemon_data['special_attack'] = {'base_stat': attribute['base_stat'], 'effort' : attribute['effort']}
                    elif attribute_name == 'special-defense':
                        new_pokemon_data['special_defense'] = {'base_stat': attribute['base_stat'], 'effort' : attribute['effort']}
                    else:
                        new_pokemon_data[attribute_name] = {'base_stat': attribute['base_stat'], 'effort' : attribute['effort']}
                
                new_pokemon_object = Pokemon()
                new_pokemon_object.from_dict(new_pokemon_data)
                u = current_user
                p = Pokemon.query.filter_by(name = pokemon).first()
                u.pokemons.append(p)
                db.session.add(u)
                db.session.commit()
                flash(f'{pokemon.capitalize()} has been added to your pokemon collections', 'success')

            all_stats = []
            for stat in data:
                stat_dict={
                    'poke_statbase':stat['base_stat'],
                    'poke_stateffort':stat['effort'],
                    'poke_statname':stat['stat']['name'],
                }
                all_stats.append(stat_dict)
            return render_template("pokemon.html.j2", form=form, stats=all_stats, sprite=spritedata, pokemon=pokemon.title())
        else:
            error_string="Invalid Pokemon name!"
            return render_template("pokemon.html.j2", form=form, error=error_string)
    return render_template("pokemon.html.j2", form=form)   
#export/set FLASK_APP=app.py
#export/set FLASK_ENV=development
