# Analytics
Social Media Performance Analysis Project

## Objective:
Develop a basic analytics module utilizing Langflow and DataStax to analyze engagement data from mock social media accounts.

### Required Tools:
- DataStax Astra DB for database operations.
- Langflow for workflow creation and GPT integration.

### Task Details:
1. Fetch Engagement Data:
   - Create a small dataset simulating social media engagement (e.g., likes, shares, comments, post types).
   - Store this data in DataStax Astra DB.
2. Analyze Post Performance: Using Langflow, construct a simple flow that:
   - Accepts post types (e.g., carousel, reels, static images) as input.
   - Queries the dataset in Astra DB to calculate average engagement metrics for each post type.
3. Provide Insights:
   - Utilize GPT integration in Langflow to generate simple insights based on the data.
   - Example outputs:
     - Carousel posts have 20% higher engagement than static posts.
     - Reels drive 2x more comments compared to other formats.

## Our Solution:
