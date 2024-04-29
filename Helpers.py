from countryinfo import CountryInfo
import requests
import pycountry
import json


# Load API key and URL from the configuration file
with open('config.json') as config_file:
    config = json.load(config_file)
    API_KEY = config['weather_api_key']
    API_URL = config['weather_api_url']


class CountryNotFoundError(Exception):
    """ Custom exception raised when a requested country's information cannot be found."""
    pass


def get_weather_data(location):
    """
      Fetches weather data from an external API for the given location.

      This function sends a GET request to an external weather API to retrieve weather
      data for the specified location. The API URL is constructed using the provided
      location and API key. The response is then checked for a successful status code,
      and if it's 200 (OK), the JSON data is parsed and returned. If the response status
      code is not 200, the function returns None.

      Args:
          location (str): The name of the location for which weather data is requested.

      Returns:
          dict or None: A dictionary containing weather data if the API response is successful,
                        or None if an issue occurs during API communication.
      """
    url = f"{API_URL}?city={location}&key={API_KEY}&days=7"     # Construct the API URL
    response = requests.get(url)                                # Send a GET request to the API and receive the response

    if response.status_code == 200:
        return response.json()                                  # Parse and return the JSON data from the response
    else:
        return None


def get_country_name(country_code):
    """
    Retrieves the country name using a country code.
    Args:
        country_code (str): The two-letter country code (alpha-2) for the country.
    Returns:
        str or None: The name of the country corresponding to the given code,
                    or None if the country is not found or an error occurs.
    """
    try:
        country = pycountry.countries.get(alpha_2=country_code)  # Retrieve the country info using the provided code
        if country:         # If country information is found, return its name
            return country.name
        else:
            return None
    except LookupError:     # Catch exceptions during the lookup process, like if the code isn't valid
        return None


def form_handler(form):
    """Processes the form submission and returns location data.
    This function processes the submitted form data and retrieves relevant location
    information, including weather data, country name, and location display name.
    It handles two modes of operation: searching by country and searching by city.
    Args:
        form (ImmutableMultiDict): The form data submitted by the user.
    Returns:
        tuple: A tuple containing:
            - location_data (dict or None): Weather data for the location.
            - country_name (str): The name of the associated country.
            - location_to_upper (str): The location name in title case or uppercase.
            - error_message (str or None): An error message if an issue occurs during processing.
    """
    location = form['input_location']
    search_by_country = bool(form.get("search_by_country", False))

    if search_by_country:
        location_data, country_name, location_to_upper, error_message = handle_country_search(location)
    else:
        location_data, country_name, location_to_upper, error_message = handle_city_search(location)

    return location_data, country_name, location_to_upper, error_message


def handle_country_search(location):
    """Handles form submission for country search mode.
    Args:
        location (str): The name of the country entered by the user.
    Returns:
        tuple: A tuple containing the location data, country name, location display name,
               and an error message (if applicable)."""
    try:
        country_info = CountryInfo(location)        # Create a "CountryInfo" instance and fetch capital city
        capital = country_info.capital()

        if not capital:
            raise CountryNotFoundError              # Raise exception if capital city is not found

        location_data = get_weather_data(capital)   # Fetch weather data for the capital city
        country_name = country_info.info().get('name')
        location_to_upper = capital.title()
        error_message = None

    except (CountryNotFoundError, KeyError):        # Handle exceptions by setting error message and resetting values
        error_message = "Country not found, please try again."
        location_data = None
        country_name = ""
        location_to_upper = ""

    return location_data, country_name, location_to_upper, error_message


def handle_city_search(location):
    """Handles form submission for city search mode.
    Args:
        location (str): The name of the city entered by the user.
    Returns:
        tuple: A tuple containing the location data, country name, location display name,
               and an error message (if applicable). """
    location_data = get_weather_data(location)                  # Fetch weather data for the entered city

    if location_data:
        country_code = location_data['country_code']            # Extract country code and country name
        country_name = get_country_name(country_code)
        location_to_upper = location.title()
        error_message = None
    else:
        error_message = "City not found, please try again."     # Handle case when no weather data is available
        country_name = ""
        location_to_upper = ""

    return location_data, country_name, location_to_upper, error_message
