python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
shiv dabot -o dabot . --python "/usr/bin/python3 -sE"
