import argparse
from kubernetes import client, config, watch
from colorama import Fore, Style, init

# Inizializza colorama
init(autoreset=True)

def monitor_pod_logs(namespace, filters=None, and_filters=None):
    config.load_kube_config()

    v1 = client.CoreV1Api()

    w = watch.Watch()
    if namespace is None:
        contexts, active_context = config.list_kube_config_contexts()
        namespace = active_context['context'].get('namespace', 'default')

    try:
        while True:
            for pod in v1.list_namespaced_pod(namespace).items:
                pod_name = pod.metadata.name
                #print(f"{Fore.YELLOW}Monitoring logs for pod: {pod_name}{Style.RESET_ALL}")
                try:
                    for line in w.stream(v1.read_namespaced_pod_log, name=pod_name, namespace=namespace, follow=True):
                        finded = False
                        if filters is None and and_filters is None:
                            finded = True
                        else:
                            if filters:
                                for f in filters:
                                    if f in line:
                                        finded = True
                                        break
                            if and_filters:
                                finded = all(f in line for f in and_filters)
                        
                        if finded:
                            output = line.replace("[Error]", f"{Fore.RED}[Error]{Style.RESET_ALL}") \
                                        .replace("[Debug]", f"{Fore.YELLOW}[Debug]{Style.RESET_ALL}") \
                                        .replace("[Information]", f"{Fore.GREEN}[Information]{Style.RESET_ALL}")
                            print(f"{Fore.YELLOW}{pod_name}{Style.RESET_ALL}: {output}")
                except Exception as e:
                    print(f"{Fore.RED}Error monitoring pod {pod_name}{Style.RESET_ALL}: {e}")
    except KeyboardInterrupt:
        print("\nMonitoring interrupted by user.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor Kubernetes pod logs with filters.")
    parser.add_argument("-n", "--namespace", required=False, help="Namespace to monitor")
    parser.add_argument("-f", "--filter", action="append", required=False, help="Filter strings to search in logs. You can specify more filters.")
    parser.add_argument("-fa", "--and-filter", action="append", required=False, help="Filter strings that must all be present in logs. You can specify more filters.")

    args = parser.parse_args()

    namespace = None
    filters = None 
    and_filters = None
    if args.namespace is not None:
        namespace = args.namespace
    if args.filter is not None:
        filters = args.filter
    if args.and_filter is not None:
        and_filters = args.and_filter

    monitor_pod_logs(namespace, filters, and_filters)
