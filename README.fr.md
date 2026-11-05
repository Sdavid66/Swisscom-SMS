<img src="https://raw.githubusercontent.com/Sdavid66/Swisscom-SMS/main/custom_components/swisscom_sms/brand/icon.png" alt="Swisscom SMS" width="96" align="right">

# Swisscom SMS pour Home Assistant

[![Release](https://img.shields.io/github/v/release/Sdavid66/Swisscom-SMS)](https://github.com/Sdavid66/Swisscom-SMS/releases)
[![HACS](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://hacs.xyz)
[![Licence](https://img.shields.io/github/license/Sdavid66/Swisscom-SMS)](LICENSE)

**English: [README.md](README.md)**

Envoyez des SMS depuis Home Assistant via l'**API Swisscom Messaging**. Vous
fournissez votre `client_id` Swisscom, et un service `notify` apparaît dans Home
Assistant, utilisable dans vos automatisations, scripts et scènes.

## Prérequis

- Un abonnement à l'**API Swisscom Messaging** (produit SMS) sur le
  [portail développeur Swisscom](https://sms.icp.swisscom.com/home), qui vous
  donne un **`client_id`**.
- Home Assistant **2026.3.0** ou plus récent, nécessaire pour les icônes de
  marque livrées dans l'intégration.

## Installation

### Via HACS

[![Ouvrir ce dépôt dans HACS sur votre instance Home Assistant.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Sdavid66&repository=Swisscom-SMS&category=integration)

1. Dans HACS, cherchez **Swisscom SMS**.
2. Téléchargez-le, puis redémarrez Home Assistant.

S'il n'apparaît pas dans la recherche, ajoutez-le comme dépôt personnalisé :

1. HACS → menu ⋮ → **Dépôts personnalisés**.
2. Ajoutez `https://github.com/Sdavid66/Swisscom-SMS`, catégorie
   *Integration*.
3. Installez **Swisscom SMS**, puis redémarrez Home Assistant.

### Manuelle

Copiez `custom_components/swisscom_sms` dans le dossier `custom_components` de
votre configuration Home Assistant, puis redémarrez.

## Configuration

[![Démarrer la configuration d'une nouvelle intégration sur votre instance Home Assistant.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=swisscom_sms)

1. **Paramètres → Appareils et services → Ajouter une intégration**.
2. Cherchez **Swisscom SMS**.
3. Renseignez votre `client_id` Swisscom et, éventuellement, le nom du service
   notify (`Swisscom SMS` par défaut).

Un service `notify.swisscom_sms` est créé, nommé selon votre choix. Ajouter une
seconde entrée avec un autre `client_id` crée un second service.

Pour modifier le `client_id` par la suite : intégration → **Reconfigurer**.

## Utilisation

Le service envoie un SMS à chaque numéro listé dans `target`. Un numéro valide
commence par `0`, `00` ou `+` et contient 7 à 15 chiffres — les numéros locaux
en `0` sont préfixés `+41` par Swisscom.

```yaml
action: notify.swisscom_sms
data:
  message: "Le portail du garage est resté ouvert."
  target:
    - "+41791234567"
```

Plusieurs destinataires :

```yaml
action: notify.swisscom_sms
data:
  message: "Alarme déclenchée à la maison !"
  target:
    - "+41791234567"
    - "+41789876543"
```

Dans une automatisation :

```yaml
automation:
  - alias: "Alerte fuite d'eau"
    triggers:
      - trigger: state
        entity_id: binary_sensor.detecteur_fuite_cuisine
        to: "on"
    actions:
      - action: notify.swisscom_sms
        data:
          message: "Fuite d'eau détectée dans la cuisine !"
          target:
            - "+41791234567"
```

Une automatisation s'arrête à l'étape du SMS si un message échoue. Pour qu'elle
continue malgré tout, ajoutez `continue_on_error` :

```yaml
- action: notify.swisscom_sms
  continue_on_error: true
  data:
    message: "Fuite d'eau détectée dans la cuisine !"
    target:
      - "+41791234567"
```

## Dépannage

Si un message ne peut pas être envoyé, l'action échoue : l'automatisation s'arrête
à cette étape et sa trace indique les numéros en échec, avec le code HTTP renvoyé
par Swisscom. Tous les numéros de `target` sont quand même tentés : un mauvais
numéro n'empêche pas l'envoi aux autres.

| Code | Signification |
|---|---|
| `400` | Numéro de téléphone invalide |
| `401` | `client_id` manquant ou incorrect |
| `429` | Quota d'envoi épuisé |

L'avertissement au démarrage `We found a custom integration swisscom_sms which
has not been tested by Home Assistant` est **normal** pour toute intégration
personnalisée et peut être ignoré.

## Limites connues

- **Envoi uniquement.** L'intégration envoie des SMS ; elle n'en reçoit pas et
  ne remonte aucun accusé de réception.
- **Service notify historique.** L'intégration expose un service
  `notify.<nom>` acceptant `target`, pas une *entité* notify.
- **L'icône n'apparaît qu'après installation.** Le tableau de bord HACS tire ses
  vignettes de `data-v2.hacs.xyz`, qui ignore les icônes livrées dans une
  intégration ([hacs/integration#5171](https://github.com/hacs/integration/issues/5171)).

## Avertissement

Projet communautaire indépendant, sans lien avec Swisscom, ni approuvé ni
soutenu par Swisscom. *Swisscom* et le logo Swisscom sont des marques déposées
de Swisscom SA.

## Licence

[GPL-3.0-or-later](LICENSE)
