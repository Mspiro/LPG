import  json
import pandas as pd

class FewShotPosts:
  def __init__(self, file_path="data/processed_posts.json"):
    self.df = None
    self.unique_tags  = None
    self.load_posts(file_path)
    
  def load_posts(self, filepath):
    with open(filepath, encoding="utf-8") as f:
      posts = json.load(f)
      self.df = pd.json_normalize(posts)
      self.df['length'] = self.df['line_count'].apply(self.categorize_lenght)
      all_tags = self.df['tags'].apply(lambda x: x).sum()
      self.unique_tags = set(list(all_tags))
      
  
  def categorize_lenght(self, line_count ):
    if line_count < 5:
      return "Short"
    elif 5 <= line_count < 10:
      return "Medium"
    else:
      return "Long"
  
  def get_tags(self):
    return self.unique_tags
    
  def get_filtered_posts(self, length, language, tag):
    df_filtered = self.df[
      (self.df['language'] == language) &
      (self.df['length'] == length) &
      (self.df['tags'].apply(lambda tags: tag in tags))
    ]
    return df_filtered.to_dict(orient="records")
    
  
    
if __name__ == "__main__":
  fs = FewShotPosts()
  posts = fs.get_filtered_posts("Short", "English", "Job Search")
  print(posts)
  