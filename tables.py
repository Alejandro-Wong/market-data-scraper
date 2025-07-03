import plotly.graph_objects as go
import pandas as pd

def table(df: pd.DataFrame, title: str, filepath: str) -> None:

    row_even_color = 'slategrey'
    row_odd_color = 'black'

    fig =  go.Figure(data=[go.Table(
        columnwidth = [25, 70, 70, 70, 70],
        header=dict(values=list(df.columns),
                    fill_color='darkslategrey',
                    align='center',
                    font_size=13,
                    font_color='white'),
        cells=dict(values=df.transpose().values.tolist(),
                   fill_color=[[row_odd_color, row_even_color]*len(df)],
                   font_color='floralwhite',
                   align='center',
                   font_size=12))
    ])


    fig.update_layout(
        paper_bgcolor='black',
        title_text=title,
        title_x=0.5,
        title_font_color='floralwhite',
        width=1000,
        height=600
    )
    fig.update_layout({'margin':{'t':50}})
    fig.write_image(f'{filepath}{title}.png', width=1000, height=600)

