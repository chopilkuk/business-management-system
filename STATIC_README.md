**Static assets guide**

- Purpose: keep a single project-level `static/` for shared assets and reduce template path churn.
- Conventions:
  - App-specific static files remain under each app's `static/` for app-local assets.
  - Shared menu icons and images should live in `static/menu/` at project root.
  - Templates should use `{% static 'menu/<name>' %}` for menu icons.
- Developer helpers:
  - Run `python scripts/organize_static.py` to copy app `static/menu/*` files into project `static/menu/`.
  - After changes, run `python manage.py collectstatic --noinput` for production asset collection.

Notes:
- The helper script copies files and does not delete originals. Review conflicts before removing duplicates.
