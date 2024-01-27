import invoke

PACKAGE_NAME = "morse_ctrl"

@invoke.task
def format(ctx):
    print("## Run ruff")
    ctx.run(f"ruff format {PACKAGE_NAME}")
    ctx.run(f"ruff check {PACKAGE_NAME} --fix")


@invoke.task
def check(ctx):
    print("## Run ruff")
    ctx.run(f"ruff format {PACKAGE_NAME} --check")
    ctx.run(f"ruff check {PACKAGE_NAME}")
    print("## Run mypy")
    ctx.run(f"mypy {PACKAGE_NAME} --check-untyped-defs")
