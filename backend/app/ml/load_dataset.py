from datasets import load_dataset

dataset = load_dataset("zefang-liu/phishing-email-dataset")

print(dataset)
print(dataset["train"][0])