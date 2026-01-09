'''
Main orchestration page
'''

from src.app.app_factory import create_dash_app


# Create Dash app
app = create_dash_app()
app.run(debug=True, use_reloader=False, port=8052)
