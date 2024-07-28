import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler

# Define the BookRecommender model
class BookRecommender(nn.Module):
    def __init__(self):
        super(BookRecommender, self).__init__()
        self.fc1 = nn.Linear(2, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 1)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Load and inspect data
try:
    books_df = pd.read_csv('books.csv', on_bad_lines='warn')
    print(books_df.columns)  # Print column names to verify
except pd.errors.ParserError as e:
    print(f"Error reading CSV file: {e}")
    raise

# Correct column names if needed
books_df.columns = books_df.columns.str.strip()  # Remove leading/trailing spaces in column names

# Check for required columns
required_columns = ['average_rating', 'num_pages']
missing_columns = [col for col in required_columns if col not in books_df.columns]

if missing_columns:
    raise ValueError(f"Missing columns in CSV file: {', '.join(missing_columns)}")

# Process data
books_df['num_pages'] = books_df['num_pages'].fillna(0)  # Handle missing values
features = books_df[['average_rating', 'num_pages']].values
ratings = books_df['average_rating'].values

# Normalize features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Prepare the dataset and dataloader
X = torch.tensor(features_scaled, dtype=torch.float32)
y = torch.tensor(ratings, dtype=torch.float32).view(-1, 1)
dataset = TensorDataset(X, y)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# Initialize the model, loss function, and optimizer
model = BookRecommender()
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training loop
epochs = 10
for epoch in range(epochs):
    for batch in dataloader:
        inputs, targets = batch
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
    # print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item()}")

# Save the trained model
model_path = 'book_recommender_model.pth'
torch.save(model.state_dict(), model_path)
print(f"Model saved to {model_path}")
