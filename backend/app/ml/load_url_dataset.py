from datasets import load_dataset

dataset = load_dataset("pirocheto/phishing-url")

print(dataset)
print(dataset["train"][0])
print(dataset["train"].features)
