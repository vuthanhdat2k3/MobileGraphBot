def remove_comments_from_cypher():
    """Remove comments from neo4j_relationships.cypher file"""
    
    # Read the relationships file
    with open('neo4j_relationships.cypher', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Filter out comment lines and empty lines
    filtered_lines = []
    for line in lines:
        stripped_line = line.strip()
        # Skip comment lines (starting with --) and empty lines
        if not stripped_line.startswith('--') and stripped_line:
            filtered_lines.append(line)
    
    # Write the filtered content back to the file
    with open('neo4j_relationships.cypher', 'w', encoding='utf-8') as f:
        f.writelines(filtered_lines)
    
    print("Comments removed from neo4j_relationships.cypher")
    print(f"Original lines: {len(lines)}")
    print(f"Lines after removing comments: {len(filtered_lines)}")

if __name__ == "__main__":
    remove_comments_from_cypher() 