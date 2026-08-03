"""Constantes de l'integration Swisscom SMS."""
from __future__ import annotations

DOMAIN = "swisscom_sms"

# Cles de configuration
CONF_CLIENT_ID = "client_id"
CONF_NAME = "name"

DEFAULT_NAME = "Swisscom SMS"

# Configuration YAML globale, conservee pour le chargement de la plateforme
# notify (voir __init__.py).
DATA_HASS_CONFIG = "swisscom_sms_hass_config"

# API Swisscom Messaging
API_URL = "https://api.swisscom.com/messaging/sms"
SCS_VERSION = "2"
REQUEST_TIMEOUT = 15  # secondes
