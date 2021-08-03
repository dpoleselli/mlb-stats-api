# MLB Stats API

Runs a Flask App that serves MLB data stored in a MongoDB. A nightly job collects the data and stores it in the database, then the Flask app provides access to the data.

## Service Configuration

To run the app as a service run `sudo mv service/\* /etc/systemd/system/`
