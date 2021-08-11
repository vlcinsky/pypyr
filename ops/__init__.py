"""Invoke task modules, one per namespace."""
import functools

from invoke import Task, task


def step(msg=None):
    """Print a message in such a way, it is visible in longer console outputs."""
    print(f"--> {msg}")


class MyTask(Task):
    """Customized invoke Task reporting it's call."""

    def __call__(self, *args, **kwargs):
        """Run the actual task."""
        self.report_call()
        try:
            result = super().__call__(*args, **kwargs)
            self.report_success()
            return result
        except Exception as exc:
            self.report_failure(exc)
            raise

    def report_call(self):
        """Print the fact the task is called."""
        module = self.__module__
        doc = self.__doc__ or ""
        doc = doc.splitlines()[0]
        print(f"==> {module}.{self.name}: {doc}")

    def report_success(self):
        """Print OK."""
        module = self.__module__
        print(f"<==: OK ({module}.{self.name})")

    def report_failure(self, exc):
        """Print FAILURE + first line of error message, if any."""
        module = self.__module__
        msg = str(exc).splitlines()[0]
        print(f"<==: FAILURE ({module}.{self.name}): {msg}")


mytask = functools.partial(task, klass=MyTask)
