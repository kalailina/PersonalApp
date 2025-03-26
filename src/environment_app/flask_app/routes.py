from flask import Blueprint, render_template, request, flash, redirect, url_for
from environment_app.flask_app import db  # Use absolute import here
from environment_app.flask_app.models import Borough, Sector, Type, EnergyConsumption, GHGEmission, Feedback
from environment_app.flask_app.helpers import (
    get_borough_data, create_combined_chart,
    get_available_years, get_available_boroughs,
    get_sector_breakdown, create_sector_pie_charts,
    create_side_by_side_charts, make_energy_prediction, 
    make_emission_prediction  
)
from environment_app.flask_app.forms import PredictionForm, FeedbackForm
from datetime import datetime

# Create Blueprint
main = Blueprint('main', __name__)


@main.route('/')
def index():
    # Get data
    boroughs_count = db.session.query(Borough).count()
    sectors_count = db.session.query(Sector).count()
    types_count = db.session.query(Type).count()
    
    # Get latest year
    latest_year = db.session.query(db.func.max(EnergyConsumption.year)).scalar()
    
    # Get totals
    total_consumption = db.session.query(
        db.func.sum(EnergyConsumption.consumption)
    ).filter(
        EnergyConsumption.year == latest_year
    ).scalar() or 0
    
    total_emission = db.session.query(
        db.func.sum(GHGEmission.emission)
    ).filter(
        GHGEmission.year == latest_year
    ).scalar() or 0
    
    # Simple render_template call
    return render_template(
        'index.html',
        boroughs_count=boroughs_count,
        sectors_count=sectors_count,
        types_count=types_count,
        latest_year=latest_year,
        total_consumption=total_consumption,
        total_emission=total_emission
    )


@main.route('/dashboard')
def dashboard():
    """Dashboard page with visualizations"""
    # Get filter parameters from query string
    selected_year = request.args.get('year', type=int)
    selected_borough = request.args.get('borough')
    
    # If selected_borough is "All Boroughs" or empty, set to None
    if selected_borough == "All Boroughs" or not selected_borough:
        selected_borough = None
    
    # Get data for visualizations
    consumption_df, emission_df = get_borough_data(selected_year)
    
    # Create charts based on whether a year is selected
    if selected_year:
        # Create separate charts for the specific year
        consumption_fig, emission_fig = create_side_by_side_charts(
            consumption_df, emission_df, selected_year, selected_borough
        )
        # Convert charts to HTML
        consumption_chart_html = consumption_fig.to_html(full_html=False)
        emission_chart_html = emission_fig.to_html(full_html=False)
    else:
        # Create line chart for all years
        main_fig = create_combined_chart(consumption_df, emission_df, selected_borough)
        # Convert chart to HTML
        consumption_chart_html = main_fig.to_html(full_html=False)
        emission_chart_html = None  # Only used when viewing a specific year
    
    # Get sector breakdown data and create pie charts
    sector_consumption_df, sector_emission_df = get_sector_breakdown(selected_year, selected_borough)
    consumption_pie, emission_pie = create_sector_pie_charts(
        sector_consumption_df, sector_emission_df, selected_year, selected_borough
    )
    
    # Convert pie charts to HTML
    consumption_pie_html = consumption_pie.to_html(full_html=False)
    emission_pie_html = emission_pie.to_html(full_html=False)
    
    # Get available years and boroughs for filter dropdowns
    years = get_available_years()
    boroughs = get_available_boroughs()
    
    return render_template(
        'dashboard.html',
        consumption_chart=consumption_chart_html,
        emission_chart=emission_chart_html,
        consumption_pie=consumption_pie_html,
        emission_pie=emission_pie_html,
        years=years,
        boroughs=boroughs,
        selected_year=selected_year,
        selected_borough=selected_borough
    )

@main.route('/prediction', methods=['GET', 'POST'])
def prediction():
    """Page for predicting future energy consumption and emissions"""
    # Populate borough and sector choices
    form = PredictionForm()
    
    # Dynamically populate borough choices
    form.borough.choices = [(-1, "All Boroughs")] + [
        (b.borough_id, b.borough_name) for b in Borough.query.all()
    ]
    
    # Dynamically populate sector choices
    form.sector.choices = [(-1, "All Sectors")] + [
        (s.sector_id, s.sector_name) for s in Sector.query.all()
    ]
    
    # Initialize prediction variables
    energy_prediction = None
    emission_prediction = None
    energy_explanation = None
    emission_explanation = None
    borough_name = "All Boroughs"
    sector_name = "All Sectors"
    
    # If form is submitted and valid
    if form.validate_on_submit():
        # Get form data
        borough_id = form.borough.data
        sector_id = form.sector.data
        prediction_year = form.year.data
        
        # Get names for display
        if borough_id != -1:
            borough = Borough.query.get(borough_id)
            borough_name = borough.borough_name if borough else "Unknown"
        
        if sector_id != -1:
            sector = Sector.query.get(sector_id)
            sector_name = sector.sector_name if sector else "Unknown"
        
        # Make predictions
        energy_prediction, energy_explanation = make_energy_prediction(
            borough_id, sector_id, prediction_year
        )
        
        emission_prediction, emission_explanation = make_emission_prediction(
            borough_id, sector_id, prediction_year
        )
    
    return render_template(
        'prediction.html',
        form=form,
        energy_prediction=energy_prediction,
        emission_prediction=emission_prediction,
        energy_explanation=energy_explanation,
        emission_explanation=emission_explanation,
        borough_name=borough_name,
        sector_name=sector_name,
        prediction_year=form.year.data if form.validate() else None
    )

@main.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """Feedback submission route"""
    form = FeedbackForm()
    
    # If form is submitted and valid
    if form.validate_on_submit():
        # Create a new feedback record
        new_feedback = Feedback(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data,
            submitted_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        # Save to database
        try:
            db.session.add(new_feedback)
            db.session.commit()
            flash('Thank you for your feedback!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    # If form is not valid, render the form again
    return render_template('feedback.html', form=form)