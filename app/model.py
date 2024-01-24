from dataclasses import dataclass
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
import torch
import pickle


def embed_bert_cls(text, model, tokenizer):
    t = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**{k: v.to(model.device) for k, v in t.items()})
    embeddings = model_output.last_hidden_state[:, 0, :]
    embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings[0].cpu().numpy()


categories = {
    0: 'Mobile Phones',
    1: 'TVs',
    2: 'CPUs',
    3: 'Digital Cameras',
    4: 'Microwaves',
    5: 'Dishwashers',
    6: 'Washing Machines',
    7: 'Freezers',
    8: 'Fridge Freezers',
    9: 'Fridges'
}


@dataclass
class ClassificationModel:
    model_name: str
    model_parameters: dict
    model_path: str
    model_cost: int

    def create_model(self):
        if self.model_name not in ['k_neighbors', 'random_forest', 'mlp']:
            raise ValueError("Unknown model name: {}".format(self.model_name))

        with open(self.model_path, 'rb') as file:
            model = pickle.load(file)
        return model

    def get_price(self):
        return self.model_cost


k_neighbors_model_data = {
    'model_name': 'k_neighbors',
    'model_parameters': {},
    'model_path': 'k_neighbors.pkl',
    'model_cost': 1
}

k_neighbors_classification_model = ClassificationModel(**k_neighbors_model_data)

mlp_model_data = {
    'model_name': 'mlp',
    'model_parameters': {},
    'model_path': 'mlp.pkl',
    'model_cost': 10
}

mlp_classification_model = ClassificationModel(**mlp_model_data)
