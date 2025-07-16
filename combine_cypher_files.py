def combine_cypher_files():
    """Combine entity and relationship Cypher files into one comprehensive file"""
    
    # Read entity creation file
    with open('neo4j_entities.cypher', 'r', encoding='utf-8') as f:
        entity_queries = f.read()
    
    # Read relationship creation file
    with open('neo4j_relationships.cypher', 'r', encoding='utf-8') as f:
        relationship_queries = f.read()
    
    # Combine them
    combined_content = f"""-- Complete Neo4j Database Setup for Mobile Dataset
-- This file contains all Cypher queries to create entities and relationships

-- ===========================================
-- PART 1: CREATE ENTITIES (NODES)
-- ===========================================

{entity_queries}

-- ===========================================
-- PART 2: CREATE RELATIONSHIPS
-- ===========================================

{relationship_queries}

-- ===========================================
-- PART 3: CREATE INDEXES FOR BETTER PERFORMANCE
-- ===========================================

-- Create indexes for better query performance
CREATE INDEX model_name_index IF NOT EXISTS FOR (m:Model) ON (m.name);
CREATE INDEX company_name_index IF NOT EXISTS FOR (c:Company) ON (c.name);
CREATE INDEX processor_name_index IF NOT EXISTS FOR (p:Processor) ON (p.name);
CREATE INDEX camera_name_index IF NOT EXISTS FOR (cam:Camera) ON (cam.name);
CREATE INDEX ram_size_index IF NOT EXISTS FOR (r:RAM) ON (r.size);
CREATE INDEX battery_capacity_index IF NOT EXISTS FOR (b:Battery) ON (b.capacity);
CREATE INDEX screen_size_index IF NOT EXISTS FOR (s:Screen) ON (s.size);
CREATE INDEX price_value_index IF NOT EXISTS FOR (pr:Price) ON (pr.value);
CREATE INDEX year_index IF NOT EXISTS FOR (y:Year) ON (y.year);
CREATE INDEX weight_value_index IF NOT EXISTS FOR (w:Weight) ON (w.value);

-- ===========================================
-- PART 4: SAMPLE QUERIES FOR TESTING
-- ===========================================

-- Query 1: Find all iPhone models
-- MATCH (m:Model)-[:HAS_COMPANY_NAME]->(c:Company {name: 'Apple'}) RETURN m.name, c.name;

-- Query 2: Find all models with 6GB RAM
-- MATCH (m:Model)-[:HAS_RAM]->(r:RAM {size: '6GB'}) RETURN m.name, r.size;

-- Query 3: Find all models with Snapdragon processors
-- MATCH (m:Model)-[:HAS_PROCESSOR]->(p:Processor) WHERE p.name CONTAINS 'Snapdragon' RETURN m.name, p.name;

-- Query 4: Find all models with 50MP cameras
-- MATCH (m:Model)-[:HAS_BACK_CAMERA]->(c:Camera) WHERE c.name CONTAINS '50MP' RETURN m.name, c.name;

-- Query 5: Find all models launched in 2024
-- MATCH (m:Model)-[:HAS_YEAR]->(y:Year {year: 2024}) RETURN m.name, y.year;

-- Query 6: Find all models with price range in Pakistan
-- MATCH (m:Model)-[:HAS_PAKISTAN_PRICE]->(p:Price) WHERE p.value CONTAINS 'PKR 200,000' RETURN m.name, p.value;

-- Query 7: Find all models with battery capacity above 4000mAh
-- MATCH (m:Model)-[:HAS_BATTERY]->(b:Battery) WHERE b.capacity CONTAINS '4' AND b.capacity CONTAINS 'mAh' RETURN m.name, b.capacity;

-- Query 8: Find all Samsung models with their specifications
-- MATCH (m:Model)-[:HAS_COMPANY_NAME]->(c:Company {name: 'Samsung'})
-- MATCH (m)-[:HAS_RAM]->(r:RAM)
-- MATCH (m)-[:HAS_PROCESSOR]->(p:Processor)
-- MATCH (m)-[:HAS_BATTERY]->(b:Battery)
-- RETURN m.name, c.name, r.size, p.name, b.capacity LIMIT 10;

-- Query 9: Find all models with screen size 6.7 inches or larger
-- MATCH (m:Model)-[:HAS_SCREEN]->(s:Screen) WHERE s.size CONTAINS '6.7' OR s.size CONTAINS '6.8' OR s.size CONTAINS '6.9' RETURN m.name, s.size;

-- Query 10: Find all models with their prices in all countries
-- MATCH (m:Model)-[:HAS_COMPANY_NAME]->(c:Company)
-- MATCH (m)-[:HAS_PAKISTAN_PRICE]->(p1:Price)
-- MATCH (m)-[:HAS_INDIA_PRICE]->(p2:Price)
-- MATCH (m)-[:HAS_USA_PRICE]->(p3:Price)
-- RETURN m.name, c.name, p1.value, p2.value, p3.value LIMIT 5;
"""
    
    # Write combined file
    with open('neo4j_complete_setup.cypher', 'w', encoding='utf-8') as f:
        f.write(combined_content)
    
    print("Combined Cypher file created: neo4j_complete_setup.cypher")
    print("This file contains:")
    print("1. Entity creation queries")
    print("2. Relationship creation queries") 
    print("3. Performance indexes")
    print("4. Sample queries for testing")

if __name__ == "__main__":
    combine_cypher_files() 