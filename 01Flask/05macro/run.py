from app import app
app.add_template_global(str,'str')
app.run(debug=True)
