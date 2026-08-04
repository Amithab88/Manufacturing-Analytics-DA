def load_css():
    return """
    <style>

    .main{
        background-color:#F8F9FA;
    }

    .block-container{
        padding-top:2rem;
        padding-bottom:2rem;
        padding-left:3rem;
        padding-right:3rem;
    }

    h1{
        color:#1F2937;
        font-weight:700;
    }

    h2,h3{
        color:#374151;
    }

    div[data-testid="stMetric"]{
        background-color:white;
        border:1px solid #E5E7EB;
        padding:20px;
        border-radius:12px;
        box-shadow:0 2px 8px rgba(0,0,0,0.05);
    }

    div[data-testid="stMetricLabel"]{
        font-size:16px;
        font-weight:600;
    }

    div[data-testid="stMetricValue"]{
        font-size:34px;
        color:#111827;
    }

    hr{
        margin-top:30px;
        margin-bottom:30px;
    }

    </style>
    """