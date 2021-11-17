# yield is used with contextlib.contextmanager or
# contextli.asynccontextmanager
# some learning to do on both fronts.
# info on yield: https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do
# yield like return but it returns a generator

from fastapi import Depends

async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close

async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()

async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)


async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)


# do not use HTTPException with yield
# exit code in dependencies with yield is executed after exception handlers
# meaning there's nothing catching the exceptions in the exit code(code that's after the yield)
# meaning the exception is sent already, these tasks are running after that has ocurred
# if you have code that could raise an error, typically you'r just going to wrap it in
# a pythonic try/except/finally block

# you can still raise an exception, including HTTPException BEFORE yield, but not after

# context managers are those python objects that you use the keyword "with" with
# Example:
with open("./somefile.txt") as f:
    contents = f.read()
    print(contents)
# beneath the surface open(...) creates an object that is a context manager
# it closes the file at the end of the block. even if there were exceptions