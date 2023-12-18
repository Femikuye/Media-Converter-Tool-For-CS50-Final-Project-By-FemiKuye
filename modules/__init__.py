from flask import render_template




APP_PORT = 7200
ROOT_URL = f"http://localhost:{APP_PORT}"
def error_response(message, type = 'json', code=400):
    if type == "json":
        return { "msg": message } , code
    
def apology_copied_from_CS50(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code