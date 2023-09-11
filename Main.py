from flask import Flask, request, render_template
import Helpers  # Importing helper methods

app = Flask(__name__)


@app.route('/')
def index():
    """
    Renders the main page of the weather forecast app.

    This route function is responsible for rendering the main page of the weather
    forecast application. When a user accesses the root URL ("/"), this function
    is triggered, and it returns the rendered HTML template for the main page.

    Returns:
        str: Rendered HTML template for the main page.
    """
    return render_template('index.html')


@app.route('/', methods=["POST"])
def requests_handler():
    """
      Handles form submissions for weather data retrieval.

      This function processes form submissions from the main page to retrieve
      weather data based on the user's input. It distinguishes between POST
      requests (form submissions) and GET requests (initial page load).

      Returns:
          str: Rendered HTML template with updated weather data or error messages.
      """
    if request.method == "POST":
        # Process the form submission and retrieve location data
        location_data, country_name, location_display, error_message = Helpers.form_handler(request.form)

        # Display the weather information using the updated page
        return update_page(location_display, location_data, country_name, error_message)

    return render_template('index.html')                # Render the initial form page for GET requests


def update_page(location_name, weather_data, country_name, error_message=None):
    """
       Renders the HTML template with updated weather data and information.

       This function generates and returns the rendered HTML template for the main page
       of the weather forecast app. It takes as input the updated weather data and
       information, including the location name, weather data, country name, and optional
       error message.

       Args:
           location_name (str): The name of the location (city or capital) to display.
           weather_data (dict or None): The weather data to be displayed.
           country_name (str): The name of the country associated with the location.
           error_message (str, optional): An optional error message to display in case of errors.

       Returns:
           str: Rendered HTML template with updated weather data and information.
       """
    return render_template(
        'index.html',
        locationName=location_name,
        data=weather_data,
        country_name=country_name,
        error_message=error_message
    )


if __name__ == '__main__':
    app.run(debug=False)
