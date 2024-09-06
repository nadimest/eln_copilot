import plotly.graph_objs as go
import pandas as pd
import numpy as np
import itertools
from functools import cache

# Define a list of distinct color scales
color_scales = ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
         'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
         'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
         'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
         'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
         'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
         'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
         'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',
         'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
         'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',
         'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar',
         'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
         'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid',
         'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',
         'ylorrd']

# Create a cycler for color scales
color_scale_cycler = itertools.cycle(color_scales)

@cache
def get_color_scale(selected_metadata):
    """
    Get a color scale for the given metadata key.
    The @cache decorator ensures that the same metadata key always gets the same color scale.
    """
    return next(color_scale_cycler)

def create_heatmap(samples, heatmap_config, selected_metadata):
    """
    Create a heatmap visualization based on the sample data and selected metadata.
    
    Args:
    samples (list): List of Sample objects.
    heatmap_config (HeatmapConfig): Configuration for the heatmap.
    selected_metadata (str): The metadata to use for coloring the heatmap.
    
    Returns:
    plotly.graph_objs._figure.Figure: Plotly figure object for the heatmap.
    """
    df = pd.DataFrame([s.model_dump() for s in samples])
    
    # Extract row and column from position
    if 'position' not in df.columns:
        raise ValueError("'position' column not found in the DataFrame")
    
    # Convert position to string if it's not already
    df['position'] = df['position'].astype(str)
    
    df['row'] = df['position'].str[0]
    df['col'] = df['position'].str[1:].astype(int)

    # Create a pivot table for the heatmap
    heatmap_data = df.pivot(index='row', columns='col', values=selected_metadata)
    
    # Ensure all rows and columns are present
    all_rows = pd.Index(heatmap_config.rows)
    all_cols = pd.Index(range(1, len(heatmap_config.columns) + 1))  # Start from 1
    heatmap_data = heatmap_data.reindex(index=all_rows, columns=all_cols)

    # Create hover text
    hover_text = df.apply(lambda row: f"Sample: {row['sample_name']}<br>Compound: {row['starting_compound']}<br>Process: {row['process']}<br>Enzyme: {row['enzyme']}", axis=1)
    hover_text = hover_text.to_frame('hover_text')
    hover_text['row'] = df['row']
    hover_text['col'] = df['col']
    hover_text = hover_text.pivot(index='row', columns='col', values='hover_text')
    hover_text = hover_text.reindex(index=all_rows, columns=all_cols)

    # Create a mapping of unique values to numeric values for coloring
    unique_values = sorted(df[selected_metadata].unique())
    value_to_numeric = {value: i for i, value in enumerate(unique_values)}
    
    # Convert heatmap_data to numeric values
    z_values = [[value_to_numeric.get(val, -1) if pd.notna(val) else -1 for val in row] for row in heatmap_data.values]
    
    # Get the color scale for the selected metadata
    color_scale = get_color_scale(selected_metadata)

    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        x=all_cols,  # Use all_cols instead of heatmap_config.columns
        y=heatmap_config.rows,
        hoverinfo='text',
        text=hover_text.values,
        colorscale=color_scale,
        colorbar=dict(
            title=selected_metadata.capitalize(),
            tickvals=list(value_to_numeric.values()),
            ticktext=list(value_to_numeric.keys())
        ),
        showscale=True
    ))

    # Add grid lines with offset
    for i in range(len(heatmap_config.rows) + 1):
        fig.add_shape(
            type="line",
            x0=0.5,  # Start from 0.5
            y0=i - 0.5,
            x1=len(heatmap_config.columns) + 0.5,  # End at len + 0.5
            y1=i - 0.5,
            line=dict(color="Black", width=1)
        )
    for j in range(len(heatmap_config.columns) + 1):
        fig.add_shape(
            type="line",
            x0=j + 0.5,  # Adjust to j + 0.5
            y0=-0.5,
            x1=j + 0.5,  # Adjust to j + 0.5
            y1=len(heatmap_config.rows) - 0.5,
            line=dict(color="Black", width=1)
        )

    fig.update_layout(
        title=f'Sample Grid - {selected_metadata.capitalize()}',
        xaxis_title='Column',
        yaxis_title='Row',
        yaxis=dict(autorange='reversed'),
        width=800,
        height=400,  # Reduced height for multiple heatmaps
        xaxis=dict(
            side='top',
            tickmode='linear',
            tick0=1,
            dtick=1,
            tickfont=dict(size=10)
        ),
        xaxis_range=[0.5, len(heatmap_config.columns) + 0.5],  # Adjust range
        yaxis_range=[-0.5, len(heatmap_config.rows) - 0.5]
    )

    return fig

# Add any additional helper functions for heatmap visualization here