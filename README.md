# Swisscom SMS pour Home Assistant

Intégration personnalisée qui envoie des SMS via l'**API Swisscom Messaging**.
Vous fournissez votre `client_id` Swisscom, et un service `notify` apparaît dans
Home Assistant : utilisable dans vos automatisations, scripts et scènes en
précisant les numéros destinataires et le message.

## Prérequis

- Un abonnement à l'API **Swisscom Messaging** (produit SMS) sur
  [developer.swisscom.com](https://developer.swisscom.com), qui vous donne un
  **`client_id`**.
- Home Assistant 2024.11 ou plus récent.

## Installation

### Via HACS (recommandé)

1. HACS → Intégrations → menu ⋮ → **Dépôts personnalisés**.
2. Ajoutez `https://github.com/Sdavid66/Homeassistant_Swisscom` (catégorie
   *Integration*).
3. Installez **Swisscom SMS**, puis redémarrez Home Assistant.

### Manuelle

Copiez le dossier `custom_components/swisscom_sms` dans le dossier
`custom_components` de votre configuration Home Assistant, puis redémarrez.

## Configuration

1. **Paramètres → Appareils et services → Ajouter une intégration**.
2. Cherchez **Swisscom SMS**.
3. Renseignez votre `client_id` Swisscom (et, éventuellement, le nom du service
   notify — par défaut `Swisscom SMS`).

Un service `notify.swisscom_sms` est alors créé (le nom suit celui que vous
avez choisi).

## Utilisation

Le service envoie un SMS à chaque numéro listé dans `target`. Un numéro valide
commence par `0`, `00` ou `+` et contient 7 à 15 chiffres (les numéros locaux
en `0` sont préfixés `+41` par Swisscom).

### Exemple simple

```yaml
service: notify.swisscom_sms
data:
  message: "Le portail du garage est resté ouvert."
  target:
    - "+41791234567"
```

### Plusieurs destinataires

```yaml
service: notify.swisscom_sms
data:
  message: "Alarme déclenchée à la maison !"
  target:
    - "+41791234567"
    - "+41789876543"
```

### Dans une automatisation

```yaml
automation:
  - alias: "Alerte fuite d'eau"
    trigger:
      - platform: state
        entity_id: binary_sensor.detecteur_fuite_cuisine
        to: "on"
    action:
      - service: notify.swisscom_sms
        data:
          message: "Fuite d'eau détectée dans la cuisine !"
          target:
            - "+41791234567"
```

## Dépannage

- Les erreurs d'envoi (mauvais `client_id`, numéro invalide, quota épuisé…)
  sont écrites dans les **journaux** de Home Assistant
  (`Paramètres → Système → Journaux`), avec le code HTTP renvoyé par Swisscom.
- `HTTP 401` : `client_id` manquant ou incorrect.
- `HTTP 400` : numéro de téléphone invalide.
- `HTTP 429` : quota d'envoi épuisé.

Pour modifier le `client_id` ultérieurement : intégration → **Reconfigurer**.
