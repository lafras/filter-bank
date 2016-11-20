# filter-bank
Examples of simple filter banks.

A common task (for me at least) is to find a combination (or sequence) of filters to apply to a signal. `batching.py` uses tasks, targets and workflows. Each filter is a Luigi task and can be combiined into a workflow.

`streaming.py` uses RxPy (Reactive X for Python). Dataframes are streamed from function to function. This example also demonstrates the use of pyfilesystems.
