from transformers import BertForSequenceClassification, BertTokenizer

# Load the model and tokenizer
model = BertForSequenceClassification.from_pretrained("bert-base-uncased")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Save the model and tokenizer
model.save_pretrained("C:\\Users\\DELL\\Desktop\\programming\\VsCodeProjects\\WID3002_NLP\\models\\intent_classification_model")
tokenizer.save_pretrained("C:\\Users\\DELL\\Desktop\\programming\\VsCodeProjects\\WID3002_NLP\\models\\intent_classification_tokenizer")
