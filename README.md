# Train Connection and Restaurant Finder App

## Description

This Streamlit application helps users find train connections and discover top-rated restaurants near their destinations. It is based on Assignment 6 of the FCS course at the University of St. Gallen. It uses the `Connection` [(in connection.py)](connection.py) class as well as the functions `find_connection`, `find_restaurants` and `find_top10_restaurants_for_trip` [(in utils.py)](utils.py) with some small adjustments. These functions are used in the [app.py](app.py) file which contains the code for running the app, storing session information and displaying the input forms and results. The app uses streamlit secrets to store the Yelp API key. The key is retrieved from the secrets file and passed to the `find_restaurants` function (see below for more details).

## Setup and Installation

### Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/hawk-li/fcs-streamlit-connection-finder.git
```

### Install Dependencies

Install the dependencies in a virtual environment:

```bash
pip install -r requirements.txt
```

### Setting up the API Key

The application requires a Yelp Fusion API key to run.

[Register](https://www.yelp.com/signup) to Yelp and [request a private API key](https://www.yelp.com/developers/v3/manage_app). (Note: The second link will work only if you logged in to Yelp).

After retrieving the key, we need to store it in a streamlit secrets file. This file is used to store secrets like API keys and passwords. The file must be added to the `.streamlit` folder. The folder needs to be located in the root directory of the app (create it if it doesn't exist already). In the `.streamlit` folder, create a file named `secrets.toml`. The file should look like this:

```bash
# .streamlit/secrets.toml
API_KEY = "YOUR_API_KEY_HERE"
```

The [app.py](app.py) file retrieves this key automatically from the secrets file on startup which is then passed to the `find_top10_restaurants` function to query the Yelp API (see lines 60 and 110). This way, the API key is not exposed in the code and the `find_top10_restaurants` is agnostic of the streamlit implementation (does not have to use `st.secrets`).

### Run the Application

To run the application, run the following command in the terminal in the root directory of the repository:

```bash
streamlit run app.py
```
