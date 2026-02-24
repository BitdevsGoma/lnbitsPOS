```markdown
# POS LNbits – Django Lightning Point of Sale

Petit projet **Django + Bootstrap** permettant de générer des factures Lightning (BOLT11) via un wallet **LNbits** et d’afficher un QR code lisible sur terminal de caisse (mobile / desktop).

Palette : bleu-vert-blanc, design glassmorphism, optimisé pour l’usage PoS sur smartphone.

---

## Aperçu

> Les captures ci‑dessous doivent être placées dans un dossier `media/` à la racine du dépôt  
> (`media/1_(1).png`, `media/1_(2).png`, `media/1_(3).png`, `media/1_(4).png`).

### 1. Liste des instances LNbits

![Table des instances LNbits](media/1_(1).png)

### 2. Détail d’une instance ouverte

![Instance LNbits ouverte](media/1_(2).png)

### 3. Écran POS sans facture générée

![Page POS en attente d’invoice](media/1_(3).png)

### 4. Écran POS avec facture générée

![Page POS avec invoice et QR](media/1_(4).png)

---

## 1. Prérequis

- Python 3.10+
- Git
- Un wallet LNbits déjà créé, avec :
  - **Instance URL** (ex. `https://madwhiting0.lnbits.com`)
  - **Wallet ID**
  - **Admin key**
  - **Invoice/read key**

---

## 2. Récupérer le projet

```bash
git clone https://github.com/<votre-user>/<votre-repo>.git
cd <votre-repo>
```

---

## 3. Créer et activer l’environnement virtuel

```bash
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

---

## 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

Si le fichier `requirements.txt` n’existe pas encore, vous pouvez en générer un minimal :

```bash
pip install django requests
pip freeze > requirements.txt
```

---

## 5. Configuration LNbits

Dans `poslnbits/settings.py`, configurez vos paramètres LNbits :

```python
LNBITS_URL = "https://votre-instance.lnbits.com"
LNBITS_WALLET_ID = "VOTRE_WALLET_ID"
LNBITS_ADMIN_KEY = "VOTRE_ADMIN_KEY"
LNBITS_INVOICE_KEY = "VOTRE_INVOICE_KEY"
```

> Pour un projet en production, il est recommandé d’utiliser des variables d’environnement et de ne jamais committer vos clés directement dans le dépôt.

Le module `payments/lnbits.py` utilise ces variables pour :
- récupérer les détails du wallet,
- créer des invoices entrantes (incoming),
- vérifier l’état d’une invoice.

---

## 6. Migrations de base de données

```bash
python manage.py migrate
```

La base par défaut est SQLite (fichier `db.sqlite3`).  
Vous pouvez adapter le backend DB dans `poslnbits/settings.py` si nécessaire.

---

## 7. Lancer le serveur de développement

```bash
python manage.py runserver
```

Par défaut, le projet est accessible à :

- `http://127.0.0.1:8000/pos/`

---

## 8. Utilisation de la page POS

1. Ouvrez `http://127.0.0.1:8000/pos/` sur votre navigateur (idéalement sur un smartphone utilisé comme terminal PoS).
2. Saisissez :
   - un **montant en sats**,
   - un mémo (optionnel),
   puis cliquez sur **“Générer l’invoice”**.
3. La page affiche :
   - le **payment hash**,
   - la **demande de paiement BOLT11**,
   - un **QR code** haute lisibilité (noir sur blanc, marge suffisante).
4. Demandez au client de scanner le QR avec son wallet Lightning (LNbits, Phoenix, Breez, etc.).
5. Une fois la facture payée, vous pouvez :
   - actualiser la page,
   - ou implémenter ultérieurement une vérification automatique via `check_invoice`.

---

## 9. Structure principale du projet

```text
.
├── manage.py
├── poslnbits/
│   ├── __init__.py
│   ├── settings.py        # Config Django + paramètres LNbits
│   ├── urls.py            # Route /pos/
│   └── wsgi.py / asgi.py
├── payments/
│   ├── __init__.py
│   ├── lnbits.py          # Fonctions d’appel à l’API LNbits
│   ├── views.py           # Vue PosView (formulaire + rendu template)
│   └── templates/
│       └── payments/
│           └── pos.html   # Interface POS glassmorphisme responsive
└── media/
    ├── 1_(1).png          # Table des instances LNbits
    ├── 1_(2).png          # Détail d’une instance ouverte
    ├── 1_(3).png          # POS sans facture
    └── 1_(4).png          # POS avec facture générée
```

---

## 10. Personnalisation

- **Styles / thème**  
  Toute la partie glassmorphisme + palette bleu-vert-blanc est dans le `<style>` du template `pos.html`.  
  Vous pouvez :
  - ajuster les couleurs dans `:root`,
  - adapter la disposition mobile/desktop en modifiant les règles `.pos-grid` et les media queries.

- **Internationalisation / langue**  
  Les textes sont en français, mais peuvent facilement être adaptés ou internationalisés via les outils Django i18n.

- **Sécurité / déploiement**  
  - Pensez à déplacer vos clés LNbits dans des variables d’environnement.
  - Configurez `ALLOWED_HOSTS`, la base de données et un serveur web (Nginx, Caddy…) pour une mise en prod.

---

## 11. Roadmap / idées d’améliorations

- Rafraîchissement auto de l’état de paiement (polling ou WebSocket).
- Historique des ventes en base (montant, mémo, statut).
- Multi-wallet / multi-guichet.
- Authentification pour restreindre l’accès à la page POS.

---

## 12. Licence

Précisez ici la licence de votre choix, par exemple :

```text
MIT License
```
```