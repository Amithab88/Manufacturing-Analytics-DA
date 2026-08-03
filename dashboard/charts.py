import plotly.express as px


def factory_production_chart(df):
    fig = px.bar(
        df,
        x="factory_name",
        y="total_units_produced",
        color="factory_name",
        title="Factory-wise Production",
        text="total_units_produced"
    )

    fig.update_layout(
        xaxis_title="Factory",
        yaxis_title="Units Produced",
        showlegend=False,
        height=500
    )

    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside"
    )

    return fig