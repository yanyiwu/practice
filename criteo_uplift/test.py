from datasets import load_dataset

ds = load_dataset("criteo/criteo-uplift")

print(ds)
print(ds.keys())
print(ds['train'])
print(ds['test'])
