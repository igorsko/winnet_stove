DOMAIN = "winet_stufa"
CONF_HOST = "host"
CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_SCAN_INTERVAL = 30

# Stati della stufa
STOVE_STATES = {
    0: "unknown",
    1: "off",
    2: "starting",
    3: "working",
    4: "wait_on",
    5: "temp_ok",
    6: "no_program",
    7: "wait_time",
    8: "stop",
    9: "sunout"
}
