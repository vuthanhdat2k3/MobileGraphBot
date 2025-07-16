import pandas as pd
import re
from collections import defaultdict

def clean_text(text):
    """Clean text by removing special characters and normalizing"""
    if pd.isna(text):
        return ""
    text = str(text).strip()
    # Remove quotes and extra spaces
    text = re.sub(r'["\']', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def read_csv_data(csv_file):
    """Read CSV file with different encodings"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    df = None
    
    for encoding in encodings:
        try:
            df = pd.read_csv(csv_file, encoding=encoding)
            print(f"Successfully read CSV with {encoding} encoding")
            break
        except UnicodeDecodeError:
            continue
    
    if df is None:
        raise Exception("Could not read CSV file with any encoding")
    
    return df

def generate_filtered_relationship_queries(df, target_count=1000):
    """Generate filtered Cypher queries for creating relationships"""
    
    cypher_queries = []
    
    # Define the mapping of columns to relationship types and target labels
    column_mapping = {
        'Company Name': ('HAS_COMPANY_NAME', 'Company', 'name'),
        'Mobile Weight': ('HAS_WEIGHT', 'Weight', 'value'),
        'RAM': ('HAS_RAM', 'RAM', 'size'),
        'Front Camera': ('HAS_FRONT_CAMERA', 'Camera', 'name'),
        'Back Camera': ('HAS_BACK_CAMERA', 'Camera', 'name'),
        'Processor': ('HAS_PROCESSOR', 'Processor', 'name'),
        'Battery Capacity': ('HAS_BATTERY', 'Battery', 'capacity'),
        'Screen Size': ('HAS_SCREEN', 'Screen', 'size'),
        'Launched Price (Pakistan)': ('HAS_PAKISTAN_PRICE', 'Price', 'value'),
        'Launched Price (India)': ('HAS_INDIA_PRICE', 'Price', 'value'),
        'Launched Price (China)': ('HAS_CHINA_PRICE', 'Price', 'value'),
        'Launched Price (USA)': ('HAS_USA_PRICE', 'Price', 'value'),
        'Launched Price (Dubai)': ('HAS_DUBAI_PRICE', 'Price', 'value'),
        'Launched Year': ('HAS_YEAR', 'Year', 'year')
    }
    
    # Calculate how many models we need to process
    # Each model has 14 relationships (one for each column)
    models_needed = min(target_count // 14, len(df))
    
    print(f"Processing {models_needed} models to generate approximately {models_needed * 14} relationships")
    
    # Process selected models
    for index in range(models_needed):
        row = df.iloc[index]
        model_name = clean_text(row['Model Name'])
        if not model_name or model_name == "nan":
            continue
            
        # Create relationships for each column
        for column, (relationship_type, target_label, target_property) in column_mapping.items():
            value = clean_text(row[column])
            if not value or value == "nan":
                continue
                
            # Handle special cases for Camera and Price
            if column == 'Front Camera':
                cypher_queries.append(f"MATCH (m:Model {{name: '{model_name}'}}), (c:Camera {{name: '{value}', type: 'Front'}}) CREATE (m)-[:{relationship_type}]->(c);")
            elif column == 'Back Camera':
                cypher_queries.append(f"MATCH (m:Model {{name: '{model_name}'}}), (c:Camera {{name: '{value}', type: 'Back'}}) CREATE (m)-[:{relationship_type}]->(c);")
            elif column.startswith('Launched Price'):
                country = column.split('(')[1].split(')')[0]
                cypher_queries.append(f"MATCH (m:Model {{name: '{model_name}'}}), (p:Price {{value: '{value}', country: '{country}'}}) CREATE (m)-[:{relationship_type}]->(p);")
            else:
                cypher_queries.append(f"MATCH (m:Model {{name: '{model_name}'}}), (t:{target_label} {{{target_property}: '{value}'}}) CREATE (m)-[:{relationship_type}]->(t);")
    
    return cypher_queries

def main():
    csv_file = "data/Mobiles-Dataset(2025).csv"
    
    print("Reading CSV file...")
    df = read_csv_data(csv_file)
    
    print("Generating filtered relationship queries...")
    cypher_queries = generate_filtered_relationship_queries(df, 1000)
    
    # Write Cypher queries to file
    output_file = "neo4j_relationships_filtered.cypher"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cypher_queries))
    
    print(f"Filtered relationship queries written to {output_file}")
    print(f"Total number of relationship queries: {len(cypher_queries)}")
    
    # Count relationship types
    relationship_counts = defaultdict(int)
    for query in cypher_queries:
        for rel_type in ['HAS_COMPANY_NAME', 'HAS_WEIGHT', 'HAS_RAM', 'HAS_FRONT_CAMERA', 
                        'HAS_BACK_CAMERA', 'HAS_PROCESSOR', 'HAS_BATTERY', 'HAS_SCREEN',
                        'HAS_PAKISTAN_PRICE', 'HAS_INDIA_PRICE', 'HAS_CHINA_PRICE', 
                        'HAS_USA_PRICE', 'HAS_DUBAI_PRICE', 'HAS_YEAR']:
            if rel_type in query:
                relationship_counts[rel_type] += 1
                break
    
    print("\nRelationship type distribution:")
    for rel_type, count in sorted(relationship_counts.items()):
        print(f"{rel_type}: {count}")

if __name__ == "__main__":
    main() 