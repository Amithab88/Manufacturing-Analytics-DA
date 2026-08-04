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

import plotly.express as px


def machine_status_chart(df):
    fig = px.pie(
        df,
        names="status",
         values="total_machines",
        hole=0.55,
        title="Machine Status Distribution"
    )

    fig.update_traces(
        textinfo="percent+label"
    )

    fig.update_layout(
        height=500,
        legend_title="Status"
    )


    return fig