# Recommendation Engine for Shopping App

## Overview
This recommendation engine employs a hybrid approach by combining:
- **Content Filtering:** Leveraging product attributes such as categories, tags, and inherent popularity scores.
- **Collaborative Filtering:** Simulating user interactions (clicks) from multiple users to identify trending products.
- **User Profile Updates:** Building and updating a lightweight user knowledge graph in-memory, which guides personalized recommendations.

## Content Filtering Logic
- **Attributes & Scoring:**  
  Each product includes a *category*, comma-separated *tags*, and a *popularity score*. During personalized recommendation, a product’s score starts with its inherent popularity. An extra boost (5 points per occurrence) is applied for every tag that matches the user's preferred tags.  
- **Purpose:**  
  This mechanism ensures that products aligning with the user's tastes (as expressed by the selected product attributes) are prioritized while still considering overall product popularity.

## Collaborative Filtering Simulation
- **User Interactions:**  
  The engine uses a simulated `users.csv` file containing prior user clicks. Each click represents a user's interest in a particular product.
- **Trending Items:**  
  Products are ranked based on their popularity score alongside aggregated click counts. Higher click counts denote higher collaborative interest. By merging trending (content-based) and high-click (collaborative) products, the engine forms a hybrid recommendation list.
- **Multi-user Influence:**  
  Interactions from multiple users (e.g., U1, U2, U3) are used to simulate collaborative filtering. Additionally, new sessions (simulated for users such as U4 and U5) append interactions that further inform the recommendation logic.

## User Profile Storage & Update
- **In-Memory Profile:**  
  The user profile is maintained as a lightweight knowledge graph using Python’s `defaultdict` and `Counter`. It consists of counters for:
  - **Categories:** Tracking the number of selections per product category.
  - **Tags:** Counting the frequency of each tag from the products the user has selected.
- **Profile Update:**  
  When a user selects (clicks) products, the engine updates the profile by:
  - Incrementing the count for the product’s category.
  - Parsing and incrementing counts for each tag associated with the product.
- **Usage:**  
  The updated profile is used to personalize subsequent recommendations by boosting items that match the user's demonstrated interests. A basic Matplotlib bar chart visualizes the category preferences, showing how the profile evolves over time.

## Execution
1. Ensure that **products.csv**, **users.csv**, and **recommend.py** are in the same directory.
2. Run the script using:
    ```
    python recommend.py
    ```
3. Follow the interactive prompts to enter product IDs you like for each simulated user session.
4. The script displays initial recommendations, updates user profiles (with visualization), and shows personalized recommendations for each session.
