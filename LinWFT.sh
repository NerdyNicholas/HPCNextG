#!/bin/bash
# Taken from https://medium.com/netflix-techblog/linux-performance-analysis-in-60-000-milliseconds-accc10403c55

# initialize array
COMMANDS=('uptime')
# add systemctl command if it's installed
command -v systemctl >/dev/null && COMMANDS+=('systemctl list-units --state=failed')
# add more commands
COMMANDS+=('dmesg | tail'
          'vmstat 1'
          'mpstat -P ALL 1'
          'pidstat 1'
          'iostat -xz 1'
          'free -m'
          'sar -n DEV 1'
          'sar -n TCP,ETCP 1'
)
# add htop instead of top if it's installed
command -v htop >/dev/null && COMMANDS+=('htop') || COMMANDS+=('top')

continue() {
    read -r -p "${1:-Are you sure? [Y/n]} " response
    response=${response:-yes}
    case "$response" in
        [yY][eE][sS]|[yY])
            true
            ;;
        *)
            exit
            ;;
    esac
}

echo "Pres Ctrl+C to kill forground process"
for COMMAND in "${COMMANDS[@]}"; do
    echo "------------------------------"
    continue "Run ${COMMAND}? [Y/n]"
    set -- $COMMAND
    eval setsid -c "$COMMAND"
done
