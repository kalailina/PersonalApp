import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from environment_app.flask_app import db  # Use absolute import here
from plotly.subplots import make_subplots


def get_borough_data(selected_year=None):
    """Get energy consumption and emissions data by borough"""
    
    # Build queries to get data from the database
    consumption_query = """
        SELECT Borough.borough_name, Energy_Consumption.year, 
               SUM(Energy_Consumption.consumption) as total_consumption
        FROM Energy_Consumption
        JOIN Borough ON Energy_Consumption.borough_id = Borough.borough_id
    """
    
    emission_query = """
        SELECT Borough.borough_name, GHG_Emission.year, 
               SUM(GHG_Emission.emission) as total_emission
        FROM GHG_Emission
        JOIN Borough ON GHG_Emission.borough_id = Borough.borough_id
    """
    
    # Add year filter if provided
    if selected_year:
        consumption_query += f" WHERE Energy_Consumption.year = {selected_year}"
        emission_query += f" WHERE GHG_Emission.year = {selected_year}"
    
    # Group by borough and year
    consumption_query += " GROUP BY Borough.borough_name, Energy_Consumption.year"
    emission_query += " GROUP BY Borough.borough_name, GHG_Emission.year"
    
    # Execute queries
    consumption_df = pd.read_sql_query(consumption_query, db.get_engine())
    emission_df = pd.read_sql_query(emission_query, db.get_engine())
    
    return consumption_df, emission_df


def create_combined_chart(consumption_df, emission_df, selected_borough=None):
    """Create a combined line chart showing consumption and emission data over multiple years"""
    
    if selected_borough:
        consumption_df = consumption_df[consumption_df['borough_name'] == selected_borough]
        emission_df = emission_df[emission_df['borough_name'] == selected_borough]
        title = f"Energy Consumption and Emissions for {selected_borough}"
    else:
        # Aggregate data across all boroughs if no specific borough is selected
        consumption_df = consumption_df.groupby('year')['total_consumption'].sum().reset_index()
        emission_df = emission_df.groupby('year')['total_emission'].sum().reset_index()
        title = "Energy Consumption and Emissions Across All Boroughs"
    
    # Create a figure with two y-axes
    fig = go.Figure()
    
    # Add consumption trace (blue line)
    fig.add_trace(go.Scatter(
        x=consumption_df['year'],
        y=consumption_df['total_consumption'],
        name='Energy Consumption',
        line=dict(color='blue', width=2)
    ))
    
    # Add emission trace (red line)
    fig.add_trace(go.Scatter(
        x=emission_df['year'],
        y=emission_df['total_emission'],
        name='GHG Emissions',
        line=dict(color='red', width=2),
        yaxis='y2'
    ))
    
    # Set up the layout with two y-axes
    fig.update_layout(
        title=title,
        xaxis=dict(
            title='Year',
            type='category',  # Make x-axis categorical to properly display years
            tickmode='array',
            tickvals=sorted(consumption_df['year'].unique())  # Show all years without gaps
        ),
        yaxis=dict(
            title=dict(text='Energy Consumption', font=dict(color='blue')),
            tickfont=dict(color='blue')
        ),
        yaxis2=dict(
            title=dict(text='GHG Emissions', font=dict(color='red')),
            tickfont=dict(color='red'),
            anchor='x',
            overlaying='y',
            side='right'
        ),
        legend=dict(x=0.01, y=0.99),
        height=600
    )
    
    return fig


def create_side_by_side_charts(consumption_df, emission_df, selected_year, selected_borough=None):
    """Create two separate charts side by side for energy consumption and emissions"""
    
    # Filter data based on selected borough
    if selected_borough:
        consumption_df = consumption_df[consumption_df['borough_name'] == selected_borough]
        emission_df = emission_df[emission_df['borough_name'] == selected_borough]
        subtitle = f"for {selected_borough}"
    else:
        subtitle = "for All Boroughs"
    
    # Create energy consumption chart
    consumption_fig = px.bar(
        consumption_df,
        x='borough_name',
        y='total_consumption',
        title=f"Energy Consumption in {selected_year} {subtitle}",
        color_discrete_sequence=['blue'],
        labels={'borough_name': 'Borough', 'total_consumption': 'Energy Consumption'}
    )
    
    consumption_fig.update_layout(
        xaxis=dict(tickangle=-45),
        height=500
    )
    
    # Create GHG emissions chart
    emission_fig = px.bar(
        emission_df,
        x='borough_name',
        y='total_emission',
        title=f"GHG Emissions in {selected_year} {subtitle}",
        color_discrete_sequence=['red'],
        labels={'borough_name': 'Borough', 'total_emission': 'GHG Emissions'}
    )
    
    emission_fig.update_layout(
        xaxis=dict(tickangle=-45),
        height=500
    )
    
    return consumption_fig, emission_fig


def get_sector_breakdown(selected_year=None, selected_borough=None):
    """Get sector breakdown data for pie charts"""
    
    # Query for energy consumption by sector
    consumption_query = """
        SELECT Sector.sector_name, SUM(Energy_Consumption.consumption) as total_consumption
        FROM Energy_Consumption
        JOIN Sector ON Energy_Consumption.sector_id = Sector.sector_id
        JOIN Borough ON Energy_Consumption.borough_id = Borough.borough_id
    """
    
    # Query for emissions by sector
    emission_query = """
        SELECT Sector.sector_name, SUM(GHG_Emission.emission) as total_emission
        FROM GHG_Emission
        JOIN Sector ON GHG_Emission.sector_id = Sector.sector_id
        JOIN Borough ON GHG_Emission.borough_id = Borough.borough_id
    """
    
    # Add filters if provided
    where_clauses = []
    
    if selected_year:
        where_clauses.append(f"Energy_Consumption.year = {selected_year}")
    
    if selected_borough:
        where_clauses.append(f"Borough.borough_name = '{selected_borough}'")
    
    if where_clauses:
        consumption_query += " WHERE " + " AND ".join(where_clauses)
    
    # Reset where_clauses for emission query
    where_clauses = []
    
    if selected_year:
        where_clauses.append(f"GHG_Emission.year = {selected_year}")
    
    if selected_borough:
        where_clauses.append(f"Borough.borough_name = '{selected_borough}'")
    
    if where_clauses:
        emission_query += " WHERE " + " AND ".join(where_clauses)
    
    # Group by sector
    consumption_query += " GROUP BY Sector.sector_name"
    emission_query += " GROUP BY Sector.sector_name"
    
    # Execute queries
    consumption_df = pd.read_sql_query(consumption_query, db.get_engine())
    emission_df = pd.read_sql_query(emission_query, db.get_engine())
    
    return consumption_df, emission_df


def create_sector_pie_charts(consumption_df, emission_df, selected_year=None, selected_borough=None):
    """Create pie charts showing sector breakdown"""
    
    # Create consumption pie chart
    consumption_title = "Energy Consumption by Sector"
    if selected_year:
        consumption_title += f" ({selected_year})"
    if selected_borough:
        consumption_title += f" - {selected_borough}"
    
    consumption_fig = px.pie(
        consumption_df,
        values='total_consumption',
        names='sector_name',
        title=consumption_title,
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    
    # Create emission pie chart
    emission_title = "GHG Emissions by Sector"
    if selected_year:
        emission_title += f" ({selected_year})"
    if selected_borough:
        emission_title += f" - {selected_borough}"
    
    emission_fig = px.pie(
        emission_df,
        values='total_emission',
        names='sector_name',
        title=emission_title,
        color_discrete_sequence=px.colors.sequential.Reds_r
    )
    
    # Layout settings
    for fig in [consumption_fig, emission_fig]:
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400, margin=dict(t=50, b=20, l=20, r=20))
    
    return consumption_fig, emission_fig


def get_available_years():
    """Get all available years from the database"""
    query = """
        SELECT DISTINCT year FROM Energy_Consumption
        UNION
        SELECT DISTINCT year FROM GHG_Emission
        ORDER BY year
    """
    years_df = pd.read_sql_query(query, db.get_engine())
    return years_df['year'].tolist()


def get_available_boroughs():
    """Get all available boroughs from the database"""
    query = "SELECT borough_id, borough_name FROM Borough ORDER BY borough_name"
    boroughs_df = pd.read_sql_query(query, db.get_engine())
    return boroughs_df


def make_energy_prediction(borough_id, sector_id, prediction_year):
    """Make a prediction for future energy consumption
    
    If borough_id is -1, it indicates 'All Boroughs' was selected
    If sector_id is -1, it indicates 'All Sectors' was selected
    """
    # Build the base query
    query = """
        SELECT year, SUM(consumption) as total_consumption
        FROM Energy_Consumption
    """
    
    # Add filters based on selections
    where_clauses = []
    
    if borough_id != -1:  # If specific borough selected
        where_clauses.append(f"borough_id = {borough_id}")
    
    if sector_id != -1:  # If specific sector selected
        # This will correctly handle sector_id=0 (domestic)
        where_clauses.append(f"sector_id = {sector_id}")
    
    # Add WHERE clause if any filters are applied
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    # Group by year to get annual totals
    query += " GROUP BY year ORDER BY year"
    
    # Debug output
    print("Energy Query:", query)
    
    # Execute query and get historical data
    historical_data = pd.read_sql_query(query, db.get_engine())
    
    if historical_data.empty:
        return None, "No historical data available for this combination."
    
    # Get latest data
    latest_year = historical_data['year'].max()
    latest_value = historical_data[historical_data['year'] == latest_year]['total_consumption'].iloc[0]
    
    # If only one data point, return that value as prediction
    if len(historical_data) < 2:
        return latest_value, f"Prediction based on limited data (only {latest_year} available)"
    
    # Calculate average annual change rate
    historical_data['year_diff'] = historical_data['year'].diff()
    historical_data['consumption_diff'] = historical_data['total_consumption'].diff()
    historical_data['annual_change_rate'] = historical_data['consumption_diff'] / historical_data['total_consumption'].shift(1)
    
    # Remove NaN values (first row)
    historical_data = historical_data.dropna()
    
    # Calculate average annual change rate
    avg_annual_change = historical_data['annual_change_rate'].mean()
    
    # Simple prediction using compound growth formula
    years_to_predict = prediction_year - latest_year
    prediction = latest_value * ((1 + avg_annual_change) ** years_to_predict)
    
    # Ensure prediction is not negative
    prediction = max(0, prediction)
    
    explanation = f"Based on historical data from {historical_data['year'].min()} to {latest_year}, " \
                 f"with an average annual change rate of {avg_annual_change:.2%}"
    
    return prediction, explanation


def make_emission_prediction(borough_id, sector_id, prediction_year):
    """Make a prediction for future GHG emissions
    
    If borough_id is -1, it indicates 'All Boroughs' was selected
    If sector_id is -1, it indicates 'All Sectors' was selected
    """
    # Build the base query
    query = """
        SELECT year, SUM(emission) as total_emission
        FROM GHG_Emission
    """
    
    # Add filters based on selections
    where_clauses = []
    
    if borough_id != -1:  # If specific borough selected
        where_clauses.append(f"borough_id = {borough_id}")
    
    if sector_id != -1:  # If specific sector selected
        # This will correctly handle sector_id=0 (domestic)
        where_clauses.append(f"sector_id = {sector_id}")
    
    # Add WHERE clause if any filters are applied
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    # Group by year to get annual totals
    query += " GROUP BY year ORDER BY year"
    
    # Debug output
    print("Emission Query:", query)
    
    # Execute query and get historical data
    historical_data = pd.read_sql_query(query, db.get_engine())
    
    if historical_data.empty:
        return None, "No historical data available for this combination."
    
    # Get latest data
    latest_year = historical_data['year'].max()
    latest_value = historical_data[historical_data['year'] == latest_year]['total_emission'].iloc[0]
    
    # If only one data point, return that value as prediction
    if len(historical_data) < 2:
        return latest_value, f"Prediction based on limited data (only {latest_year} available)"
    
    # Calculate average annual change rate
    historical_data['year_diff'] = historical_data['year'].diff()
    historical_data['emission_diff'] = historical_data['total_emission'].diff()
    historical_data['annual_change_rate'] = historical_data['emission_diff'] / historical_data['total_emission'].shift(1)
    
    # Remove NaN values (first row)
    historical_data = historical_data.dropna()
    
    # Calculate average annual change rate
    avg_annual_change = historical_data['annual_change_rate'].mean()
    
    # Simple prediction using compound growth formula
    years_to_predict = prediction_year - latest_year
    prediction = latest_value * ((1 + avg_annual_change) ** years_to_predict)
    
    # Ensure prediction is not negative
    prediction = max(0, prediction)
    
    explanation = f"Based on historical data from {historical_data['year'].min()} to {latest_year}, " \
                 f"with an average annual change rate of {avg_annual_change:.2%}"
    
    return prediction, explanation