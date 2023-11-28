.main-container {
    font-family: 'Roboto', sans-serif;
    color: #333;
}

.nav-bar {
    background-color: #f8f9fa;
    padding: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-link {
    margin-right: 15px;
    color: #007bff;
    text-decoration: none;
    font-weight: 500;
}

.nav-link:hover {
    color: #0056b3;
    text-decoration: underline;
}

@media (max-width: 768px) {
    .nav-link {
        display: block;
        margin-bottom: 10px;
    }
}

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Home', href='/', className='nav-link'),
        dcc.Link('Page 1', href='/page1', className='nav-link'),
        dcc.Link('Page 2', href='/page2', className='nav-link'),
    ], className='nav-bar'),
    html.Div(id='page-content')
], className='main-container')
