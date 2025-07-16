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

def extract_unique_entities(csv_file):
    """Extract all unique entities from the CSV file"""
    
    # Read CSV file with different encodings
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
    
    # Dictionary to store unique entities by category
    entities = defaultdict(set)
    
    # Extract entities from each column
    for column in df.columns:
        print(f"Processing column: {column}")
        
        for value in df[column]:
            cleaned_value = clean_text(value)
            if cleaned_value and cleaned_value != "nan":
                entities[column].add(cleaned_value)
    
    return entities

def generate_cypher_queries(entities):
    """Generate Cypher queries for Neo4j"""
    
    cypher_queries = []
    
    # Create constraints and indexes
    cypher_queries.append("-- Create constraints and indexes")
    cypher_queries.append("CREATE CONSTRAINT company_name_unique IF NOT EXISTS FOR (c:Company) REQUIRE c.name IS UNIQUE;")
    cypher_queries.append("CREATE CONSTRAINT model_name_unique IF NOT EXISTS FOR (m:Model) REQUIRE m.name IS UNIQUE;")
    cypher_queries.append("CREATE CONSTRAINT processor_name_unique IF NOT EXISTS FOR (p:Processor) REQUIRE p.name IS UNIQUE;")
    cypher_queries.append("CREATE CONSTRAINT camera_name_unique IF NOT EXISTS FOR (cam:Camera) REQUIRE cam.name IS UNIQUE;")
    cypher_queries.append("CREATE CONSTRAINT ram_size_unique IF NOT EXISTS FOR (r:RAM) REQUIRE r.size IS UNIQUE;")
    cypher_queries.append("CREATE CONSTRAINT battery_capacity_unique IF NOT EXISTS FOR (b:Battery) REQUIRE b.capacity IS UNIQUE;")
    cypher_queries.append("CREATE CONSTRAINT screen_size_unique IF NOT EXISTS FOR (s:Screen) REQUIRE s.size IS UNIQUE;")
    cypher_queries.append("CREATE CONSTRAINT price_unique IF NOT EXISTS FOR (pr:Price) REQUIRE pr.value IS UNIQUE;")
    cypher_queries.append("CREATE CONSTRAINT year_unique IF NOT EXISTS FOR (y:Year) REQUIRE y.year IS UNIQUE;")
    cypher_queries.append("")
    
    # Create Company nodes
    cypher_queries.append("-- Create Company nodes")
    for company in entities['Company Name']:
        cypher_queries.append(f"CREATE (c:Company {{name: '{company}'}});")
    cypher_queries.append("")
    
    # Create Model nodes
    cypher_queries.append("-- Create Model nodes")
    for model in entities['Model Name']:
        cypher_queries.append(f"CREATE (m:Model {{name: '{model}'}});")
    cypher_queries.append("")
    
    # Create Processor nodes
    cypher_queries.append("-- Create Processor nodes")
    for processor in entities['Processor']:
        cypher_queries.append(f"CREATE (p:Processor {{name: '{processor}'}});")
    cypher_queries.append("")
    
    # Create Camera nodes (Front and Back)
    cypher_queries.append("-- Create Camera nodes")
    for camera in entities['Front Camera']:
        cypher_queries.append(f"CREATE (cam:Camera {{name: '{camera}', type: 'Front'}});")
    for camera in entities['Back Camera']:
        cypher_queries.append(f"CREATE (cam:Camera {{name: '{camera}', type: 'Back'}});")
    cypher_queries.append("")
    
    # Create RAM nodes
    cypher_queries.append("-- Create RAM nodes")
    for ram in entities['RAM']:
        cypher_queries.append(f"CREATE (r:RAM {{size: '{ram}'}});")
    cypher_queries.append("")
    
    # Create Battery nodes
    cypher_queries.append("-- Create Battery nodes")
    for battery in entities['Battery Capacity']:
        cypher_queries.append(f"CREATE (b:Battery {{capacity: '{battery}'}});")
    cypher_queries.append("")
    
    # Create Screen nodes
    cypher_queries.append("-- Create Screen nodes")
    for screen in entities['Screen Size']:
        cypher_queries.append(f"CREATE (s:Screen {{size: '{screen}'}});")
    cypher_queries.append("")
    
    # Create Price nodes for different countries
    cypher_queries.append("-- Create Price nodes")
    for price in entities['Launched Price (Pakistan)']:
        cypher_queries.append(f"CREATE (pr:Price {{value: '{price}', country: 'Pakistan'}});")
    for price in entities['Launched Price (India)']:
        cypher_queries.append(f"CREATE (pr:Price {{value: '{price}', country: 'India'}});")
    for price in entities['Launched Price (China)']:
        cypher_queries.append(f"CREATE (pr:Price {{value: '{price}', country: 'China'}});")
    for price in entities['Launched Price (USA)']:
        cypher_queries.append(f"CREATE (pr:Price {{value: '{price}', country: 'USA'}});")
    for price in entities['Launched Price (Dubai)']:
        cypher_queries.append(f"CREATE (pr:Price {{value: '{price}', country: 'Dubai'}});")
    cypher_queries.append("")
    
    # Create Year nodes
    cypher_queries.append("-- Create Year nodes")
    for year in entities['Launched Year']:
        cypher_queries.append(f"CREATE (y:Year {{year: {year}}});")
    cypher_queries.append("")
    
    # Create Weight nodes
    cypher_queries.append("-- Create Weight nodes")
    for weight in entities['Mobile Weight']:
        cypher_queries.append(f"CREATE (w:Weight {{value: '{weight}'}});")
    cypher_queries.append("")
    
    return cypher_queries

def main():
    csv_file = "data/Mobiles-Dataset(2025).csv"
    
    print("Extracting unique entities from CSV file...")
    entities = extract_unique_entities(csv_file)
    
    print("\nGenerating Cypher queries...")
    cypher_queries = generate_cypher_queries(entities)
    
    # Write Cypher queries to file
    output_file = "neo4j_entities.cypher"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cypher_queries))
    
    print(f"\nCypher queries written to {output_file}")
    
    # Print summary
    print("\nEntity Summary:")
    for category, entity_set in entities.items():
        print(f"{category}: {len(entity_set)} unique entities")
    
    # Print some examples
    print("\nExample entities by category:")
    for category, entity_set in entities.items():
        print(f"\n{category}:")
        for entity in list(entity_set)[:5]:  # Show first 5 entities
            print(f"  - {entity}")
        if len(entity_set) > 5:
            print(f"  ... and {len(entity_set) - 5} more")

if __name__ == "__main__":
    main()
