#!/usr/bin/env bash

source venv/bin/activate
python ./banking_battle/manage.py loaddata ./data_to_base/game.json -i
python ./banking_battle/manage.py loaddata ./data_to_base/rounds.json -i
python ./banking_battle/manage.py loaddata ./data_to_base/user.json -i
python ./banking_battle/manage.py loaddata ./data_to_base/teams.json -i
deactivate