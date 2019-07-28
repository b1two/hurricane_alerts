# hurricane_alerts
Sends daily SMS about current atlantic hurricane situation and Kick'em Jenny volcano alerts with Bouygues Telecom SMS service.

## Setup
```
git clone --recursive git@github.com:b02c/hurricane_alerts.git
cd hurricane_alerts/
cp pass_config.example.py pass_config.py
```
* Edit pass_config.py
* Run `hurricane.py`

## Run periodically
Add an entry in your crontab (here using fcron):
```
fcrontab -e
```
Add this line for running the script every day at 3pm :
```
0 15 * * * <path_to_hurricane.py> > <path_to_log_file_if_desired_or_/dev/null> 2>&1
```

## Thanks to
Thanks to abdel-elbel for providing the script to use easily the Bouygues Telecom SMS service. His repo : [github.com/abdel-elbel/bouygues_pysms](github.com/abdel-elbel/bouygues_pysms)
