# Developer informatie

Qua netheid van de code was er eerst config voor "black" (python formatting). Voor Vscode werd er o.a. een plugin voor "black" en "isort" voorgesteld. Regellengte voor Python was op 120 karakters ingesteld.

Dit is nu uitgebreid en meer geautomatiseerd:

- Voor formatting gebruiken we [Ruff](https://docs.astral.sh/ruff/), een snelle vervanger voor black+isort+pyflakes. Alles in één, en snel. En met dezelfde defaults.

- Een `.editorconfig` bestand (zie [EditorConfig](https://editorconfig.org/)) wordt door de meeste editors opgepikt: standaardinstellingen voor regeleindes, wel/niet "enter" aan het eind van bestanden, enz. Voor Vscode wordt er automatisch een plugin voorgesteld.

- Ruff (en een paar andere formatters) moeten wel eerst geïnstalleerd worden. Standaard in de Python wereld is om [pre-commit](https://pre-commit.com/) te installeren. Dat is dan één tool die de andere andere formatters ophaalt en runt.

- In `.pre-commit-config.yaml` staat welke checks/formatters worden gedraaid.

- TODO: "github action runner" die automatisch pre-commit draait voor elk pull request op github, ter controle.


## Eenmalige installatie

Eenmalig:

- Installeer pre-commit (`pip install pre-commit`).

- Installeer de editorconfig plugin zoals vscode voorstelt, indien van toepassing.


## In de praktijk

Met pre-commit alles controleren en deels automatisch fixen: `pre-commit run --all`, dit is wat er ook op github gedraaid wordt, dus als de controle daar faalt hoort het lokaal ook fout te gaan (en is het makkelijk te fixen).
