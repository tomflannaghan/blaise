
check:
	uv run ruff format --check
	uv run ruff check
	uv run ty check
	uv run pytest --doctest-modules

fix:
	uv run ruff format
	uv run ruff check --fix
	uv run ty check
	uv run pytest --doctest-modules
