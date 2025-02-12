# Monitor Kubernetes logs

I needed to monitor all the logs from various pods simultaneously. So, I created this script.

You can use it by passing multiple filters with  `-f`  or  `-fa`. The script will search the log output for the presence of any filters passed with  `-f`  or all filters passed with  `-fa`.

```
py kube_log_monitor.py -n mionamespace -fa "[Debug]" -fa "connection string"
```

# Python Dependencies
```
pip install kubernetes
pip install colorama
```


